#!/usr/bin/env node
/**
 * Deterministic artifact builder.
 *
 *   node build.mjs <spec.json> <out.html>
 *
 * Reads `template.html` from this script's own directory, strips every
 * `[data-demo]` element and demo data block, and emits one self-contained
 * artifact. Write the spec; never edit the template, and never hand-write the
 * markup a builder already produces.
 *
 * What the script owns: host markup per component, panel and caption wrappers,
 * JSON serialization that survives a script context, HTML escaping, the
 * bootstrap order (sync builders, then `await Promise.all` over the async ones,
 * then `buildToc()`), interaction-status labels, and spec validation.
 *
 * ---------------------------------------------------------------------------
 * SPEC SCHEMA
 * ---------------------------------------------------------------------------
 * {
 *   "lang": "zh-TW",              // required. <html lang>
 *   "title": "...",               // required. <title>, <h1>, and the rail title
 *   "kicker": "PR #922 · repo",   // optional. small line above the title, and the rail kicker
 *   "tocTitle": "...",            // optional. shorter rail title when title is long
 *   "lead": "...",                // optional. lead paragraph under the title
 *   "meta": ["base ← head", "16 files"],   // optional. document-meta list
 *
 *   "messages": {                 // optional. merged over the template defaults
 *     "renderer": { "diagram": "...", "diff": "...", "code": "...", "signatures": "..." },
 *     "ui": { "source": "...", "interactive": "...", ... }
 *   },
 *
 *   "closing": {                  // optional. paragraph after the last section
 *     "text": "...",
 *     "href": "...",              // optional. without linkText the whole text becomes the link
 *     "linkText": "..."           // optional. link appended after the text
 *   },
 *
 *   "css": "...",                 // optional. appended inside the template <style>
 *   "js": "...",                  // optional. module JS appended before buildToc();
 *                                 //   runs in the template's module scope (ArtifactUI, element, ...)
 *
 *   "sections": [                 // required, at least one
 *     {
 *       "id": "overview",         // required. unique, [A-Za-z][\w-]*
 *       "title": "...",           // required
 *       "summary": "...",         // optional
 *       "visuals": [              // required, at least one
 *         {
 *           "id": "change-map",   // required. unique across the document
 *           "title": "...",       // required
 *           "copy": "...",        // optional. plain text, one short paragraph
 *           "source": "path:line",// optional but expected. the evidence line
 *           "links": [{ "text": "...", "href": "..." }],   // optional. rendered under copy
 *
 *           "component": "statCards" | "fileChanges" | "signatures" | "pseudocode"
 *                      | "tree" | "code" | "diff" | "diagram" | "checklist"
 *                      | "matrix" | "callout" | "html",
 *
 *           "caption": {          // optional. caption bar for panel components
 *             "kind": "matrix", "name": "...", "meta": "..."
 *           },
 *           "options": { ... },   // per-component, see below
 *           "data": { ... },      // exactly the builder's data contract
 *           "interactive": "可互動",   // optional. interaction-status label.
 *                                     //   Collapsible trees and scrollable diagrams
 *                                     //   get one automatically when omitted.
 *           "callout": { "tone": "warning", "title": "...", "body": "..." }  // optional, one per visual
 *         }
 *       ]
 *     }
 *   ]
 * }
 *
 * ---------------------------------------------------------------------------
 * COMPONENT DATA CONTRACTS  (see references/GALLERY.md for the full APIs)
 * ---------------------------------------------------------------------------
 * statCards    data { items: [{ label, value, tone?, note? }] }
 *              host .stat-grid, no panel
 * fileChanges  data { files: [{ path, change, changeLabel, additions?, deletions?, note? }] }
 *              change is added | modified | removed | renamed. Panel host.
 * signatures   data { lang?, groups: [{ owner, summary?, items: [{ declaration, lang?, fields? }] }] }
 *              fields are [{ label, value }]. Panel host. Async.
 * pseudocode   data { lines: [{ indent, segments: [{ type, text }], note? }] }
 *              type is plain|keyword|function|value|operator|symbol|comment. Panel host.
 * tree         data { roots: [...] }, options { variant, collapsible? }
 *              variant is call-stack | component-tree | file-tree. Panel host.
 *              call-stack node    { frame, location?, detail?, children?, active?, badges? }
 *              component-tree node{ component, props?, responsibility?, children?, active?, badges? }
 *              file-tree node     { name, kind, path?, note?, children?, active?, badges? }
 * code         data { source, lang? }, options { lang? }. Panel host. Async.
 * diff         data { oldFile: { name, contents }, newFile: { name, contents } }
 *              host .diff-host.artifact-surface, no panel. Async.
 * diagram      data { source }, options passed through to the mermaid renderer.
 *              host .mermaid-host.artifact-surface, no panel. Async.
 * checklist    data { items: [{ state, stateLabel, label, note? }] }
 *              state is pass | pending | fail. Panel host.
 * matrix       data { columns: [...], rows: [{ label, cells: [{ value, tone?, note? }] }], corner? }
 *              tone is positive | warning | negative. Panel host.
 * callout      data { tone, title?, body }. tone is note|positive|warning|negative.
 *              host .artifact-surface, no panel.
 * html         data { html }. A trusted fragment authored for a custom component.
 *              Inserted verbatim as the visual body. Pair it with spec.css / spec.js.
 */

import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))

/* ------------------------------------------------------------------ escaping */

/** Escape a string for an HTML text node or a double-quoted attribute value. */
const esc = (value) =>
  String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')

/**
 * Serialize JSON for a `<script type="application/json">` block.
 *
 * Script content is raw text, so HTML entities would never be decoded: the
 * characters that could end the script element, or break a JS parser, are
 * escaped as JSON \u sequences instead, which JSON.parse decodes back.
 * The line separators are written as escape sequences on purpose — a literal
 * U+2028 in this source would be the very bug this guards against.
 */
const jsonForScript = (value) =>
  JSON.stringify(value).replace(
    /[<>&\u2028\u2029]/g,
    (ch) => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0'),
  )

/* ---------------------------------------------------------------- components */

const PANEL_HOSTS = {
  fileChanges: { tag: 'ol', className: 'filechange-list' },
  signatures: { tag: 'div', className: 'signature-list' },
  pseudocode: { tag: 'div', className: 'pseudocode-host' },
  tree: { tag: 'div', className: 'tree-host' },
  code: { tag: 'div', className: 'code-host' },
  checklist: { tag: 'div', className: 'checklist-host' },
  matrix: { tag: 'div', className: 'matrix-host' },
}

const BARE_HOSTS = {
  statCards: 'stat-grid',
  diff: 'diff-host artifact-surface',
  diagram: 'mermaid-host artifact-surface',
  callout: 'artifact-surface',
}

const COMPONENTS = new Set([...Object.keys(PANEL_HOSTS), ...Object.keys(BARE_HOSTS), 'html'])
const ASYNC_COMPONENTS = new Set(['signatures', 'code', 'diff', 'diagram'])
const TREE_VARIANTS = new Set(['call-stack', 'component-tree', 'file-tree'])
const TOKEN_TYPES = new Set([
  'plain', 'keyword', 'function', 'value', 'operator', 'symbol', 'comment',
])
const CHANGE_KINDS = new Set(['added', 'modified', 'removed', 'renamed'])
const CHECK_STATES = new Set(['pass', 'pending', 'fail'])
const CALLOUT_TONES = new Set(['note', 'positive', 'warning', 'negative'])
const CELL_TONES = new Set(['positive', 'warning', 'negative'])

/* --------------------------------------------------------------- validation */

const problems = []
const ID_PATTERN = /^[A-Za-z][\w-]*$/

const fail = (where, message) => problems.push(where + ': ' + message)
const isText = (value) => typeof value === 'string' && value.trim() !== ''
const isList = (value) => Array.isArray(value) && value.length > 0

function requireText(where, object, key) {
  if (!isText(object?.[key])) fail(where, 'missing string "' + key + '"')
}

function validateData(where, visual) {
  const data = visual.data
  const options = visual.options || {}
  if (data === null || typeof data !== 'object' || Array.isArray(data)) {
    fail(where, 'missing object "data"')
    return
  }
  const eachOf = (key, check) => {
    if (!isList(data[key])) {
      fail(where, 'data.' + key + ' must be a non-empty array')
      return
    }
    data[key].forEach((entry, index) => check(entry, where + ' data.' + key + '[' + index + ']'))
  }

  switch (visual.component) {
    case 'statCards':
      eachOf('items', (item, at) => {
        requireText(at, item, 'label')
        if (item?.value === undefined || item.value === null) fail(at, 'missing "value"')
      })
      break
    case 'fileChanges':
      eachOf('files', (file, at) => {
        requireText(at, file, 'path')
        requireText(at, file, 'changeLabel')
        if (!CHANGE_KINDS.has(file?.change)) {
          fail(at, 'change must be one of ' + [...CHANGE_KINDS].join(' | '))
        }
      })
      break
    case 'signatures':
      eachOf('groups', (group, at) => {
        requireText(at, group, 'owner')
        if (!isList(group?.items)) {
          fail(at, 'items must be a non-empty array')
          return
        }
        group.items.forEach((item, index) => {
          requireText(at + '.items[' + index + ']', item, 'declaration')
        })
      })
      break
    case 'pseudocode':
      eachOf('lines', (line, at) => {
        if (!isList(line?.segments)) {
          fail(at, 'segments must be a non-empty array')
          return
        }
        line.segments.forEach((segment, index) => {
          if (!TOKEN_TYPES.has(segment?.type)) {
            fail(at + '.segments[' + index + ']', 'type must be one of ' + [...TOKEN_TYPES].join(' | '))
          }
          if (typeof segment?.text !== 'string') fail(at + '.segments[' + index + ']', 'missing "text"')
        })
      })
      break
    case 'tree':
      if (!TREE_VARIANTS.has(options.variant)) {
        fail(where, 'options.variant must be one of ' + [...TREE_VARIANTS].join(' | '))
      }
      eachOf('roots', (node, at) => {
        const key = { 'call-stack': 'frame', 'component-tree': 'component', 'file-tree': 'name' }[
          options.variant
        ]
        if (key && !isText(node?.[key])) fail(at, 'missing string "' + key + '"')
      })
      break
    case 'code':
      requireText(where + ' data', data, 'source')
      if (!isText(options.lang) && !isText(data.lang)) {
        fail(where, 'needs options.lang or data.lang')
      }
      break
    case 'diff':
      for (const side of ['oldFile', 'newFile']) {
        const file = data[side]
        if (!file || typeof file !== 'object') {
          fail(where, 'missing object "data.' + side + '"')
          continue
        }
        requireText(where + ' data.' + side, file, 'name')
        if (typeof file.contents !== 'string') fail(where + ' data.' + side, 'missing "contents"')
      }
      break
    case 'diagram':
      requireText(where + ' data', data, 'source')
      break
    case 'checklist':
      eachOf('items', (item, at) => {
        requireText(at, item, 'label')
        requireText(at, item, 'stateLabel')
        if (!CHECK_STATES.has(item?.state)) {
          fail(at, 'state must be one of ' + [...CHECK_STATES].join(' | '))
        }
      })
      break
    case 'matrix': {
      if (!isList(data.columns)) fail(where, 'data.columns must be a non-empty array')
      eachOf('rows', (row, at) => {
        requireText(at, row, 'label')
        if (!isList(row?.cells)) {
          fail(at, 'cells must be a non-empty array')
          return
        }
        if (Array.isArray(data.columns) && row.cells.length !== data.columns.length) {
          fail(at, 'has ' + row.cells.length + ' cells for ' + data.columns.length + ' columns')
        }
        row.cells.forEach((cell, index) => {
          if (cell?.value === undefined) fail(at + '.cells[' + index + ']', 'missing "value"')
          if (cell?.tone !== undefined && !CELL_TONES.has(cell.tone)) {
            fail(at + '.cells[' + index + ']', 'tone must be one of ' + [...CELL_TONES].join(' | '))
          }
        })
      })
      break
    }
    case 'callout':
      requireText(where + ' data', data, 'body')
      if (!CALLOUT_TONES.has(data.tone)) {
        fail(where + ' data', 'tone must be one of ' + [...CALLOUT_TONES].join(' | '))
      }
      break
    case 'html':
      requireText(where + ' data', data, 'html')
      break
    default:
      break
  }
}

function validate(spec) {
  requireText('spec', spec, 'lang')
  requireText('spec', spec, 'title')
  if (!isList(spec.sections)) {
    fail('spec', 'sections must be a non-empty array')
    return
  }
  const seen = new Map()
  const claim = (id, where) => {
    if (!ID_PATTERN.test(id || '')) {
      fail(where, 'id "' + id + '" must match ' + ID_PATTERN.source)
      return
    }
    if (seen.has(id)) fail(where, 'duplicate id "' + id + '", already used by ' + seen.get(id))
    else seen.set(id, where)
  }

  spec.sections.forEach((section, sectionIndex) => {
    const where = 'section[' + sectionIndex + ']' + (section?.id ? ' #' + section.id : '')
    requireText(where, section, 'title')
    claim(section?.id, where)
    if (!isList(section?.visuals)) {
      fail(where, 'visuals must be a non-empty array')
      return
    }
    section.visuals.forEach((visual, visualIndex) => {
      const at = where + ' visual[' + visualIndex + ']' + (visual?.id ? ' #' + visual.id : '')
      requireText(at, visual, 'title')
      claim(visual?.id, at)
      if (!COMPONENTS.has(visual?.component)) {
        fail(at, 'component must be one of ' + [...COMPONENTS].join(' | '))
        return
      }
      if (visual.callout) {
        requireText(at + ' callout', visual.callout, 'body')
        if (!CALLOUT_TONES.has(visual.callout.tone)) {
          fail(at + ' callout', 'tone must be one of ' + [...CALLOUT_TONES].join(' | '))
        }
      }
      if (visual.links !== undefined) {
        if (!Array.isArray(visual.links)) fail(at, 'links must be an array')
        else
          visual.links.forEach((link, index) => {
            requireText(at + ' links[' + index + ']', link, 'text')
            requireText(at + ' links[' + index + ']', link, 'href')
          })
      }
      validateData(at, visual)
    })
  })
}

/* ------------------------------------------------------------------ emitting */

const indent = (text, pad) =>
  String(text)
    .split('\n')
    .map((line) => (line.trim() === '' ? '' : pad + line))
    .join('\n')

function captionMarkup(caption, pad) {
  if (!caption || (!caption.kind && !caption.name && !caption.meta)) return ''
  const left = [
    caption.kind ? '<span class="panel-kind">' + esc(caption.kind) + '</span>' : '',
    caption.name ? '<span class="caption-name">' + esc(caption.name) + '</span>' : '',
  ]
    .filter(Boolean)
    .join(' ')
  const right = caption.meta ? '<span class="caption-meta">' + esc(caption.meta) + '</span>' : ''
  return (
    pad + '<div class="code-caption">\n' +
    pad + '  <span>' + left + '</span>\n' +
    (right ? pad + '  ' + right + '\n' : '') +
    pad + '</div>\n'
  )
}

function bodyMarkup(visual, pad) {
  const hostId = visual.id + '-host'
  if (visual.component === 'html') return indent(visual.data.html, pad)
  if (BARE_HOSTS[visual.component]) {
    return pad + '<div id="' + hostId + '" class="' + BARE_HOSTS[visual.component] + '"></div>'
  }
  const host = PANEL_HOSTS[visual.component]
  return (
    pad + '<div class="code-panel">\n' +
    captionMarkup(visual.caption, pad + '  ') +
    pad + '  <' + host.tag + ' id="' + hostId + '" class="' + host.className + '"></' + host.tag + '>\n' +
    pad + '</div>'
  )
}

function visualMarkup(visual) {
  const pad = '          '
  const parts = [pad + '<article id="' + esc(visual.id) + '" class="visual-block" data-toc-visual>']
  parts.push(pad + '  <header class="visual-header">')
  parts.push(pad + '    <p class="visual-number" data-visual-number></p>')
  parts.push(pad + '    <div>')
  parts.push(pad + '      <h3 class="visual-title" data-visual-title>' + esc(visual.title) + '</h3>')
  if (isText(visual.copy)) {
    parts.push(pad + '      <p class="visual-copy">' + esc(visual.copy) + '</p>')
  }
  if (isList(visual.links)) {
    const links = visual.links
      .map((link) => '<a href="' + esc(link.href) + '">' + esc(link.text) + '</a>')
      .join('')
    parts.push(pad + '      <p class="visual-copy visual-links">' + links + '</p>')
  }
  if (isText(visual.source)) {
    parts.push(pad + '      <p class="source-line">' + esc(visual.source) + '</p>')
  }
  parts.push(pad + '    </div>')
  if (isText(visual.interactive)) {
    parts.push(pad + '    <span class="interaction-status">' + esc(visual.interactive) + '</span>')
  }
  parts.push(pad + '  </header>')
  parts.push(bodyMarkup(visual, pad + '  '))
  if (visual.callout) {
    parts.push(pad + '  <div id="' + esc(visual.id) + '-callout" class="artifact-surface visual-aside"></div>')
  }
  parts.push(pad + '</article>')
  return parts.join('\n')
}

function mainMarkup(spec) {
  const parts = []
  parts.push('        <header class="document-header">')
  if (isText(spec.kicker)) {
    parts.push('          <p class="document-kicker">' + esc(spec.kicker) + '</p>')
  }
  parts.push('          <h1 class="document-title">' + esc(spec.title) + '</h1>')
  if (isText(spec.lead)) {
    parts.push('          <p class="document-summary">' + esc(spec.lead) + '</p>')
  }
  if (isList(spec.meta)) {
    parts.push('          <ul class="document-meta">')
    for (const entry of spec.meta) parts.push('            <li>' + esc(entry) + '</li>')
    parts.push('          </ul>')
  }
  parts.push('        </header>')

  for (const section of spec.sections) {
    parts.push('')
    parts.push('        <section id="' + esc(section.id) + '" class="doc-section" data-toc-section>')
    parts.push('          <header class="section-header">')
    parts.push('            <p class="section-number" data-section-number></p>')
    parts.push('            <div>')
    parts.push('              <h2 class="section-title" data-section-title>' + esc(section.title) + '</h2>')
    if (isText(section.summary)) {
      parts.push('              <p class="section-summary">' + esc(section.summary) + '</p>')
    }
    parts.push('            </div>')
    parts.push('          </header>')
    parts.push('')
    parts.push(section.visuals.map(visualMarkup).join('\n\n'))
    parts.push('        </section>')
  }

  if (spec.closing && isText(spec.closing.text)) {
    const { text, href, linkText } = spec.closing
    let body
    if (isText(href) && isText(linkText)) {
      body = esc(text) + ' <a href="' + esc(href) + '">' + esc(linkText) + '</a>'
    } else if (isText(href)) {
      body = '<a href="' + esc(href) + '">' + esc(text) + '</a>'
    } else {
      body = esc(text)
    }
    parts.push('')
    parts.push('        <footer class="document-closing">')
    parts.push('          <p class="closing-text">' + body + '</p>')
    parts.push('        </footer>')
  }
  return parts.join('\n')
}

function dataBlocks(spec) {
  const blocks = []
  for (const section of spec.sections) {
    for (const visual of section.visuals) {
      if (visual.component !== 'html') {
        blocks.push(
          '    <script id="' + visual.id + '-data" type="application/json">\n' +
            '      ' + jsonForScript(visual.data) + '\n' +
            '    </script>',
        )
      }
      if (visual.callout) {
        blocks.push(
          '    <script id="' + visual.id + '-callout-data" type="application/json">\n' +
            '      ' + jsonForScript(visual.callout) + '\n' +
            '    </script>',
        )
      }
    }
  }
  return blocks.join('\n')
}

const SYNC_CALL = {
  statCards: (id) => "createStatCards('" + id + "-host', readData('" + id + "-data'))",
  fileChanges: (id) => "createFileChangeList('" + id + "-host', readData('" + id + "-data'))",
  pseudocode: (id) => "createPseudocode('" + id + "-host', readData('" + id + "-data'))",
  checklist: (id) => "createChecklist('" + id + "-host', readData('" + id + "-data'))",
  matrix: (id) => "createMatrix('" + id + "-host', readData('" + id + "-data'))",
  callout: (id) => "createCallout('" + id + "-host', readData('" + id + "-data'))",
  tree: (id, visual) =>
    "createTree('" + id + "-host', readData('" + id + "-data'), " +
    JSON.stringify({
      variant: visual.options.variant,
      collapsible: visual.options.collapsible === true,
    }) + ')',
}

const ASYNC_CALL = {
  signatures: (id) => "createSignatureList('" + id + "-host', readData('" + id + "-data'))",
  diagram: (id, visual) => {
    const rest = { ...visual.options }
    const options = Object.keys(rest).length ? ', ' + JSON.stringify(rest) : ''
    return "renderDiagram('" + id + "-host', readData('" + id + "-data').source" + options + ')'
  },
  code: (id, visual) => {
    const options = { ...visual.options }
    if (!options.lang && visual.data.lang) options.lang = visual.data.lang
    return (
      "renderCode('" + id + "-host', readData('" + id + "-data').source, " +
      JSON.stringify(options) + ')'
    )
  },
  diff: (id) =>
    "renderDiff('" + id + "-host', readData('" + id + "-data').oldFile, readData('" + id + "-data').newFile)",
}

function bootstrap(spec) {
  const pad = '      '
  const lines = []
  const zh = String(spec.lang).toLowerCase().startsWith('zh')
  const ui = { interactive: zh ? '可互動' : 'Interactive', ...(spec.messages?.ui || {}) }
  const renderer = spec.messages?.renderer || {}

  if (Object.keys(renderer).length) {
    lines.push('Object.assign(rendererMessages, ' + jsonForScript(renderer) + ')')
  }
  lines.push('Object.assign(uiMessages, ' + jsonForScript(ui) + ')')
  lines.push('')
  lines.push('/** Label an interactive visual the probe can see but the spec did not name. */')
  lines.push('function ensureInteractionStatus() {')
  lines.push('  for (const visual of document.querySelectorAll(\'[data-toc-visual]\')) {')
  lines.push('    if (!visual.querySelector(\'.tree-toggle, .is-scrollable\')) continue')
  lines.push('    if (visual.querySelector(\'.interaction-status\')) continue')
  lines.push('    visual')
  lines.push('      .querySelector(\'.visual-header\')')
  lines.push('      ?.append(element(\'span\', \'interaction-status\', uiMessages.interactive))')
  lines.push('  }')
  lines.push('}')
  lines.push('')
  lines.push('localizeSourceLines()')

  const asyncCalls = []
  for (const section of spec.sections) {
    for (const visual of section.visuals) {
      const normalized = { ...visual, options: visual.options || {} }
      if (SYNC_CALL[visual.component]) {
        lines.push(SYNC_CALL[visual.component](visual.id, normalized))
      } else if (ASYNC_COMPONENTS.has(visual.component)) {
        asyncCalls.push(ASYNC_CALL[visual.component](visual.id, normalized))
      }
      if (visual.callout) {
        lines.push(
          "createCallout('" + visual.id + "-callout', readData('" + visual.id + "-callout-data'))",
        )
      }
    }
  }

  if (asyncCalls.length) {
    lines.push('await Promise.all([')
    for (const call of asyncCalls) lines.push('  ' + call + ',')
    lines.push('])')
  }
  if (isText(spec.js)) {
    lines.push('')
    lines.push(spec.js.trim())
  }
  lines.push('')
  lines.push('ensureInteractionStatus()')
  lines.push('buildToc()')
  return indent(lines.join('\n'), pad)
}

const BUILDER_CSS = `
      /* build.mjs: layout for spec-level extras the demo template never showed. */
      .visual-links {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
      }

      .visual-aside {
        margin-top: 20px;
      }

      .document-closing {
        display: block;
        margin-top: 64px;
        padding: 40px 0 24px;
        border-top: 1px solid var(--artifact-border);
      }

      .closing-text {
        max-width: var(--prose-measure);
        margin: 0;
        color: var(--artifact-muted);
        font-size: 17px;
        line-height: var(--prose-line-height);
      }
`

/* ---------------------------------------------------------------------- main */

function replaceOnce(html, pattern, replacement, label) {
  if (!pattern.test(html)) throw new Error('template anchor not found: ' + label)
  return html.replace(pattern, () => replacement)
}

function build(spec, template) {
  let html = template
  html = replaceOnce(html, /<html lang="[^"]*">/, '<html lang="' + esc(spec.lang) + '">', 'html lang')
  html = replaceOnce(html, /<title>[\s\S]*?<\/title>/, '<title>' + esc(spec.title) + '</title>', 'title')
  html = replaceOnce(
    html,
    /<p class="toc-kicker">[\s\S]*?<\/p>/,
    isText(spec.kicker) ? '<p class="toc-kicker">' + esc(spec.kicker) + '</p>' : '',
    'toc kicker',
  )
  html = replaceOnce(
    html,
    /<p class="toc-title" data-toc-document-title>[\s\S]*?<\/p>/,
    '<p class="toc-title" data-toc-document-title>' + esc(spec.tocTitle || spec.title) + '</p>',
    'toc title',
  )
  html = replaceOnce(
    html,
    /<!-- Replace the visible demo[\s\S]*?-->\n/,
    '',
    'template banner comment',
  )
  html = replaceOnce(
    html,
    /\n {4}<\/style>/,
    '\n' + BUILDER_CSS + (isText(spec.css) ? '\n' + indent(spec.css.trim(), '      ') + '\n' : '') +
      '    </style>',
    'style close',
  )
  html = replaceOnce(
    html,
    /<main class="artifact-main" id="artifact-main">[\s\S]*?<\/main>/,
    '<main class="artifact-main" id="artifact-main">\n' + mainMarkup(spec) + '\n      </main>',
    'main',
  )
  html = replaceOnce(
    html,
    /\n {4}<!-- Escape script-sensitive characters[\s\S]*?(?=\n {4}<script type="module">)/,
    '\n' + dataBlocks(spec),
    'demo data blocks',
  )

  const anchor = 'window.ArtifactUI = ArtifactUI'
  const start = html.indexOf(anchor)
  if (start < 0) throw new Error('template anchor not found: ArtifactUI export')
  const end = html.indexOf('</script>', start)
  html =
    html.slice(0, start + anchor.length) + '\n\n' + bootstrap(spec) + '\n    ' + html.slice(end)

  if (/\bdata-demo\b/.test(html)) throw new Error('demo scaffolding survived the build')
  return html
}

const [specPath, outPath] = process.argv.slice(2)
if (!specPath || !outPath) {
  console.error('usage: node build.mjs <spec.json> <out.html>')
  process.exit(2)
}

let spec
try {
  spec = JSON.parse(readFileSync(resolve(specPath), 'utf8'))
} catch (error) {
  console.error('cannot read spec ' + specPath + ': ' + error.message)
  process.exit(1)
}

validate(spec)
if (problems.length) {
  console.error('spec is not buildable (' + problems.length + ' problem(s)):')
  for (const problem of problems) console.error('  - ' + problem)
  process.exit(1)
}

try {
  const template = readFileSync(resolve(HERE, 'template.html'), 'utf8')
  const html = build(spec, template)
  writeFileSync(resolve(outPath), html)
  const visuals = spec.sections.reduce((total, section) => total + section.visuals.length, 0)
  console.log(
    'built ' + resolve(outPath) + ' — ' + spec.sections.length + ' section(s), ' + visuals + ' visual(s)',
  )
} catch (error) {
  console.error('build failed: ' + error.message)
  process.exit(1)
}

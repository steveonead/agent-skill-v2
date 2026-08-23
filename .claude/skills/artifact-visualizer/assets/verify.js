/**
 * Artifact verification probe.
 *
 * Evaluate this file's contents in the rendered artifact's page, after every
 * renderer has settled, and read the result it returns. It reports the defects a
 * browser can prove and names the visuals worth a screenshot, so the whole
 * verification loop costs one evaluation plus a few targeted captures.
 *
 * Returns { ok, problems, visuals, suspects }.
 *   problems: one string per proven defect, empty when the artifact passes.
 *   visuals:  every visual with its absolute page position.
 *   suspects: the visuals to screenshot, defective ones first.
 */
;(() => {
  const problems = []
  const all = (selector, root = document) => [...root.querySelectorAll(selector)]
  const inDemo = (node) => Boolean(node.closest('[data-demo]'))
  const positionOf = (node) => Math.round(node.getBoundingClientRect().top + window.scrollY)
  const identify = (node) => node.id || (typeof node.className === 'string' && node.className) || node.tagName

  const visuals = all('[data-toc-visual]').map((visual) => ({
    id: visual.id,
    title: (visual.querySelector('[data-visual-title]')?.textContent || '').trim(),
    y: positionOf(visual),
  }))
  const flagged = new Set()
  const blame = (node, message) => {
    problems.push(message)
    const visual = node.closest('[data-toc-visual]')
    if (visual?.id) flagged.add(visual.id)
  }

  // Demo scaffolding the artifact was supposed to replace.
  for (const demo of all('[data-demo]')) {
    problems.push('leftover demo section: ' + (demo.id || demo.className))
  }

  // A host that stayed empty means its data block, its id, or its call is wrong.
  const hostSelector = [
    '.mermaid-host', '.diff-host', '.code-host', '.matrix-host', '.tree-host',
    '.pseudocode-host', '.checklist-host', '.filechange-list', '.signature-list',
    '.stat-grid', '.mockup-frame',
  ].join(',')
  for (const host of all(hostSelector)) {
    if (inDemo(host) || host.childElementCount > 0) continue
    blame(host, 'empty mount: ' + identify(host))
  }

  // A renderer that failed replaced its mount with the local error component.
  for (const failure of all('.renderer-error')) {
    if (inDemo(failure)) continue
    blame(failure, 'renderer error: ' + (failure.closest('[data-toc-visual]')?.id || 'unknown visual'))
  }

  // Content wider than its box overlaps whatever sits beside it, unless something
  // between it and its visual gives it a scroll track. Diagram renderers manage
  // their own SVG geometry, so their internals stay out of this.
  const scrolls = new Set(['auto', 'scroll'])
  const contained = (node) => {
    for (let box = node; box && !box.matches('[data-toc-visual]'); box = box.parentElement) {
      if (scrolls.has(getComputedStyle(box).overflowX)) return true
    }
    return false
  }
  for (const node of all('.artifact-main *')) {
    if (inDemo(node) || node.closest('svg') || node.scrollWidth <= node.clientWidth + 1) continue
    if (contained(node)) continue
    blame(node, 'content overflows with no scroll track: ' + identify(node))
  }
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 1) {
    problems.push('the page scrolls horizontally')
  }

  // Table of contents: complete, resolvable, and self-contained in the viewport.
  const rail = document.querySelector('.toc-rail')
  const links = all('.toc-link')
  const sublinks = all('.toc-sublink')
  if (links.length !== all('[data-toc-section]').length) {
    problems.push('the table of contents is missing sections')
  }
  if (sublinks.length !== visuals.length) {
    problems.push('the table of contents is missing visuals')
  }
  for (const link of [...links, ...sublinks]) {
    const anchor = link.getAttribute('href') || ''
    if (!document.getElementById(anchor.slice(1))) problems.push('dead anchor: ' + anchor)
  }
  // The rail is sticky and grows to its content, so the accordion fails by pushing
  // the rail past the viewport rather than by growing a scrollbar inside it.
  if (rail && rail.getBoundingClientRect().height > window.innerHeight + 1) {
    problems.push('the table of contents is taller than the viewport at this size')
  }

  // Interactive visuals must say so.
  for (const visual of all('[data-toc-visual]')) {
    const interactive = visual.querySelector('.tree-toggle, .is-scrollable')
    if (!interactive || visual.querySelector('.interaction-status')) continue
    blame(visual, 'interactive visual has no interaction-status text: ' + visual.id)
  }

  // Embedded data must survive its script context.
  for (const block of all('script[type="application/json"]')) {
    try {
      JSON.parse(block.textContent || '')
    } catch (error) {
      problems.push('unparsable data block ' + block.id + ': ' + error.message)
    }
  }

  const suspects = [
    ...visuals.filter((visual) => flagged.has(visual.id)),
    ...(visuals.length ? [visuals[0], visuals[visuals.length - 1]] : []),
  ].filter((visual, index, list) => list.findIndex((other) => other.id === visual.id) === index)

  return { ok: problems.length === 0, problems, visuals, suspects }
})()

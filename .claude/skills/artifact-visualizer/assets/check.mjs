#!/usr/bin/env node
/**
 * Run the verify.js probe against a built artifact.
 *
 *   node check.mjs <out.html> [width] [height]     # default 1440 900
 *
 * With `agent-browser` on PATH it sets the viewport, opens the file, waits for
 * the renderers to settle, and pipes verify.js into `agent-browser eval --stdin`,
 * printing the probe's JSON. Without it, it prints the commands to run by hand.
 */
import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = dirname(fileURLToPath(import.meta.url))
const [target, width = '1440', height = '900'] = process.argv.slice(2)
if (!target) {
  console.error('usage: node check.mjs <out.html> [width] [height]')
  process.exit(2)
}

const file = resolve(target)
const probe = resolve(HERE, 'verify.js')
const url = 'file://' + file
const steps = [
  ['set', 'viewport', width, height],
  ['open', url],
  ['wait', '8000'],
]

const run = (args, input) =>
  execFileSync('agent-browser', args, { input, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 })

let available = true
try {
  execFileSync('agent-browser', ['--version'], { stdio: 'ignore' })
} catch {
  available = false
}

if (!available || !existsSync(file)) {
  if (!existsSync(file)) console.error('missing artifact: ' + file)
  console.log('Run these, then read the JSON the last one prints:\n')
  for (const step of steps) console.log('  agent-browser ' + step.join(' '))
  console.log('  cat ' + probe + " | agent-browser eval --stdin --json\n")
  process.exit(existsSync(file) ? 0 : 1)
}

try {
  for (const step of steps) run(step)
  // verify.js ends in one parenthesized call expression, which `eval --stdin`
  // returns as-is. Do not wrap it: a `return` prefix makes the CLI reject it.
  process.stdout.write(run(['eval', '--stdin', '--json'], readFileSync(probe, 'utf8')))
} catch (error) {
  console.error('probe failed: ' + (error.stderr || error.message))
  process.exit(1)
}

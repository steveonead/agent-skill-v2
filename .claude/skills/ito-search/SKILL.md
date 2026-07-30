---
name: ito-search
description: Research a topic across several sources at once, then report a TL;DR, an explanation, and references.
disable-model-invocation: true
---

# ito-search

Research a question by dispatching search sub agents, then judging and writing up what they bring back yourself.

`--codebase` adds Step 2.

## Step 1: Scope the question

Break the request into concrete sub-questions, each one answerable by a single search, and let complexity set both the count and each searcher's tool-call budget: one sub-question and up to 10 calls for a single fact, two and up to 15 calls each for a comparison or a multi-part request, three and up to 20 calls each for a question spanning distinct domains.

Set the time range: prefer material published within the last year, unless the request or the subject names a version, release, or era (Vue 2, ES5, a 2019 outage), in which case the range follows the subject.

Give each sub-question one or two tools, picked in this order of preference:

- `exa`: the open web, articles, blog posts, comparisons, news, and the first look at a repository's issues and discussions
- `context7`: library and framework documentation, API syntax, configuration, version migration
- `deepwiki`: how a public GitHub repository works internally
- `gh` CLI: confirms the details of an issue, PR, release, or commit that `exa` already surfaced
- built-in `WebSearch` and `WebFetch`: use these when every tool above is unavailable or has come back empty

**Done when**: Every sub-question is written down.

## Step 2: Explore the codebase (`--codebase` only)

Dispatch an Explore agent to report the state relevant to the request, each fact cited to a file path: versions pinned in the dependency manifests, where the relevant behaviour lives today, and the constraints the code imposes.

Fold those facts into the sub-questions, rewriting every one the codebase touches against a cited fact.

## Step 3: Dispatch the searchers

Send one sub agent per sub-question, each on the harness's mid tier (`sonnet` in Claude Code).

Give each agent its sub-question, its time range, its tools, its call budget, and this reporting contract:

- one entry per finding, carrying title, URL, publication date, publisher, and the passage that answers the question, quoted or closely paraphrased so it can be judged here from the entry alone
- each passage condensed to the part that bears on the sub-question, and the entries returned on their own, with no account of the search that found them
- findings reported as found, including ones that contradict each other
- spend the call budget as a ceiling, and report back as soon as the sub-question is answered

**Done when**: Every sub-question has a report back and every finding carries a URL and a date.

## Step 4: Filter and synthesize

Judge every finding against [`references/source-quality.md`](references/source-quality.md), and record a keep or drop verdict with a one-line reason.

Corroborate any claim that rests on a single finding before building on it, either by matching it against another surviving finding or by sending one more targeted search.

**Done when**: Every finding has a verdict and every claim you plan to state has at least one named surviving source behind it.

## Step 5: Write the answer

Write it plain and short: one sentence where one will do, bullets where a paragraph would only string them together, each point stated once.

Three sections, in order:

1. **TL;DR**: the answer in a line or two
2. **Explanation**: the evidence, where sources disagree, and what the codebase state implies when Step 2 ran
3. **References**: title, publisher, URL, and publication date per entry

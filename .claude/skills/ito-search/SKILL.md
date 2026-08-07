---
name: ito-search
description: Get a concise, evidence-backed answer from authoritative sources, with optional codebase context.
argument-hint: "你想研究什麼問題？想先讓我看過目前的 codebase，加上 --codebase 參數。"
disable-model-invocation: true
---

## Step 1: Classify and frame the question

Treat `--codebase` as a workflow flag and the remaining arguments as the research question. Use the current conversation when the question is implicit.

Classify the question by the smallest tier that covers every requested facet:

- **Simple**: one fact, one narrow claim, or one source lookup.
- **Comparative**: a direct comparison, tradeoff, or two independent claims.
- **Complex**: three or more independent lines of inquiry, an exhaustive survey, conflicting claims, or multi-stage synthesis.

Phrase each research question so it stands on its own, and apply the tier's hard budget across the run:

| Tier | Research questions | Search sub-agents | Search calls per research question |
| --- | ---: | ---: | ---: |
| Simple | 1 | 0 | 3 |
| Comparative | 2 | 2 | 5 |
| Complex | 3 | 3 | 8 |

Count each query issued to a search tool, including retries and follow-up verification queries. Treat every number in the table as a maximum, and stop below it when the evidence is sufficient. When `--codebase` is present, permit one code-inspection sub-agent beyond these budgets. Set the relevant time range from the question, or record an unrestricted time range.

Finish when the question has one tier, the corresponding self-contained research questions, a time range, and recorded sub-agent and search-call budgets. Continue to Step 2 when `--codebase` is present. Otherwise continue to Step 3 and draw every finding from external sources.

## Step 2: Inspect the codebase when requested

Use the harness's delegation capability to dispatch one code-inspection sub-agent. Include the original question and one objective that identifies the local implementation, constraints, versions, and terminology relevant to the research. Require local-only findings with file paths and line references. Wait for its result, then refine the research questions while preserving the tier and budgets.

Finish when the codebase findings have been incorporated into the research questions.

## Step 3: Run budgeted searches

- **Context7 MCP**: current documentation for a named library, framework, SDK, or CLI tool.
- **DeepWiki**: architecture and implementation questions about a public repository.
- **GitHub CLI (`gh`)**: GitHub-native evidence such as repository code, issues, pull requests, and releases.
- **Exa**: sources outside a single documentation or repository boundary.

Discover which tools and capabilities are available in the current harness. For each research question, select the most suitable available listed tool, with the harness's general search capability as the fallback.

Run the Simple tier's searches in the main context.

At the Comparative and Complex tiers, dispatch one search sub-agent per research question. Include the assigned question, tool, call limit, an instruction to start broad and narrow from intermediate findings, and a distinct task boundary that holds each sub-agent to its own question. Require each sub-agent to gather evidence only from external sources reached through its assigned tool, count every search call, distinguish evidence from inference, and return source titles, direct URLs, publication or update dates, and named authors or publishers when exposed. Run independent searches in parallel when the harness supports it.

Keep each delegated research question with its original sub-agent for retries and refinements within the search-call limit. Record an evidence gap for a failed search, an exhausted call limit, or incomplete source checks required by Step 4.

Finish when every research question has evidence or a recorded evidence gap, the number of dispatched search sub-agents and reported search calls is within the tier's budgets, and all external search is complete.

## Step 4: Filter and synthesize the evidence

Before filtering search results, read [`references/source-quality.md`](references/source-quality.md) in full. Apply its Keep and Drop criteria to every returned source, and perform its checks against the evidence Step 3 already returned.

State material uncertainty, and discard weak or duplicate findings. Synthesize the retained evidence into one independently reasoned answer.

Format the answer for scanning:

- **Simple**: state the conclusion in a paragraph of at most three sentences, followed by at most three evidence bullets when needed.
- **Comparative and Complex**: start with a `## Conclusion` heading in the answer's language, then use one `##` heading per research question. At the Complex tier, add two to four key-takeaway bullets under the Conclusion heading. Use a compact table when the compared subjects share the same dimensions.

In each Comparative or Complex research-question section, use at most four evidence bullets. Present additional shared dimensions in a compact table or synthesize them into prose. Keep each paragraph to at most three sentences and each bullet to one claim expressed in at most two sentences. Put code, commands, and configuration examples in their own fenced blocks between paragraphs. End with a **Key sources** section containing only the authoritative direct links that materially support the answer.

Report search-process detail where it explains an evidence gap, limitation, or confidence level.

Finish when every returned source has a keep-or-drop disposition, the answer covers the original question, relevant codebase evidence is reflected when requested, uncertainty and surviving disagreements are identified, every evidence gap is accounted for, the strongest supporting sources are cited, and the tier's formatting limits are satisfied.

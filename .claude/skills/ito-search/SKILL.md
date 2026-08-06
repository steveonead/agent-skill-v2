---
name: ito-search
description: Get a concise, evidence-backed answer from authoritative sources, with optional codebase context.
argument-hint: "What should I research? Pass --codebase to inspect the current codebase first."
disable-model-invocation: true
---

## Step 1: Frame the question

Parse the invocation. Treat `--codebase` as a workflow flag and the remaining arguments as the research question. Use the current conversation when the question is implicit.

Treat a question that spans distinct technologies, repositories, claims, or tradeoffs as complex and split it into two or three self-contained research questions. Keep every other question as one research question. Cap the search at three research questions.

Finish when the original question is represented by one to three distinct research questions. Continue to Step 2 when `--codebase` is present and Step 3 otherwise.

## Step 2: Inspect the codebase when requested

Use the harness's delegation capability to dispatch one sub-agent that can inspect the codebase. Include the original question and one code-inspection objective that identifies the local implementation, constraints, versions, and terminology relevant to the research. Require findings with file paths and line references. Wait for its result, then refine the research questions with that evidence.

Finish when the codebase findings have been incorporated into the research questions.

## Step 3: Assign one search per sub-agent

- **Context7 MCP**: current documentation for libraries, frameworks, SDKs, APIs, CLI tools, and cloud services.
- **DeepWiki**: architecture and implementation questions about a public repository.
- **GitHub CLI (`gh`)**: repository code, issues, pull requests, releases, and other GitHub-native evidence.
- **Exa**: broad web research, current developments, and sources outside a single documentation or repository boundary.

Discover which tools and capabilities are available in the current harness. For each research question, select the most suitable available listed tool, with the harness's general search capability as the fallback.

Use the harness's delegation capability to dispatch one search sub-agent per research question. Choose a sub-agent that can access its assigned tool. Include the assigned question, the assigned tool, an instruction to use exactly that tool, a requirement to distinguish evidence from inference, and a requirement to return source titles and direct URLs in every delegation brief. Run independent searches in parallel when the harness supports it.

When a search fails and the three-sub-agent budget has capacity, dispatch one replacement sub-agent with the next suitable available tool. Count the replacement against the same budget. Record an evidence gap when the retry fails or the budget is exhausted.

Finish when every research question has returned evidence or has a recorded evidence gap after its available retry.

## Step 4: Synthesize the evidence

Evaluate the returned evidence for relevance, authority, recency, and agreement. Resolve conflicts from the available sources, state material uncertainty, and discard weak or duplicate findings. Synthesize the reports into one independently reasoned answer.

Write the answer in this order:

1. State the conclusion first.
2. Support it with concise bullet points. Group them by research question when that improves clarity.
3. Add a **Key sources** section with a few authoritative direct links that materially support the answer.

Prefer one sentence when one sentence is sufficient. Mention search-process detail when it explains an evidence gap, limitation, or confidence level.

Finish when the answer covers the original question, reflects relevant codebase evidence when requested, separates uncertainty from conclusions, accounts for every evidence gap, and cites the strongest supporting sources.

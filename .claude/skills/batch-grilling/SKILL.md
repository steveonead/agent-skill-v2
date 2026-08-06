---
name: batch-grilling
description: Grill the user a whole round of questions at a time about a plan, decision, or idea. Use when the user asks to be grilled in batches, in rounds, or several questions at a time.
user-invocable: false
---

Interview the user relentlessly. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. Ask the whole frontier in one round and wait for the user's answers. Then recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round.

Format each question like so:

```
❓ **Q<n>** - **<question title>**: <question body, might be multiple paragraphs>

A) <option>
B) <option>
C) <option>

➡️ <your recommended option, and why it beats the others>
```

Offer lettered options whenever the decision has discrete candidate answers, and always name your recommendation. When the answer space is open-ended, drop the options and give your recommended answer alone.

Finding _facts_ is your job. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it. A running exploration is an unsettled prerequisite, so only the questions downstream of it wait for the sub-agent to report. Ask the rest of the frontier now. The _decisions_ are the user's, so put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Act on the plan only after the user confirms you have reached a shared understanding.

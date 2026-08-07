---
name: grilling
description: Grill the user one question at a time about a plan, decision, or idea. Use when the user asks to be grilled or wants their thinking stress-tested, and has not asked for questions in batches.
argument-hint: "給我一個模糊的計畫或想法，我一次問一題，幫你釐清。"
user-invocable: false
---

Interview the user relentlessly. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Walk the tree one decision at a time. Ask the highest-leverage question whose prerequisites are already settled, then wait for the user's answer. That answer opens the branches under it, so pick the next question from the tree it leaves behind.

Format each question like so:

```
❓ **Q<n>** - **<question title>**: <question body, might be multiple paragraphs>

A) <option>
B) <option>
C) <option>

➡️ <your recommended option, and why it beats the others>
```

Offer lettered options whenever the decision has discrete candidate answers, and always name your recommendation. When the answer space is open-ended, drop the options and give your recommended answer alone.

Finding _facts_ is your job. When a question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it. While the sub-agent works, ask a question that doesn't depend on the answer. The _decisions_ are the user's, so put each to them and wait.

The session is done when every branch of the design tree has been visited: every decision settled, nothing left silently assumed. Act on the plan only after the user confirms you have reached a shared understanding.

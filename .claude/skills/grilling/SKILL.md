---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
user-invocable: false
---

Interview me relentlessly about every aspect of this until we reach a shared understanding. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

Every question carries 2-4 options labeled **A**, **B**, **C**, **D**, one marked as your recommendation with a one-line reason. Write them as plain text in your reply, never through the AskUserQuestion tool. A bare letter and a free-text answer both count as my reply.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Act only after I confirm we have reached a shared understanding.

# Logic prototype

Use this branch when the question concerns business logic, state transitions, a data shape, or an API that becomes clearer when someone can perform actions and watch state change.

## State the question

Place the one-sentence question in a visible introduction at the top of the demo. Name the state model being explored and what the reviewer should watch for.

## Isolate the model

Put the logic in one small pure module inside the HTML file. Choose the form that matches the question:

- a reducer for discrete actions over one state value
- an explicit state machine when legal actions depend on the current state
- pure functions for independent transformations
- a class or module when the model genuinely owns ongoing internal state

Keep the model independent of the DOM. The page calls the model through its public operations and renders its output.

## Build the shareable demo

Produce one self-contained HTML file with inline HTML, CSS, and JavaScript. It must open directly without a framework, build step, server, or installation.

Write labels in the domain's language so a non-developer can operate the demo. Arrange the page in this order:

1. The question and a one-line explanation of the model.
2. A current-state panel that renders every relevant field with readable labels and updates after each action.
3. Free-play controls for every action, available in any order.
4. Guided walkthroughs in tabs, with one scenario per tab and ordered action buttons below its explanation.

Starting a walkthrough resets the model to a known initial state. Each step performs a real model action and advances the walkthrough. Include the normal path, the hardest relevant edge case, and an action that should be rejected when those scenarios bear on the question.

Use restrained typography, spacing, and one accent color. Keep attention on the state and actions.

## Evaluate it

Give the user the HTML path and the question it answers. Let the user drive the walkthroughs and free-play controls. Add a scenario or action when feedback reveals an assumption that the current demo cannot test.

The logic prototype is complete when a non-developer can operate it, inspect each state change, and support or reject the proposed model. Return to [SKILL.md](../SKILL.md) to record the verdict and preserve the prototype.

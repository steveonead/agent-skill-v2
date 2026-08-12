---
name: ito-visual-spec-v2
description: Generate a visual feature spec with verified explanations, user stories, API interfaces, and wireframes.
argument-hint: "要幫哪個 feature 產 spec？可以附 GitHub issue 編號或連結當輸入來源。"
disable-model-invocation: true
---

# Visual Spec

Produce a visual spec the team reviews in a browser. Use this workflow for changes that require more than a one-paragraph description.

## Step 1: Collect and verify the material

When the invocation arguments name a GitHub issue, read it with `gh issue view <number> --comments`.

Ground every technical claim in the codebase: trace each file path, symbol, endpoint, and data structure the spec will mention to its definition, and read enough surrounding code to state its real shape. Mark anything that extends beyond the current code as `proposed`.

Finish when every identifier the spec will name is traced to a real definition or marked as `proposed`.

## Step 2: Prepare the spec material

Write prose in Traditional Chinese (zh-TW). Keep code, identifiers, and API names in English.

- **Feature**: what the feature does and why, goals and out of scope, and the main flow.
- **User Stories**: one story per behavior a user can observe, each carrying its role statement and acceptance criteria. Include this section when the feature changes behavior a user can observe.
- **API Interface**: one entry per endpoint and one per public function or type. Include one entry per parameter and one response example for each status code that returns a body. Use whichever interface kinds the feature actually has.
- **Wireframe**: screens, navigation, and per-screen states. Identify the start screen, every navigation target, and the available state controls.

Give every acceptance criterion an `AC-NN` identifier and express the criteria as labeled transitions suitable for a `flowchart TD` diagram. Ensure every wireframe navigation target names a screen in the same flow and every screen is reachable from the start screen.

Finish when every applicable section is complete, every acceptance criterion has one labeled transition, every parameter and response body is accounted for, every wireframe screen is reachable, and every `proposed`, `assumption`, and `unknown` claim carries its status.

## Step 3: Render the visual spec

Resolve the output path as `docs/specs/<date>-<feature-slug>.html` under the project root, where `<date>` comes from `date +%F` and the slug is lowercase English kebab-case.

Invoke `visual-artifact` with the prepared material and the resolved output path.

Finish when the HTML artifact exists and `visual-artifact` reports successful structural validation and browser verification.

## Step 4: Deliver

Finish when the delivered report states the file path, gives a one-line summary per section, lists every `proposed`, `assumption`, and `unknown` item, and includes the structural validation and browser verification results.

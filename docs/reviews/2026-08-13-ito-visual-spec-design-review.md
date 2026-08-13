# ito-visual-spec Design Review

- Review date: 2026-08-13
- Review type: read-only design and contract review
- Target: `.claude/skills/ito-visual-spec/SKILL.md`
- Observed output: `docs/specs/2026-08-13-performance-report-phase-1.html`
- Direct dependencies: `grilling`, `batch-grilling`, `visual-artifact`

## Executive Summary

The overall architecture is sound: `ito-visual-spec` owns requirement convergence and semantic completeness, while `visual-artifact` owns presentation, HTML composition, structural validation, and browser verification. The module skeleton, claim-state vocabulary, and caller-supplied render path are useful foundations.

The design is not yet internally consistent enough to be treated as a stable workflow. Four issues should be fixed before relying on update mode or treating successful validation as proof of spec completeness:

1. `proposed` conflates implementation state with resolution state.
2. Early stop contradicts the completion contract of both interview engines.
3. Update mode can overwrite the only valid artifact before validation succeeds.
4. Seeds cross into agent instructions and authored HTML without an explicit untrusted-input boundary.

The observed output passes the current structural validator, but it also demonstrates that the validator does not enforce the complete `ito-visual-spec` contract. In particular, six CRUD endpoints are represented as a summary table without the required per-endpoint parameter and response contracts, yet validation exits successfully.

## Scope And Evidence

This review covers:

- `.claude/skills/ito-visual-spec/SKILL.md`
- `.claude/skills/ito-visual-spec/agents/openai.yaml`
- `.claude/skills/grilling/SKILL.md`
- `.claude/skills/grilling/agents/openai.yaml`
- `.claude/skills/batch-grilling/SKILL.md`
- `.claude/skills/batch-grilling/agents/openai.yaml`
- `.claude/skills/visual-artifact/SKILL.md`
- `.claude/skills/visual-artifact/references/authoring-rules.md`
- `.claude/skills/visual-artifact/references/core-components.md`
- `.claude/skills/visual-artifact/references/spec-components.md`
- `.claude/skills/visual-artifact/scripts/validate_artifact.py`
- `.claude/skills/visual-artifact/assets/template.html`
- `docs/specs/2026-08-13-performance-report-phase-1.html`

Other HTML files under `docs/specs/` were produced by different skill versions and are not used to assess this version's output quality or compatibility.

## Findings

### P0. Claim state and resolution state are conflated

Evidence:

- `ito-visual-spec/SKILL.md:32` defines `open-items` as unresolved items grouped into `proposed`, `assumption`, and `unknown`.
- `ito-visual-spec/SKILL.md:38` requires every design beyond current code to be marked `proposed`.
- `visual-artifact/references/authoring-rules.md:29` defines `proposed` as an intended change or recommendation, not necessarily an unresolved decision.
- `performance-report-phase-1.html:1536` places agreed new tables, APIs, services, and routes under Open Items only because they are not implemented.

Impact:

An agreed design that is ready for implementation is reported as unresolved. Reviewers cannot distinguish a settled proposal from an open product or technical decision. Delivery summaries consequently overstate uncertainty.

Recommendation:

Model two independent axes:

- Claim state: `verified`, `proposed`, `assumption`, `unknown`.
- Resolution state: `settled`, `open`.

Keep settled proposals in their owning modules. Put only genuinely open questions in `open-items`. An assumption may be settled for the current draft or open pending confirmation, so it also needs the second axis.

### P0. Early stop contradicts both interview engines

Evidence:

- `ito-visual-spec/SKILL.md:40-42` allows the user to stop early, preserve partial modules, mark gaps `unknown`, and proceed to preparation and rendering.
- `grilling/SKILL.md:28` allows action only after every branch is visited and the user confirms shared understanding.
- `batch-grilling/SKILL.md:28` has the same action gate.

Impact:

When a user says "stop asking and produce a draft," the wrapper requires rendering while the invoked engine forbids acting. There is no defined precedence, so executions may continue interviewing, refuse to render, or silently override the dependency.

Recommendation:

Make the caller own post-interview action and define two explicit completion states:

- `converged`: every selected branch is settled and the user confirms convergence.
- `draft-authorized`: the user explicitly ends the interview and authorizes a draft with named gaps.

The engine should expose question-selection behavior without owning the wrapper's render decision, or both engine skills should document the caller-controlled early-exit contract.

### P0. Update mode is non-atomic

Evidence:

- `ito-visual-spec/SKILL.md:60-64` keeps the existing artifact path in update mode.
- `visual-artifact/SKILL.md:32` copies the template directly to the resolved target.
- Structural validation and browser verification happen only afterward at `visual-artifact/SKILL.md:36-50`.

Impact:

A validation error, browser failure, tool interruption, or agent failure after the template copy can destroy the only valid version of the existing spec. No rollback or recovery contract exists.

Recommendation:

Write updates to a temporary sibling file in the same directory. Run structural validation and available browser verification against that file. Atomically replace the target only after required checks pass. On failure, retain the original and report the staging path and failure.

### P0. Seeds have no untrusted-input boundary

Evidence:

- `ito-visual-spec/SKILL.md:14` reads GitHub issue comments, files, and inline text as seeds.
- The same material is passed through interview engines into HTML rendering.
- `validate_artifact.py:262-268` rejects authored `<script>` and `<style>` elements but does not reject event-handler attributes, `javascript:` URLs, or other executable markup.

Impact:

Instructions embedded in an issue comment or seed file can compete with workflow instructions. Unescaped or insufficiently constrained seed content can also become active behavior when the generated artifact is opened in a browser.

Recommendation:

State that every seed is untrusted requirement data and never an instruction source. Normalize it into a structured brief, escape literal text, and permit only catalog markup generated by the renderer. Extend validation to reject event-handler attributes, unsafe URL schemes, non-template executable markup, and unexpected scripts.

### P1. Structural validation does not enforce the caller's spec contract

Evidence:

- `ito-visual-spec/SKILL.md:48-50` requires `US-NN`, `AC-NN`, Given/When/Then, complete API entries, parameter rows, response examples, navigation targets, states, and a start screen.
- `validate_artifact.py:168-201` checks only part of the story contract.
- The validator does not check story IDs, global identifier uniqueness, all three acceptance-criterion beats, API ledgers, parameter and response completeness, required modules, claim-state grouping, or lowercase kebab-case section IDs.
- `performance-report-phase-1.html:1486` summarizes six CRUD endpoints in a plain table without individual API entries, parameters, or response examples.
- The same artifact still passes `validate_artifact.py`.

Impact:

"Structural validation passed" can be interpreted as spec completeness even when required contracts are missing. This is a false-positive validation boundary, not merely missing polish.

Recommendation:

Add a spec validation profile or a dedicated `validate_visual_spec.py`. It should validate:

- Required `overview` and `open-items` modules.
- The selected conditional module manifest.
- `US-NN` presence and uniqueness.
- The intended scope and uniqueness of `AC-NN` identifiers.
- Given, When, and Then elements for every criterion.
- One API ledger entry per endpoint or exported symbol.
- One parameter row per parameter and one response example per body-returning status.
- Wireframe start, reachability, targets, screen states, and labels.
- Claim-state and open-item structure.

Until then, name the existing result "HTML shell and component-subset validation," not "spec validation."

### P1. Update mode can preserve stale verified facts

Evidence:

- `ito-visual-spec/SKILL.md:39` carries unchanged sections forward.
- `ito-visual-spec/SKILL.md:54` rechecks only `proposed`, `assumption`, and `unknown` markers.
- `visual-artifact/references/authoring-rules.md:28` presents `verified` claims as current facts.

Impact:

An endpoint, symbol, type, field, or state changed in code can remain marked `verified` when the user updates an unrelated section. The resulting artifact mixes current changes with stale contracts.

Recommendation:

Re-ground all carried technical claims in update mode. At minimum, verify each source path, symbol, and signature. Downgrade claims that cannot be confirmed to `unknown` or `assumption`, and report the changed status.

### P1. Update target detection can overwrite a reference seed

Evidence:

- `ito-visual-spec/SKILL.md:14` treats a file path as a seed.
- `ito-visual-spec/SKILL.md:16` automatically enters update mode whenever arguments name an existing spec under `docs/specs/`.
- The workflow does not define behavior for multiple existing specs, absolute versus relative paths, symlinks, or a path cited only as a comparison source.

Impact:

"Use `docs/specs/old.html` as a reference for a new spec" can be interpreted as authorization to overwrite it. Multiple named specs produce no deterministic update target.

Recommendation:

Require explicit update intent such as `--update <path>`. All other existing paths remain seeds. Resolve the update target to one canonical path and reject or clarify zero or multiple targets before writing.

### P1. Grounding evidence is not preserved across the handoff

Evidence:

- `ito-visual-spec/SKILL.md:38` requires tracing identifiers to definitions.
- Step 3 does not require claim-level source data in the prepared material.
- `visual-artifact/references/authoring-rules.md:33` attaches a source only when the supplied material includes one.
- `ito-visual-spec/SKILL.md:68-70` reports seeds, which are not equivalent to grounding sources.

Impact:

The agent can perform the code investigation but omit its result from the artifact. A reviewer then sees a `verified` claim without enough evidence to reproduce it, and future update runs cannot reliably recheck it.

Recommendation:

Require a source ledger in the prepared material. Each technical claim should carry a path and symbol, a line when stable and useful, and the code revision. Issue-derived claims should retain a canonical URL and comment identity. Distinguish "explicitly proposed new design" from "seed claims existing behavior but no definition was found"; the latter is `unknown`, with search evidence.

### P1. Create-path collision ownership is ambiguous

Evidence:

- `ito-visual-spec/SKILL.md:60` resolves a fixed caller-supplied path.
- `visual-artifact/SKILL.md:26-28` owns collision suffixing for new artifacts while also requiring caller-supplied paths to be honored and create targets to be new.

Impact:

On a same-day, same-slug create, the renderer cannot simultaneously preserve the supplied path, avoid overwriting, and require a new target. Different executions may fail, suffix, or accidentally be treated as updates.

Recommendation:

Give one skill sole ownership. Prefer passing a create naming intent or preferred path to `visual-artifact`, allowing it to select the next available path and return the authoritative actual path. A collision must never imply update mode.

### P2. Mandatory modules conflict with early-stop pruning

Evidence:

- `ito-visual-spec/SKILL.md:24` requires `overview` and `open-items` in every spec.
- `ito-visual-spec/SKILL.md:40` drops modules with no material after an early stop.

Impact:

If a user stops before overview is complete, or a converged design has no open items, the agent must choose between an empty mandatory module and violating the module rule.

Recommendation:

Apply pruning only to conditional modules. Define minimum valid content for mandatory modules: `overview` contains known scope plus named gaps, and `open-items` explicitly states `None` when no item remains.

### P2. Conditional module thresholds are not checkable

Evidence:

- `ito-visual-spec/SKILL.md:28-29` uses "numerous enough" and "fewer" to decide whether data models and domain rules deserve modules.
- `ito-visual-spec/SKILL.md:56` says every module follows its format, while explicit format requirements at lines 48-50 cover only stories, APIs, and wireframes.

Impact:

Different runs can choose different module sets for the same requirement and still satisfy the written completion criterion. Data model, domain rules, overview, and open items can be declared complete without an exhaustive content contract.

Recommendation:

Use relationship-based triggers rather than quantity terms. For example, include `data-model` when cardinality or ownership relationships must be expressed, and include `domain-rules` when behavior requires a state machine, rule matrix, or reusable field dictionary. Define required fields and completion checks for every module.

### P2. API preparation wording is ambiguous

Evidence:

- `ito-visual-spec/SKILL.md:49` says "one entry per parameter."
- `visual-artifact/references/spec-components.md:75` defines one ledger entry per endpoint or exported symbol, and line 101 defines one table row per parameter.

Impact:

The handoff can represent one endpoint with three parameters as three API entries, producing duplicated or malformed renderer input.

Recommendation:

Use: "Give each endpoint or exported symbol one API entry. Add one parameter-table row per parameter and one response example per status code that returns a body."

### P2. `self-contained` contradicts runtime dependencies

Evidence:

- `visual-artifact/SKILL.md:3` describes the output as self-contained.
- `visual-artifact/SKILL.md:48` requires network access for CDN modules.
- `visual-artifact/assets/template.html:7-10` loads Google Fonts.
- `visual-artifact/assets/template.html:1454` loads `beautiful-mermaid` from `esm.sh`.
- `visual-artifact/assets/template.html:1603-1612` loads Shiki and Prettier from `esm.sh`.

Impact:

The HTML is a single file but is not self-contained. Offline, CSP-restricted, or CDN-failure environments lose diagrams, code rendering, or typography. The current blocked branch covers unavailable browser tooling but not unavailable network or runtime dependencies.

Recommendation:

Either call the output a "single-file, network-backed HTML artifact" and expand blocked reasons to include network, CDN, CSP, and runtime failures, or vendor all runtime dependencies before retaining the `self-contained` claim.

### P3. Grilling metadata sends mixed UI signals

Evidence:

- Both interview skills set `user-invocable: false` and display `NOT INVOCABLE`.
- Their `agents/openai.yaml` files still contain default prompts asking the user to invoke `$grilling` or `$batch-grilling`.

Impact:

Internal skill-to-skill use remains viable, but the user-facing picker metadata contradicts the invocation policy.

Recommendation:

If the skills are caller-only, remove or rewrite the user invocation prompts. If direct use is intended, align frontmatter, display names, and policy accordingly.

## Observed Output Assessment

`docs/specs/2026-08-13-performance-report-phase-1.html` demonstrates several strengths:

- It includes all seven selected modules in a coherent order.
- User stories have `US-NN` identifiers and acceptance criteria with Given, When, and Then content.
- The wireframe declares a start screen, navigation targets, and per-screen states.
- Claim states are visible and the artifact explicitly exposes unresolved blockers.
- The current structural validator exits successfully.

It also demonstrates the contract gaps:

- `performance-report-phase-1.html:1486` summarizes six CRUD endpoints without the required per-endpoint ledger details.
- `performance-report-phase-1.html:1536` treats settled but unimplemented architecture as an unresolved proposed item.
- Technical claims are often marked proposed or unknown without a uniform claim-level source ledger.
- Successful validation does not detect these semantic omissions.

## Design Decisions To Preserve

- Keep the separation between semantic convergence and visual rendering.
- Keep scope and module-list confirmation before deeper questions.
- Keep conditional modules to avoid empty template sections.
- Keep the four claim states, but separate them from resolution state.
- Keep explicit `US-NN`, `AC-NN`, API, and wireframe handoff contracts.
- Keep structural validation plus browser verification as separate results.
- Keep honest `blocked` reporting when browser verification cannot run, and broaden its reason taxonomy.
- Keep safe create collision suffixing and explicit update authorization, after assigning each responsibility to one owner.

## Recommended Revision Order

1. Separate claim state from resolution state and redefine `open-items`.
2. Align early-stop and convergence contracts across all three interview-related skills.
3. Make update mode explicit and atomic.
4. Add the untrusted-seed and HTML-safety boundary.
5. Define a complete prepared-material schema with claim-level provenance.
6. Add spec-profile semantic validation and valid/invalid fixtures.
7. Resolve create-path ownership and module completion criteria.
8. Clean up naming, self-contained claims, and metadata wording.

## Suggested Test Matrix

| Scenario | Expected result |
| --- | --- |
| Create with a new slug | New artifact at the authoritative returned path |
| Create with an existing same-day slug | New suffixed path, never implicit update |
| Explicit update succeeds | Original replaced atomically after validation |
| Explicit update fails validation | Original remains byte-for-byte intact |
| Existing spec supplied only as reference | Create mode, reference is never overwritten |
| Multiple update targets | Stop before writing and require one target |
| User confirms convergence | Render a settled spec |
| User explicitly stops early | Render a draft with every unvisited decision marked open |
| GitHub comment contains instructions | Treat as quoted requirement data only |
| Seed contains HTML or unsafe URL | Escape or reject unsafe content |
| API entry omits a body response | Spec validator fails |
| Duplicate or missing US/AC identifiers | Spec validator fails |
| Browser unavailable | Structural result preserved, browser result is blocked |
| CDN or CSP prevents rendering | Browser result is blocked with runtime reason |
| Update after code contract drift | Re-ground or downgrade stale verified claims |

## Validation Record

- `docs/specs/2026-08-13-performance-report-phase-1.html` passes the current `validate_artifact.py`.
- The same artifact contains the API-contract false positive described above.
- All four relevant `agents/openai.yaml` files parse successfully as YAML.
- The available `quick_validate.py` could not run because the environment lacks the Python `yaml` module (`ModuleNotFoundError`). This is validator-tool unavailability, not a skill validation failure.
- The review did not modify any skill or generated HTML file.


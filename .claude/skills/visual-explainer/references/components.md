# Component gallery

Select a component by the relationship the reader must see. Combine only the patterns needed to support the main explanation.

## Presentation pass

After selecting a pattern, choose its presentation by the reading task and the available width. Treat orientation and renderer as variants of the pattern.

| Reader's task | Presentation | Renderer guidance |
| --- | --- | --- |
| Match corresponding details | Parallel views with identical landmarks | Use HTML and CSS when alignment must stay exact |
| Understand two complete states in order | Stacked views with explicit labels and shared internal structure | HTML and CSS or separate Mermaid diagrams can work |
| Follow branching or routed edges | A connected diagram with short node labels | Use Mermaid and put explanatory prose outside the diagram |
| Scan independent text-heavy items | Full-width vertical rows | Use HTML and CSS so each row can grow with its content |

Use a parallel layout only when direct alignment helps and both sides remain legible at the baseline viewport. Stack the same pattern when either side needs more width or the reader can understand each item independently. Apply the template's `.is-stacked` modifier to a compatible grid instead of recreating its one-column layout.

## Comparison and change

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Hero thesis | The reader needs the topic and takeaway immediately | Eyebrow, literal title, focused thesis | Generic slogans or feature lists |
| Not / But | A misconception blocks understanding | Rejected model beside corrected model, one reason | More than one contrast per row |
| Before / After | A change is spatial or structural | Two labeled frames, shared landmarks, highlighted delta | Unmatched structures that force a visual search |
| Change ledger | Several changes need both action and rationale | Keep, cut, or change columns with short what and why rows | Repeating the diff without explaining impact |

```text
BEFORE                         AFTER
+------------------+          +------------------+
| old path         |   --->   | new path         |
| friction here  x |          | direct route   * |
+------------------+          +------------------+
```

Use semantic backgrounds for accepted and removed material. Do not rely on color alone when a short label such as `kept`, `removed`, or `new` makes the state obvious.

For Before / After, keep matching landmarks and a clear before-then-after reading order in either orientation. Use parallel HTML and CSS when the reader must compare corresponding details. Stacked Mermaid diagrams are acceptable when each state is independently understandable.

In a Change ledger, treat a move, rename, or relocation as one paired change. Show the old and new values in one row with a visible direction. Keep a missing counterpart blank or omit it. Do not split one move into separate deletion and addition rows, add placeholder dashes, or draw an arrow toward an empty field.

## Hierarchy and composition

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Architecture map | Parts, boundaries, and major connections define the subject | A few grouped nodes, directional connectors, boundary labels | Exhaustive dependency graphs |
| Pillar grid | Several peer ideas support one outcome | Three to five equal pillars with a shared cap or base | Using peers when the ideas are actually sequential |
| Scope or file tree | Location and containment matter | Pruned tree, highlighted path, short annotations | Dumping the full repository tree |

```text
                 [ shared outcome ]
                  /      |       \
          [pillar A] [pillar B] [pillar C]
```

Group first, label second. The visual silhouette should reveal hierarchy before the reader parses names.

## Flow, sequence, and state

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Numbered flow | Order matters more than participants | Large step numbers, short action, visible handoff | More than one branch |
| Compact vertical flow | A short ordered mental model belongs beside the hero thesis | Connected number nodes, action, brief explanation | Peer ideas, branching, or more than four steps |
| Sequence diagram | Participants exchange messages over time | Few actors, top-to-bottom messages, one highlighted path | Internal calls that do not change understanding |
| State or decision diagram | Conditions change what can happen next | Explicit states, labeled decisions, terminal outcomes | Unlabeled arrows or mixed time scales |

```text
1. RECEIVE  --->  2. CHECK  --->  3. APPLY  --->  4. REPORT
                       |
                       +------> stop with reason
```

Use Beautiful Mermaid when edge routing or branching carries the meaning. Use an HTML numbered flow when the story is linear and labels matter more than graph layout. Use the compact vertical form only for a short sequence in the hero rail. Replace it with a pillar grid or another peer structure when order does not matter.

Treat a terminal result, output, or destination as the consequence of the numbered steps. Leave it unnumbered and distinguish it with a boundary, lower contrast, or another clear state treatment. When a label declares a step count, that count must equal the number of numbered items.

## Time and dependencies

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Timeline or phases | The reader must see order, duration, or maturity | Shared axis, named phases, milestone markers | Equal widths when duration is meaningful |
| Dependency map | Work order or behavior is constrained by prerequisites or consumers | Focus node, incoming and outgoing groups, labeled edges | Crossing lines, duplicate nodes, or presenting a dependency as a suggestion |

Distinguish sequence from schedule. A plan without reliable dates should show phases or dependencies, not a fake calendar.

## Quantity, impact, and uncertainty

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Metric strip | A few numbers anchor scale or outcome | Two to four large values, units, comparison context | Vanity metrics without a baseline |
| Impact map | One change affects several people, systems, or behaviors | Central change, direct effects, second-order effects | Treating every possible effect as equally likely |
| Risk or open-question ledger | Uncertainty changes a decision | Risk or question, consequence, current status or next evidence | Mixing confirmed defects with speculation |

```text
                    [ direct effect ]
                   /
[ change ] -------- [ direct effect ] ---- [ second-order effect ]
                   \
                    [ open question ? ]
```

Keep fact, inference, and unknown visually distinct when the source distinguishes them. A question mark, status label, or dashed boundary is often enough.

## Code and evidence

| Pattern | Use when | Anatomy | Avoid |
| --- | --- | --- | --- |
| Code or diff excerpt | Exact syntax proves a breaking contract, counter-intuitive control flow, shared invariant, or concurrency behavior | Short highlighted excerpt, focused lines, plain-language caption | Full files or decorative code |
| Glossary | A few terms block novice understanding | Term, concise meaning, optional relation | Definitions that introduce more jargon |
| Callout | One implication deserves a pause | Short label, one conclusion, optional evidence pointer | Repeating the section heading |
| Evidence footer | The reader may need to inspect sources | Compact list of files, URLs, commands, or assumptions | Hiding caveats in tiny text |

Introduce what the reader should notice before showing the excerpt. Include the excerpt when the syntax is the shortest reliable proof of a central claim. Use Shiki only when syntax or diff markers materially help.

## Common compositions

These are starting points, not schemas.

| Source context | Useful opening | Likely middle | Useful close |
| --- | --- | --- | --- |
| Diff | Hero thesis plus before / after | Change ledger, focused flow, code evidence | Impact and risks |
| PR | Hero thesis plus architecture or flow | Key changes, behavior path, selected evidence | Impact, unknowns, and evidence |
| Spec | Hero thesis plus overall mental model | Concepts, states, rules, examples | Unknowns and source notes |
| Plan | Hero thesis plus target state | Phases, dependencies, ownership boundaries | Risks and success signals |

## Custom components

Invent a component only when all three statements are true:

1. The reader needs to see a relationship that the existing patterns obscure.
2. The new shape can be understood without lengthy instructions.
3. It reuses the design tokens, typography, spacing, and semantic color roles.

Prefer a direct HTML or inline SVG construction. Give fixed-format visuals stable dimensions so rendering or interaction cannot shift the surrounding layout. Let text-heavy items grow with their content.

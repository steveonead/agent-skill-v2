---
name: ito-write-skill
description: Create a new skill, or edit an existing one, against the writing-great-skills principles.
disable-model-invocation: true
---

Write `SKILL.md`, `agents/openai.yaml`, and every reference file in English, regardless of the conversation language.

Punctuation: use commas, colons, or separate sentences for asides, and a period to split independent clauses, never an em dash or a semicolon.

## Step 1: Load the principles

Read [`references/writing-great-skills.md`](references/writing-great-skills.md) in full at the start of every run, before drafting anything. Look up any **bold term** you are unsure of in [`references/GLOSSARY.md`](references/GLOSSARY.md).

## Step 2: Fix the track and the target

Choose the track from what the user asked for: **creating** a new skill, or **editing** an existing one.

Resolve the skills directory by searching the working directory and its parents for `.claude/skills/`, and record its absolute path. Ask the user for a path when that search finds no directory, or more than one candidate.

## Creating a skill

### Step 3: Interview

Put these five decisions to the user one at a time, waiting for an answer before asking the next. Carry a recommended answer with each question, drawn from the principles, so the user can agree in one word.

1. **Purpose**: what work does this skill do, in one sentence?
2. **Branches**: which distinct ways will it be used?
3. **Invocation**: model-invoked or user-invoked?
4. **Content shape**: steps, reference, or both, and which material belongs behind a context pointer?
5. **Completion criteria**: for each step, what condition tells the agent it is done?

Look up with your tools anything the filesystem can settle, and put to the user only the five decisions above.

Then propose a name built from the purpose and its leading word, and get the user's agreement on it.

### Step 4: Draft

Write the full text of the new `SKILL.md` and its `agents/openai.yaml`, following Frontmatter and Codex metadata below.

## Editing a skill

### Step 3: Classify the request

Read the target `SKILL.md` and its reference files in full, then sort the request into one of two kinds.

A **specified change** names what to change, so take it as given.

When the request is a **symptom** of the skill misbehaving, judge each of the six entries in the Failure modes section of `references/writing-great-skills.md` against it, one by one, and state for each whether it fits. Adopt the cure the reference prescribes for every mode that fits.

### Step 4: Revise

Write out the full revised text of `SKILL.md`, and of `agents/openai.yaml` when the invocation changed.

## Closing steps

### Step 5: Prune with fresh eyes

Write the draft to a temporary file created by the operating system (`mktemp`). Delegate the pruning pass to a fresh agent that has not seen this conversation, and give it only that path plus this brief:

- Run the no-op test on every sentence in isolation, and return a keep-or-cut verdict for each, with a one-line reason for every cut.
- Report duplication, lines that no longer bear on what the skill does, and any prohibition that could be phrased as a positive instruction instead.

Apply its verdicts. Keeping a sentence it marked for cutting is yours to decide.

Delete the temporary file.

### Step 6: Write the files

On the creating track, write `SKILL.md` and `agents/openai.yaml` into `<skills directory>/<name>/`.

On the editing track, show the user the changes and wait for approval before writing.

### Step 7: Report

Report the track, the absolute path of every file written, the number of sentences cut, and each sentence kept against the pruner's verdict with a one-line reason.

## Frontmatter and Codex metadata

Every skill carries a `SKILL.md` and a sibling `agents/openai.yaml`, and a skill is user-invoked in both harnesses or in neither.

`SKILL.md` frontmatter holds `name` and `description`, plus `disable-model-invocation: true` when the skill is user-invoked.

`agents/openai.yaml` holds the Codex side:

```yaml
interface:
  display_name: "Human Readable Name"
  short_description: "One line for the skill picker"
policy:
  allow_implicit_invocation: false
```

A model-invoked skill omits both `disable-model-invocation` and the whole `policy` block. A user-invoked skill carries both.

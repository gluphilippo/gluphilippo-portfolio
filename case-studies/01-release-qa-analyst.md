# Release QA analyst

## Problem

The game ships every week: develop is merged into main on Wednesday, a new limited-time location starts on Thursday. A release is 50–150 commits across client code, server code and thousands of lines of XML content for three platforms. The tracker's fix version is a plan, not a fact: some tickets roll over, some code lands without a ticket. Regression was built from memory, and the same classes of bugs kept coming back: an item added on one platform but not the others, a missing English string, a content date range that doesn't line up, a tutorial step that hides the HUD and never shows it again.

## What the skill does

1. **Scope.** Resolves "the release" to a commit range and a tracker fix version, and reconciles them: tickets with no code, code with no ticket, unverified tickets, hotfixes not merged back, content that goes live later by date.
2. **Classifies the diff** by area (UI, content, economy, social, platform SDK, server state…).
3. **Maps files to risks.** A "hot files" map built from ~2,300 historical tickets and the files their fixes touched: *this file/folder → what broke there before → what to regress when it changes*.
4. **Static checks** for a dozen known pitfalls: platform parity of items, tutorial actions, localisation completeness, date ranges, submodule pointers, double-click races on purchase buttons, paid access activation, sell prices, old player states.
5. **Precedents.** Searches the cached tracker for past bugs on the same files and mechanics.
6. **Writes a test plan** a tester who hasn't seen the code can run: summary, release composition, verified static findings (with file:line, mechanism, precedent, one-line fix), risk table, 8–25 concrete test cases with preconditions and expected results, a regression list filtered to what the diff can reach.

Other modes: draft a bug report from a template, triage "client or server?" from a symptom or crash signature, and refresh its own knowledge from the tracker (reads new bugs, merges new patterns, shows the diff of the knowledge base before saving).

## Knowledge base

Distilled from every bug and task ticket in the project:

| File | Contents |
|---|---|
| hot-files | file/dir → past failures → what to regress |
| process | "what actually fixed the bug" table, forget-checklists (content port, chapter launch, live-op, A/B offer, new HUD button/window/string), condition matrix (reload, platforms, mobile, offline, double click, server time, old state…), bug template, list of non-bugs |
| areas-* (3 files) | patterns by area: symptom, trigger, cause/fix, how to check in the diff, how to check by hand, examples |
| features | how each feature is supposed to work: rules, limits, prices, timings (source of expected results) |

## Design decisions

- **State limits openly.** The skill doesn't play the game; the report says so and leaves manual cases to a human.
- **Instructions in English, output in Russian**: the team reads Russian, while English instructions are more compact and the model follows them more reliably.
- **Only verified findings in "Problems".** Guesses go to "Risks for manual testing".
- **Never commits, pushes or changes tickets** while testing.

## Outcome

- A release test plan in minutes instead of hours, with a consistent structure.
- Static checks catch config-level defects (cross-platform drift, missing strings, broken quest chains) before a tester opens the build.
- The bug history became something the whole team can query, not one person's memory.

---
name: release-qa
description: Use this skill when the user asks to test, QA, check or write a test plan for an update: by default the next weekly release (the develop → main merge), but also a branch, MR, commit range, ticket(s) or the current diff (e.g. "test the release", "what should I check in this branch", "regression for this diff"). Acts as the team's QA engineer: reconciles the release scope between git and the tracker, maps the diff onto bug patterns distilled from the project's ticket history, runs static checks for known pitfalls and produces a test plan with risks, cases and regression. Also use for "file a bug using the QA template" and "is this a client or a server bug?". Not a live playtest.
---

# release-qa

<!-- A skeleton of how I structure QA skills. Project-specific content is replaced with placeholders. -->

## When to use

The user wants an update checked the way the QA team would check it: what can break, what to click, in which environment and state, and what to regress.

Release model (adapt to your project):
- A release = a tracker fix version `<YYYY-MM-DD> <NAME>`; its code = `origin/main..origin/develop` at merge time.
- Hotfixes go straight to `main` and must be merged back.
- Tickets in a fix version are a plan, not a fact.

**Limits: state them in the report, never hide them.** The skill cannot play the game. Findings come from the diff, configs and bug history; manual cases are for a human tester.

## Output language

Instructions are English. Everything the skill produces is in <team language>. Identifiers, paths and error texts are quoted verbatim.

## Knowledge base

`references/` holds knowledge distilled from all tickets (snapshot <date>, <N> issues). Read only what the update touches.

| File | Use it for |
|---|---|
| `references/hot-files.md` | **Start here.** File/dir → what broke there → what to regress. |
| `references/process.md` | "What fixed the bug" table, forget-checklists, condition matrix, bug template, non-bugs. |
| `references/areas-*.md` | Patterns by area. Each pattern: Symptom, Trigger, Cause/fix, **Check in diff**, **Manual check**, Examples. |
| `references/features.md` | How features are supposed to work: source of expected results. |

## Scripts

- `scripts/refresh_cache.py`: download all Bug/Task tickets and the ticket → changed files index.
- `scripts/release_scope.py <version>`: tickets vs commits reconciliation.
- `scripts/search_issues.py <words> [--full]`: search the cached tickets for precedents.
- `scripts/related_issues.py <paths…>`: past tickets that touched the same files.

## Procedure

1. **Scope.** Resolve the target to a commit range and a ticket list; reconcile them.
2. **Classify** the diff by area.
3. **Static checks.** For each known pitfall, check the diff; report only verified problems with file:line, mechanism, precedent and a one-line fix.
4. **Test plan.** Expected results from the ticket and `features.md`. Pick axes from the condition matrix only where the diff makes them relevant.
5. **Report.** Save to `<reports>/<slug>/TEST_PLAN.md` and print a short summary with the path.

Never commit, push or change ticket fields while testing.

## Report template

```
# Test plan: <target>
Scope: <version / branch / range>, <N commits>, tickets: …; main@<sha> → develop@<sha>
Limits: no live run; …

## 1. Summary
## 2. Problems found (static, verified only)
## 3. Risks for manual testing   (area | risk | why | cases)
## 4. Test cases                  (preconditions, steps, expected result + source, axes)
## 5. Regression                  (filtered to what the diff can reach)
## 6. Precedents
```

## Other modes

- **File a bug**: draft with the template from `process.md`; create a ticket only when explicitly asked, show the draft first.
- **Client or server?**: heuristics + crash signatures + duplicate search.
- **Refresh knowledge**: re-download tickets, merge new patterns into `references/`, show the diff before finishing.

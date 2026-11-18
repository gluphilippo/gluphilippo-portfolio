# Merge review before a release

*A skill we built as a team. I use it in my release workflow next to my own [release QA analyst](01-release-qa-analyst.md).*

## What it is

A Claude Code skill that reviews a merge between two branches (usually develop → main before the weekly release) and lists the defects **the merge itself introduces**: not old tech debt, not style. Each finding comes with the commit, a code fragment, how it fails and a one-line fix, grouped by area (client / server / resources) and by impact (real vs potential).

Rules that make it useful:
- **Only what the merge brings**: pre-existing problems are out of scope.
- **Check that the code is live before calling something a bug**: trace config → server → protocol → client → UI. A removed flag nobody reads is dead config, not a defect.
- **Separate guaranteed failures from conditional ones**, and give evidence instead of pointers. High and critical findings need a full trace.
- The diff is sorted by area (client code, server, configs, UI markup, localisation, build, CI, submodules), with a checklist for each area.

## How I use it

The two skills cover different questions:
- **merge-review**: *what in this code will break?* (line-by-line defects)
- **release QA analyst**: *what should a tester check, and where did it break before?* (scope, risks, test cases, regression)

On a release I run both. Then I **verify the merge-review findings myself** before they go to developers. For example, on one release I compared the daily-quest and player-level configs between main and develop with small Python scripts: duplicate task references per date range, the number of task variants, level-by-level differences. That way only confirmed problems were reported, and the false positives were dropped.

## Outcome

Code-level defects are caught before the merge, and with the manual verification step developers get findings they can act on, without noise.

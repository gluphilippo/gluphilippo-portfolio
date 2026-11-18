# QA × AI agents: portfolio

I'm a QA engineer on a live-ops browser game: a social farm/adventure game with weekly releases, published on three web platforms, with a TypeScript client, a Java/Spring server and content driven by XML game-design configs.

Over the last year I moved a lot of my QA routine into **Claude Code skills**: packaged instructions plus scripts and MCP servers that an AI agent follows to do a QA task end to end. This repository describes those tools and the rest of my QA work.

> All project, company, people and infrastructure names are removed. Internal code and knowledge bases stay private; what's here is the design, the numbers and a few generic parts that I rewrote to work anywhere.

## In numbers

| | |
|---|---|
| Bugs reported | **620+** in ~15 months (about 40% of all bugs filed on the project), 575+ of them verified fixed |
| Severity | ~125 Highest, ~240 High |
| Own fixes in the codebase | **140+ commits**: client UI/UX fixes (TypeScript), game-design config fixes, content launches |
| AI tools I built | **5 Claude Code skills** used by the team, 2 MCP servers, a Playwright harness for a canvas-only game |
| Knowledge distilled | ~2,300 bug/task tickets turned into a searchable risk map for release testing |

## Skills I built

| Skill | What it does | Case study |
|---|---|---|
| **Release QA analyst** | Takes a weekly release (or a branch/ticket/diff), reconciles the scope between git and the tracker, maps the diff to bug patterns from the project's whole history, runs static checks for known pitfalls and writes a test plan with risks, cases and regression. Also triages "client or server bug?" and drafts bug reports. | [case-studies/01-release-qa-analyst.md](case-studies/01-release-qa-analyst.md) |
| **TestRail run filler** | Creates a TestRail run with only the cases that apply to this release, checks each one with static analysis scripts and records Passed/Failed with evidence. Cases that need real gameplay stay Untested with a hint for the tester. | [case-studies/02-testrail-run-filler.md](case-studies/02-testrail-run-filler.md) |
| **Test state generator** | Builds a player save "one step before quest X" or "right before cutscene Y" by replaying the game on the real server code in a test harness, so the state looks like real progress (fog of war, objects, rewards). Validates it against client rules. | [case-studies/03-test-state-generator.md](case-studies/03-test-state-generator.md) |
| **Game-design config consultant** | Answers "why does this object/quest/cutscene behave like that and how do I change it?": traces the config chain, explains the mechanism from engine code, finds precedents in other content and proposes a minimal diff for all platforms. | [case-studies/04-game-config-consultant.md](case-studies/04-game-config-consultant.md) |
| **Test environment admin** | An MCP server that turns test preconditions into one sentence: "upload this state to bot_042 on the branch environment and set game time to Thursday 10:00". Creates players, uploads/downloads states with automatic backups, gives items, finishes quests, moves server time. | [case-studies/05-test-env-admin.md](case-studies/05-test-env-admin.md) |

### Skills we built as a team

| Skill | How I use it | Case study |
|---|---|---|
| **Merge review** | Before each release I run it on develop → main next to my release analyst: it finds line-level defects the merge introduces, then I verify its findings with my own config-diff scripts before reporting. | [case-studies/08-merge-review.md](case-studies/08-merge-review.md) |

## Other QA work

- **UI automation for a canvas game**: the game draws everything into one WebGL canvas, so there's no DOM to select. I built a Playwright harness that walks the engine's display list instead, plus a quest autopilot that played a fresh account through the tutorial up to level 5. → [case-studies/06-canvas-playwright.md](case-studies/06-canvas-playwright.md)
- **API testing of a backend microservice**: ran the service locally (Spring Boot + Postgres in a container), wrote a 70-request Postman collection from the README and the controllers, and found two contract violations. → [case-studies/07-api-testing.md](case-studies/07-api-testing.md)
- **Fixing bugs myself**: 140+ commits to the game: mobile input, window layout and scaling, tutorial blockers, helpers/arrows, quest configs, localisation, content launches.

## Generic code in this repo

- [examples/testrail-mcp/](examples/testrail-mcp/): a minimal TestRail MCP server (TestRail API v2) that any Claude Code / MCP client can use to read cases, create runs and post results.
- [examples/skill-skeleton/](examples/skill-skeleton/): the structure I use for a QA skill: trigger description, scope rules, knowledge base layout, procedure, report template.

## Stack

Claude Code (skills, MCP, subagents) · Python · TypeScript/JavaScript · Playwright · Java/Spring test harness · Gradle · Git/GitLab · YouTrack · TestRail · Postman · Podman · Cassandra/Postgres · XML configs

# TestRail run filler

## Problem

Every release had a TestRail run built by hand from a ~100-case suite: pick the sections that apply (limited-time location, story chapter, which live-ops restart), then go through cases that are really config checks ("every quest has a helper", "quest tokens cover the shop", "news and calendar are active in the location's window", "every string has an English translation").

## What the skill does

1. Connects to TestRail through a small MCP server (generic version: [examples/testrail-mcp](../examples/testrail-mcp/)). A setup script checks the API key, builds a venv and registers the server.
2. Reuses the release scope from the QA analyst skill and decides which sections apply.
3. Shows the run name and the case list with reasons for dropped sections, and **creates the run only after confirmation**.
4. Checks every case it can from what actually ships (`git archive` of the release branch, not the working tree), using check scripts:
   - window/date-range timeline of news, calendar and the location
   - quest token income vs total shop cost
   - energy needed per "stopper" object
   - micro-goal ids exist and there are enough objects on the map
   - quest tasks: unresolved references, tasks without a helper, broken chains
   - localisation: every string of the location has a non-empty English value
5. Posts results: **Passed/Failed only for what was actually verified, always with evidence** (file:line, command, numbers). Cases that need gameplay stay Untested with a hint about what a human should look at.

## Outcome

The run is created and pre-filled before manual testing starts; testers spend their time on gameplay cases instead of config checks.

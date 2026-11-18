# TestRail MCP server

A minimal MCP server over TestRail API v2: one file, standard library plus `mcp` and `certifi`.
It lets an AI agent (Claude Code or any MCP client) read a suite, create a run with selected cases and post results.

## Tools

| Tool | What it does |
|---|---|
| `get_sections` | sections of a suite |
| `get_cases` | cases with preconditions, steps, expected results |
| `add_run` | create a run (all cases or a list of case ids) |
| `get_runs` | recent runs with pass/fail counts |
| `get_tests` | tests of a run with current status |
| `add_results_for_cases` | post results: `passed / failed / blocked / retest / untested` + comment |
| `close_run` | close a run (irreversible) |

`untested` posts a comment-only result: TestRail rejects `status_id=3` in results, so the field is omitted and the test keeps its Untested status.

## Setup

1. TestRail → My Settings → API Keys → generate and **save** a key.
2. Install and register:

```sh
python3 -m venv ~/.cache/testrail-mcp/venv
~/.cache/testrail-mcp/venv/bin/pip install -r requirements.txt

claude mcp add testrail --scope user \
  -e TESTRAIL_URL=https://your-company.testrail.io \
  -e TESTRAIL_USER=you@example.com \
  -e TESTRAIL_API_KEY=... \
  -e TESTRAIL_PROJECT_ID=1 \
  -e TESTRAIL_SUITE_ID=1 \
  -- ~/.cache/testrail-mcp/venv/bin/python "$PWD/testrail_mcp.py"
```

3. Restart the Claude Code session.

Errors: HTTP 401 means the key wasn't saved or the login is wrong; `CERTIFICATE_VERIFY_FAILED` means `certifi` is missing from the venv.

## Rule baked into the server instructions

Set Passed/Failed only for cases that were actually verified, and always put the evidence in the comment.

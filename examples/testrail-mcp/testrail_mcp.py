"""Minimal TestRail MCP server (TestRail API v2).

Env (all required): TESTRAIL_URL, TESTRAIL_USER, TESTRAIL_API_KEY,
                   TESTRAIL_PROJECT_ID, TESTRAIL_SUITE_ID.
"""
import base64
import json
import os
import ssl
import urllib.error
import urllib.request

import certifi
from mcp.server.mcpserver import MCPServer

URL = os.environ["TESTRAIL_URL"].rstrip("/")
USER = os.environ["TESTRAIL_USER"]
KEY = os.environ["TESTRAIL_API_KEY"]
PROJECT_ID = int(os.environ["TESTRAIL_PROJECT_ID"])
SUITE_ID = int(os.environ["TESTRAIL_SUITE_ID"])
SSL_CTX = ssl.create_default_context(cafile=certifi.where())
AUTH = "Basic " + base64.b64encode(f"{USER}:{KEY}".encode()).decode()

STATUSES = {"passed": 1, "blocked": 2, "untested": 3, "retest": 4, "failed": 5}

mcp = MCPServer(
    "testrail",
    instructions=(
        f"TestRail at {URL}. Default project {PROJECT_ID}, suite {SUITE_ID}. "
        "Status ids: 1 Passed, 2 Blocked, 3 Untested, 4 Retest, 5 Failed. "
        "Set Passed/Failed only for cases actually verified; always put the evidence in the comment."
    ),
)


def _api(method: str, endpoint: str, body: dict | None = None):
    req = urllib.request.Request(
        f"{URL}/index.php?/api/v2/{endpoint}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": AUTH, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60, context=SSL_CTX) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"TestRail {e.code}: {e.read().decode(errors='replace')}") from None
    return json.loads(raw) if raw else None


def _paged(endpoint: str, key: str) -> list:
    items, offset = [], 0
    while True:
        page = _api("GET", f"{endpoint}&limit=250&offset={offset}")
        if isinstance(page, list):
            return page
        items += page[key]
        if not page.get("_links", {}).get("next"):
            return items
        offset += len(page[key])


@mcp.tool(description="List sections of a suite (id, name, parent_id, depth).")
def get_sections(suite_id: int = SUITE_ID) -> list:
    secs = _paged(f"get_sections/{PROJECT_ID}&suite_id={suite_id}", "sections")
    return [{k: s.get(k) for k in ("id", "name", "parent_id", "depth")} for s in secs]


@mcp.tool(description="List cases of a suite with section, title, preconditions, steps and expected results.")
def get_cases(suite_id: int = SUITE_ID, section_id: int | None = None) -> list:
    ep = f"get_cases/{PROJECT_ID}&suite_id={suite_id}"
    if section_id:
        ep += f"&section_id={section_id}"
    out = []
    for c in _paged(ep, "cases"):
        out.append({
            "id": c["id"], "section_id": c.get("section_id"), "title": c.get("title"),
            "refs": c.get("refs"), "priority_id": c.get("priority_id"),
            "preconds": c.get("custom_preconds"), "steps": c.get("custom_steps"),
            "expected": c.get("custom_expected"),
            "steps_separated": c.get("custom_steps_separated"),
        })
    return out


@mcp.tool(description="Create a test run for a suite. include_all=True takes every case; otherwise pass case_ids.")
def add_run(name: str, suite_id: int = SUITE_ID, description: str = "",
            include_all: bool = True, case_ids: list[int] | None = None) -> dict:
    body = {"suite_id": suite_id, "name": name, "description": description, "include_all": include_all}
    if not include_all:
        body["case_ids"] = case_ids or []
    run = _api("POST", f"add_run/{PROJECT_ID}", body)
    return {k: run.get(k) for k in ("id", "name", "url", "untested_count")}


@mcp.tool(description="List recent runs of the project (optionally only open ones).")
def get_runs(only_open: bool = True, limit: int = 20) -> list:
    ep = f"get_runs/{PROJECT_ID}&suite_id={SUITE_ID}" + ("&is_completed=0" if only_open else "")
    runs = _api("GET", ep + f"&limit={limit}")
    runs = runs["runs"] if isinstance(runs, dict) else runs
    return [{k: r.get(k) for k in ("id", "name", "url", "is_completed", "passed_count",
                                     "failed_count", "untested_count")} for r in runs]


@mcp.tool(description="List tests of a run with case_id, title and current status_id.")
def get_tests(run_id: int) -> list:
    return [{k: t.get(k) for k in ("id", "case_id", "title", "status_id")}
            for t in _paged(f"get_tests/{run_id}", "tests")]


@mcp.tool(description=(
    "Add results to a run by case id. results: [{case_id, status, comment}], "
    "status is passed|failed|blocked|retest|untested or a numeric status_id. "
    "untested adds a comment-only result: the test keeps the Untested status."
))
def add_results_for_cases(run_id: int, results: list[dict]) -> str:
    payload = []
    for r in results:
        st = r.get("status")
        status_id = st if isinstance(st, int) else STATUSES[str(st or "untested").lower()]
        item = {"case_id": int(r["case_id"]), "comment": r.get("comment", "")}
        # TestRail rejects status_id=3 in results; omitting it leaves the test Untested.
        if status_id != STATUSES["untested"]:
            item["status_id"] = status_id
        payload.append(item)
    _api("POST", f"add_results_for_cases/{run_id}", {"results": payload})
    return f"Added {len(payload)} results to run {run_id}"


@mcp.tool(description="Close (complete) a run. Irreversible: results can no longer be added.")
def close_run(run_id: int) -> str:
    _api("POST", f"close_run/{run_id}", {})
    return f"Run {run_id} closed"


if __name__ == "__main__":
    mcp.run()

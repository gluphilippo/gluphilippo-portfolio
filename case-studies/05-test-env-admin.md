# Test environment admin (MCP server)

## Problem

Test preconditions ("player at this state, has these items, quest X done, server time is Thursday 10:00") were set through a browser admin page, separately for each environment: per-branch dynamic environments, debug and prerelease stands for each platform, and a local server. Every step was manual, and a wrong upload could break a test account with no way back.

## What I built

An MCP server (Python) plus a skill that tells the agent how to use it safely. Tools:

`env_info · create_user · get_state · set_state · reset_state · add_item · finish_mission · finish_tutorial · get_time · set_time · add_time_offset · reset_time · find_ids`

- **Environment resolution**: `env` can be a branch name, a CI slug, a ticket id (it finds the branch, even if it was already merged and deleted), a stand name or "local". The reply always names the server that was touched.
- **Safe state upload**: back up the current state first (falling back to the raw DB record if the session can't load it), refuse anything that isn't the persistence format (the client-side projection bricks a player), upload, read back and verify.
- **Guardrails**: never production; on shared stands write only to accounts the user named as theirs or as test ones; game time is global for an environment, so changing it needs confirmation (except on the user's own local server).
- **One-command setup** for macOS and Windows (Git Bash): venv, credentials, registration.

## Outcome

Preconditions take one sentence in chat: "upload the state from step 1 to bot_042 on the branch environment and move the time to Thursday 10:00". Together with the state generator this gives a full loop: generate a state → upload → test → restore from the automatic backup.

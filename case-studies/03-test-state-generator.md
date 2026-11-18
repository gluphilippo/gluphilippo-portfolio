# Test state generator

## Problem

To test quest 14 of a new location, a tester has to reach quest 14. Saves edited by hand ("mark quests 1–13 done") looked wrong in the client: objects visible through the fog of war, bare explored ground, missing rewards. That happens because the client rebuilds fog from obstacles on load, and the server doesn't spawn default objects into cells you open "by hand". Developers used to write a throwaway Java test for every such state.

## What the skill does

One command builds a state:

```
stategen --net <platform> --quest <QUEST_ID>              # one step before the quest is done
stategen --net <platform> --quest <QUEST_ID> --mode open  # quest just opened
stategen --net <platform> --quest <QUEST_ID> --mode done  # quest closed, next ones open
stategen --net <platform> --cutscene <CUTSCENE_ID>        # cutscene starts on entry
stategen --net <platform> --cutscene <CUTSCENE_ID> --trigger step   # one action before it
stategen ... --branch <feature-branch>                    # content that only exists in a branch
```

How it works:
- **Plans** the path to the target: quest dependencies, which tasks to complete, which obstacles must be cleared to open the fog.
- **Replays the game on the real server code** inside a Spring test harness with the platform's real item configs: completes quest tasks through game events, plays cutscenes step by step, clears obstacles, so the result is what a real player would have.
- **Validates the result**: loads it back (`verify`), checks fog invariants, checks client rules, and writes a fog map as the client would see it (ASCII), plus a JSON report.
- For content that exists only in a branch, it makes a git worktree and reuses it.

## Outcome

- A realistic save for any quest or cutscene in ~25 seconds instead of an hour of play or a custom test.
- Bug reproduction and fix verification start from the exact point in the content.
- Paired with the environment admin skill: generate the state, then upload it to a test server in one sentence.

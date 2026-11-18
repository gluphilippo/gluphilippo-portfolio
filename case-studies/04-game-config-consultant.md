# Game-design config consultant

## Problem

All game content (objects, quests, tasks, hints, triggers, cutscenes, drops, locations) is XML configs, duplicated for three platforms. A typical question from QA or a designer: "this object turns into the wrong thing after clearing, how do I fix it?" or "why does this quest task never count?" The answer is spread across configs, engine code on both client and server, and conventions that nobody wrote down.

## What I built

1. **A configuration reference**: 14 chapters, ~600 KB. Every object type and parameter, every quest task type and the server event that counts it, rule events, matchers and actions, ~80 cutscene actions, drops, locations and date ranges. Each entry is checked against the engine code and has usage statistics from the real content. A plain-language version was published as an internal wiki for designers.
2. **A "findings" chapter**: what in the current configs is dead or broken by code (unsupported events, no-op parameters, unhandled cutscene actions, typos that silently never fire). The skill checks it before blaming the designer's config.
3. **A troubleshooting index**: symptom → cause in config → fix, plus "idioms": why designers configure things a certain way.
4. **Two scripts**:
   - `find`: the definition of an id and every reference to it across all config kinds, maps and map states, on all platforms.
   - `analog`: how a tag is usually configured: attribute frequencies, typical values, newest examples. This is how the skill finds precedents ("where has this already been done the way you want?").

## Procedure the skill follows

Pin the ids → collect the whole config chain → explain the current behaviour mechanically → match the symptom against troubleshooting and idioms → find a precedent → propose a minimal before/after diff **for all three platforms**, with side effects (other references, players who already passed this point, date ranges, localisation) and how to verify (generate a state, upload it) → edit files only when asked.

## Outcome

Config questions get an answer with a mechanism and a precedent instead of guesswork, and several silent config defects were found while building the reference.

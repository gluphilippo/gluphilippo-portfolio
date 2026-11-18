# UI automation for a canvas-only game

## Problem

The game renders everything (world and UI) into one WebGL canvas. There are no DOM elements, so the usual Playwright selectors have nothing to find.

## Approach

Test builds expose the engine's application object on `window`. A helper injected into the page (`window.__qa`) works with the **engine's display list** instead of the DOM:

- `walk(predicate)`: depth-first search over visible nodes
- `findText` / `findClass`: find nodes by visible text or by class name
- `point(id)`: convert a node's bounds from stage coordinates to page pixels (taking canvas CSS scaling into account) so Playwright can click it
- clicks bubble up to the nearest button-like ancestor

Generic idea:

```js
// stage coordinates -> CSS pixels of the page
function toPage(rect, stage, canvas) {
  const cr = canvas.getBoundingClientRect();
  const kx = cr.width / stage.width, ky = cr.height / stage.height;
  return { x: cr.left + (rect.x + rect.w / 2) * kx,
           y: cr.top  + (rect.y + rect.h / 2) * ky };
}
```

Scripts:

| Script | What it does |
|---|---|
| smoke | headless: load → accept the agreement window → check that it closed |
| probe | headless: scene tree, visible texts, console errors, screenshot |
| server | keeps a visible Chrome with CDP open; other scripts attach to it |
| step | one action (click by text / coordinates / eval / wait) + screenshot |
| drag | multi-point gesture (harvesting, planting) |
| autopilot | plays quests on its own |

The **quest autopilot** follows a priority list each step: recover from error windows; close the energy shop (it never presses "Buy"); skip cutscene dialogs; follow the tutorial finger; press action buttons (with a stop list for timers and spending); click the object under the quest arrow; if there's nothing to do, call the quest's own helper and follow the arrow or path it shows.

## Lessons

- World objects ignore an instant click: they need hover, then mouse down/up with ~100 ms between them.
- Take a world object's screen centre from bounds relative to the stage, not from local-to-global; the latter was offset by ~100 px.
- Headless Chrome with GPU (Metal) gives 60 fps; software GL is under 1 fps.
- Preconditions (fresh state, energy, items, time) come from the environment admin MCP.

## Outcome

On a clean account the autopilot went through the tutorial, the whole first region and part of the second, up to level 5, unattended. The harness is used for smoke checks and for reproducing UI bugs step by step with screenshots.

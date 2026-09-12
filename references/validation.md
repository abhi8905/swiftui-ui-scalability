# Validate adaptive behavior

Use this reference to turn a layout recommendation into falsifiable checks. Scale the effort to the requested change and available tools. A read-only review remains read-only; propose missing runtime checks rather than silently changing the app to perform them.

## Establish evidence and scope

Record the target, minimum OS, SDK/toolchain, inspected entry view, relevant parent constraints, descendants, and the environments actually exercised. An app-level deployment default may differ from a target override or extension target.

Classify each finding:

| Evidence | What it supports |
| --- | --- |
| Static source evidence | A particular branch, constraint, dependency, or identity change exists. Explain its triggering condition. |
| Runtime observation | A recorded environment reproduces clipping, loss of state, unreachable controls, layout oscillation, or another concrete failure. |
| Measurement/profile | Measured layout frames, update frequency, scrolling behavior, or performance under specified conditions. |
| Hypothesis / untested | The risk is plausible but depends on missing caller code, runtime behavior, or content. State the next check. |

Do not describe a screenshot as proof of interaction correctness or a successful build as proof of fit. Grep matches and fixed-number counts are not severity scores.

## Exercise space, content, and transitions

Choose extremes and boundary cases from the feature's actual supported environments. A useful initial set of **container sizes in points** is 320×568, 390×844, 600×400, 768×1024, 1024×768, and an intermediate 477×613. These are illustrative test inputs, not device assumptions, support requirements, or production breakpoints. Add the actual system minimum, maximum, and nested presentation sizes relevant to the app.

- Resize width and height independently, including a short wide container. Sweep through each arrangement boundary in both directions and while the screen is active. If the layout uses an explicit threshold, inspect values just below, at, and above it; verify the threshold has a content-based rationale.
- Exercise iPad window arrangements and resizable iPhone contexts when available. A narrow iPad window and an enlarged phone-idiom window should both behave sensibly. A frame override on a preview does not automatically reproduce every system trait or safe-area change.
- Test default and largest standard Dynamic Type, then accessibility sizes including the largest. Include long translations, meaningful empty content, unusually long labels, and RTL when applicable. Do not use invented unreadable text if realistic localized content exposes the same constraint.
- Show and hide the keyboard on an actual input screen. Confirm the focused field and primary action remain reachable by scrolling or appropriate safe-area accommodation. Test both physical landscape orientations where asymmetric safe areas matter.
- Resize with entered text, selected items, a navigation path, nonzero scroll position, focus, and in-progress animation/task state. Verify continuity according to product intent, rather than restarting the screen for every screenshot.
- For collections, include realistic large data and late-arriving content. Check lazy estimates, stable item identity, scroll targets, and layout work during repeated resizing. Profile a suspected performance problem before claiming a faster alternative.

Use Xcode previews and temporary borders to localize sizing issues. Use the View Debugger or measurements to distinguish layout bounds from transformed drawing bounds. Xcode 27/Device Hub resize controls accelerate arbitrary-size checks; older toolchains can use explicit container previews and available simulators. Verify relevant real-device behavior separately. See [A1–A6 and HIG sources](sources.md).

### iPhone Duo test configurations

When targeting the iOS 27.1 SDK, test in the iPhone Duo simulator (Device Hub, Xcode 27.1) across these configurations:

| # | Configuration | What to verify |
| --- | --- | --- |
| 1 | Outer display, portrait | Content offset from vertical side controls; nothing hidden under the bar. |
| 2 | Outer display, landscape | Compact/compact layout; asymmetric insets handled per side. |
| 3 | Inner display, flat, portrait | Regular/regular layout; horizontal bars; no stretched-phone appearance. |
| 4 | Inner display, flat, landscape | Sidebar / split behavior; column reflow. |
| 5 | Partially folded (book pose) | Fold avoidance; displacement of interactive controls; no elements straddling the fold. |
| 6 | Tent / laptop pose | Content visible at top; interactive controls reachable at bottom. |
| 7 | Open ↔ close transitions | State preserved; smooth resize; hinge callbacks reset correctly. |
| 8 | Split View, app on LEFT | Vertical bar docks to the left outer edge; layout correct. |
| 9 | Split View, app on RIGHT | Vertical bar docks to the right outer edge; layout correct. |
| 10 | Stacked PiP layout | App resizes vertically in real time; content remains scrollable. |
| 11 | Rotation in every pose | Layout driven by size classes only; no orientation-based branching. |
| 12 | Sheets / alerts / menus per pose | Correct placement; fold avoidance; vertical bar rules by display. |
| 13 | Multi-scene (if supported) | New window request on outer display fails gracefully / action hides. |

## Acceptance scenarios

Select the rows relevant to the task. These are behavioral checks, not requirements to build every pattern into every app.

| Scenario | Observable acceptance |
| --- | --- |
| Layout selected by phone/pad or portrait/landscape | The recommendation traces the actual branch and its descendants, explains the available-space mismatch, and accounts for height as well as width. Any replacement reacts to local constraints. |
| Stateful form changes arrangement | Entered values and meaningful selection persist; focus and navigation have deliberate continuity; tasks are not duplicated by the arrangement switch. |
| No candidate presentation fits | The final presentation still provides usable wrapping, scrolling, or another explicit overflow path. Essential text is not silently removed to make the fit test pass. |
| Child inside a constrained stack uses container sizing | The identified sizing ancestor is correct. The result respects the actual component contract, not an assumed percentage of its immediate parent. |
| Geometry used for drawing or observation | Valid local drawing/observation is retained. Child-to-ancestor sizing feedback is diagnosed by its dependency and runtime cost, not merely by the presence of geometry APIs. |
| Small aligned table, large card collection, variable-width tags | Choices respect shared alignment, deferred creation, and wrapping needs respectively. Laziness and custom layout have a reason. |
| Short window, keyboard, long translation, large text | Important content and controls remain reachable, meaningful text remains readable, and RTL reading order is coherent. |
| Older deployment target or limited toolchain | Suggested overloads compile with the declared availability or an explicit compatible alternative; the minimum OS is unchanged unless requested. |
| Clean portable invocation | The skill works from another project using its own references. It requests neither the author's private source folders nor an unrelated installed skill. |
| Already suitable component | The review identifies what is sound and avoids unnecessary geometry removal, wholesale font scaling, or architectural churn. |

## Verify implementations and the skill itself

For a code change, run the relevant build/typecheck and established tests; add behavior tests only where they guard meaningful logic or regression risk. Re-run affected runtime cases after the fix. Keep temporary harnesses and generated artifacts outside application source unless they are intentionally part of the requested deliverable.

For this skill's maintenance, validate its metadata and relative links, then give a fresh evaluator the packaged skill and realistic raw examples. Keep the expected answer out of the evaluator prompt. Include a positive control with correct code, a stateful arrangement, a constrained container, and an older target. Review the actual recommendations, reproduction steps, scope discipline, and unsupported claims. Improve a rule only when a demonstrated failure warrants it.

Report outcomes with their limits: which examples typechecked, which devices/runtimes ran, which sizes and settings were exercised, and which real-device or keyboard checks remain. A runtime harness validates its exercised examples; it does not certify unrelated application screens.

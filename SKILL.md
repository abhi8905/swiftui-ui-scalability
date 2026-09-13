---
name: swiftui-ui-scalability
description: "Review, refactor, and build adaptive SwiftUI layouts for iPhone and iPad. Use for resizing, constrained containers, Dynamic Type, content overflow, device-idiom layout branches, or choosing stacks, grids, ViewThatFits, Layout, geometry, and scrolling APIs. Covers resizable iPad windows and iPhone Mirroring; excludes UIKit migrations and unrelated SwiftUI cleanup."
---

# SwiftUI UI Scalability

Make layout decisions from the space offered to the component, the content it must present, and the person's settings. Preserve the product's visual hierarchy and behavior as that space changes. More room may justify rearrangement or a bounded reading column; it does not automatically justify enlarging every element.

Starting with iOS 27 and iPadOS 27, all apps run in resizable windows. iPhone apps on iPad, iPhone Mirroring, and future form factors can present any width at any time. Layout that depends on device idiom, screen bounds, orientation, or fixed device breakpoints will break. This skill enforces **space-aware, content-driven layout** as the default: measure the space offered to the component, not the device it runs on.

This is an independent skill informed by Apple documentation, WWDC sessions, and attributed supplementary material. It requires no other skill or machine-specific source files.

## Follow the requested action

- **Review / recommend:** inspect and explain; do not edit application code. A skill invocation without an action defaults to review.
- **Refactor / fix:** implement the requested adaptive behavior and perform relevant checks. An explicit implementation request is authorization to work within that scope; do not introduce another approval step.
- **Build:** create adaptive SwiftUI UI within the requested design and supported OS versions, applying the same decision criteria.

Limit work to the requested screen or feature and the dependencies that determine its layout. Follow nested components rather than stopping at the container's file. For a whole-app request, organize work by feature and track coverage. Do not turn a sizing review into unrelated architecture, concurrency, styling, or API modernization work. If the cause lies in UIKit, describe the integration boundary; UIKit migration is outside this skill.

## Establish the layout contract

1. Discover the relevant target, deployment version, build SDK, and toolchain from project/package settings and available tools. Distinguish SDK availability from minimum runtime availability. Inspect the exact overload before introducing newer APIs; do not raise the deployment target implicitly. Use [sources and compatibility](references/sources.md) for the verified baseline and source-specific caveats.
2. Trace how the requested view is presented and constrained: window, navigation or split-view column, sheet, tab, scroll container, parent frames, overlays, and descendants. Determine who owns sizing and who owns persistent state. If caller code is unavailable, state that limitation.
3. Read the relevant source, not just search matches. Useful leads include `userInterfaceIdiom`, screen bounds, orientation-based layout branches, fixed frames/fonts, offsets, `scaleEffect`, `minimumScaleFactor`, Dynamic Type limits, geometry-to-state writes, and layout-dependent identity. These are leads, not automatic findings.
4. Identify the content priorities and the failure condition: which width, height, text size, content length, keyboard, or transition makes something unusable? Trace proposals and modifier order before choosing a replacement. Record what is proven statically, observed at runtime, or still a hypothesis.

Device idiom (`userInterfaceIdiom`) identifies the device type, not the available space. A `.phone`-idiom app can run in a resizable window on iPad, in iPhone Mirroring, or in future form factors at any width. Interface orientation describes the device's physical attitude, not the component's available dimensions. Size classes express coarse environmental constraints useful for *presentation-style* decisions — sheet vs. full-screen, sidebar visibility, padding adjustments — but they do not tell whether a particular group of controls fits. A narrow component can exist inside a wide window; a wide component can appear in a narrow split-view column. Examine height independently of width. **Never use idiom, orientation, or screen bounds as inputs to layout geometry. Use the proposed size and content requirements for sizing; reserve size classes for presentation-level decisions only.**

### Codebase audit checklist

Before changing code, audit for these patterns. Each breaks on multi-display or foldable devices.

| Anti-pattern | What to search for | Why it breaks |
| --- | --- | --- |
| Main screen references | `UIScreen.main`, `.main.bounds`, `.main.scale` | Ambiguous on a two-display device; deprecated. Use `traitCollection.displayScale` or scene bounds. |
| Idiom-based layout | `userInterfaceIdiom`, `UI_USER_INTERFACE_IDIOM` | Device is `.phone` but inner display has regular/regular size classes. |
| Orientation-based layout | `UIDevice.current.orientation`, `interfaceOrientation`, `statusBarOrientation` | Inner display ignores supported orientations; app gets scaled instead. |
| Hardcoded screen widths | Literal `375`, `390`, `393`, `430`, or device-model checks | New screen shapes and continuous live resizing invalidate fixed breakpoints. |
| Symmetric inset assumptions | `safeAreaInsets.left * 2`, shared constants for both sides | Vertical bars produce asymmetric leading/trailing insets. Calculate each edge independently. |
| `UIRequiresFullScreen` as opt-out | `UIRequiresFullScreen` in Info.plist | Honored, but the app **still resizes** when the device opens/closes and scales in Split View. Not an opt-out from resizing. |
| Manual frame math from screen bounds | `view.frame = UIScreen.main.bounds` | Use scene bounds or view bounds. |

## Load only the guidance needed

| Task | Reference |
| --- | --- |
| Diagnose proposals, frames, text competition; choose stacks, fit alternatives, identity-preserving arrangements, grids, flow, or custom layout; adapt navigation | [Layout decisions](references/layout-decisions.md) |
| Choose container sizing, geometry observation, drawing, scroll behavior, margins, or safe-area handling | [Geometry and scrolling](references/geometry-and-scrolling.md) |
| Adapt to text settings/locales; preserve state, focus, selection, tasks, and accessibility during rearrangement | [Accessibility and state](references/accessibility-and-state.md) |
| Define reproduction steps, exercise boundaries, distinguish static/build/runtime evidence, or validate a change | [Validation](references/validation.md) |
| Verify an API/version claim, resolve conflicting guidance, or trace a recommendation to evidence | [Sources](references/sources.md) |

Choose the least complex approach that meets the actual constraints. Explain why it suits this content. Follow this escalation order before reaching for direct geometry measurement:

1. Built-in composition — `HStack`, `VStack`, flexible frames, alignment guides.
2. `ViewThatFits` — fit selection from preferred alternatives on the constrained axes.
3. `ArrangementView` — fold-aware container for split or overlaid primary/secondary views (iOS 27.1+).
4. `AnyLayout` — identity-preserving arrangement switching under an explicit condition.
5. `Grid` / `LazyVGrid` — shared alignment, spanning, or responsive column count.
6. `containerRelativeFrame` — sizing relative to a recognized container (iOS 17+).
7. Custom `Layout` — coordinated measurement and placement beyond built-in composition.
8. `onGeometryChange` — declarative geometry observation with an equatable transform (iOS 16+, back-deployed via Xcode 16+). For observation only; do not feed raw dimensions into ancestor sizing.
9. `visualEffect` — geometry-dependent drawing transformations without a container view (iOS 17+).
10. **`GeometryReader` — last resort, justified downward drawing only.** Exhaust all alternatives above first. GeometryReader expands to fill all proposed space (breaking content-hugging layouts), has a 10×10 ideal size (breaking scroll views), inverts SwiftUI's top-down layout contract, and causes layout loops when `proxy.size` drives `@State` that affects the measured region. Its legitimate domain is downward geometry for shapes, canvas, and visual effects where dimensions flow into the render pass without feeding back into ancestor sizing. If you reach for GeometryReader for layout, justify why no alternative above applies.

Do not prescribe a universal breakpoint, a whole-screen scale factor, or fixed device thresholds. Keep justified design tokens and appropriately sized artwork. Add custom layout or shared abstractions only when their measurement or reuse requirements warrant them.

When changing arrangement, check whether the content hierarchy changes identity. Preserve meaningful selection, entered data, focus, navigation, scroll position, and task ownership; resizing must not accidentally restart work or discard progress. Use content reflow and reachable overflow paths when room is insufficient.

On devices that support multiple scenes (iPhone Duo is the first iPhone to do so), each scene receives its own size class and window. New windows can only be created on the inner display; use `UIWindowSceneActivationAction` which auto-hides when new windows are unavailable. Layout logic must not assume a single window or a single set of size classes for the app.

## Deliver useful findings and changes

Lead with the most consequential user-visible issues. For each material finding include:

- Location and inspected scope, including the relevant caller or descendant.
- Triggering condition, evidence level, and practical impact.
- Recommended change, why it fits, and the material tradeoff if another approach is plausible.
- Required API/runtime compatibility and a concrete verification scenario.

Group repeated root causes without losing affected locations. Call out existing approaches that should remain. A review may legitimately find no required changes; do not manufacture issues from search patterns.

For implementation, make the changes and validate according to [Validation](references/validation.md). For review, provide a prioritized conversion sequence or focused illustrative snippet where useful. Report checks actually completed separately from untested conditions. Compilation and source inspection do not prove visual correctness, state continuity, performance, or universal size support.

## Distribution note

This skill follows the portable Agent Skills directory format: `SKILL.md` is the entry point and every runtime reference is relative to this directory. Installation for Codex, Gemini CLI, Claude Code, and Xcode-hosted agents is documented in [INSTALL.md](INSTALL.md). Do not add this directory to an Xcode application's target membership or Copy Bundle Resources; it is development-agent configuration, not app runtime content.

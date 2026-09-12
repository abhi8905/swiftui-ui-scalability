# Sources and compatibility

Verified: **2026-09-06**. This is an independently authored synthesis, not an Apple-authored or Apple-endorsed skill. The bundle contains original guidance and examples, not copies of the source articles or transcripts. Source material is attributed below; access to the author's original files is unnecessary.

## How to resolve a claim

Prefer the applicable official API contract and installed SDK declarations for signatures and availability. Use Apple sessions for rationale and behavior, with current documentation to resolve version-specific changes. Use supplementary articles for explanation and examples; test observations that are not documented guarantees. The author's presentation establishes design intent, not an API contract.

Separate build SDK, compiler/toolchain, minimum deployment target, and runtime OS. A new toolchain may expose an API back-deployed to an older runtime. Verify the exact overload used by the project; do not infer availability from the API name or announcement year. When the evidence is incomplete, label the uncertainty and identify the check rather than inventing an API or guarantee.

Recheck dated claims when adopting a newer SDK or proposing an API outside this baseline. Update the relevant source and compatibility entry after verification, not every unrelated rule. The current resizing guidance covers **WWDC 26 / iOS 27 and iOS 27.1** (including WWDC 26 Tech Talks on iPhone Duo). Announced hardware with shipped SDK APIs (e.g., iPhone Duo and its `ArrangementView`, reserved regions, vertical bars) is valid input to layout rules; unannounced device speculation is not.

## Apple sessions

Timestamps are navigation landmarks from the official session chapters or the supplied timestamped transcript; closely related explanations may span several segments.

| ID | Primary source | Relevant evidence |
| --- | --- | --- |
| A1 | [WWDC26 278 — Modernize your UIKit app](https://developer.apple.com/videos/play/wwdc2026/278/) | 0:34 app adaptivity; 2:51 main screen; 6:17 idiom; 6:50 orientation; 8:19 testing. Phone idiom persists in resizable contexts. Use size classes and local dimensions for layout. UIKit migration procedures are outside this skill. |
| A2 | [WWDC26 269 — What's new in SwiftUI](https://developer.apple.com/videos/play/wwdc2026/269/) | About 3:49–4:52: resizable SwiftUI apps and preview handles; about 5:27–6:32: adaptive toolbar behavior. Confirms A1's relevance to SwiftUI. |
| A3 | [Meet with Apple 271 — A guide to layout in SwiftUI](https://developer.apple.com/videos/play/meet-with-apple/271/) | About 5:37–9:00: proposal/response; 12:16–15:10: layout priority; 15:15–15:55: fit selection; 19:04–21:39: debugging layout. |
| A4 | [WWDC22 10056 — Compose custom layouts with SwiftUI](https://developer.apple.com/videos/play/wwdc2022/10056/) | Grid measurement, custom Layout, child placement, ViewThatFits, and AnyLayout. Distinguishes downward geometry for drawing from upward measurement feedback. |
| A5 | [WWDC23 10159 — Beyond scroll views](https://developer.apple.com/videos/play/wwdc2023/10159/) | About 2:35–4:03: margins and safe areas; 4:38–7:08: targets/paging; 7:15–8:44: container-relative sizing. |
| A6 | [WWDC26 321 — Dive into lazy stacks and scrolling with SwiftUI](https://developer.apple.com/videos/play/wwdc2026/321/) | About 2:45–4:34: estimated geometry; 17:13–17:33: durable state; 19:08–19:47: geometry-to-state layout feedback; 20:19–20:43: estimates and offsets. |
| A7 | [WWDC26 Tech Talk 111461 — Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) | Codebase audit anti-patterns (`UIScreen.main`, idiom, orientation, hardcoded widths, symmetric insets, `UIRequiresFullScreen`); SDK behavior tiers; `ConcentricRectangle` / `UICornerConfiguration`; `ReservedRegion` safe-positioning; verification matrix. |
| A8 | [WWDC26 Tech Talk 111462 — Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) | Vertical bar ordering hierarchy (`cancellationAction`, `topBarPinnedTrailing`, `pinnedTrailingGroup`); `.axisBehavior`; `@Environment(\.toolbarVerticalEdge)`; `.toolbarCompressionBehavior`; sheet vertical bar rules by display and placement; flexible spacer behavior. |
| A9 | [WWDC26 Tech Talk 111463 — Strike a pose with adaptive layouts on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111463/) | `ArrangementView` split/overlay; `reservedRegions` (`.division`, `.occlusion`); `.includeInactive`; displacement patterns; when ArrangementView cannot split on the primary axis. |
| A10 | [WWDC26 Tech Talk 111464 — Leverage multiple displays and scenes on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111464/) | `.onHingeChange` / `UIHingeInteraction`; `hinge.status` and `hinge.angle`; multi-scene support (new windows inner-display only); `UIWindowSceneActivationAction` auto-hiding; hinge is for interactions, not layout. |
| A11 | [WWDC26 Tech Talk 111466 — Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) | Inner display adaptation strategies (multi-column, column reflow, tab→sidebar); asymmetric insets; centered layout audit; PiP vertical resizing; sheet fold avoidance; Split View side-switching. |

The supplied session 278 transcript, JSON metadata, and code samples were reviewed together. Its code shows why local context and reactive updates matter. The SwiftUI equivalents are chosen by intent, rather than copied from UIKit snippets.

## Official documentation

| ID | Documentation | Use |
| --- | --- | --- |
| D1 | [ViewThatFits](https://developer.apple.com/documentation/swiftui/viewthatfits) | Preference order and ideal-size selection on chosen axes. |
| D2 | [AnyLayout](https://developer.apple.com/documentation/swiftui/anylayout) | One child hierarchy whose arrangement changes without replacing child identity. |
| D3 | [Layout](https://developer.apple.com/documentation/swiftui/layout), [ProposedViewSize](https://developer.apple.com/documentation/swiftui/proposedviewsize) | Measurement, proposals, spacing, and placement. |
| D4 | [Grid](https://developer.apple.com/documentation/swiftui/grid) | Shared alignment, spanning, and eager measurement. |
| D5 | [LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid), [GridItem](https://developer.apple.com/documentation/swiftui/griditem) | Deferred creation and track sizing. |
| D6 | [containerRelativeFrame](https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:_:)) | Eligible ancestors, safe-area-adjusted dimensions, proportional sizing. |
| D7 | [onGeometryChange](https://developer.apple.com/documentation/swiftui/view/ongeometrychange(for:of:action:)) | Transformed geometry observation; inspect the exact action overload. |
| D8 | [Layout adjustments](https://developer.apple.com/documentation/swiftui/layout-adjustments), [SafeAreaRegions](https://developer.apple.com/documentation/swiftui/safearearegions) | Insets, padding, content margins, container and keyboard regions. |
| D9 | [GeometryReader](https://developer.apple.com/documentation/swiftui/geometryreader), [visualEffect](https://developer.apple.com/documentation/swiftui/view/visualeffect(_:)) | Local measurement versus drawing effects. |
| D10 | [ScrollView](https://developer.apple.com/documentation/swiftui/scrollview), [ScrollPosition](https://developer.apple.com/documentation/swiftui/scrollposition) | Scrolling, targets, position, and version-specific APIs. |
| D11 | [HIG: Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography) | Resizing, readable widths, safe areas, Dynamic Type reflow, and meaningful hierarchy. |
| D12 | [ScaledMetric](https://developer.apple.com/documentation/swiftui/scaledmetric), [DynamicTypeSize](https://developer.apple.com/documentation/swiftui/dynamictypesize) | Text-relative metrics and accessibility text sizes. |
| D13 | [LayoutDirection](https://developer.apple.com/documentation/swiftui/layoutdirection), [Applying custom fonts to text](https://developer.apple.com/documentation/swiftui/applying-custom-fonts-to-text) | RTL environment and scalable custom typography. |
| D14 | [NavigationSplitView](https://developer.apple.com/documentation/swiftui/navigationsplitview), [sidebarAdaptable](https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable) | Adaptive system navigation; preserve navigation and selection ownership. |
| D15 | [TN3192: Migrating from UIRequiresFullScreen](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) | App-configuration context and the qualified iOS/iPadOS 27 resizing behavior. |

## iPhone/iPad availability baseline

Verified from Apple's documentation and the installed Xcode 27 SDK's public SwiftUI/SwiftUICore interfaces. This table is a lookup aid; inspect overloaded, beta, and changed declarations before using them. The skill does not impose a minimum OS on the consuming project.

| API family / specific overload | Minimum iOS/iPadOS runtime | Qualification |
| --- | --- | --- |
| `ScaledMetric` | 14 | Choose a relative text style appropriate to the metric. |
| `safeAreaInset`, `DynamicTypeSize` | 15 | Container and keyboard safe areas are distinct. |
| `Layout`, `AnyLayout`, `Grid`, `ViewThatFits`, `NavigationSplitView` | 16 | Arrangement and fit selection have different semantics. |
| `onGeometryChange` with new-value-only action | 16 | Requires a toolchain exposing the back-deployed API (Xcode 16+); not present in the original iOS 16 SDK. |
| `containerRelativeFrame`, `safeAreaPadding`, `contentMargins`, `visualEffect` | 17 | Check exact container and axis semantics. |
| `scrollTargetLayout`, `scrollTargetBehavior`, item-ID `scrollPosition` | 17 | ID binding is not an absolute scroll-offset measurement. |
| `onGeometryChange` with old-and-new-value action | 18 | Not interchangeable with the back-deployed action overload. |
| `ScrollPosition`, scroll geometry/phase observation, `sidebarAdaptable` | 18 | Inspect the specific initializer/modifier and platform before recommending. |
| Newly added toolbar overflow/pinning APIs discussed at WWDC26 | 27 or API-specific | Verify the exact declaration; do not raise the app's minimum to obtain convenience APIs. |

In the inspected Xcode 27 interfaces, `onGeometryChange` uses an equatable, sendable result and a sendable transform. Older SDK signatures and actor-isolation diagnostics can differ. Keep transforms free of side effects and check captures against the actual compiler mode.

## Supplementary material and attribution

| ID | Source | Contribution and limit |
| --- | --- | --- |
| E1 | Apple's exported `swiftui-specialist` skill, especially `structure.md`, `dataflow.md`, `modifiers.md`, `localization.md`, and `foreach.md` | View identity, narrow update dependencies, invalidation-boundary factoring, semantic direction, and stable collection identity. Exported snapshots were supplied locally; the skill uses distilled principles without requiring those files. |
| E2 | Apple's exported `uikit-app-modernization` skill and screen/orientation/safe-area references; [export described in A1 at 14:07](https://developer.apple.com/videos/play/wwdc2026/278/?time=847) | Local context and asymmetric safe areas. Its mutation rules, UIKit lifecycle migration, and broad replacement recipes are not adopted. |
| E3 | Apple's exported `swiftui-specialist` skill, `environment.md` — rapidly updating environment values and high-frequency geometry | Warns against flowing `GeometryReader` / `onGeometryChange` values through environment; shows `@Observable` + coarsened boolean threshold pattern as the correct replacement. Per-item coarsening for scroll-dependent rows. |
| C1 | Fatbobman — [GeometryReader: Blessing or Curse?](https://fatbobman.com/en/posts/geometryreader-blessing-or-curse/) | Greediness, 10×10 ideal size, top-leading origin, layout loops, and geometry alternatives. Substantiates the escalation ladder's last-resort stance. API-specific observations need current SDK checks. |
| C2 | Fatbobman — [Mastering ViewThatFits](https://fatbobman.com/en/posts/mastering-viewthatfits/) | Ideal-size reasoning, evaluation algorithm, and fallback examples. Treat state lifetime and no-fit behavior as cases to validate. |
| C3 | Fatbobman — [Mastering containerRelativeFrame](https://fatbobman.com/en/posts/mastering-the-containerrelativeframe-/) | Ancestor lookup, axes, spacing, and safe areas. Historical Xcode 15.3 List observations are not universal current restrictions. |
| C4 | Fatbobman — [New Features of ScrollView in SwiftUI](https://fatbobman.com/en/posts/new-features-of-scrollview-in-swiftui/) | iOS 17 scrolling concepts. Historical position/anchor limitations do not describe every newer overload. |
| C5 | Antoine van der Lee — [SwiftUI Grid, LazyVGrid, LazyHGrid Explained with Code Examples](https://www.avanderlee.com/swiftui/grid-lazyvgrid-lazyhgrid-gridviews/) | Grid structure, spanning, unsized axes, and laziness tradeoffs. Dynamic data alone does not require a lazy grid. |
| P1 | Author-supplied `master_slides.html`, "SwiftUI Adaptive Layout APIs — Building iPad-Ready Views with Modern Layout Tools" | Design direction: content-aware adaptation, GeometryReader as last resort, declarative breakpoints with `.frame(minWidth:)`, two-layer strategy (size class + ViewThatFits), and choosing appropriate modern layout tools. Private presentation; its original file is not required or bundled. |

## Resolved differences

- The presentation's (P1) preference for avoiding `GeometryReader` is adopted as **exhaust alternatives first**. `GeometryReader` is a last-resort tool for justified downward drawing geometry. Apple's custom-layout session (A4) confirms valid downward sizing/drawing; the `environment.md` high-frequency invalidation guidance (E3) and the Fatbobman analysis (C1) confirm that feeding geometry back into ancestor sizing or environment is an anti-pattern. The skill's escalation ladder codifies this.
- E3's high-frequency environment warning applies to any rapidly changing dimension, not only `GeometryReader`. Scroll offset, drag translation, and timer-driven values flowing through environment or broad `@State` create the same invalidation cost. The coarsened `@Observable` threshold pattern is the standard replacement.
- E2's direct screen-bounds replacement advice is a migration shortcut, not a universal SwiftUI layout prescription. First see whether ordinary layout removes the measurement need.
- `onGeometryChange` is not a universal replacement for layout measurement: A6 explains how geometry-to-state-to-layout feedback can destabilize scrolling even with the modern API. It is appropriate for observation (thresholds, analytics, conditional behavior); it is not a layout primitive.
- `containerRelativeFrame` is not a percentage-of-any-parent API. Resolve its eligible ancestor before proposing it for a nested component.
- `ViewThatFits` does not guarantee sufficient overflow handling or transfer of editing state. Retain useful content in alternatives and exercise no-fit/state scenarios; use D2 for identity-preserving arrangement.
- Reported historical SDK bugs and unsupported overloads in articles are dated observations. Verify them against the consuming project's environment before repeating them as restrictions.

# Choosing a SwiftUI layout

Use this reference when deciding how content should rearrange, size, or remain stable as its available region changes. For measurement and scroll containers, continue with [geometry and scrolling](geometry-and-scrolling.md). Source IDs refer to the bundled [source register](sources.md).

## Establish the actual constraint

Read the parent hierarchy before proposing a replacement. A view inside a sheet, navigation column, padded card, or scroll container receives different proposals from the same view at the window root. Available width and height can change independently; neither the physical device nor portrait/landscape identifies the space a component receives. Size classes remain useful environmental signals for presentation changes, but they do not tell whether a particular group of labels fits. ([A1, A2, D11](sources.md))

Separate three requirements: content that must remain visible, relationships that must remain intact, and decoration that may shrink or move. Let text reflow and collections rearrange before reducing legibility. A maximum reading width can improve a large window; scaling every font, gap, and control with the window does not create an adaptive interface.

SwiftUI proposes a size, children choose sizes, and containers place them. An unspecified dimension requests ideal sizing; it is not the same proposal as infinity. A custom layout may receive finite, unspecified, zero, and unbounded proposals. Investigate a view's response instead of assuming every flexible child has a useful content-derived ideal size. ([A4, D3](sources.md))

## Match the content relationship

| Requirement | First approach to assess | What determines suitability |
| --- | --- | --- |
| One row or column, ordinary alignment | `HStack` / `VStack`, flexible frames and alignment guides | Content can wrap or compress without changing the relationship. |
| Several acceptable presentations | `ViewThatFits` | Preferred alternatives have meaningful ideal sizes on the tested axes. |
| Same children, different arrangement | `AnyLayout` with built-in or custom layouts | Preserve identity while an explicit condition chooses the arrangement. |
| Shared row and column alignment or spanning | `Grid` | Measuring all cells is appropriate; alignment needs both dimensions. |
| Repeated uniform cards with responsive column count | `LazyVGrid` with adaptive `GridItem` | A minimum usable card width is known and equal column sizing suits the content. |
| Variable-width tags that wrap naturally | A reusable flow `Layout` | Children should retain different natural widths rather than occupy equal grid tracks. |
| Coordinated pane proportions or equalized child dimensions | Existing custom `Layout`, or a small new one | Built-in composition cannot express the required measurement/placement relationship. |

The table is a decision aid, not an API upgrade ladder. Reuse an existing correct layout after checking its proposal handling. A small fixed collection can require `Grid`; dynamic data can also use `Grid`. Laziness reduces creation work but limits what can be measured eagerly. Choose it for collection behavior and observed or plausible scale, rather than merely because `ForEach` appears. ([A4, D3–D5](sources.md))

## GeometryReader is a last resort

If you are reaching for `GeometryReader` to make a layout decision, stop and assess the escalation ladder in the parent [SKILL.md](../SKILL.md). The table above and the APIs below handle the vast majority of adaptive layout without direct geometry measurement. `GeometryReader` is justified only for **downward drawing geometry** — shapes, canvas, and visual effects where dimensions flow into the render pass without feeding back into ancestor sizing. ([A4, D3, D9](sources.md))

### Why GeometryReader breaks adaptive layout

1. **Greediness.** GeometryReader expands to fill all proposed space. Unlike stacks and text, it does not hug its content. Placing one inside a layout that expects content-derived sizing forces the parent to offer its entire region, breaking the proposal/response contract. ([C1](sources.md))
2. **10×10 ideal size.** When a parent proposes an unspecified dimension — common inside a `ScrollView`'s scrolling axis — GeometryReader responds with its ideal size of 10×10 points, producing invisible or collapsed content. ([C1, D9](sources.md))
3. **Layout loops.** Reading `proxy.size` → writing to `@State` → re-rendering the view that contains the reader → re-reading `proxy.size` creates a feedback loop. Even with `onGeometryChange`, feeding raw dimensions back into the measured region's sizing can destabilize layout, particularly inside lazy scroll containers. ([A6, C1](sources.md))
4. **Inverted contract.** SwiftUI's layout is top-down: parent proposes, child responds. GeometryReader reads bottom-up, which can lead to designs that depend on the measured region before the region is determined, rather than letting the layout system resolve sizes naturally.
5. **Per-frame invalidation cost.** Flowing GeometryReader values through environment or broad `@State` can invalidate every view in the subtree on every pixel of a resize. Prefer `@Observable` models with coarsened boolean thresholds. ([E3](sources.md))

### Declarative breakpoints without GeometryReader

Use `.frame(minWidth:)` inside `ViewThatFits` to create content-aware breakpoints. The `minWidth` sets the threshold at which `ViewThatFits` considers the alternative too wide; this is a declarative breakpoint that responds to the actual proposed space without reading screen dimensions.

```swift
import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ScalabilityDashboard: View {
    var body: some View {
        ViewThatFits(in: .horizontal) {
            // Tier 1: Ultra-wide — side-by-side with sidebar
            HStack(alignment: .top, spacing: 24) {
                VStack { HeroBanner(); MainContent() }
                    .frame(minWidth: 700)
                SideCards()
                    .frame(width: 320)
            }
            // Tier 2: Standard landscape — stacked hero, side-by-side content
            VStack(spacing: 24) {
                HeroBanner()
                HStack(alignment: .top, spacing: 24) {
                    MainContent()
                        .frame(minWidth: 400)
                    SideCards()
                        .frame(width: 320)
                }
            }
            // Tier 3: Narrow / fallback — all stacked
            VStack(spacing: 24) {
                HeroBanner()
                MainContent()
                SideCards()
            }
        }
    }
}
```

The `minWidth` values are derived from the content's actual requirements (labels, controls, padding at the current text size), not from device dimensions. Each tier is a complete, usable presentation — the last alternative (Tier 3) is the fallback when no candidate fits. ([D1, P1](sources.md))

### Two-layer strategy: size class + ViewThatFits

Combine `horizontalSizeClass` for presentation-level decisions (padding, styling, navigation mode) with `ViewThatFits` for column arrangement. This solves the intermediate-width problem — for example, a 2/3 split-view column on iPad that is wider than an iPhone but narrower than a full iPad screen:

```swift
import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ScalabilityAdaptiveContainer<Content: View>: View {
    @Environment(\.horizontalSizeClass) private var sizeClass
    @ViewBuilder let content: () -> Content

    var body: some View {
        content()
            .padding(sizeClass == .regular ? 24 : 16)
    }
}
```

Size class determines the presentation style (padding, margins, whether to show a sidebar). `ViewThatFits` determines the content arrangement (columns vs. stacked). Neither reads the screen width. ([A1, A2, P1](sources.md))

## Fit selection and identity solve different problems

`ViewThatFits` examines candidates in preference order and chooses using their ideal size on the selected axes. Both axes are tested by default. Test only horizontal fit when vertical growth is acceptable; testing both can reject a useful arrangement for an unrelated height constraint. ([D1](sources.md))

Design the last alternative as a usable compact presentation, and test the case where no candidate's ideal size fits. Selection alone does not provide scrolling or guarantee that text will remain untruncated. A flexible frame, image, shape, custom layout, or nested scroll container can change the ideal-size response and therefore change selection unexpectedly. A `minWidth` can express a component's real minimum requirement; it is not a universal device breakpoint.

This example adapts action placement without measuring the screen. The two closures belong to the caller, so changing presentation does not create separate business state. Labels are intentionally complete in both alternatives.

```swift
import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ScalabilityActions: View {
    let save: () -> Void
    let continueLater: () -> Void

    var body: some View {
        ViewThatFits(in: .horizontal) {
            HStack {
                saveButton
                laterButton
            }
            VStack(alignment: .leading) {
                saveButton
                laterButton
            }
        }
    }

    private var saveButton: some View {
        Button("Save my preferences", action: save)
    }

    private var laterButton: some View {
        Button("Continue later", action: continueLater)
    }
}
```

Alternative branches are not a mechanism for transferring a text field's editing state, focus, scroll position, or active task. Examine ownership and lifetime before duplicating interactive content. `AnyLayout` explicitly supports changing layout type while preserving subview identity; it still needs a selection condition and does not perform `ViewThatFits`' fit search. ([D1, D2](sources.md))

The following component receives its arrangement decision from its surrounding presentation. It demonstrates one child hierarchy; the caller should derive `stackVertically` from relevant content/space or accessibility requirements, not a device name. Text values belong to the caller. Focus continuity still requires runtime verification.

```swift
import SwiftUI

@available(iOS 16.0, macOS 13.0, *)
struct ScalabilityNameFields: View {
    let stackVertically: Bool
    @Binding var givenName: String
    @Binding var familyName: String

    var body: some View {
        let layout = stackVertically
            ? AnyLayout(VStackLayout(alignment: .leading))
            : AnyLayout(HStackLayout(alignment: .firstTextBaseline))

        layout {
            TextField("Given name", text: $givenName)
            TextField("Family name", text: $familyName)
        }
        .textFieldStyle(.roundedBorder)
    }
}
```

## Fold-aware arrangements (iOS 27.1+)

For side-by-side or layered primary/secondary relationships, prefer `ArrangementView` over manual `HStack` or `ZStack`. This container is system-provided, dynamically fold-aware, and handles layout and z-index changes automatically on foldable devices like iPhone Duo.

```swift
import SwiftUI

@available(iOS 27.1, *)
struct FoldAwarePlayer: View {
    var body: some View {
        ArrangementView {
            PlayerView()          // primary
        } secondary: {
            UpNextView()          // secondary
        }
        // Default is .split, which places views side-by-side or stacked.
        // Use .overlay for ZStack-style layout that adapts when folded:
        .arrangementViewStyle(.overlay)
    }
}
```

- **Split (`.split`)**: Use when neither view may be obscured (replaces side-by-side manual stacks).
- **Overlay (`.overlay`)**: Use for clear foreground–background relationships (controls over content). It automatically transitions to side-by-side when the device is folded. Use the `\.overlayArrangementZIndex` environment value to react to fold-driven z-order changes.

Do not place navigation containers (like `NavigationSplitView`) inside an `ArrangementView`, and avoid placing `ArrangementView` inside a `List` or `ScrollView`.

## Inspect sizing modifiers and custom layouts

Modifier order changes the hierarchy being measured. Padding inside a frame consumes its offered space; padding outside enlarges the result. A background before a frame observes a different region from a background after it. Review those relationships before adding width calculations.

`fixedSize(horizontal: false, vertical: true)` can preserve a text view's required height at its proposed width, but an ancestor can still clip or fail to accommodate that height. Full `fixedSize()` can force horizontal overflow. `layoutPriority` changes allocation between siblings; it does not make insufficient space sufficient. Avoid using `minimumScaleFactor` or restrictive line limits to conceal an essential-content layout failure.

For adaptive grids, derive minimum card width from actual labels, controls, padding, and text-size requirements. A flow layout also needs an explicit oversized-item policy: propose the available width where wrapping is permitted, or provide an appropriate overflow behavior. Do not let an indivisible long token silently extend beyond the container. In `Grid`, a flexible divider can enlarge the grid; assess `gridCellUnsizedAxes` when that view should decorate rather than determine track sizing. ([D4, D5](sources.md))

For custom `Layout`, inspect `sizeThatFits` and `placeSubviews` together: account for spacing, measure content at widths it will actually receive, respect nonzero placement bounds, and handle an empty collection and unspecified proposals. Return finite meaningful sizes rather than forwarding an infinite proposal as a result. Add caching only when useful and invalidate calculations when the relevant proposal or subviews change. For proportional panes, verify that the narrowest pane still supports its content; a ratio alone does not establish a usable minimum. ([A4, D3](sources.md))

Any numbers introduced in an example or recommendation are design choices to justify against the component. They are not universal iPhone/iPad thresholds. Record the condition that needs adaptation and validate around that condition, including Dynamic Type and longer localized content.

## Adaptive system navigation

When the feature has navigation hierarchy, evaluate native `NavigationStack`, `NavigationSplitView`, or an available adaptive `TabView` style before building a manual device-specific replacement. A split view can collapse columns in constrained space; decide where selection and navigation paths live so the user's location remains meaningful as presentation changes. Column visibility preferences do not guarantee a column can remain visible at every width.

Keep primary destinations and actions reachable when a sidebar or toolbar contracts. Changing a tab presentation must not discard selected content. `sidebarAdaptable` requires iOS 18. Do not convert an onboarding page-style `TabView` into application navigation merely because both use `TabView`. Start from the feature's purpose and retain supported behavior. ([A2, D14](sources.md))

### Inner display adaptation (regular/regular size class)

On foldable devices like iPhone Duo, the inner display presents regular width and regular height simultaneously — the first time an iPhone has done so. Do not simply stretch the compact phone layout across the larger canvas. Three strategies to evaluate:

1. **Multi-column navigation** — `NavigationSplitView` / `UISplitViewController` to expose list-detail or sidebar-detail concurrently. Columns collapse to a stack when the device is closed.
2. **Adaptive column reflow** — Rearrange vertically stacked items into multi-column grids when horizontal width expands (e.g., a card list becomes a two-column grid).
3. **Tab bar → sidebar** — Transform a bottom `TabView` into an expandable sidebar for information-dense apps. Use `.defaultTabBarPlacement(.sidebar)` (SwiftUI) or `tabBarController.sidebar.preferredPlacement = .sidebar` (UIKit).

### Vertical bars and overflow (iOS 27.1+)

On foldable devices like iPhone Duo, horizontal space is maximized by moving toolbars, navigation bars, and tab bars to the **vertical edges** of the screen. Standard system containers adapt automatically. Rebuild against the iOS 27.1 SDK and use bars from standard navigation containers (`NavigationStack`, `NavigationSplitView`, `TabView` / `UINavigationController`, `UITabBarController`). Custom standalone `UIToolbar`, `UINavigationBar`, or `UITabBar` instances will not participate.

When adding custom toolbar items, prefer symbol-only (SF Symbol) items because text-only or mixed text/symbol items remain in the horizontal header area instead of migrating to the vertical side bar. Use standard `badge` modifiers instead of inline text counters so the item remains symbol-only and can adapt vertically.

#### Toolbar item ordering

Vertical bars enforce a strict top-to-bottom hierarchy. Keep placement consistent across poses:

1. **Top**: Primary navigation — Back or Close. Use `cancellationAction` placement (SwiftUI) or a leading item with `leftItemSupplementsBackButton = false` (UIKit). System back buttons in `UINavigationController` are automatic.
2. **Below navigation**: Prominent actions — Done, Save. Use `topBarPinnedTrailing` placement (SwiftUI) or `pinnedTrailingGroup` (UIKit).
3. **Vertical spacer**: Visually separates top placements from bottom placements.
4. **Bottom**: Remaining tool/tab icons, ordered by `.visibilityPriority`. Items collapse bottom-up into the overflow menu.
5. **Overflow menu**: Lowest-priority actions. Use `ToolbarOverflowMenu` (SwiftUI) or `additionalOverflowItems` (UIKit). The ellipsis (`…`) is the standard overflow symbol on iPhone; reserve it for overflow and give other menus a distinct symbol.

#### Axis behavior and custom views

- **Vertical axes**: `.axisBehavior(.verticalPreferred)` — opts a custom view into the vertical bar if it supports a vertical representation.
- **Horizontal lock**: `.axisBehavior(.horizontalOnly)` — keeps items that toggle between text and symbols (like a custom Edit/Select button) in the horizontal header. The system Edit button stays horizontal automatically.
- **Detecting vertical bar state**: Read `@Environment(\.toolbarVerticalEdge)` (SwiftUI) or `traitCollection.toolbarVerticalEdge` (UIKit). The value is populated when a vertical bar is present; `nil` / unspecified when horizontal. Use this to conditionally hide titles, adjust padding, or resize custom toolbar views to fit the bar's fixed width.
- **Flexible spacers**: In the vertical axis, `Spacer()` collapses to zero size by default. Fixed spacers maintain their minimum size. Avoid adding manual extra spacing.

#### Compression, overflow, and priorities

- **Compression order**: Use `.toolbarCompressionBehavior` to specify whether the toolbar or tab bar compresses first. Navigation-focused views (default) compress the toolbar first to keep tab destinations visible. Task-oriented views compress the tab bar first.
- **Item priorities**: Use `.visibilityPriority(.high)` on frequently used actions (Compose, New Note) and status items with badges so they are the last to enter the overflow menu.
- **Opt-out**: For single-page, bottom-heavy apps (like Calculator) or simple sheets with just a close button, disable the vertical bar shift with `.toolbarVerticalBehavior(.disabled)` (SwiftUI) or `preferredVerticalBarBehavior = .never` (UIKit).

#### Split View and column behavior

In Split View multitasking, the vertical bar docks to the **outer edge** of the app's half of the screen. If the app occupies the left half, bars appear on the left; on the right half, bars appear on the right. In `NavigationSplitView`, only the **detail column** participates in vertical bars — sidebar and supplementary columns keep horizontal bars. Expanded inspectors do not receive their own vertical bar to avoid duplicate side bars.

#### Sheet and presentation rules

Sheet behavior differs by display and placement:

- **Outer display**: Sheets receive vertical bars by default.
- **Inner display**: Centered sheets keep standard horizontal bars.
- **`preferredPlacement` API**: Sheets placed on the right edge receive a vertical bar; sheets placed on the left edge do not.
- **Simple sheets**: If a sheet has minimal controls (e.g., a single close button), disable its vertical bar to avoid consuming horizontal space.
- **Fold avoidance**: When partially folded, system sheets auto-slide away from the fold center.

#### Dynamic vertical resizing (PiP)

Picture-in-Picture video can be pinned to the top of the inner display, dynamically shrinking the app's vertical space in real time. When the device partially folds with PiP pinned, PiP occupies the top half and the app fills the bottom half. Apps must remain vertically resizable to handle this; test with PiP active.

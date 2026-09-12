# Geometry, containers, and scrolling

Use this reference when code reads dimensions, sizes content proportionally, positions persistent controls, or coordinates scrolling. Inspect layout proposals first using [layout decisions](layout-decisions.md). Source IDs link to [sources](sources.md).

## Choose the dimension source deliberately

| Need | API to assess | Key boundary |
| --- | --- | --- |
| Arrange siblings from their measured sizes | Built-in composition or `Layout` | Measurement and placement stay inside the layout process. |
| Size a child relative to a recognized container | `containerRelativeFrame` | Uses the nearest eligible ancestor, not every immediate parent. |
| Draw using the local region | `Shape`, `Canvas`, or justified `GeometryReader` | Geometry can flow downward into drawing without feeding ancestor sizing. |
| Observe a relevant geometry change | `onGeometryChange` | Transform to the smallest useful value and limit affected state. |
| Apply a geometry-dependent visual effect | `visualEffect` | Changes appearance; it does not solve sibling layout allocation. |
| Observe scroll geometry or visibility | Matching scroll observation API when available | Verify the exact overload and target before recommending it. |

`GeometryReader` is not deprecated, but it is a **last-resort sizing tool**. Exhaust built-in composition, `ViewThatFits`, `AnyLayout`, `containerRelativeFrame`, custom `Layout`, `onGeometryChange`, and `visualEffect` before reaching for it — see the [escalation ladder](layout-decisions.md#geometryreader-is-a-last-resort). Its legitimate domain is **downward geometry for drawing**: shapes, canvas rendering, and visual effects where dimensions flow into the render pass without feeding back into ancestor layout. ([A4, D3, D7, D9](sources.md))

When reviewing existing `GeometryReader` usage, identify what is measured, the coordinate space, who consumes the result, and whether that consumer changes the measured region. The following problems make it unsuitable for layout decisions:

- **Greediness:** It occupies all proposed space and does not hug its content. In a stack expecting content-derived sizing, it forces the parent to offer its entire region. ([C1](sources.md))
- **10×10 ideal size:** Inside a `ScrollView`'s scrolling axis, an unspecified proposal makes GeometryReader respond with 10×10 points, producing collapsed or invisible content. Diagnose that proposal before adding hard-coded heights. ([C1, D9](sources.md))
- **Origin alignment:** Children are placed at top-leading (0,0) instead of center, unlike stacks. ([C1](sources.md))
- **Layout loops:** `proxy.size` → `@State` → re-render → re-read creates feedback cycles that can crash or produce unstable layouts. Even `onGeometryChange` can produce this if the observed geometry feeds back into the measured region's sizing. ([A6, C1](sources.md))
- **Per-frame invalidation:** Flowing raw `proxy.size` through environment or broad model state invalidates every reading view on every pixel of a resize. Use `@Observable` models with coarsened boolean thresholds instead. ([E3](sources.md))

A background or overlay can measure a view without inserting a new expanding primary container, but moving measurement there does not automatically remove feedback or update cost.

Include animation travel distances and stored offsets in this inspection. An offscreen card transition based on global screen width can be wrong inside a smaller presentation even when its resting frame is correct. Derive motion from the relevant local region or artwork dimensions, and decide how an in-progress transition responds to resizing; replacing the initial measurement alone may leave a stale cached offset.

## Container-relative sizing

`containerRelativeFrame` finds the nearest eligible container, such as a scroll container, navigation stack/column, tab, or enclosing window/screen context. A `VStack`, custom card, or arbitrary intermediate frame does not automatically become that reference container. Applicable safe-area insets affect the dimensions supplied. Moving a reusable component between ancestors can therefore change its result. ([D6](sources.md))

Use it when that recognized container is the intended reference, for example sizing cards relative to a scroll viewport. To size two panes relative to their own shared region, evaluate their parent layout rather than assuming this modifier measures that parent. Inspect modifier axes and the nearest eligible ancestor before replacing a geometry reader mechanically.

In the count/span overload, spacing affects the width calculation; it does not insert gaps between siblings. Coordinate it with the actual stack/grid spacing. The following original example deliberately shows one card per viewport with content margins. The spacing, padding, and corner radius are sample visual choices, not scalability thresholds. Stable model IDs belong to the caller.

```swift
import SwiftUI

@available(iOS 17.0, macOS 14.0, *)
struct ScalabilityGalleryItem: Identifiable {
    let id: String
    let title: String
}

@available(iOS 17.0, macOS 14.0, *)
struct ScalabilityGallery: View {
    let items: [ScalabilityGalleryItem]

    var body: some View {
        ScrollView(.horizontal) {
            LazyHStack(spacing: 16) {
                ForEach(items) { item in
                    Text(item.title)
                        .font(.title2)
                        .padding(20)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .containerRelativeFrame(.horizontal)
                        .background(.quaternary,
                                    in: RoundedRectangle(cornerRadius: 16))
                }
            }
            .scrollTargetLayout()
        }
        .safeAreaPadding(.horizontal, 20)
        .scrollTargetBehavior(.viewAligned)
    }
}
```

This is a container-sizing example, not a universal onboarding carousel. A lazy horizontal container may not provide the content-derived height required by another design. Validate height and long text in the actual embedding hierarchy before adopting it. Prefer view alignment when snapping should follow items; paging follows different container-based behavior. ([A5, D6, D10](sources.md))

## Observe changes without building a sizing loop

For `onGeometryChange`, derive the value that matters: a threshold-crossing Boolean, a relevant dimension, or a small equatable value. Propagating every changing frame to a screen-level model can invalidate much more content than the feature requires. Keep observation transforms free of side effects; perform the necessary response in the action. Geometry that determines its own measured size needs a stable dependency design even with a modern modifier. ([D7](sources.md))

Check both SDK/toolchain support and runtime availability. In the inspected Apple SDK, the action receiving only the new value supports iOS 16/macOS 13; the old-and-new-value overload requires iOS 18/macOS 15. Do not replace one with the other because their names match. Current signatures also impose concurrency/sendability requirements; inspect the project's SDK declarations and compiler mode when examples capture actor-isolated data. A newer SDK can expose an API back-deployed to an older OS, so announcement year alone is insufficient.

### Coarsened thresholds instead of raw geometry

When layout decisions depend on a width threshold (e.g., "show two columns above 600pt"), **do not** store the raw `CGFloat` in environment or a broadly observed model. Every pixel of a resize would invalidate every reading view. Instead, hold the raw value in an `@Observable` model and expose a coarsened Boolean that flips only at the threshold. Views that read the Boolean invalidate only when crossing the boundary, not on every frame. ([E3](sources.md))

```swift
import SwiftUI

@MainActor
@Observable
final class ViewportModel {
    var width: CGFloat = 0 {
        didSet { isWide = width > 600 }
    }

    private(set) var isWide: Bool = false
}

@available(iOS 16.0, macOS 13.0, *)
struct ScalabilityRootView: View {
    @State private var viewport = ViewportModel()

    var body: some View {
        ContentView()
            .environment(viewport)
            .onGeometryChange(for: CGFloat.self) { proxy in
                proxy.size.width
            } action: { newWidth in
                viewport.width = newWidth
            }
    }
}
```

This pattern replaces the anti-pattern of `GeometryReader { proxy in … .environment(\.windowWidth, proxy.size.width) }`, which incurs a comparison cost for all environment-reading views on every pixel.

### Modern geometry replacements

- **`onGeometryChange(for:of:action:)`** (iOS 16+, back-deployed via Xcode 16+): Declarative geometry observation without a container view. Transform the proxy to the smallest useful equatable value in `of:` and perform the response in `action:`. Unlike `GeometryReader`, it does not expand to fill space or insert a new view into the hierarchy. Prefer this over `GeometryReader` for any observation-only need. ([D7](sources.md))
- **`visualEffect(_:)`** (iOS 17+): Applies geometry-dependent visual transformations (offset, scale, opacity, blur) in a single closure that receives the proxy. The effect does not participate in layout sizing — it changes appearance after layout is resolved. Use this for parallax, scroll-dependent opacity, and position-based effects instead of storing `GeometryReader` measurements in `@State`. ([D9](sources.md))

For visual motion based on local geometry, evaluate `visualEffect` before storing measurements. For actual scroll offset, visibility, or phase, choose the matching available scroll API. An item-ID binding is not a raw offset measurement. Retain an existing appropriate `ScrollViewReader` instead of treating it as universally obsolete. ([D7, D9, D10](sources.md))

## Reserved regions and fold avoidance (iOS 27.1+)

On foldable devices like iPhone Duo, hardware features divide or occlude the screen. iOS 27.1 introduces `reservedRegions` to the `GeometryProxy`. Instead of guessing device poses from screen width, query the geometry for these specific regions:

- **Division regions (`.division`)**: The fold or hinge. This has a frame only when the device is partially folded.
- **Occlusion regions (`.occlusion`)**: Hardware that blocks content, such as an active under-display camera.

```swift
// SwiftUI (via onGeometryChange or GeometryReader)
.onGeometryChange(for: [CGRect].self) { proxy in
    proxy.reservedRegions(kind: .division).map(\.frame)
} action: { foldFrames in
    // Update layout offsets or spacing
}
```

By default, only active regions are returned. You can query inactive regions (e.g., `options: .includeInactive`) to make high-level decisions—like preferring an even number of grid columns on a foldable device even when it is lying flat.

Use division regions for **displacement patterns**: moving interactive elements (like buttons or active text fields) entirely into the trailing, top, or bottom region so they do not straddle the physical fold. Continuous scrolling content (like feeds or articles) handles the fold naturally and does not need to displace.

### Custom bar safe-positioning

For custom navigation bars, toolbars, or other edge-to-edge UI that needs to claim space outside the standard safe area without colliding with system UI (status bar, camera, fold), use the reserved region safe-positioning API: `ReservedRegion` (SwiftUI) / `UIViewReservedRegion` (UIKit). This lets custom UI maximize screen real estate while respecting hardware features, rather than relying solely on safe area insets.

## Hinge interactions (not layout) (iOS 27.1+)

The `.onHingeChange` modifier (SwiftUI) and `UIHingeInteraction` (UIKit) provide live fold-state callbacks for driving **interactions and effects** — instrument pitch bends, page curl animations, dynamic camera adjustments. They are **not for structural layout**; use reserved regions and `ArrangementView` for that.

```swift
.onHingeChange { previousContext, currentContext in
    guard let hinge = currentContext.hinge else { return } // nil on non-hinge devices
    switch hinge.status {
    case .closed: resetEffect()
    case .partiallyOpen: applyEffect(angle: hinge.angle) // continuous Angle
    case .fullyOpen: resetEffect()
    }
}
```

- `context.hinge` is `nil` on devices without a hinge — **always guard**.
- `hinge.status`: `.closed`, `.partiallyOpen`, `.fullyOpen` (discrete states).
- `hinge.angle`: continuous `Angle` value for driving dynamic effects.

## Safe areas, margins, and scroll continuity

Distinguish the desired relationship before choosing a modifier:

- `padding` changes ordinary layout spacing.
- `safeAreaPadding` adjusts the safe region used by content.
- `safeAreaInset` places content at an edge and reserves space for it; its spacing also matters.
- `contentMargins` can separately target scroll content and indicators, useful when readable content should be inset without moving indicators equally.

### Asymmetric insets

On foldable devices with vertical side bars, safe-area insets are asymmetric — leading and trailing differ depending on which edge hosts the bar and which pose the device is in. **Never assume opposite insets are equal.** Calculate each edge independently:

```swift
// WRONG — assumes symmetric insets
let width = view.bounds.width - view.safeAreaInsets.left * 2
// RIGHT — handles each side independently
let width = view.bounds.inset(by: view.safeAreaInsets).width
```

In Split View multitasking, vertical bars can appear on either side of the app depending on which half of the screen the app occupies. Test both docking positions.

### Concentricity APIs (iOS 26+)

Use `ConcentricRectangle` (SwiftUI) or `UICornerConfiguration` (UIKit) for custom edge-to-edge backgrounds that need to match the physical bezel curves of the device. Do not hardcode corner radiuses; these APIs adapt automatically across device shapes including iPhone Duo.

A bottom action that overlays a scroll view can hide its last field. A safe-area inset is often appropriate when the action should participate in the region available for scrolling. Account for the keyboard and a short window; avoid imposing a fixed action-region height that clips larger text. Apply `ignoresSafeArea` according to the intended background/content behavior rather than using it to erase unexplained gaps. ([A5, D8](sources.md))

Scroll targets require stable identity. For item-based position and view alignment, put `scrollTargetLayout` on the container representing the relevant targets. Preserve model IDs across layout changes; regenerating IDs or using shifting indexes can invalidate selection and navigation to content. A lazy child's appearance is not a one-time workflow event, and storing durable form data only in transient rows can lose it when structure changes.

During resizing, test whether the user's current content remains reachable and the intended position remains understandable. Do not reset to the first page merely because dimensions changed. For text entry, combine scrolling checks with focus and keyboard behavior; for long collections, inspect responsiveness during repeated size changes. State preservation and visual correctness are runtime questions: successful typechecking establishes neither. Record unexecuted checks explicitly instead of presenting a static recommendation as an observed result.

# Accessibility and continuity during adaptation

Use this reference when space changes intersect with text settings, localization, focus, selection, navigation, animations, or task lifetimes. Read [layout decisions](layout-decisions.md) when selecting the arrangement and [validation](validation.md) when proving behavior. Evidence is indexed in [sources](sources.md), especially A4, A6, D11–D13, and E1.

## Content must remain understandable

A component's usable minimum depends on its actual content, not only its frame. Include its labels, padding, interactive elements, text settings, and translations when deciding whether a row, column, or pane arrangement fits.

Prefer semantic text styles such as `.body` and `.headline` where they express the design. For a custom font, use a scaling API with an appropriate relative text style. When a custom dimension must track text, evaluate `@ScaledMetric(relativeTo:)`. Avoid multiplying every dimension by screen width: a readable line length, artwork proportion, and touch target have different constraints.

A numeric size is not automatically incorrect. An icon, progress dot, image aspect ratio, or design spacing can have a deliberate size. Inspect whether adjacent text scales and whether the relationship remains usable. Conversely, a fixed-height button with a multiline localized label can truncate even if its width is flexible.

When text grows, assess wrapping, vertical growth, fewer columns, rearrangement, and scrolling before shrinking or removing meaningful content. `fixedSize(horizontal: false, vertical: true)` can allow full text height, but the ancestor must accommodate that height. `layoutPriority` negotiates among siblings; it does not create room. A smaller fallback label is appropriate only if its meaning and accessible name remain sufficient.

Do not cap Dynamic Type or apply a tiny `minimumScaleFactor` simply to preserve a screenshot. If the product has a real constraint on a particular label, explain that constraint and provide another way to access the information. Avoid truncating essential text in an already scrollable region when additional lines can solve the problem. At large accessibility sizes, primary content and actions should remain recognizable and reachable. (D11–D13)

## Direction, safe areas, and input

Use semantic leading/trailing alignment and padding. SwiftUI supplies layout direction from the environment; inspect existing mirroring before manually reversing order or coordinates, which can mirror twice. Natural reading order should survive column-to-row changes. Geometric arrow placement or custom drawing may require explicit direction handling; the requirement comes from its meaning, not a blanket reversal rule.

Exercise realistic long localized strings and text input. Layout direction and locale are related but distinct test controls; changing only the locale does not prove the intended RTL state was rendered in a harness.

Preserve meaningful accessibility labels and grouping when rearranging content. Decorative graphics can remain accessibility-hidden. Avoid creating a duplicate set of focusable controls just to keep two layouts alive, and do not impose arbitrary accessibility sort priorities without checking the resulting order. Check VoiceOver focus and reading order on the actual UI when those relationships change.

For keyboard presentation and short windows, keep the focused field visible and controls reachable. A scroll view plus an appropriate safe-area inset may express a persistent action region; validate the combined height of content, actions, and keyboard. Ignoring the keyboard safe area at the wrong ancestor can make the last field unreachable. Full-bleed backgrounds can be intentional while interactive content respects safe areas. Do not infer device type from safe-area values. (D8, D11)

## Preserve identity and ownership

| Change | What to inspect |
| --- | --- |
| Replace `HStack` with `VStack` using `if/else` | Branches create different structural identities. Descendant state may reset even if the view names match. |
| Switch an `AnyLayout` around the same children | The arrangement can change while child identity is preserved. Still verify focus, scrolling, and presentation behavior in context. |
| Use `ViewThatFits` for alternative content | It chooses a presentation; it is not a promise to transfer local state or focus between alternatives. |
| Change row IDs, `.id`, ordering, or filtering | Selection, scrolling, and navigation may depend on those identities. |
| Add a conditional modifier that wraps/removes `self` | The conditional structure may replace the subtree. Prefer value changes for the same view when they express the requested behavior. |

Keep durable data in an owner whose lifetime matches the feature: a stable ancestor or model, with bindings passed to editable children. Do not move every value into a global model; transient visual state can remain local. A lazy container can discard or recreate descendants, so persistence must not depend on offscreen view storage. (A4, A6, E1)

Hold navigation paths, selected pages, and meaningful scroll identities at a stable level when the visible arrangement changes. Native navigation containers can adapt presentation, but custom structural switches still need deliberate state ownership. Avoid tying `.id` to width, orientation, or text size merely to force a layout refresh.

Task lifetimes deserve a separate check. `onAppear` is not a once-only workflow guarantee, and `.task` follows view lifetime. A resize-triggered subtree replacement can cancel, restart, or duplicate work. An onboarding animation's completion callback should not advance twice because a different layout appeared. Keep an operation with its intended owner, retain required cancellation behavior, and respect Reduce Motion where animation communicates the transition. Do not introduce unrelated concurrency rewrites in a scalability review.

## Limit unnecessary updates

Observe only the geometry or environment values the feature consumes. If a Boolean threshold is sufficient, storing an entire changing rectangle in a broad model can cause needless updates. Separate substantial regions into views with narrow inputs when that limits real update dependencies; splitting code into computed properties alone does not create an independent view boundary. Avoid turning a layout fix into blanket extraction of every tiny fragment.

### Factor adaptive branches as separate View types

When a layout uses `ViewThatFits`, `AnyLayout`, or `if/else` to switch arrangement, each section of the layout should be its own `View` struct with narrow value-type inputs — not a computed property or `@ViewBuilder` helper on the parent. A computed property is inlined into the enclosing view's body and shares its invalidation boundary: toggling the arrangement re-evaluates every section, even those whose data did not change. A separate `View` type invalidates only when its own inputs change. ([E1, E3](sources.md))

```swift
// AVOID: Computed properties share the parent's invalidation boundary.
// Switching between HStack and VStack re-evaluates header, details,
// AND footer together — even though only the arrangement changed.
struct AdaptiveCard: View {
    let title: String
    let subtitle: String
    let metric: Int
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        let layout = sizeClass == .regular
            ? AnyLayout(HStackLayout())
            : AnyLayout(VStackLayout())
        layout {
            header   // computed property — no invalidation boundary
            details  // computed property — no invalidation boundary
            footer   // computed property — no invalidation boundary
        }
    }

    private var header: some View { Text(title).font(.headline) }
    private var details: some View { Text(subtitle) }
    private var footer: some View { Text("\(metric) points") }
}
```

```swift
// PREFER: Each section is its own View with narrow inputs.
// Switching arrangement only re-evaluates AdaptiveCard's body;
// CardHeader, CardDetails, and CardFooter are skipped unless
// their own inputs changed.
struct AdaptiveCard: View {
    let title: String
    let subtitle: String
    let metric: Int
    @Environment(\.horizontalSizeClass) private var sizeClass

    var body: some View {
        let layout = sizeClass == .regular
            ? AnyLayout(HStackLayout())
            : AnyLayout(VStackLayout())
        layout {
            CardHeader(title: title)
            CardDetails(subtitle: subtitle)
            CardFooter(metric: metric)
        }
    }
}

struct CardHeader: View {
    let title: String
    var body: some View { Text(title).font(.headline) }
}

struct CardDetails: View {
    let subtitle: String
    var body: some View { Text(subtitle) }
}

struct CardFooter: View {
    let metric: Int
    var body: some View { Text("\(metric) points") }
}
```

This matters most when the adaptive parent re-evaluates frequently — during resizing, when `horizontalSizeClass` changes, or when `ViewThatFits` re-selects. Pass each subview only the fields it reads: a view declared with `let user: User` (a struct) invalidates when any field of `User` changes, even fields it never reads. A view declared with `let name: String` invalidates only when the name changes. ([E1, E3](sources.md))

Do not equate identity preservation with complete behavioral correctness. After a change, exercise entered text, selection, focus, navigation, scroll position, and ongoing tasks across size transitions. Record which behaviors were observed and which still need device validation.

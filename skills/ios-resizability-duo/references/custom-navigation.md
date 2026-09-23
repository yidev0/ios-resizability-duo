# Custom controls and containers that lack Duo adaptation

Audit custom UI by its role and behavior, not its class name. Missing system integration can be the defect even when no `UINavigationItem`, `UITabBar`, or other bar API occurs. UIKit rules apply to Swift and Objective-C and to UIKit embedded in SwiftUI; inspect pure SwiftUI custom containers too. Navigation titles and Back buttons are illustrative cases, not an exhaustive checklist.

## Audit adaptation gaps across custom UI

Inventory user journeys for bespoke destination selectors/tab bars, toolbars/action strips, navigation headers, sidebars/split containers, floating palettes, custom sheets/popovers, and overlays. For each, ask which relevant system behaviors it inherits, implements itself, or lacks: vertical/side placement, available-space compression and overflow, safe-area and asymmetric-margin updates, fold/occlusion avoidance, container/state continuity, accessibility, and gestures. Not every component needs every behavior. Flag an evidence-backed missing behavior or an explicitly unverified risk rather than declaring all custom UI defective.

**Fully bespoke tab bar example:** A bottom `UIView`/`UIStackView` row or SwiftUI `HStack` of buttons that changes a selected child/tab does not become a system tab bar just because it resembles one. Even with safe-area constraints, it will not automatically move into Duo's side region or acquire system compression/overflow and tab-navigation semantics. Report the bottom-placement/behavior assumptions and recommend either `UITabBarController`/`TabView` integration or the additional explicit custom adaptation needed. On a 27.1-SDK build, unused side space can coexist with this row remaining at the bottom; describe that as a likely consequence until observed on the runtime.

For other custom components, explain their own gap rather than reusing the tab-bar diagnosis. For example, a custom sheet may resize but fail to avoid an active fold; a floating palette may cover content when the safe area becomes asymmetric. Ordinary content that already adapts is not required to move into the system bar.

For a retained custom bar or sheet on 27.1+, combine local geometry with supported reserved-region queries and preferred-edge traits as needed; no API converts an arbitrary view into a system tab bar. Edge safe-area padding does not describe an interior fold. Inspect active division/occlusion regions and keep relevant interactive controls clear. A preferred vertical edge supplies direction, not bar visibility or the region's dimensions. See [reserved regions](https://developer.apple.com/documentation/uikit/uiview/reservedregion) and [verticalBarEdge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge). Do not add these symbols to an older-SDK source path.

Qualify each warning by the linked SDK. Missing 27.1-style side placement on a 27.0-SDK binary is expected compatibility behavior, not itself proof of broken custom UI. Separate current resizing/accessibility defects from work needed for a future 27.1-linked build; see [the 27.0-on-Duo path](toolchains.md#a-270-sdk-binary-running-on-duo).

## Detect and classify

Search authorized source plus storyboards/xibs, then trace view ownership, controller containment, actions, and call sites. Useful terms include `UINavigationBar`, `UIToolbar`, `UITabBar`, `setItems`, `pushNavigationItem`, `topItem`, `UILabel`, `titleLabel`, `backButton`, `closeButton`, `addSubview`, `addTarget`, `UIAction`, `popViewController`, `popToViewController`, `popToRootViewController`, `dismiss`, `setNavigationBarHidden`, and `hidesBackButton`. Follow delegate/coordinator/router methods too; navigation actions need not mention UIKit in the button's own file.

Explicitly inspect:

- Manually created or manually populated `UINavigationBar`, `UIToolbar`, or `UITabBar`, including storyboard-owned standalone bars and direct writes to a navigation controller's managed bar item stack.
- `UILabel`s constrained or framed where a navigation title normally sits: top-center rows, a title alongside a Back/Close button, or a replacement header while the system bar is hidden.
- Custom Back/Close buttons inserted into the content hierarchy, especially buttons calling `popViewController` or `dismiss` whose actions are not represented through `navigationItem`/system toolbar placements.
- Title/back controls in a controller outside `UINavigationController`, `UISplitViewController`, or `UITabBarController`. Walk ancestors and presentation sites: merely setting `navigationItem` on an uncontained controller will not display a managed bar. A split/tab controller alone is not proof that its child has a navigation controller.
- SwiftUI equivalents: top-aligned overlays/HStacks with a title and dismiss/path-mutating button, hidden system navigation, or UIKit representables containing a manually built bar. Map navigation intent to the owning system container and semantic toolbar placement.
- Fully custom bars with **no bar-class names**: arrays of icon/text buttons, `selectedIndex`/selected-tab state, tab route enums, child-view swaps, `addChild`/`setViewControllers` wrappers, bottom-pinned stacks, `safeAreaInset`/overlay rows, or gesture-driven destination selectors. Trace their semantic role and selection/state behavior. Generic class searches alone will miss them.

These are **candidates**, not blanket violations. Assigning `navigationItem.title`, bar button items, or a controller's `toolbarItems` programmatically is ordinary system configuration. Customizing a managed bar's appearance is not the same as populating its item stack manually. A document heading, media transport row, in-content Cancel action, or accessible custom navigation implementation can be intentional. Confirm intent with surrounding code and the user journey; retain correct cases with evidence.

## Why this matters on Duo

Standalone bar components don't participate in the same automatic vertical navigation adaptation as controller-managed bars. [Apple's bar guidance](https://developer.apple.com/videos/play/tech-talks/111462/)

For other custom controls, infer risk from their actual ownership and layout. The system's side region can remain empty while a hand-positioned title and Back button stay at their old coordinates. Audit side-region participation and overflow, dynamic safe areas, asymmetric margins, fold avoidance, accessibility, and navigation gestures individually. Do not claim all are broken just because a view is custom: constraints may already track safe areas, and accessibility/gestures may be implemented explicitly. Source-only findings must say which consequences require runtime verification.

## Evaluation-only output

For each candidate report:

`File/line | Inferred intent and confidence | Owning controller and container/presentation | Missing system integration and concrete adaptation risk | Recommended mapping | SDK/runtime boundary | Verification/retention reason`

Name the component construction and action/selection/containment call site when they differ. Explain its role, which Duo behaviors are missing, and why resizing the underlying view is insufficient. State the additional implementation required and offer a concrete system-component mapping when appropriate. Recommend changes without editing source or inserting TODOs. An intentionally content-level control needs an explicit adaptive-layout rationale and checks, not an automatic migration.

## Implementation mappings

| Existing intent | Preferred mapping |
| --- | --- |
| Ordinary screen title | `navigationItem.title`; preserve typography/color through supported bar appearance configuration at an appropriate scope. |
| Essential custom title content | `navigationItem.titleView` with adaptive intrinsic sizing and accessibility. A custom title view is not a promise of vertical placement or overflow; test it and prefer a semantic title when sufficient. |
| Ordinary stack Back action | Let `UINavigationController` supply its Back item and preserve the existing stack. Customize supported back appearance/title as needed; don't replace a normal pop with dismissal. |
| Custom Close/Cancel or required navigation action | Use the owning controller's `navigationItem` leading/left bar items or appropriate supported group API; retain the exact action, validation, and dismissal owner. Prefer a standard title/image item over `customView` when possible. Verify custom Back behavior and gestures separately. |
| Standalone navigation/toolbar/tab structure | Integrate the existing controllers into the appropriate system container; use their navigation items, toolbar items, or tab items. Preserve identity, selected tab, delegates, and restoration. Do not wrap an existing stack again or flatten a split view. |
| Bespoke destination/tab selector | Prefer `UITabBarController`/`TabView` with stable existing destinations, selection bindings, per-tab navigation stacks, badges and restoration. Preserve reselection/deep-link behavior and any custom appearance using supported configuration. If retaining the custom selector is a product requirement, implement relevant side/compact placement, overflow, safe-area/fold adaptation and accessibility explicitly; do not claim system parity from safe-area padding alone. |
| Other custom action surfaces/presentations | Choose the corresponding system toolbar, split container, sheet or popover where it preserves the product interaction. Otherwise implement and verify the specific missing adaptive behaviors. Keep content-linked actions near their content and avoid moving every control to the side indiscriminately. |
| Intentional content control | Retain within content only with explicit adaptive layout: local geometry, independent safe-area edges, readable/hittable sizes, keyboard handling, and fold-aware placement when applicable. It must not be mistaken for a system navigation action. |

Use [UINavigationItem](https://developer.apple.com/documentation/uikit/uinavigationitem) and the actual SDK declarations for exact configuration. Preserve custom appearance through supported attributes, tint, images, semantic labels and—where necessary—adaptive custom views. Preserving appearance does not require retaining absolute coordinates. If essential appearance cannot be preserved without a product tradeoff, document the concrete choice rather than silently dropping it.

Make the migration atomic: wire the container/items and actions, remove redundant content chrome and its constraints, update content layout, and reconcile bar visibility throughout the affected journey. Prevent duplicate titles/back controls and double safe-area padding. Keep restoration identifiers, selected items, controller instances, and navigation state intact. For split views preserve column ownership, collapse/expand behavior, selection, and each column's actions.

Do not assume that moving a button into `leftBarButtonItem` preserves interactive-pop behavior. Prefer the system Back item for ordinary stack navigation. Check existing gesture/delegate/custom-transition behavior and test both completed and cancelled interactive pops. Never “fix” swipe-back by indiscriminately clearing `interactivePopGestureRecognizer.delegate` or forcing it enabled on a root controller. Preserve unsaved-change guards and custom actions; a required behavior change needs an explicit decision. [Gesture API](https://developer.apple.com/documentation/uikit/uinavigationcontroller/interactivepopgesturerecognizer)

Preserve accessibility labels, identifiers, traits, logical focus order and usable targets; use Dynamic Type where applicable. Preserve RTL semantics and directional images/anchors, without manually flipping hardware-aligned Duo chrome. Verify modal Close still dismisses the intended presentation, and Back still pops exactly the intended stack level. State restoration and deep links must reconstruct the same container hierarchy.

When an overflow action opens a SwiftUI `confirmationDialog`, let the action update persistent presentation state and attach the dialog to a stable view in the hierarchy. A system overflow item is not a reliable view anchor. Test invocation, cancellation, and confirmation with the action both visible and overflowed, including after resizing. [Official lab clarification](https://developer.apple.com/forums/thread/847644).

## Xcode boundary

- **26.x:** The basic UIKit containers, `navigationItem.title`, `titleView`, left/right bar button items, and system Back approach predate 26. They can repair navigation ownership now, subject to the app's deployment target. Do not claim the resulting 26-SDK binary has Duo's 27.1 vertical behavior.
- **27.0:** Apply the same migration while retaining the 27.0 main/CI build. Use 27.0 overflow APIs only where verified and useful. No 27.1-only symbol may be introduced merely because a side-installed beta exists; a runtime availability check does not make that symbol compilable with the old SDK.
- **27.1+:** Verify full-display/vertical behavior with a 27.1+ linked SDK on a compatible Duo runtime. Inspect current availability before adding axis/vertical-edge customizations. Standard title/back/container migrations often need no new API at all.

For every path, distinguish static ownership fixes from runtime verification. Test title and action access through outer/inner display changes, asymmetric left/right Split View, short-height overflow, keyboard, RTL, accessibility, restoration, and back/close/interactive-pop transitions. Retained content UI must pass its own adaptive-layout checks; system-container membership alone is not a pass.

For custom tab migrations, also test selected destination, independent per-tab state/navigation paths, badge updates, reselection, deep links and restoration across size changes. Preserve initialization order: selection configured before destinations exist must not be lost when the system container is installed; reconcile stored selection with later user-driven tab changes. A side-installed newer SDK must not leak newer symbols into a 26.x/27.0 main or CI build. If equivalent bespoke behavior needs unavailable APIs, implement the supported baseline and report the remaining 27.1+ work explicitly.

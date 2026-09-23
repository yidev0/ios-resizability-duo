# Duo interaction and product review

Apply the baseline first. Offer feature-specific improvements only when supported by this app's code or the current session. Treat SDK 27.1 features as staged suggestions if the main compiler cannot build them.

## One adaptive experience

Keep the same destinations, actions, and navigation identity when the phone opens or closes. Use compact/regular environment and actual local space, not a Duo model identifier or a hardcoded hinge angle. A wider surface may reveal a list and detail together or show existing secondary content. Avoid a special screen for every pose; all essential actions remain usable closed, open, and partially folded. [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/)

The [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) also recommends small, necessary fold adjustments and keeping navigation outside arrangement views. For an existing grid, consider an even column count where it helps content divide around the fold without sacrificing usable item size; don't force this onto every width. In Split View, controls can occupy the left app's outer left edge. Hardware-aligned chrome is not mirrored simply because text uses RTL. Keep controls close to the content they affect and use semantic groups instead of fixed spacers.

## Navigation, bars, and presentations

Audit every navigation stack, split view, tab, inspector, sheet, and custom bar:

Audit custom controls and containers for missing Duo behavior; use [custom-navigation.md](custom-navigation.md). This includes a tab bar built entirely from generic views/buttons, not just standalone UIKit bars or custom title/Back controls. A resizable content view or correct safe-area padding does not establish side-region participation, compression/overflow or fold adaptation.

- Use container-managed bars (`NavigationStack`/`NavigationSplitView`/`TabView`, or navigation/tab/split view controllers). Standalone hand-built `UINavigationBar`, `UIToolbar`, or `UITabBar` does not gain the same automatic adaptation.
- Preserve the Back/Close action, semantic grouping, and important actions when items move vertically. Supply both title and symbol so the system can choose a representation; keep meaningful text and wide controls horizontal.
- Check detail-column bars separately from sidebar/content columns and inspectors. Inner portrait may use horizontal bars. Sheets depend on display and placement; don't force every container vertical.
- Test keyboard, short height, and competing system UI. Consolidate duplicate ellipsis menus; assign item visibility by actual task importance. Choose whether destinations or task actions deserve more space. Adapt a custom view only if it fits and remains accessible; don't shrink tap targets to fit.

Bar behavior and custom-item guidance: [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/). Exact API routes: [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo).

Do not derive bar placement from orientation, width, or RTL alone. Query the supported environment/trait when layout truly depends on it. `toolbarVerticalEdge` is the **preferred** edge even if no bar is visible; nil means a context where the system never places a vertical bar. It is not a Boolean visibility test or an inset measurement. [API semantics](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge)

Use the version table before coding overflow or axis control. For UIKit and other APIs not listed there, inspect the exact declaration. Useful lookup names include `verticalBarEdge`, `axisBehavior`, `toolbarVerticalCompressionBehavior`, `verticalBarCompressionBehavior`, `toolbarVerticalBehavior`, `preferredVerticalBarBehavior`, `additionalOverflowItems`, and sheet placement. These are lookup candidates, not a promise that every symbol exists in 27.0.

## Fold and reserved regions

Prefer a system container that already adapts. For custom spatial content, inspect division and occlusion reserved regions in local coordinates and respond as they activate/deactivate. Use a layout container before manual displacement; don't use raw hinge angle as a layout breakpoint. Continuous lists/articles usually remain scrollable through the fold; controls or a non-scrolling focal element may need displacement. [Strike a pose with adaptive layouts on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111463/)

`ArrangementView` supports paired primary/secondary content with split or overlay styles; the choice should follow their relationship. It complements navigation rather than replacing it. Preserve content identity and avoid nesting where scrolling or split-view sizing could make part of the arrangement inaccessible. [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview)

Safe-area edges and size classes alone do not locate an interior division. For retained custom layouts, inspect each reserved region's local frame and active state; UIKit queries can return inactive intersecting regions, and the returned frame already includes its margins. Avoid applying margins twice. Check custom bottom sheets, floating controls, and dense tables when the fold becomes active. [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion)

## Suggestions grounded in the app

First name the actual feature or code evidence, then explain the opportunity. These examples are prompts for judgment, not a list to implement in every app:

| Existing feature | Possible user benefit | What to investigate |
| --- | --- | --- |
| Library, mail, notes, bookmarks, or documents | Keep the selected item visible alongside its collection when space allows. | Existing split navigation; preserve path/selection when collapsing. This can be baseline work using older APIs. |
| Media playback, timer, practice, or guided activity | Place existing controls where they remain reachable while hands-free content stays visible. | Arrangement/reserved regions on 27.1; same actions and ordinary adaptive layout as fallback. |
| Photo/video capture | Show a subject preview or teleprompter on the other display, if useful to the existing capture workflow. | Camera capture accessory availability, permission flow, display/camera transitions, and physical-device testing. No assumption of unrestricted second-display output. |
| Document editing or comparison | Work with independent documents in multiple scenes where supported. | Separate scene state, restoration, activation errors, and dynamic availability; don't enable extra scenes merely because the device folds. |
| Musical instrument or interactive effect | Offer optional hinge-driven expressiveness with an equivalent ordinary control. | `onHingeChange`/`UIHingeInteraction` after availability verification; reset the effect when hinge data is absent. |

Apple's [multiple displays and scenes talk](https://developer.apple.com/videos/play/tech-talks/111464/) distinguishes hinge interactions from layout and explains dynamic scene/accessory availability. The [camera talk](https://developer.apple.com/videos/play/tech-talks/111465/) covers front-camera switching and direction coordination. Use these specialized APIs only when relevant, and consult their current declarations before implementation.

For a camera-accessory proposal, retain essential controls in the main capture interface. Presentation requires the appropriate foreground capture context and is system-controlled; it can disappear when capture stops, the phone closes, or another registration takes precedence. Share the capture model, separate availability from the user's enabled preference, and stop transient animation/work when withdrawn. Verify capture-dependent behavior on hardware; previews and Simulator can check ordinary accessory-view layout. [Camera accessory guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)

If the app uses motion for a level, compass, AR interaction, or game, review the coordinate frame separately from layout. `CMMotionManager.deviceMotionBody` is declared in iOS 27.0, not 27.1. Investigate view-relative sensor orientation and the lab's stated full-screen limitation before recommending it; preserve the default-frame fallback. Raw hinge effects must tolerate missing data and variable update frequency. [Sensor coordinate orientation](https://developer.apple.com/documentation/uikit/uiview#Sensor-coordinate-orientation), [deviceMotionBody](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody), [lab context](https://developer.apple.com/forums/thread/847644).

For an existing alarm or Live Activity feature, consult AlarmKit/ActivityKit presentation guidance instead of proposing arbitrary output to the outer display. For web content, the lab describes Viewport Segments and Device Posture as experimental, opt-in features in 27.1; verify current WebKit support and retain a responsive fallback before any production recommendation. These are conditional research leads, not requirements for every app. [Official lab summary](https://developer.apple.com/forums/thread/847644)

For each suggestion record **observed feature → current friction → proposed benefit → SDK/runtime/capability → fallback → effort and validation**. Rank by value to this product. Keep optional enhancements outside the mandatory readiness work unless the user requests them. Don't invent app features to fill a report.

# Source ledger and refresh policy

Research snapshot: **2026-09-22**; updated **2026-09-24** with Apple's official group-lab summary, September 23 SwiftUI/UIKit/Photos & Camera forum answers, and SDK declarations. This ledger is a starting point for later releases, not a frozen specification. Refresh it against the app's actual Xcode and SDK.

## Source priority

Use the installed SDK declarations for code that must compile, current Apple API documentation for availability and semantics, and Apple design guidance for interface decisions. The Tech Talks and Apple-staff forum answers add examples and context; retain their version and device conditions. If documentation and a beta SDK differ, record both, use declarations that compile with the selected build SDK, and flag the discrepancy. A runtime availability guard cannot make an older SDK recognize a new symbol.

For JavaScript-rendered documentation, use Apple's **View Markdown** link when available or inspect SDK headers/Swift interfaces. Check exact labels and types rather than copying an API spelling from a transcript. Direct availability links and the 26.x / 27.0 / 27.1+ matrix are in [toolchains.md](toolchains.md).

## Apple documentation and Tech Talks

### Overview, compatibility, and lifecycle

| Source | Use |
| --- | --- |
| [Get ready for iPhone Duo](https://developer.apple.com/iphone-duo/) | Entry point for Duo documentation, Tech Talks, and events. |
| [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) and [Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) | Container and API routes; consistent state/actions, restrained fold adaptation, and vertical controls. The HIG was checked through Apple's documentation JSON when its page did not render. |
| [TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) and [TN3208](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements) | Precise full-screen/discrete-resize compatibility and SDK-gated launch-screen submission requirements. |
| [Xcode support](https://developer.apple.com/xcode/system-requirements), [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes), and [UIKit updates](https://developer.apple.com/documentation/updates/uikit) | SDK bundles, current simulator limitations, and release-specific UIKit lifecycle changes. |
| [Restoring your app's state](https://developer.apple.com/documentation/uikit/restoring-your-app-s-state) | Scene-specific restoration after interruption or relaunch, separate from a normal fold. |

### UI and specialized APIs

| Source | Use |
| --- | --- |
| [UINavigationItem](https://developer.apple.com/documentation/uikit/uinavigationitem) and [interactive pop gesture](https://developer.apple.com/documentation/uikit/uinavigationcontroller/interactivepopgesturerecognizer) | Managed navigation title/actions and gesture ownership when replacing custom chrome. |
| [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion), [verticalBarEdge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge), and [UIArrangementViewController](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) | 27.1 local reserved regions, preferred bar edge, and UIKit arrangements. Check exact declarations, including Objective-C names. |
| [Camera capture accessory guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo) | SwiftUI/UIKit registration, shared capture model, dynamic availability, and hardware verification. |
| [deviceMotionBody](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody) and [UIView sensor coordinate orientation](https://developer.apple.com/documentation/uikit/uiview#Sensor-coordinate-orientation) | Display-relative motion use cases; `deviceMotionBody` is declared in 27.0, not 27.1. |

### Six iPhone Duo Tech Talks

| Talk | Use |
| --- | --- |
| [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) | One adaptive experience, hierarchy continuity, and control placement. |
| [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) | Linked-SDK 26/27/27.1 behavior, Device Hub, safe areas, and size classes. |
| [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) | System bars, semantic placement, custom controls, and overflow. |
| [Strike a pose with adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/) | Arrangements, displacement, divisions, and occlusions. |
| [Multiple displays and scenes](https://developer.apple.com/videos/play/tech-talks/111464/) | Hinge effects versus layout; dynamic scene and accessory availability. |
| [Camera experience](https://developer.apple.com/videos/play/tech-talks/111465/) | Front-camera switching, preview, direction coordination, and accessory opportunities. |

## Apple forum answers

### September 16–17 group lab

[A Summary of the iPhone Duo Group Lab](https://developer.apple.com/forums/thread/847644) is an official Apple DTS Engineer post with 16 continuation replies, reviewed **2026-09-24**. Prefer it to the secondary transcript-derived summary below. It clarifies same-scene folds, per-window state, custom bars and sheets, hybrid traits, overflow presentation, and conditional product opportunities. Its guidance is reflected in [implementation.md](implementation.md), [custom-navigation.md](custom-navigation.md), [duo-experience.md](duo-experience.md), [toolchains.md](toolchains.md), and [verification.md](verification.md).

Keep these qualifications when using the lab answers:

- `toolbarVerticalEdge` and `verticalBarEdge` indicate a **preferred edge even when a bar is hidden**, not current visibility or an inset size.
- General “iOS 27” wording does not place `ArrangementView` or `UIArrangementViewController` in 27.0; use exact declarations. SwiftUI `ToolbarOverflowMenu` and `visibilityPriority(_:)` are 27.0; `ArrangementView`, toolbar `axisBehavior(_:)`, and `toolbarVerticalEdge` are 27.1 in the checked declarations.
- A familiar aspect ratio, split navigation, multiple app instances, multitasking, and linked-SDK compatibility are different concepts. Adding a split container does not change the linked SDK.
- Orientation and RTL guidance is conditional on inner/outer context and hardware-aligned chrome. Neither a forum answer nor Auto Layout alone establishes Duo readiness; verify behavior.

The lab's [Viewport Segments](https://github.com/WebKit/standards-positions/issues/327) and [Device Posture](https://github.com/WebKit/standards-positions/issues/328) discussion is an experimental WebKit research lead, not a production-support guarantee.

### September 23 SwiftUI Q&As

Events: [morning](https://developer.apple.com/forums/activities/1664080) · [evening](https://developer.apple.com/forums/activities/1671080). The linked threads have substantive Apple-staff answers relevant to this skill; a reply count alone was not treated as an answer.

| Answered threads | Skill-relevant clarification |
| --- | --- |
| [Arrangement collapse](https://developer.apple.com/forums/thread/847800), [fold updates](https://developer.apple.com/forums/thread/848014), [semantic layout versus hinge angle](https://developer.apple.com/forums/thread/848017) | A split arrangement can show one child. Choose essential content and retain access to hidden actions; use current geometry and regions because folding can pause or reverse. The follow-up seeking an exact hidden-controls presentation has no Apple answer. `splitArrangementAxis` documents an axis, not proof both children are visible. |
| [Home layout](https://developer.apple.com/forums/thread/847877), [GeometryReader/containerRelativeFrame](https://developer.apple.com/forums/thread/847833), [half-width compatibility](https://developer.apple.com/forums/thread/847836) | Retain supported container-relative tools and avoid device-specific fixed widths. A 27.1-linked app cannot force the old compatibility width; the person may still choose a smaller Split View scene. |
| [Display identification](https://developer.apple.com/forums/thread/847995), [phone idiom](https://developer.apple.com/forums/thread/848023), [linear navigation](https://developer.apple.com/forums/thread/847818) | Duo is a phone idiom with potentially regular width. No supported UI-layout API identifies the active physical display. Keep navigation state independent of its compact/regular presentation. |

### September 23 UIKit Q&As

Events: [morning](https://developer.apple.com/forums/activities/1670080) · [evening](https://developer.apple.com/forums/activities/1665080). The guidance below is from Apple staff.

| Answered threads | Skill-relevant clarification |
| --- | --- |
| [Tab/sidebar default](https://developer.apple.com/forums/thread/847961), [inner-display sidebar](https://developer.apple.com/forums/thread/847912) | On iOS, automatic sidebar placement defaults to a tab bar; sidebar use is opt-in. `preferredPlacement` is declared in 27.0. |
| [Custom vertical bar](https://developer.apple.com/forums/thread/847835), [Back item](https://developer.apple.com/forums/thread/847875), [vertical segmented control](https://developer.apple.com/forums/thread/847811), [tab accessory](https://developer.apple.com/forums/thread/847807) | Retained custom bars need their own space, overflow, and accessibility behavior. Prefer system Back semantics and avoid a wide control in a narrow vertical bar. Tab accessories must resize. Bar layout regions and `UIBarButtonItem.axisBehavior` require 27.1. |
| [Collection layouts](https://developer.apple.com/forums/thread/847879), [asymmetric margins](https://developer.apple.com/forums/thread/848019), [container composition](https://developer.apple.com/forums/thread/847786), [existing navigation](https://developer.apple.com/forums/thread/848055) | A collection layout does not automatically avoid a division; normal scrolling can cross it. Query local regions for content that must move. Keep navigation ownership outside arrangements. |
| [Objective-C viewer](https://developer.apple.com/forums/thread/848021), [sheet placement](https://developer.apple.com/forums/thread/847797) | Use local layout values as the main sizing source, not a scene callback. Check 27.1 declarations for arrangement/region APIs; sheet placement is declared in 27.0. |

### September 23 Photos & Camera Q&As

Events: [morning](https://developer.apple.com/forums/activities/1659080) · [evening](https://developer.apple.com/forums/activities/1673080). The guidance below is from Apple staff. The handover answer is partial; the AR accessory thread contains a later Apple correction.

| Answered threads | Skill-relevant clarification |
| --- | --- |
| [Virtual-camera handover](https://developer.apple.com/forums/thread/847766), [session and timestamps](https://developer.apple.com/forums/thread/848088) | Switching physical front cameras can drop frames and disrupt sample timestamps while the capture session remains active. The first answer does not resolve the original latency and dropped-frame-reporting follow-ups. |
| [Camera availability](https://developer.apple.com/forums/thread/847754), [MultiCam sets](https://developer.apple.com/forums/thread/847763), [constituent delivery](https://developer.apple.com/forums/thread/847781) | Query direction and supported MultiCam combinations; do not infer them from hinge pose or assume a virtual rear-plus-outer-front device. The direction coordinator requires 27.1; MultiCam set discovery predates Duo. |
| [Inner-camera readout](https://developer.apple.com/forums/thread/847809), [long analysis](https://developer.apple.com/forums/thread/847839) | The inner camera supports native readout and app-owned long-running Vision analysis; app processing and thermal load can still drop frames. |
| [AR accessory](https://developer.apple.com/forums/thread/847744), [AR continuity](https://developer.apple.com/forums/thread/847767), [camera occlusion](https://developer.apple.com/forums/thread/847772), [shutter placement](https://developer.apple.com/forums/thread/847757), [Simulator testing](https://developer.apple.com/forums/thread/848083) | A later Apple reply corrects the initial AR answer: an active `ARSession` can qualify for the 27.1 `CameraCaptureAccessory`. Folding does not itself pause AR tracking. Keep controls clear of active reserved regions. Simulator checks UI flow; hardware establishes capture capability and performance. |

### Forum limitations and beta issues

The [overlay-arrangement Simulator issue](https://developer.apple.com/forums/thread/848029) is an Apple-acknowledged beta issue. Do not turn its workaround into permanent layout guidance; check the installed release notes. Exclude Feedback-only replies, unresolved follow-ups, and unrelated wallpaper or app-marketing questions from implementation rules. Recheck partial or corrected answers before relying on them in a later SDK.

## Secondary context

[frankschlegel's consolidated group-lab Q&A](https://gist.github.com/frankschlegel/6356a059426b2393528691822edfdae6) identifies itself as derived from automatically generated September 16–17 transcripts with corrections. Use it for questions and pointers, not as an official verbatim transcript or authority for exact API availability. Its conceptual guidance overlaps Apple's talks and official lab summary. Do not repeat unverified split-view restoration timing, camera Simulator behavior, or App Store eligibility as settled facts. For an unresolved claim, inspect the [official summary](https://developer.apple.com/forums/thread/847644), original session, or later Apple documentation; if still unresolved, label it.

## Updating this ledger

For a new forum link, read the question and substantive answer. Record its date, Apple-staff status, SDK/beta conditions, direct thread or answer URL, and affected finding or API. Verify technical claims against current declarations and primary documentation. Mark superseded guidance, update the relevant skill reference instead of accumulating contradictory rules, and rerun affected behavior checks. Do not invent answers for announced sessions.

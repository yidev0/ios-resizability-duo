# Source ledger and refresh policy

Research snapshot: **2026-09-22**, updated **2026-09-24** with Apple's official group-lab summary and linked documentation. This is a reusable starting point, not a frozen specification for later betas/releases. Refresh the installed-version documentation during each app evaluation.

## Primary Apple sources

| Source | Use |
| --- | --- |
| [Get ready for iPhone Duo](https://developer.apple.com/iphone-duo/) | Entry point for documentation, six Tech Talks, group labs, and upcoming forum sessions. |
| [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo) | Container selection, bars/presentations, arrangements, reserved-region and camera API links. |
| [Designing for iPhone Duo — HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) | Design guidance checked through Apple's official documentation JSON after the JS page did not render: consistent state/actions, restrained fold adaptation, arrangement/nav separation, and vertical controls. |
| [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/) | Single adaptive experience, hierarchy continuity, control positioning, content design. |
| [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/) | Linked SDK 26/27/27.1 behavior, Device Hub, safe areas, size classes. |
| [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/) | System bars, semantic placement, custom controls and overflow. |
| [Strike a pose with adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/) | Displacement, arrangements, divisions and occlusions. |
| [Multiple displays and scenes](https://developer.apple.com/videos/play/tech-talks/111464/) | Hinge effects versus layout, dynamic multi-scene and accessory availability. |
| [Camera experience](https://developer.apple.com/videos/play/tech-talks/111465/) | Camera direction/switching, preview and accessory opportunities. |
| [TN3192](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key) | SDK 27+ discrete resize behavior, older-version compatibility cutoff. |
| [TN3208](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements) | SDK-gated launch-screen submission requirement. |
| [Xcode support](https://developer.apple.com/xcode/system-requirements) | SDK bundles, host requirements, deployment/device support. |
| [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) | Version-specific testing limitations, changes and known issues. |
| [UIKit updates](https://developer.apple.com/documentation/updates/uikit) | Release-specific scene lifecycle and UIKit changes. |
| [UINavigationItem](https://developer.apple.com/documentation/uikit/uinavigationitem) | API reference for title/titleView and bar items when migrating custom navigation chrome. |
| [Interactive pop gesture recognizer](https://developer.apple.com/documentation/uikit/uinavigationcontroller/interactivepopgesturerecognizer) | Check gesture ownership and existing delegates when changing a custom Back implementation. |
| [A Summary of the iPhone Duo Group Lab](https://developer.apple.com/forums/thread/847644) | Official DTS Engineer / Apple post and 16 continuation replies, all read on 2026-09-24. Clarifies same-scene folds, per-window state, custom bars/sheets, hybrid traits, overflow presentation, and specialized feature opportunities. |
| [Restoring your app's state](https://developer.apple.com/documentation/uikit/restoring-your-app-s-state) | Scene-specific user activity restoration for actual interruption/relaunch, separate from a normal fold. |
| [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion) | 27.1 availability, local coordinates, active state, occlusion/division kinds, and frame margins. |
| [verticalBarEdge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge) | 27.1 preferred-edge semantics independent of current bar visibility. |
| [UIArrangementViewController](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) | 27.1 availability and UIKit primary/secondary arrangement behavior, including Objective-C API routes. |
| [Camera capture accessory guide](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo) | SwiftUI/UIKit registration, shared capture model, dynamic availability versus enabled state, and hardware verification. |
| [deviceMotionBody](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody) and [UIView sensor coordinate orientation](https://developer.apple.com/documentation/uikit/uiview#Sensor-coordinate-orientation) | 27.0 availability and the display-relative motion use case; do not group every Duo-relevant API under 27.1. |

Exact Apple availability metadata checked in the creation session: SwiftUI `ToolbarOverflowMenu` and `ToolbarContent.visibilityPriority(_:)`: iOS 27.0; `ArrangementView`, `ToolbarContent.axisBehavior(_:)`, and `EnvironmentValues.toolbarVerticalEdge`: iOS 27.1. Direct links are in [toolchains.md](toolchains.md).

For JS documentation, follow the page's official **View Markdown** link when available, or inspect installed SDK declarations. A transcript's API name may omit labels or be transcribed incorrectly; don't generate code from that spelling alone. If documentation and installed beta SDK differ, record both versions, prefer compilable declarations for the actual build, and flag the discrepancy.

## Official lab clarifications and source conflicts

The official [summary thread](https://developer.apple.com/forums/thread/847644) supersedes the gist as the preferred lab summary. The thread showed an Apple-affiliated DTS Engineer as author; the review date above is not an inferred publication timestamp. It discusses 26-SDK compatibility, 27.0 versus 27.1 linking, and several 27.1 APIs. Keep those conditions with each recommendation.

Applied clarifications live in `implementation.md` (scene continuity, defaults ownership, trait overrides), `custom-navigation.md` (custom adaptation and stable dialog presenters), `duo-experience.md` (region semantics and conditional feature opportunities), `toolchains.md` (additional verified API availability), and `verification.md` (corresponding scenarios). All six Tech Talks remain covered; the forum adds context rather than replacing them.

Resolve shorthand explicitly:

- A forum description of `toolbarVerticalEdge`/`verticalBarEdge` as detecting presentation does not override the API's **preferred edge even when hidden** semantics.
- General “iOS 27” phrasing does not make arrangement APIs available in 27.0. Check exact declarations, main SDK, and runtime separately.
- Statements tying familiar aspect ratio to lacking “Split View” must not conflate split navigation, multiple app instances, multitasking, and linked-SDK compatibility. Use the preparation talk's SDK matrix; adding a split container alone does not change the binary's linked SDK.
- General orientation or RTL wording is conditional: retain the documented inner/outer distinction and hardware-aligned bar behavior; don't hardcode a side from language direction.
- Neither a forum answer nor adopting Auto Layout guarantees a bug-free app. Preserve source evidence and runtime checks. Use TN3192 for precise full-screen/discrete-resizing behavior.

The lab's experimental web-feature discussion is a research lead for relevant web content, not a production-support guarantee. Follow its [Viewport Segments](https://github.com/WebKit/standards-positions/issues/327) and [Device Posture](https://github.com/WebKit/standards-positions/issues/328) links and current WebKit documentation before implementation.

## Secondary group-lab summary

The user supplied [frankschlegel's consolidated Q&A](https://gist.github.com/frankschlegel/6356a059426b2393528691822edfdae6). It identifies itself as derived from automatically generated September 16/17 transcripts with corrections. Treat it as a source of questions and useful pointers, not an official verbatim transcript or authority for exact API availability. Its conceptual guidance overlaps the Apple talks. Do not repeat unverified details such as exact split-view restoration timing, camera simulator behavior, or App Store eligibility as settled facts.

The Duo landing page links the original group labs. For an unresolved claim, inspect the official summary, original session/timestamp, or later Apple documentation. If still unresolved, label it and don't block the compatible baseline on speculation.

## Adding future forum Q&A

The official group-lab summary is incorporated above. For additional forum links, read the actual question and answer, note date, author/Apple-staff status, SDK/beta version and relevant conditions. Add the precise answer URL and affected finding/API to this ledger. Verify technical claims against current SDK declarations and primary docs; forum discussion is useful context but isn't automatically a contractual API guarantee. Identify superseded guidance explicitly, update the relevant reference rather than accumulating contradictory rules, and rerun affected behavioral checks. Do not invent answers for announced sessions.

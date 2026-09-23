# iOS Resizability and iPhone Duo

An agent skill for evaluating and implementing adaptive iOS layouts across SwiftUI, UIKit, Swift, and Objective-C.

The skill asks whether you want **evaluation only** or **evaluation followed by full implementation**. It inventories the actual Xcode and SDK versions, audits the app, and separates fixes supported by your main toolchain from later adoption work. It also suggests Duo-specific improvements when an existing app feature would benefit.

## Install

Run one of these in your app project:

```sh
# Codex
npx skills add yidev0/ios-resizability-duo --agent codex

# Claude Code
npx skills add yidev0/ios-resizability-duo --agent claude-code
```

Add `--global` to make it available across projects. Installation uses the [skills CLI](https://github.com/vercel-labs/skills).

## Use

Ask your agent:

> Use the ios-resizability-duo skill to check this app for resizability and iPhone Duo support.

It asks whether you want **evaluation only** or **evaluation and full implementation**, then checks your Xcode version before proceeding. You can also invoke it directly with `$ios-resizability-duo` in Codex or `/ios-resizability-duo` in [Claude Code](https://code.claude.com/docs/en/skills).

## Xcode and SDK boundaries

| Build SDK | Scope |
| --- | --- |
| 26.x | Adaptive baseline and system-container integration using available APIs; retain the expected compatibility presentation. |
| 27.0 | Resizable baseline and verified 27.0 APIs; assess the actual 27.0-built artifact on Duo separately from a 27.1 rebuild. |
| 27.1+ | Full-display and system vertical-bar adoption, plus relevant arrangement and reserved-region APIs after checking exact availability. |

Running a 27.0-built app on a newer Duo runtime does not change its linked SDK. A runtime availability check cannot make an older SDK compile an unknown symbol. The skill preserves the main development/CI toolchain and treats a side-installed beta as a separate test environment.

A custom tab bar built from ordinary views or buttons does not acquire system side placement or overflow behavior automatically. The audit covers these missing behaviors across custom UI; navigation titles and Back buttons are examples, not the boundary.

## Contents

- [Skill instructions](skills/ios-resizability-duo/SKILL.md)
- [Toolchain and API availability](skills/ios-resizability-duo/references/toolchains.md)
- [Baseline audit and implementation](skills/ios-resizability-duo/references/implementation.md)
- [Custom controls and navigation](skills/ios-resizability-duo/references/custom-navigation.md)
- [Duo interaction and product opportunities](skills/ios-resizability-duo/references/duo-experience.md)
- [Verification and reporting](skills/ios-resizability-duo/references/verification.md)
- [Dated source ledger and refresh policy](skills/ios-resizability-duo/references/sources.md)
- [Read-only Xcode inventory helper](skills/ios-resizability-duo/scripts/inspect_xcodes.py)

## References

Research was initially checked on September 22, 2026 and updated with Apple's official group-lab summary on September 24, 2026. The skill rechecks documentation against the SDK in use. Exact API declarations take precedence over broad wording in summaries.

### Apple overview and design guidance

- [Get ready for iPhone Duo](https://developer.apple.com/iphone-duo/)
- [Preparing your app for iPhone Duo](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)
- [Designing for iPhone Duo — Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)

### All six iPhone Duo Tech Talks

- [Design for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111466/)
- [Prepare your app for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111461/)
- [Raise the bar with iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111462/)
- [Strike a pose with adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/)
- [Leverage multiple displays and scenes on iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111464/)
- [Build a great camera experience for iPhone Duo](https://developer.apple.com/videos/play/tech-talks/111465/)

### Group lab

- [Official Apple DTS summary of the iPhone Duo Group Lab](https://developer.apple.com/forums/thread/847644) — preferred lab summary.
- [Community consolidated group-lab Q&A](https://gist.github.com/frankschlegel/6356a059426b2393528691822edfdae6) — secondary, transcript-derived context; not the authority for availability.

### Toolchain, lifecycle, and compatibility

- [Xcode support and system requirements](https://developer.apple.com/xcode/system-requirements)
- [Xcode 27.1 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)
- [UIKit updates](https://developer.apple.com/documentation/updates/uikit)
- [TN3192: Migrating from UIRequiresFullScreen](https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key)
- [TN3208: Launch-screen requirements](https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements)
- [Restoring your app's state](https://developer.apple.com/documentation/uikit/restoring-your-app-s-state)
- Apple's Xcode **App Resizability** skill — baseline migration patterns for screen geometry, orientation, scene lifecycle, safe areas, and idiom. Consult the installed skill when available; it is not bundled here.

### Navigation, layout, and specialized APIs

- [UINavigationItem](https://developer.apple.com/documentation/uikit/uinavigationitem)
- [Interactive pop gesture recognizer](https://developer.apple.com/documentation/uikit/uinavigationcontroller/interactivepopgesturerecognizer)
- [ToolbarOverflowMenu](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu)
- [Toolbar item visibility priority](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:))
- [Toolbar item axis behavior](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:))
- [SwiftUI preferred vertical toolbar edge](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge)
- [UIKit preferred vertical bar edge](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge)
- [ArrangementView](https://developer.apple.com/documentation/swiftui/arrangementview)
- [UIArrangementViewController](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller)
- [UIView.ReservedRegion](https://developer.apple.com/documentation/uikit/uiview/reservedregion)
- [Registering a camera capture accessory](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo)
- [Core Motion deviceMotionBody](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody)
- [UIView sensor coordinate orientation](https://developer.apple.com/documentation/uikit/uiview#Sensor-coordinate-orientation)
- [WebKit Viewport Segments discussion](https://github.com/WebKit/standards-positions/issues/327)
- [WebKit Device Posture discussion](https://github.com/WebKit/standards-positions/issues/328)

See the [source ledger](skills/ios-resizability-duo/references/sources.md) for how these references inform the skill and how conflicting or superseded guidance is handled.

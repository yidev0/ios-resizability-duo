# Toolchains and availability

Read this before selecting APIs or an implementation plan. Baseline facts were checked on **2026-09-22**; 27.1 was presented as beta. Future 27.1+ releases can change details. Resolve each API against the exact installed SDK and release notes, not the family label alone.

## Inventory and evidence

Use `scripts/inspect_xcodes.py`. It emits JSON to stdout and preserves failures as evidence. It searches only `/Applications/Xcode*.app`, the existing command-line selection/override, and explicit additional paths; it does not claim an exhaustive disk search. An empty result can mean command-line tools only, custom installation, or unavailable access.

Equivalent focused checks:

```sh
xcode-select -p
xcodebuild -version
xcodebuild -showsdks
xcrun --sdk iphoneos --show-sdk-version
xcrun --sdk iphonesimulator --show-sdk-version
xcrun simctl list runtimes --json
xcrun simctl list devicetypes --json
```

For another installed Xcode, prefix each command with `DEVELOPER_DIR='/Applications/Xcode-beta.app/Contents/Developer'` using the discovered path. Do not change the global selection. The executable environment override can differ from `xcode-select -p`.

Read project/target/xcconfig and CI configuration for `SDKROOT`, `IPHONEOS_DEPLOYMENT_TARGET`, supported platforms, and explicit Xcode pins. When needed, resolve build settings for the actual scheme/configuration with `xcodebuild -showBuildSettings -json`; avoid dependency updates, preserve lockfiles, and use scratch build outputs. After a build, inspect the produced Info.plist to confirm generated/merged keys. Do not infer effective settings from a single pbxproj match. License, missing SDK, and package-resolution errors are blockers to record, not prompts to install or accept terms automatically.

## Capability matrix

The **linked SDK** controls compatibility behavior; the app can have an older deployment target and run on newer iOS. Xcode versions below are the normal SDK pairing, not interchangeable with runtime versions.

| Main build toolchain | Implement now | Duo behavior and remaining work |
| --- | --- | --- |
| Xcode 26.x / iOS 26.x SDK | Scene lifecycle, local geometry, flexible layouts, asymmetric safe areas, state continuity, system navigation, and APIs present in that exact SDK. | Pre-27 builds use a familiar phone-sized compatibility presentation on the inner display. Modernizing source alone does not opt the binary into 27 SDK behavior. Do not introduce 27-only symbols. |
| Xcode 27.0 / iOS 27.0 SDK | Complete the resizable iPhone baseline; use verified 27.0 APIs such as toolbar overflow and item visibility priorities. | Uses the larger inner display up to the status-bar area. It does **not** get the complete 27.1 edge-to-edge/vertical-bar experience merely by running on 27.1. Keep 27.1 APIs out of ordinary source compiled with 27.0. |
| Xcode 27.1+ / iOS 27.1+ SDK | Baseline plus full-display adaptation and verified vertical-bar, arrangement, reserved-region, and related capabilities as relevant. | Linking the 27.1 SDK enables full display space and system vertical navigation/toolbar behavior. Test on an installed compatible Duo simulator/runtime or hardware. Feature availability still depends on runtime and context. |

Compatibility presentation: [Prepare your app for iPhone Duo, 0:30–1:33](https://developer.apple.com/videos/play/tech-talks/111461/).

### A 27.0-SDK binary running on Duo

Treat this as a supported evaluation path, even when the device runs 27.1 or later. The runtime version and installed Xcode do not change which SDK the existing app binary was linked against.

- Expect the 27.0 inner-display presentation described above. Do not flag the status-bar-side boundary or absence of the 27.1 vertical-bar experience as an app defect by itself.
- Still audit real resizing defects: fixed screen dimensions, clipped controls, stale geometry, incorrect safe areas, lost navigation/editing state, and custom components that fail within the space the system supplies. Opening/closing the phone is not exempt from the resizing audit. Check the full-screen/discrete-resizing configuration in [implementation.md](implementation.md).
- Separate **27.0 correctness** from **27.1 adoption work**. A bespoke tab selector may resize correctly today yet need replacement or custom work to match the later system side-region behavior. Report both facts; don't imply that adding a 27.1 runtime guard or fixing its constraints opts a 27.0-linked binary into the new presentation.
- When tooling supports it, test the actual 27.0-SDK artifact on Duo separately from an exploratory 27.1-SDK rebuild. Record the build SDK for each artifact and runtime for each run. A successful 27.1 rebuild is not verification of the shipped 27.0 binary. If installation/runtime compatibility prevents the first test, mark that exact test not run.

These distinctions apply to SwiftUI and UIKit. System-container migration can be useful on the main 27.0 toolchain without promising the visual behavior of a 27.1-linked build.

### Verified examples that prevent a common version mistake

| API | Minimum iOS SDK/runtime declaration | Source |
| --- | --- | --- |
| `ToolbarContent.visibilityPriority(_:)` | 27.0 | [Apple declaration](https://developer.apple.com/documentation/swiftui/toolbarcontent/visibilitypriority(_:)) |
| `ToolbarOverflowMenu` | 27.0 | [Apple declaration](https://developer.apple.com/documentation/swiftui/toolbaroverflowmenu) |
| `ToolbarContent.axisBehavior(_:)` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/swiftui/toolbarcontent/axisbehavior(_:)) |
| `EnvironmentValues.toolbarVerticalEdge` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/swiftui/environmentvalues/toolbarverticaledge) |
| `ArrangementView` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/swiftui/arrangementview) |
| `UIArrangementViewController` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/uikit/uiarrangementviewcontroller) |
| `UITraitCollection.verticalBarEdge` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/uikit/uitraitcollection/verticalbaredge) |
| `UIView.ReservedRegion` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/uikit/uiview/reservedregion) |
| `EnvironmentValues.splitArrangementAxis` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/swiftui/environmentvalues/splitarrangementaxis); an axis value is not proof both children are visible. |
| `UITabBarController.Sidebar.preferredPlacement` | 27.0 | [Apple declaration](https://developer.apple.com/documentation/uikit/uitabbarcontroller/sidebar-swift.class/preferredplacement) |
| `UISheetPresentationController.preferredPlacement` | 27.0 | [Apple declaration](https://developer.apple.com/documentation/uikit/uisheetpresentationcontroller/preferredplacement) |
| `UIBarButtonItem.axisBehavior` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/uikit/uibarbuttonitem/axisbehavior-swift.enum) |
| `UIView.LayoutRegion.bar(onEdge:extent:)` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/uikit/uiview/layoutregion) |
| `AVCaptureDeviceDirectionCoordinator` | 27.1 | [Apple declaration](https://developer.apple.com/documentation/avkit/avcapturedevicedirectioncoordinator/init%28view%3Adevicetypes%3Achangehandler%3A%29) |
| `AVCaptureDevice.DiscoverySession.supportedMultiCamDeviceSets` | 13.0 | [Apple declaration](https://developer.apple.com/documentation/avfoundation/avcapturedevice/discoverysession/supportedmulticamdevicesets); preexisting discovery API. |
| `CMMotionManager.deviceMotionBody` | 27.0 | [Apple declaration](https://developer.apple.com/documentation/coremotion/cmmotionmanager/devicemotionbody) |

This is a verified subset, not blanket availability for each framework. The new UIKit/AVKit/AVFoundation rows were checked against locally installed iOS 27.0 and 27.1 SDK headers on 2026-09-24; confirm SwiftUI and later beta declarations in the active SDK before coding. Check any unlisted counterparts independently. Never assume everything discussed in a Duo talk is new in 27.1, or that everything called “iOS 27” shipped in 27.0. The official lab summary also explicitly excludes `ArrangementView` and `UIArrangementViewController` from 27.0; broad “iOS 27” wording elsewhere in that thread does not override the declarations.

## Compile-time and runtime are separate gates

1. Does the **main SDK** declare the symbol and signature? Inspect its headers/Swift interface or matching Apple documentation.
2. Does the **deployment range** include older runtimes? Isolate newer types in availability-annotated declarations and guard calls with the exact runtime version; retain a functional fallback.
3. Does the **current device/context** provide the capability? Handle absent hinge/reserved region/accessory and rejected scene activation.

`if #available(iOS 27.1, *)` does not solve an unknown symbol in an iOS 27.0 SDK. A Swift compiler-version test is not an SDK-version test; `canImport(SwiftUI)` proves only that the module exists. Prefer a baseline without new symbols. If a shared source tree truly must build in multiple Xcodes, use verified SDK-specific source inclusion or an explicit build flag, and build both paths. For Objective-C, guard SDK declarations and runtime use separately with the appropriate verified macros and availability checks.

With main Xcode 27.0 and side-installed 27.1, maintain the 27.0 build, perform isolated testing with per-command `DEVELOPER_DIR`, and label that result precisely. Do not imply a 27.0-SDK build gained full 27.1 behavior from that test. Where supported, testing the existing binary on a newer runtime can assess compatibility separately from rebuilding it with the new SDK. Missing runtime/device type is an unperformed Duo test, not evidence of a layout defect.

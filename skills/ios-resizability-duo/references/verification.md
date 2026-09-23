# Verification and reporting

Use synthetic data and authorized targets. In evaluation mode, prefer static analysis and existing artifacts. Builds/tests may use scratch outputs if consistent with the request; do not run project scripts that would alter source/configuration or resolve/update dependencies. If this cannot be ensured, report the static finding and the proposed verification. Follow any required permission step for personal data or real-screen captures; simulators/emulators are exempt where the user's instructions say so.

## Build evidence

Record exact developer directory, Xcode build version, SDK, scheme/target/configuration, destination/runtime, and command outcome. Use the main toolchain first. Build the supported deployment range and relevant framework targets; a run on a new OS does not check old-OS fallback. Compile every intentionally maintained SDK-specific source path. Use per-command `DEVELOPER_DIR` for another Xcode.

Check the built Info.plist, scene entry, and launch-screen configuration. Preserve baseline diagnostics, distinguish new failures, and keep logs in an accessible artifact location. No need to add a test for every text replacement: test stateful transitions, routing, and behavior that could regress.

## Runtime scenarios

Prioritize each affected user journey; keep a matrix of scenario, destination, expected behavior, observed result, and status (`passed`, `failed`, `not run`, `not applicable`).

| Scenario | Evidence to collect |
| --- | --- |
| Regular iPhone and minimum supported OS | Existing navigation/actions and compatibility fallbacks still work. |
| 27.0-SDK artifact running on Duo, when supported | Verify the artifact's linked SDK and actual runtime. Assess its expected 27.0 presentation and real resizing/state defects; do not fail it solely for lacking 27.1 full-display/vertical bars. Keep an exploratory 27.1-SDK rebuild as a separate result. |
| Resize continuously, including same-size-class changes | Layout tracks bounds; no clipping, constraint conflicts, stale scale/images, or expensive per-frame rebuilds. |
| Compact → regular → compact during use | Selected item, navigation path, scroll position, unsaved draft, focus, and playback survive. |
| Fold during a stateful flow | The scene and state owners continue in place; no root recreation, duplicate request/transaction, or playback restart. Separately test genuine disconnect/reconnect restoration. Do not infer transaction correctness from visual continuity alone. |
| Hybrid UIKit/SwiftUI and trait overrides | Bounds, safe areas, and inherited traits reach both sides of hosting/representable boundaries. Any retained override is scoped and justified; removing it restores inheritance. Test same-size-class resizing too. |
| Duo outer/inner, portrait/landscape, flat/partially folded; repeat transitions | Content and controls stay reachable; sheets/popovers and custom chrome adapt without root-state reset. |
| Duo Split View on left and right; supported pinned PiP | All four safe-area edges update correctly; width AND height changes work. |
| Keyboard open/close and text editing while resizing | Input remains visible, no doubled inset, no lost draft/focus. |
| Short bar space, status/Live Activity changes, overflow | Back/Close and critical actions remain accessible; overflow has meaningful labels and no duplicate actions. |
| Dialog launched from toolbar overflow | A stable presenter survives moving the action into/out of overflow; invocation, cancellation, and confirmation still work after resizing. |
| Custom-navigation migration | No duplicate title/back controls or empty system action region caused by unwired navigation items. Verify original actions, custom appearance, completed/cancelled interactive pop, modal dismissal ownership, restoration, and split-column collapse/expansion. |
| Bespoke tab bars and other custom control systems | Identify missing side placement, overflow/compression, fold or safe-area behavior even without system bar classes. After migration, verify selected tab, independent per-tab stacks/state, badges, reselection, deep links and restoration. Retained custom UI needs explicit implementation and testing of its relevant adaptation gaps. |
| Intentionally retained content controls | Explicit local/safe-area/fold adaptation, keyboard clearance, usable targets, RTL and accessibility are checked; retaining a content control does not implicitly waive these checks. |
| Dynamic Type, VoiceOver, RTL, Reduce Motion/Transparency | Reading order and focus remain meaningful; labels fit; controls remain legible and operable. |
| Multi-scene, if supported | Shared preferences remain shared, while each window's selection, draft and navigation remain independent. Reconnection/restoration and URL routes choose the intended scene; activation failures handled. Folding alone does not require enabling multiple instances. |
| Custom sheet or controls across an active fold | Test division activation/deactivation, local region coordinates, occlusion hit testing, and margins without double padding; edge safe-area checks alone are insufficient. |
| Camera/accessory/hinge feature, if implemented | Capability loss handled; fallback works; actual hardware checks distinguished from simulator evidence. |

Inspect screenshots only where appropriate and permitted; screenshots alone do not prove interactive state continuity. Keep a short before/after reproduction for defects. Do not delete an installed app to test a launch screen unless its data is disposable or deletion is authorized; use a fresh simulator/install when possible.

## If Duo tooling is unavailable

Use available iPad resizing, previews, and suitable iPhone Mirroring configurations to exercise general layout. iPhone Mirroring interacts with a real personal device; obtain required permission first. Those checks do not verify fold transitions, vertical bars, reserved-region geometry, camera behavior, or exact Duo compatibility presentation. Record each as not run and provide the next concrete test when Xcode 27.1+ and a compatible runtime become available. Do not install/switch Xcode to erase this limitation.

Xcode/runtime availability, simulator device type, and beta limitations are independent checks. Read the exact installed release's [release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes) before diagnosing a simulator failure as an app bug. Do not copy an old beta limitation into a permanent claim about Duo.

## Report structure

Use a concise table where it helps comparison:

`Finding | File/line and evidence | User impact | Supported fix | SDK/runtime | Status`

Separate **implemented and tested**, **implemented but unverified**, **requires newer SDK**, **needs user decision**, and **optional suggestion**. Include the per-file coverage ledger if the audit is large. Summarize why retained matches are correct. Provide links to patches/reports and meaningful logs so the user can review the result.

“Full implementation” means all agreed applicable fixes have been completed. If a required scene route, supported-Xcode build, or runtime check is blocked, say what remains; don't relabel it as an optional future enhancement merely to report success.

---
name: ios-resizability-duo
description: Evaluate or implement iOS app resizability and iPhone Duo readiness in SwiftUI, UIKit, Swift, and Objective-C, using the project's actual Xcode and SDK versions. Use for whole-app readiness, custom controls that lack Duo adaptation, adaptive bars, folding transitions, or a staged Xcode 26.x/27.0/27.1+ adoption plan.
---

# iOS Resizability and iPhone Duo

Prepare one continuous app experience across changing window sizes and Duo displays. Evaluate existing code or carry the supported implementation through build and runtime verification. Keep the team's main Xcode usable; a newer installed beta is not permission to migrate.

## Choose the mode first

Ask: **“Do you want an evaluation of the current code, or an evaluation followed by full implementation?”** Offer those two choices. If the user already explicitly chose one in this session, honor it without asking again. While awaiting a choice, only inspect the authorized project and toolchain; do not edit app code or configuration. No reply does not authorize implementation.

- **Evaluation:** Report findings and a concrete, version-compatible implementation plan. Do not edit source, project settings, manifests, dependencies, or insert TODOs. A report in the agreed output location is allowed. Describe suggested patches rather than applying them.
- **Evaluation and full implementation:** Evaluate, then complete all applicable readiness fixes supported by the agreed main toolchain, including layout, navigation, scene integration, and configuration. Carry straightforward decisions forward autonomously. Ask only for missing product decisions or genuinely risky changes outside the existing authorization. Optional new Duo features remain suggestions unless requested. Explicitly separate unavailable-toolchain work and unperformed verification from completed work.

Follow project privacy instructions. Before accessing personal app data or capturing a real device/desktop screen, explain the exact data or surface and purpose and obtain any required permission. Prefer synthetic fixtures and simulators. Do not inspect the user's desktop merely to identify Xcode.

## Establish the actual toolchain

Read [toolchains.md](references/toolchains.md) before making version-dependent recommendations. Run the bundled read-only inventory, or equivalent commands:

```sh
python3 <skill-directory>/scripts/inspect_xcodes.py
```

The script checks the command-line selection, an existing `DEVELOPER_DIR`, Xcode bundles in `/Applications`, SDKs, and simulator runtimes/types. It does not select Xcode, install components, boot simulators, or inspect device contents. Pass `--developer-dir '/path/to/Xcode.app'` for a known custom installation. If local access is unavailable, request the small set of version outputs in the reference; don't invent installed versions.

Record **main development/CI Xcode**, **effective command-line Xcode**, **other installed Xcodes**, **build SDK**, **deployment target**, and **runtime/test destination** separately. CLI selection is evidence, not proof of the team's main Xcode. If there are competing installations or CI requirements, clarify which must remain buildable before adding newer API references. Continue compatible analysis meanwhile. Never run `xcode-select --switch` or update the deployment target as a shortcut.

Check Apple's current documentation against that SDK. Use availability metadata and local SDK declarations for exact signatures, not just a video saying “latest.” Runtime `#available` cannot make an older SDK recognize a new symbol. Consult the dated source ledger in [sources.md](references/sources.md); recheck beta APIs when applying them.

The source ledger includes Apple's official group-lab summary and linked API clarifications. Use it ahead of the unofficial transcript summary, while preserving exact SDK declarations when a lab answer uses broad version or behavior shorthand.

## Evaluate the project

1. Establish authorized targets, languages/frameworks, entry points, supported OS versions, build configurations, existing tests, and user journeys. Use the current request and session to understand product features. For file-only requests, stay within those files and mark project-level checks unavailable.
2. Read [implementation.md](references/implementation.md). Audit every applicable category: screen assumptions; orientation; scene lifecycle; safe areas/keyboard; idiom; SwiftUI state continuity; navigation/bars; **custom controls and containers that don't inherit Duo adaptation**; presentations; and custom layouts. Search results are candidates, not proof of defects. Read [custom-navigation.md](references/custom-navigation.md) for custom tab bars, toolbars, navigation chrome, overlays, and other control systems—even when built entirely from generic views/buttons. Title and Back controls are examples, not the audit boundary.
3. Inspect effective launch-screen, scene, orientation, and full-screen configuration. Resolve generated Info.plist settings, target/configuration overrides, and xcconfig inheritance rather than assuming a key absent from one file is absent from the app. Keep discovery read-only.
4. Read [duo-experience.md](references/duo-experience.md) when evaluating Duo navigation, controls, regions, camera/AR behavior, or product opportunities. Identify broken existing functionality separately from optional enhancements.
5. Track each candidate file/site with its intent, evidence, impact, proposed change, minimum SDK/runtime, and status: issue, already correct, intentionally retained, fixed, or blocked with reason. Every audited file needs an outcome, not a forced diff.

If the installed **app-resizability** skill is available, read its relevant task references for additional mechanical migration patterns (UIScreen, orientation, scene lifecycle, safe area, idiom). This skill remains usable without that installation. Do not copy its blanket mutation requirements into evaluation mode. For this whole-app workflow, necessary edits to callers, state owners, manifests, and navigation containers are in scope; a “target API line only” rule must not leave a partial migration. Prefer current Apple evidence over stale reference claims, especially for `UIRequiresFullScreen`.

## Implement and verify

In implementation mode, first state a short plan that groups work into **supported now**, **27.1+ additions**, and **optional product improvements**. Review it against the main toolchain before editing. Do not stop after supplying that plan.

Apply changes in coherent units, preserving unrelated behavior, deployment support, navigation state, and public contracts. Pair cached geometry/trait replacements with reactive updates. Keep intentional full-bleed backgrounds; fix controls that become inaccessible. Do not turn an adaptive-layout task into a UIKit-to-SwiftUI rewrite.

When the main Xcode lacks a required symbol, implement the compatible baseline and document the later enhancement. Add conditional compilation only if the project deliberately supports multiple SDKs and the guard is verified with both builds. Do not leave uncompilable 27.1 symbols under runtime-only guards in a 26.x/27.0 project.

Use [verification.md](references/verification.md) for build and interaction checks. Reconcile the findings ledger with changes and explicit retained/blocked cases. Check main-toolchain compilation before optional secondary-toolchain testing. A successful build or iPad test alone does not establish Duo readiness.

## Deliver an accessible result

Provide a linked report or a concise inline report with:

- Selected mode, project scope, exact toolchains/SDKs/deployment target, and evidence date.
- Findings with clickable file/line references, impact, and fix or decision; distinguish defects from hypotheses.
- A clear 26.x / 27.0 / 27.1+ split: what works now, what awaits a newer SDK, and the retained fallback.
- Changes made (implementation mode), tests actually performed, outcomes, and exact blocked checks.
- App-specific Duo opportunities tied to features found in this session/code, expected user benefit, version/capability needs, fallback, and effort. “No compelling feature-specific enhancement” is a valid conclusion.

Never claim full implementation or verified Duo support while required work or device-specific checks remain blocked. Explain the remaining boundary without insisting that the user upgrade their main Xcode.

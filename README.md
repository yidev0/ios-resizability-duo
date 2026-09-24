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

## License

MIT. See [LICENSE](LICENSE).

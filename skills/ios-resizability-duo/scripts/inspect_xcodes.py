#!/usr/bin/env python3
"""Read-only, bounded Xcode/SDK inventory. Does not inspect personal devices."""

import argparse
import glob
import json
import os
from pathlib import Path
import plistlib
import subprocess


def run(argv, env):
    try:
        result = subprocess.run(argv, env=env, capture_output=True, text=True,
                                timeout=45, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"command": argv, "ok": False, "error": str(error)}
    record = {"command": argv, "ok": result.returncode == 0,
              "returncode": result.returncode}
    output = result.stdout.strip()
    if output:
        try:
            record["data"] = json.loads(output)
        except ValueError:
            record["output"] = output[:6000]
    if result.stderr.strip():
        record["stderr"] = result.stderr.strip()[:2000]
    return record


def developer_path(path):
    candidate = Path(path).expanduser()
    if candidate.suffix == ".app":
        candidate = candidate / "Contents" / "Developer"
    return str(candidate.resolve())


def bundle_version(developer_dir):
    info = Path(developer_dir).parent / "Info.plist"
    try:
        with info.open("rb") as stream:
            values = plistlib.load(stream)
        return {key: values[key] for key in
                ("CFBundleShortVersionString", "CFBundleVersion") if key in values}
    except (OSError, ValueError, plistlib.InvalidFileException):
        return {}


def inspect(extra_paths=()):
    env = os.environ.copy()
    selection_env = env.copy()
    selection_env.pop("DEVELOPER_DIR", None)
    selection = run(["/usr/bin/xcode-select", "-p"], selection_env)
    selected_path = selection.get("output") if selection.get("ok") else None
    override = env.get("DEVELOPER_DIR")
    candidates = []
    for value in [override, selected_path, *sorted(glob.glob("/Applications/Xcode*.app")),
                  *extra_paths]:
        if value:
            resolved = developer_path(value)
            if resolved not in candidates:
                candidates.append(resolved)
    effective = developer_path(override or selected_path) if (override or selected_path) else None
    records = []
    commands = [
        ["/usr/bin/xcodebuild", "-version"],
        ["/usr/bin/xcodebuild", "-showsdks"],
        ["/usr/bin/xcrun", "--sdk", "iphoneos", "--show-sdk-version"],
        ["/usr/bin/xcrun", "--sdk", "iphonesimulator", "--show-sdk-version"],
        ["/usr/bin/xcrun", "simctl", "list", "runtimes", "--json"],
        ["/usr/bin/xcrun", "simctl", "list", "devicetypes", "--json"],
    ]
    for directory in candidates:
        entry = {"developer_dir": directory, "effective_cli_selection": directory == effective,
                 "exists": Path(directory).is_dir(), "bundle_version": bundle_version(directory)}
        if entry["exists"]:
            scoped_env = dict(env, DEVELOPER_DIR=directory)
            entry["checks"] = [run(command, scoped_env) for command in commands]
        else:
            entry["checks"] = []
            entry["error"] = "Developer directory does not exist; not queried."
        records.append(entry)
    return {"xcode_select": selection, "developer_dir_override": override,
            "effective_cli_developer_dir": effective,
            "main_team_xcode": "Not inferred: confirm against project/CI/user context.",
            "search_scope": "/Applications/Xcode*.app, CLI selection/override, explicit paths only",
            "toolchains": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--developer-dir", action="append", default=[],
                        help="Also inspect this Xcode.app or Contents/Developer directory; repeatable.")
    args = parser.parse_args()
    print(json.dumps(inspect(args.developer_dir), indent=2))


if __name__ == "__main__":
    main()

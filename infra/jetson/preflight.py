#!/usr/bin/env python3
"""Read-only JetPack / Axiom native-office deployment preflight.

Supports Python 3.6+ (including the legacy JetPack 4 system Python).
This reports observable host facts, not a compatibility certification.
"""
from __future__ import print_function
import argparse
import json
import os
import platform
import shutil
import sys

def _read(path):
    try:
        with open(path, "r") as handle:
            return handle.read().strip()
    except (IOError, OSError, UnicodeError):
        return ""

def _os_release():
    values = {}
    for line in _read("/etc/os-release").splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values

def _ram_mib():
    for line in _read("/proc/meminfo").splitlines():
        if line.startswith("MemTotal:"):
            try:
                return round(int(line.split()[1]) / 1024, 1)
            except (IndexError, ValueError):
                return None
    return None

def _family(model):
    lower = model.lower()
    if "jetson nano" in lower:
        return "jetson_nano"
    if "jetson" in lower or "orin" in lower or "tegra" in lower:
        return "jetson_other"
    return "unidentified"

def preflight():
    release = _os_release()
    model = _read("/proc/device-tree/model").replace("\x00", "")
    tegra = _read("/etc/nv_tegra_release").splitlines()
    family = _family(model)
    report = {
        "schema": "jerp.jetpack.office_preflight.v1",
        "system": release.get("PRETTY_NAME", platform.platform()),
        "architecture": platform.machine(),
        "board_model": model or "not_detected",
        "board_family": family,
        "l4t_release": tegra[0] if tegra else "not_detected",
        "memory_mib": _ram_mib(),
        "python": platform.python_version(),
        "office": {
            "libreoffice": shutil.which("libreoffice"),
            "soffice": shutil.which("soffice"),
            "xdg_open": shutil.which("xdg-open"),
        },
        "browser": {
            "chromium": shutil.which("chromium") or shutil.which("chromium-browser"),
            "firefox": shutil.which("firefox"),
        },
        "compatible_verified": False,
        "installed_or_changed_anything": False,
        "next_action": "Verify native office compatibility, workbook fidelity and Axiom runtime on this exact board before deployment.",
    }
    notes = []
    if family == "jetson_nano":
        notes.append("Original Jetson Nano targets the legacy final JetPack 4.6.6; it does not support JetPack 5/6 officially.")
    if platform.machine().lower() not in ("aarch64", "arm64"):
        notes.append("Host is not ARM64; this is not Jetson acceptance evidence.")
    if not (report["office"]["libreoffice"] or report["office"]["soffice"]):
        notes.append("No native LibreOffice command detected on PATH; package availability must be checked for this distro.")
    report["notes"] = notes
    return report

def main():
    parser = argparse.ArgumentParser(description="Read-only JERP JetPack native-office preflight")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    result = preflight()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("JERP / Axiom JetPack native-office preflight")
        print("OS:", result["system"])
        print("CPU:", result["architecture"])
        print("Board:", result["board_model"])
        print("L4T:", result["l4t_release"])
        print("RAM MiB:", result["memory_mib"])
        print("Python:", result["python"])
        for name, command in sorted(result["office"].items()):
            print("Editor/helper {}: {}".format(name, command or "not detected"))
        print("Compatibility confirmed: NO (requires real workbook and Axiom tests)")
        for note in result["notes"]:
            print("Note:", note)
    return 0

if __name__ == "__main__":
    sys.exit(main())

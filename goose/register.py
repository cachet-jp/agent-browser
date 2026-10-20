"""Register (or refresh) the agent-browser stdio extension in goose's config.yaml.

Usage: python3 register.py <config.yaml> <launcher path>

Edits the file textually so it needs no YAML library and leaves the rest of the
config untouched. A timestamped backup is written next to the config first.
"""
import json
import shutil
import sys
import time
from pathlib import Path

KEY = "agent-browser"


def block(launcher: str) -> list[str]:
    return [
        f"  {KEY}:\n",
        "    enabled: true\n",
        "    type: stdio\n",
        f"    name: {KEY}\n",
        f"    cmd: {json.dumps(launcher)}\n",  # JSON strings are valid YAML scalars
        "    args: []\n",
        "    envs: {}\n",
        "    env_keys: []\n",
        "    timeout: 300\n",
        "    description: Browser automation via agent-browser (navigate, snapshot, click, fill, screenshot)\n",
        "    bundled: false\n",
    ]


def main() -> None:
    config, launcher = Path(sys.argv[1]), sys.argv[2]
    lines = config.read_text().splitlines(keepends=True) if config.exists() else []

    try:
        ext = lines.index("extensions:\n")
    except ValueError:
        lines += ["extensions:\n"]
        ext = len(lines) - 1

    # Locate an existing entry inside the extensions mapping.
    start = end = None
    for i in range(ext + 1, len(lines)):
        line = lines[i]
        if line.strip() and not line.startswith(" "):
            break  # left the extensions mapping
        if start is None and line == f"  {KEY}:\n":
            start = i
        elif start is not None and line.startswith("  ") and not line.startswith("   "):
            end = i
            break
    if start is not None and end is None:
        end = i if lines[i].strip() and not lines[i].startswith(" ") else len(lines)

    if config.exists():
        backup = config.with_name(f"{config.name}.bak-agent-browser-{time.strftime('%Y%m%d-%H%M%S')}")
        shutil.copy2(config, backup)
        print(f"backup: {backup}")

    if start is None:
        lines[ext + 1:ext + 1] = block(launcher)
        print(f"added extension '{KEY}' to {config}")
    else:
        lines[start:end] = block(launcher)
        print(f"updated extension '{KEY}' in {config}")
    config.write_text("".join(lines))


if __name__ == "__main__":
    main()

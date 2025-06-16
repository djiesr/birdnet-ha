#!/usr/bin/env python3
"""Update manifest version."""
import argparse
import json
import sys
from pathlib import Path


def update_manifest(version: str) -> None:
    """Update manifest version."""
    manifest_path = Path("custom_components/birdnet-pi/manifest.json")
    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found")
        sys.exit(1)

    with open(manifest_path) as manifest_file:
        manifest = json.load(manifest_file)

    manifest["version"] = version

    with open(manifest_path, "w") as manifest_file:
        json.dump(manifest, manifest_file, indent=4)
        manifest_file.write("\n")


def main() -> None:
    """Run the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    update_manifest(args.version)


if __name__ == "__main__":
    main() 
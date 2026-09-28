"""Check that all five segmentation packages can be imported."""

from __future__ import annotations

import importlib
import sys


PACKAGES = ("streamlit", "jieba", "hanlp", "ltp", "pkuseg", "thulac")


def main() -> int:
    failed: list[tuple[str, str]] = []
    for package in PACKAGES:
        try:
            importlib.import_module(package)
            print(f"[OK] {package}")
        except Exception as exc:
            failed.append((package, str(exc)))
            print(f"[FAILED] {package}: {exc}")

    if failed:
        print("\nOne or more packages could not be imported.")
        return 1

    print("\nAll five segmentation packages are available.")
    print("HanLP and LTP may download their model files the first time they run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())


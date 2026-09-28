"""Plain-text export helpers for segmentation results."""

from __future__ import annotations

import re

from segmenters.base import Token


def segmented_text(tokens: list[Token]) -> str:
    """Format tokens with visible boundaries while preserving source whitespace."""
    parts: list[str] = []
    needs_separator = False
    for token in tokens:
        if token.text.isspace():
            parts.append(token.text)
            needs_separator = False
            continue
        if needs_separator:
            parts.append(" / ")
        parts.append(token.text)
        needs_separator = True
    return "".join(parts) + ("\n" if parts else "")


def export_filename(tool_name: str) -> str:
    """Return a stable, filesystem-friendly filename for a tool result."""
    slug = re.sub(r"[^a-z0-9]+", "-", tool_name.casefold()).strip("-")
    return f"segmented-{slug or 'result'}.txt"


def comparison_report(
    source_text: str,
    results: dict[str, tuple[list[Token], dict[str, str]]],
    disputed_boundaries: set[int],
) -> str:
    """Create a reproducible plain-text report for a multi-tool comparison."""
    lines = [
        "Chinese Word Segmentation Comparison",
        "",
        "Original text:",
        source_text,
        "",
        "Successful tools: " + ", ".join(results),
        "Disputed character boundaries: "
        + (", ".join(str(offset) for offset in sorted(disputed_boundaries)) or "None"),
    ]

    for name, (tokens, metadata) in results.items():
        lines.extend(
            [
                "",
                f"[{name}]",
                f"Package version: {metadata['package_version']}",
                f"Model: {metadata['model']}",
                f"Settings: {metadata['settings']}",
                "Segmentation:",
                segmented_text(tokens).rstrip("\n"),
            ]
        )

    return "\n".join(lines) + "\n"

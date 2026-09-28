"""Input validation shared by the Streamlit form and portable tests."""

from __future__ import annotations


def request_error(text: str, mode: str, selected_tools: list[str]) -> str | None:
    if not text.strip():
        return "Enter some text before running segmentation."
    if mode == "Compare tools" and len(selected_tools) < 2:
        return "Select at least two tools to compare."
    if mode == "Use one tool" and len(selected_tools) != 1:
        return "Select exactly one tool."
    return None

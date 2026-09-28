import pytest

from comparison.validation import request_error


@pytest.mark.parametrize(
    ("mode", "tools"),
    [
        ("Use one tool", ["Jieba"]),
        ("Compare tools", ["Jieba", "HanLP"]),
        ("Compare tools", ["Jieba", "LTP", "pkuseg"]),
        ("Compare tools", ["Jieba", "HanLP", "LTP", "pkuseg", "THULAC"]),
    ],
)
def test_valid_single_and_comparison_tool_counts(mode, tools):
    assert request_error("北京大学。", mode, tools) is None


@pytest.mark.parametrize("text", ["", "  \n\t  "])
def test_empty_input_is_rejected(text):
    assert request_error(text, "Use one tool", ["Jieba"]) == "Enter some text before running segmentation."


def test_comparison_requires_two_tools():
    assert request_error("。", "Compare tools", ["Jieba"]) == "Select at least two tools to compare."


def test_short_punctuation_and_multiline_input_are_valid():
    assert request_error("。", "Use one tool", ["Jieba"]) is None
    assert request_error("北京大学。\n人工智能。", "Compare tools", ["Jieba", "THULAC"]) is None


def test_single_tool_mode_rejects_multiple_tools():
    assert request_error("人工智能", "Use one tool", ["Jieba", "HanLP"]) == "Select exactly one tool."

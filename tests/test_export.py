from comparison.export import comparison_report, export_filename, segmented_text
from segmenters.base import Token


def test_segmented_text_uses_visible_word_boundaries():
    tokens = [Token("我们", 0, 2), Token("今天", 2, 4), Token("。", 4, 5)]
    assert segmented_text(tokens) == "我们 / 今天 / 。\n"


def test_segmented_text_preserves_multiline_whitespace():
    tokens = [
        Token("北京大学", 0, 4),
        Token("\n", 4, 5),
        Token("人工智能", 5, 9),
        Token("。", 9, 10),
    ]
    assert segmented_text(tokens) == "北京大学\n人工智能 / 。\n"


def test_empty_result_exports_empty_text():
    assert segmented_text([]) == ""


def test_export_filename_is_tool_specific_and_safe():
    assert export_filename("Jieba") == "segmented-jieba.txt"
    assert export_filename("pkuseg") == "segmented-pkuseg.txt"
    assert export_filename("Tool / custom") == "segmented-tool-custom.txt"


def test_comparison_report_includes_source_metadata_results_and_differences():
    metadata = {
        "package_version": "1.2.3",
        "model": "test model",
        "settings": "deterministic",
    }
    report = comparison_report(
        "北京大学。",
        {
            "Tool A": ([Token("北京大学", 0, 4), Token("。", 4, 5)], metadata),
            "Tool B": ([Token("北京", 0, 2), Token("大学", 2, 4), Token("。", 4, 5)], metadata),
        },
        {2},
    )

    assert "Original text:\n北京大学。" in report
    assert "Successful tools: Tool A, Tool B" in report
    assert "Disputed character boundaries: 2" in report
    assert "Package version: 1.2.3" in report
    assert "北京 / 大学 / 。" in report

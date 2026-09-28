from segmenters.registry import TOOL_NAMES


def test_required_tools_are_exposed_in_researcher_facing_order():
    assert TOOL_NAMES == ["Jieba", "HanLP", "LTP", "pkuseg", "THULAC"]

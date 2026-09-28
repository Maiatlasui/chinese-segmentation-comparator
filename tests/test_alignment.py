from comparison.alignment import disagreement_boundaries
from segmenters.base import Token


def test_highlights_split_boundary_in_compound():
    results = {
        "Jieba": [Token("北京大学", 0, 4), Token("。", 4, 5)],
        "HanLP": [Token("北京", 0, 2), Token("大学", 2, 4), Token("。", 4, 5)],
        "pkuseg": [Token("北京大学", 0, 4), Token("。", 4, 5)],
    }
    assert disagreement_boundaries(results) == {2}


def test_agreement_has_no_highlights():
    results = {
        "A": [Token("心理健康", 0, 4)],
        "B": [Token("心理健康", 0, 4)],
    }
    assert disagreement_boundaries(results) == set()


def test_single_result_has_no_highlights():
    assert disagreement_boundaries({"A": [Token("。", 0, 1)]}) == set()

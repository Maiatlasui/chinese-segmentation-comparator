import pytest

from segmenters.base import tokens_with_offsets


@pytest.mark.parametrize(
    ("text", "pieces", "expected"),
    [
        ("我们今天去了北京大学。", ["我们", "今天", "去", "了", "北京大学", "。"], [(0, 2), (2, 4), (4, 5), (5, 6), (6, 10), (10, 11)]),
        ("人工智能\n机器学习。", ["人工智能", "\n", "机器学习", "。"], [(0, 4), (4, 5), (5, 9), (9, 10)]),
        ("北京大学北京大学", ["北京大学", "北京", "大学"], [(0, 4), (4, 6), (6, 8)]),
    ],
)
def test_tokens_keep_character_offsets(text, pieces, expected):
    assert [(token.start, token.end) for token in tokens_with_offsets(text, pieces)] == expected


def test_unmappable_token_is_an_explicit_error():
    with pytest.raises(ValueError, match="Cannot map"):
        tokens_with_offsets("北京大学", ["北京", "学院"])

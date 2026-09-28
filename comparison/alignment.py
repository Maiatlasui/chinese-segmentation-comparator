"""Character-offset comparison for segmentation outputs."""

from __future__ import annotations

from collections import Counter

from segmenters.base import Token


def disagreement_boundaries(results: dict[str, list[Token]]) -> set[int]:
    """Return boundaries present in at least one but not all selected results.

    This treats word boundaries as character offsets, so repeated words and unequal
    token counts do not require fragile token-by-token alignment.
    """
    if len(results) < 2:
        return set()
    boundaries = Counter(
        offset
        for tokens in results.values()
        for token in tokens
        for offset in (token.start, token.end)
    )
    tool_count = len(results)
    return {offset for offset, count in boundaries.items() if 0 < count < tool_count}

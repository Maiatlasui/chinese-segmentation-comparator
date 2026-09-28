"""Jieba adapter."""

from __future__ import annotations

from .base import BackendUnavailableError, SegmentationBackend, Token, tokens_with_offsets


class JiebaBackend(SegmentationBackend):
    name = "Jieba"
    distribution = "jieba"
    model_name = "jieba default dictionary"
    settings = "accurate mode; HMM=True; no custom dictionary"

    def __init__(self) -> None:
        try:
            import jieba

            self._tokenizer = jieba.Tokenizer()
        except Exception as exc:
            raise BackendUnavailableError(f"Could not initialise Jieba: {exc}") from exc

    def segment(self, text: str) -> list[Token]:
        return tokens_with_offsets(text, self._tokenizer.lcut(text, cut_all=False, HMM=True))

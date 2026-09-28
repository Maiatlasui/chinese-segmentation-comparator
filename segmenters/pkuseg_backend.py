"""pkuseg adapter."""

from __future__ import annotations

from .base import BackendUnavailableError, SegmentationBackend, Token, tokens_with_offsets


class PkusegBackend(SegmentationBackend):
    name = "pkuseg"
    distribution = "pkuseg"
    model_name = "default mixed-domain model"
    settings = "postag=False; default user dictionary"

    def __init__(self) -> None:
        try:
            import pkuseg

            self._segmenter = pkuseg.pkuseg(model_name="default", postag=False)
        except Exception as exc:
            raise BackendUnavailableError(f"Could not initialise pkuseg: {exc}") from exc

    def segment(self, text: str) -> list[Token]:
        return tokens_with_offsets(text, self._segmenter.cut(text))

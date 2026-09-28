"""THULAC adapter."""

from __future__ import annotations

from .base import BackendUnavailableError, SegmentationBackend, Token, tokens_with_offsets


class THULACBackend(SegmentationBackend):
    name = "THULAC"
    distribution = "thulac"
    model_name = "bundled THULAC segmentation model"
    settings = "seg_only=True; T2S=False; filt=False"

    def __init__(self) -> None:
        try:
            import thulac

            self._segmenter = thulac.thulac(seg_only=True, T2S=False, filt=False)
        except Exception as exc:
            raise BackendUnavailableError(f"Could not initialise THULAC: {exc}") from exc

    def segment(self, text: str) -> list[Token]:
        pairs = self._segmenter.cut(text, text=False)
        return tokens_with_offsets(text, (pair[0] for pair in pairs))

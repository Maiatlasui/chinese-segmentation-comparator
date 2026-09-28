"""LTP 4.x adapter."""

from __future__ import annotations

from .base import BackendUnavailableError, SegmentationBackend, Token, tokens_with_offsets


class LTPBackend(SegmentationBackend):
    name = "LTP"
    distribution = "ltp"
    model_name = "LTP/tiny"
    settings = "LTP 4.x cws pipeline; no added words; pretrained model download on first use"

    def __init__(self) -> None:
        try:
            from ltp import LTP

            self._ltp = LTP(self.model_name)
        except Exception as exc:
            raise BackendUnavailableError(f"Could not initialise LTP model: {exc}") from exc

    def segment(self, text: str) -> list[Token]:
        output = self._ltp.pipeline([text], tasks=["cws"], return_dict=False)
        # LTP 4.x returns an LTPOutput for some releases and a tuple for others
        # when return_dict=False. Both shapes carry the same CWS token list.
        pieces = output.cws if hasattr(output, "cws") else output[0]
        if pieces and isinstance(pieces[0], list):
            pieces = pieces[0]
        return tokens_with_offsets(text, pieces)

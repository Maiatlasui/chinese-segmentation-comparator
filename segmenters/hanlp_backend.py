"""HanLP 2.x adapter using its explicit pretrained tokenizer constant."""

from __future__ import annotations

from .base import BackendUnavailableError, SegmentationBackend, Token, tokens_with_offsets


class HanLPBackend(SegmentationBackend):
    name = "HanLP"
    distribution = "hanlp"
    model_name = "COARSE_ELECTRA_SMALL_ZH"
    settings = "HanLP 2.x coarse Electra tokenizer; pretrained model download on first use"

    def __init__(self) -> None:
        try:
            import hanlp
            import hanlp.pretrained.tok

            self._tokenizer = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
        except Exception as exc:
            raise BackendUnavailableError(f"Could not initialise HanLP model: {exc}") from exc

    def segment(self, text: str) -> list[Token]:
        batches = self._tokenizer([text])
        return tokens_with_offsets(text, batches[0])

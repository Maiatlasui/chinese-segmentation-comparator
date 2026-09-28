"""Single registry used by the Streamlit layer."""

from __future__ import annotations

from .base import SegmentationBackend
from .hanlp_backend import HanLPBackend
from .jieba_backend import JiebaBackend
from .ltp_backend import LTPBackend
from .pkuseg_backend import PkusegBackend
from .thulac_backend import THULACBackend


BACKENDS: dict[str, type[SegmentationBackend]] = {
    "Jieba": JiebaBackend,
    "HanLP": HanLPBackend,
    "LTP": LTPBackend,
    "pkuseg": PkusegBackend,
    "THULAC": THULACBackend,
}
TOOL_NAMES = list(BACKENDS)


def create_backend(name: str) -> SegmentationBackend:
    try:
        return BACKENDS[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown segmentation tool: {name}") from exc

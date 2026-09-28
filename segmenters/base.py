"""Shared types and offset handling for segmentation backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Iterable


class BackendUnavailableError(RuntimeError):
    """Raised when an optional backend cannot be imported or initialised."""


@dataclass(frozen=True)
class Token:
    text: str
    start: int
    end: int


def package_version(distribution: str) -> str:
    try:
        return version(distribution)
    except PackageNotFoundError:
        return "not installed"


def tokens_with_offsets(source: str, pieces: Iterable[str]) -> list[Token]:
    """Map each returned token back to its first unmatched source occurrence.

    The adapters use models that preserve source characters. Raising on a mismatch
    avoids quietly reporting incorrect offsets when a model normalises text.
    """
    tokens: list[Token] = []
    cursor = 0
    for piece in pieces:
        piece = str(piece)
        if not piece:
            continue
        start = source.find(piece, cursor)
        if start < 0:
            raise ValueError(
                f"Cannot map returned token {piece!r} to the original text. "
                "This backend may have normalised characters."
            )
        end = start + len(piece)
        tokens.append(Token(text=piece, start=start, end=end))
        cursor = end
    return tokens


class SegmentationBackend(ABC):
    name: str
    distribution: str
    model_name: str
    settings: str

    @abstractmethod
    def segment(self, text: str) -> list[Token]:
        """Segment text and return source-character offsets."""

    def metadata(self) -> dict[str, str]:
        return {
            "package_version": package_version(self.distribution),
            "model": self.model_name,
            "settings": self.settings,
        }

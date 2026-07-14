"""Public exception hierarchy used by mootdx."""

from __future__ import annotations

from typing import Any


class MootdxException(Exception):
    """Base class for all package-specific errors."""

    def __init__(
        self,
        message: str | None = None,
        *,
        provider: str | None = None,
        response: Any = None,
        data: Any = None,
    ) -> None:
        self.provider = provider
        self.response = response
        self.message = message or self.__class__.__name__
        self.data = data
        super().__init__(self.message)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.message}>"


class MootdxValidationException(MootdxException, ValueError):
    """Raised when a public API argument is invalid."""


class MootdxModuleNotFoundError(MootdxException, ModuleNotFoundError):
    """Raised when an optional integration dependency is unavailable."""


class FileNeedRefresh(FileNotFoundError):
    """Internal signal indicating that a cached file has expired."""

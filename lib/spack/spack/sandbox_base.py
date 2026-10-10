# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

import spack.error


class Sandbox(ABC):
    """Abstract base class for sandbox implementations."""

    def allow_read(self, path: Union[str, Path]):
        p = Path(path).absolute()
        resolved = p.resolve()
        if resolved.exists():
            self._allow_read(p, resolved)

    def allow_write(self, path: Union[str, Path]):
        p = Path(path).absolute()
        resolved = p.resolve()
        if resolved.exists():
            self._allow_write(p, resolved)

    @abstractmethod
    def _allow_read(self, original: Path, resolved: Path): ...

    @abstractmethod
    def _allow_write(self, original: Path, resolved: Path): ...

    @abstractmethod
    def apply(self, block_network: bool = False): ...


class SandboxError(spack.error.SpackError):
    """Raised when the build sandbox cannot be set up or applied."""

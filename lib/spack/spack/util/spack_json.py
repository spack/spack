# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump."""

import json
from typing import IO, Any, Dict

import spack.error

__all__ = ["load", "dump", "dumps", "SpackJSONError"]

_DEFAULT_SEPARATORS = (",", ":")
_DEFAULT_INDENT = None
_PRETTY_SEPARATORS = (", ", ": ")
_PRETTY_INDENT = "  "


def load(stream: Any) -> Dict:
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, str):
        return json.loads(stream)
    return json.load(stream)


def dump(data: Any, stream: IO[str], pretty: bool = False) -> None:
    """Wrapper around json.dump with different default arguments"""
    indent = _PRETTY_INDENT if pretty else _DEFAULT_INDENT
    separators = _PRETTY_SEPARATORS if pretty else _DEFAULT_SEPARATORS
    json.dump(data, stream, separators=separators, indent=indent)


def dumps(data: Any, pretty: bool = False) -> str:
    """Wrapper around json.dumps with different default arguments"""
    indent = _PRETTY_INDENT if pretty else _DEFAULT_INDENT
    separators = _PRETTY_SEPARATORS if pretty else _DEFAULT_SEPARATORS
    return json.dumps(data, separators=separators, indent=indent)


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg: str, json_error: BaseException):
        super().__init__(msg, str(json_error))

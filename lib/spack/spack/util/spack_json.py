# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump."""

import json
from typing import IO, Any, Dict  # noqa: F401

import spack.error

__all__ = ["load", "dump", "dumps", "SpackJSONError"]

_json_dump_args = {"indent": None, "separators": (",", ":")}
_pretty_dump_args = {"indent": "  ", "separators": (", ", ": ")}


def load(stream: Any) -> Dict:
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, str):
        return json.loads(stream)
    return json.load(stream)


def dump(data: Dict, stream: IO, pretty: bool = False) -> None:
    """Wrapper around json.dump with different default arguments"""
    dump_args = _pretty_dump_args if pretty else _json_dump_args
    json.dump(data, stream, **dump_args)


def dumps(data: Dict, pretty: bool = False) -> str:
    """Wrapper around json.dumps with different default arguments"""
    dump_args = _pretty_dump_args if pretty else _json_dump_args
    return json.dumps(data, **dump_args)


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg: str, json_error: BaseException):
        super().__init__(msg, str(json_error))

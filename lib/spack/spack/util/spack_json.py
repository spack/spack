# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump. """
import json
from typing import Any, Dict, Optional

import spack.error

__all__ = ["load", "dump", "SpackJSONError", "encode_json_dict", "decode_json_dict"]

_json_dump_args = {"indent": 2, "separators": (",", ": ")}


def load(stream: Any) -> Dict:
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, str):
        load = json.loads  # type: ignore[assignment]
    else:
        load = json.load  # type: ignore[assignment]

    return _strify(load(stream, object_hook=_strify), ignore_dicts=True)


def encode_json_dict(data: Dict) -> Dict:
    """Converts python 2 unicodes to str in JSON data."""
    return _strify(data)


def dump(data: Dict, stream: Optional[Any] = None) -> Optional[str]:
    """Dump JSON with a reasonable amount of indentation and separation."""
    data = _strify(data)
    if stream is None:
        return json.dumps(data, **_json_dump_args)  # type: ignore[arg-type]
    json.dump(data, stream, **_json_dump_args)  # type: ignore[arg-type]
    return None


def decode_json_dict(data: Dict) -> Dict:
    """Converts str to python 2 unicodes in JSON data."""
    return _strify(data)


def _strify(data: Dict, ignore_dicts: bool = False) -> Dict:
    """Helper method for ``encode_json_dict()`` and ``decode_json_dict()``.

    Converts python 2 unicodes to str in JSON data, or the other way around."""
    # this is a no-op in python 3
    return data


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg: str, json_error: BaseException):
        super(SpackJSONError, self).__init__(msg, str(json_error))

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Simple wrapper around JSON to guarantee consistent use of load/dump. """
import json
from typing import Any, Dict, Optional  # novm

from six import PY3, iteritems, string_types

import spack.error

__all__ = ['load', 'dump', 'SpackJSONError', 'encode_json_dict', 'decode_json_dict']

_json_dump_args = {
    'indent': 2,
    'separators': (',', ': ')
}


def load(stream):
    # type: (Any) -> Dict
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, string_types):
        load = json.loads       # type: ignore[assignment]
    else:
        load = json.load        # type: ignore[assignment]

    return _strify(load(stream, object_hook=_strify), ignore_dicts=True)


def encode_json_dict(data):
    # type: (Dict) -> Dict
    """Converts python 2 unicodes to str in JSON data."""
    return _strify(data)


def dump(data, stream=None):
    # type: (Dict, Optional[Any]) -> Optional[str]
    """Dump JSON with a reasonable amount of indentation and separation."""
    data = _strify(data)
    if stream is None:
        return json.dumps(data, **_json_dump_args)     # type: ignore[arg-type]
    json.dump(data, stream, **_json_dump_args)         # type: ignore[arg-type]
    return None


def decode_json_dict(data):
    # type: (Dict) -> Dict
    """Converts str to python 2 unicodes in JSON data."""
    return _strify(data)


def _strify(data, ignore_dicts=False):
    # type: (Dict, bool) -> Dict
    """Helper method for ``encode_json_dict()`` and ``decode_json_dict()``.

    Converts python 2 unicodes to str in JSON data, or the other way around."""
    # this is a no-op in python 3
    if PY3:
        return data

    # if this is a unicode string in python 2, return its string representation
    if isinstance(data, string_types):
        return data.encode('utf-8')

    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_strify(item, ignore_dicts=True) for item in data]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return dict((_strify(key, ignore_dicts=True),
                     _strify(value, ignore_dicts=True)) for key, value in
                    iteritems(data))

    # if it's anything else, return it in its original form
    return data


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""

    def __init__(self, msg, json_error):
        # type: (str, BaseException) -> None
        super(SpackJSONError, self).__init__(msg, str(json_error))

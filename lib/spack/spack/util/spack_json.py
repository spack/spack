##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Simple wrapper around JSON to guarantee consistent use of load/dump. """
import sys
import json
from six import string_types
from six import iteritems

import spack.error

__all__ = ['load', 'dump', 'SpackJSONError']

_json_dump_args = {
    'indent': True,
    'separators': (',', ': ')
}


def load(stream):
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, string_types):
        load = json.loads
    else:
        load = json.load

    return _strify(load(stream, object_hook=_strify), ignore_dicts=True)


def dump(data, stream=None):
    """Dump JSON with a reasonable amount of indentation and separation."""
    if stream is None:
        return json.dumps(data, **_json_dump_args)
    else:
        return json.dump(data, stream, **_json_dump_args)


def _strify(data, ignore_dicts=False):
    # if this is a unicode string in python 2, return its string representation
    if sys.version_info[0] < 3:
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
        super(SpackJSONError, self).__init__(msg, str(json_error))

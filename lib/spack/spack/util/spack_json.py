##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import json
import spack.error

__all__ = ['load', 'dump', 'SpackJSONError']

_json_dump_args = {
    'indent': True,
    'separators': (',', ': ')
}


def load(stream):
    """Spack JSON needs to be ordered to support specs."""
    if isinstance(stream, basestring):
        return json.loads(stream)
    else:
        return json.load(stream)


def dump(data, stream=None):
    """Dump JSON with a reasonable amount of indentation and separation."""
    if stream is None:
        return json.dumps(data, **_json_dump_args)
    else:
        return json.dump(data, stream, **_json_dump_args)


class SpackJSONError(spack.error.SpackError):
    """Raised when there are issues with JSON parsing."""
    def __init__(self, msg, yaml_error):
        super(SpackJSONError, self).__init__(msg, str(yaml_error))

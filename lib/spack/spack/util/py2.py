# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import base64

from six import PY3, binary_type, text_type


def b32encode(digest):
    # type: (binary_type) -> text_type
    b32 = base64.b32encode(digest)
    if PY3:
        return b32.decode()
    return b32

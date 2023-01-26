# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.mock.a import A


class Disinherit(A):
    """Disinherit from A and add our own versions."""

    disinherit("versions")
    version("4.0", "abcdef0123456789abcdef0123456789")
    version("3.0", "0123456789abcdef0123456789abcdef")

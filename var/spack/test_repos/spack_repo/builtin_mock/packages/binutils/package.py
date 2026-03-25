# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Binutils(Package):
    """Mock binutils package used in tests."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/binutils-1.0.tar.gz"

    version("2.42", md5="0123456789abcdef0123456789abcdef")

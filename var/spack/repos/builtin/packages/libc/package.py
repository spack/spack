# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libc(Package):
    """Dummy libc package to provide `iconv` virtual package"""

    homepage = "https://en.wikipedia.org/wiki/C_standard_library"
    url      = ""
    has_code = False
    phases = []

    version('1.0')  # Dummy
    variant('iconv', default=False, description='Set to True if libc provides iconv')
    provides('iconv', when='+iconv')

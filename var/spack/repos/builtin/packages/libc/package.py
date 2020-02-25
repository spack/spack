# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install libc
#
# You can edit this file again by typing:
#
#     spack edit libc
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

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

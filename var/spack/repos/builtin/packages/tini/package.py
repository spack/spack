# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install tini
#
# You can edit this file again by typing:
#
#     spack edit tini
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Tini(CMakePackage):
    """A tiny but valid `init` for containers"""

    homepage = "https://github.com/krallin/tini"
    url      = "https://github.com/krallin/tini/archive/refs/tags/v0.19.0.tar.gz"
    maintainers = ["teonnik", "Madeeks"]

    version('0.19.0', sha256='0fd35a7030052acd9f58948d1d900fe1e432ee37103c5561554408bdac6bbf0d')
    patch('disable_tini_static.patch', when='@0.19.0:')

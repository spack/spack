# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install r-inside
#
# You can edit this file again by typing:
#
#     spack edit r-inside
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class RInside(RPackage):
    """RInside: C++ Classes to Embed R in C++ Applications"""

    homepage = "https://cran.r-project.org/package=RInside"
    url      = "https://cloud.r-project.org/src/contrib/RInside_0.2.15.tar.gz"

    version('0.2.15', sha256='1e1d87a3584961f3aa4ca6acd4d2f3cda26abdab027ff5be2fd5cd76a98af02b')

    def configure_args(self, spec, prefix):
        args = []
        return args

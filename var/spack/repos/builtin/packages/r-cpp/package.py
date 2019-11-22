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
#     spack install r-cpp
#
# You can edit this file again by typing:
#
#     spack edit r-cpp
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class RCpp(RPackage):
    """Seamless R and C++ Integration"""

    homepage = "https://cloud.r-project.org/package=Rcpp"
    url      = "https://cloud.r-project.org/src/contrib/Rcpp_1.0.3.tar.gz"

    version('1.0.3', sha256='2b3500dd3aca16f7b3cb5442625e76dcf4f7c974b4249d33041e9184a5ff030e')


    def configure_args(self, spec, prefix):
        args = []
        return args

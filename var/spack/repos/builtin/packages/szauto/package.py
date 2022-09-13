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
#     spack install szauto
#
# You can edit this file again by typing:
#
#     spack edit szauto
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Szauto(CMakePackage):
    """SZauto: SZ C++ Version that Supports Second-Order Prediction and Parameter Optimization"""

    homepage = "https://github.com/szcompressor/SZauto"
    url      = "https://github.com/szcompressor/SZauto/releases/download/1.0.0/SZauto-1.0.0.tar.gz"
    git      = "https://github.com/szcompressor/szauto"

    maintainers = ['disheng222', 'robertu94']

    version('master', branch='master')
    version('1.2.1', sha256='55c58f58df3a874f684ef864a9247907df0501e5598c089fd2d855ae0309b03a')
    version('1.0.0', commit="03f3ab0312bd1de647e9d65746add73a0e8602d2")

    depends_on('zstd')
    depends_on('pkgconfig')


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
#     spack install cusz
#
# You can edit this file again by typing:
#
#     spack edit cusz
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Cusz(MakefilePackage):
    """cuSZ is a CUDA-based error-bounded lossy compressor for scientific data (floating point and integers)."""

    homepage = "https://szcompressor.org"
    url      = "https://github.com/szcompressor/cuSZ/releases/download/v0.1.2/cuSZ-0.1.2.tar.gz"
    git      = "https://github.com/szcompressor/cuSZ"
    maintainers = ['dingwentao', 'jtian0']

    version('master', branch='master')
    version('0.1.2', sha256='c6e89a26b295724edefc8052f62653c5a315c78eaf6d5273299a8e11a5cf7363')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')

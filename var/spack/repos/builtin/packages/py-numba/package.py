# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNumba(PythonPackage):
    """NumPy aware dynamic Python compiler using LLVM"""

    homepage = "https://numba.pydata.org/"
    url      = "https://pypi.io/packages/source/n/numba/numba-0.35.0.tar.gz"

    version('0.35.0', '4f447383406f54aaf18ffaba3a0e79e8')

    depends_on('py-numpy@1.10:',    type=('build', 'run'))
    depends_on('py-llvmlite@0.20:', type=('build', 'run'))
    depends_on('py-argparse',       type=('build', 'run'))
    depends_on('py-funcsigs',       type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-singledispatch', type=('build', 'run'), when='^python@:3.3.99')

    # Version 6.0.0 of llvm had a hidden symbol which breaks numba at runtime.
    # See https://reviews.llvm.org/D44140
    conflicts('^llvm@6.0.0')

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyScs(PythonPackage):
    """SCS: splitting conic solver"""

    homepage = "https://github.com/cvxgrp/scs"
    pypi = "scs/scs-2.1.1-2.tar.gz"

    version('2.1.1-2', sha256='f816cfe3d4b4cff3ac2b8b96588c5960ddd2a3dc946bda6b09db04e7bc6577f2')

    variant('cuda', default=False, description="Also compile the GPU CUDA version of SCS")
    variant('float32', default=False, description="Use 32 bit (single precision) floats, default is 64 bit")
    variant('extra_verbose', default=False, description="Extra verbose SCS (for debugging)")
    variant('int32', default=False, description="Use 32 bit ints")
    variant('blas64', default=False, description="Use 64 bit ints for the blas/lapack libs")

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-scipy@0.13.2:', type=('build', 'run'))

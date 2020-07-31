# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyarrow(PythonPackage):
    """A cross-language development platform for in-memory data.

    This package contains the Python bindings.
    """

    homepage = "http://arrow.apache.org"
    url      = "https://pypi.org/packages/source/p/pyarrow/pyarrow-0.9.0.tar.gz"
    git      = "https://github.com/apache/arrow.git"

    version('0.17.1', tag='apache-arrow-0.17.1')
    version('0.15.1', sha256='7ad074690ba38313067bf3bbda1258966d38e2037c035d08b9ffe3cce07747a5')
    version('0.15.0', tag='apache-arrow-0.15.0')
    version('0.14.1', tag='apache-arrow-0.14.1')
    version('0.14.0', sha256='8f34e76b03e1c4f73c8cf31b6ed9c89bc909d34657b96271a0c45c59b4decc3d')
    version('0.13.0', sha256='1bf34856831af53e2eb5178fb04301ff000bbb8fe0a7e7a7723abf7fe355eeef')
    version('0.12.1', sha256='10db6e486c918c3af999d0114a22d92770687e3a6607ea3f14e6748854824c2a')
    version('0.11.0', sha256='07a6fd71c5d7440f2c42383dd2c5daa12d7f0a012f1e88288ed08a247032aead')
    version('0.9.0', sha256='7db8ce2f0eff5a00d6da918ce9f9cfec265e13f8a119b4adb1595e5b19fd6242')

    variant('parquet', default=False, description="Build with Parquet support")

    depends_on('cmake@3.0.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    for v in ('@0.9.0', '@0.11.0', '@0.12.1', '@0.13.0', '@0.14.0',
              '@0.14.1', '@0.15.0', '@0.15.1', '@0.17.1'):
        depends_on('arrow+python' + v, when=v)
        depends_on('arrow+python+parquet' + v, when='+parquet' + v)

    phases = ['build_ext', 'install']

    @property
    def build_directory(self):
        if self.spec.satisfies('@0.14.1:0.15.0'):
            return 'python'
        return '.'

    def build_ext_args(self, spec, prefix):
        args = []
        if spec.satisfies('+parquet'):
            args.append('--with-parquet')
        return args

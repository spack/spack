# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysam(PythonPackage):
    """A python module for reading, manipulating and writing genomic data
       sets."""

    homepage = "https://github.com/pysam-developers/pysam"
    pypi = "pysam/pysam-0.14.1.tar.gz"

    version('0.18.0', sha256='1d6d49a0b3c626fae410a93d4c80583a8b5ddaacc9b46a080b250dbcebd30a59')
    version('0.15.3', sha256='a98dd0a164aa664b1ab30a36f653752f00e93c13deeb66868597f4b2a30f7265')
    version('0.15.2', sha256='d049efd91ed5b1af515aa30280bc9cb46a92ddd15d546c9b21ee68a6ed4055d9')
    version('0.15.1', sha256='658421124c2f3de1b7445e03ca8413df0077f67ea9980abdaab0d1b5f7a8936f')
    version('0.14.1', sha256='2e86f5228429d08975c8adb9030296699012a8deba8ba26cbfc09b374f792c97')
    version('0.7.7',  sha256='c9f3018482eec99ee199dda3fdef2aa7424dde6574672a4c0d209a10985755cc')

    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.29.12:', when='@0.18:', type='build')
    depends_on('py-cython@0.21:', when='@0.14:', type='build')
    depends_on('py-cython@0.17:', type='build')
    depends_on('curl')
    depends_on('bcftools')
    depends_on('htslib')
    depends_on('samtools')

    depends_on('htslib@:1.6', when='@:0.13')

    def setup_build_environment(self, env):
        env.set('LDFLAGS', self.spec['curl'].libs.search_flags)

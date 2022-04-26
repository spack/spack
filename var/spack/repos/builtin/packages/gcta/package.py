# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gcta(CMakePackage):
    """GCTA (Genome-wide Complex Trait Analysis) was originally designed to
    estimate the proportion of phenotypic variance explained by all genome-wide
    SNPs for complex traits (the GREML method), and has subsequently extended
    for many other analyses to better understand the genetic architecture of
    complex traits. GCTA currently supports the following analyses."""

    homepage = "https://github.com/jianyangqt/gcta"
    url      = "https://github.com/jianyangqt/gcta/archive/refs/tags/v1.91.2.tar.gz"
    git      = "https://github.com/jianyangqt/gcta.git"
    maintainers = ['snehring']

    version('1.94.0beta',  commit='746e3975ddb463fc7bd15b03c6cc64b023eca497', submodules=True)
    version('1.91.2',      sha256='0609d0fba856599a2acc66adefe87725304117acc226360ec2aabf8a0ac64e85')

    conflicts('target=aarch64:', when='@:1.91.2', msg='aarch64 support added in 1.94.0')

    depends_on('cmake@3.1:', type='build')
    depends_on('intel-mkl@2017:', type=('build', 'link'), when='target=x86_64:')
    depends_on('openblas', type=('build', 'link'), when='target=aarch64:')
    depends_on('eigen@3.3.1', type=('build', 'link'), when='@1.91.2')
    depends_on('eigen@3.3.7:', type=('build', 'link'), when='@1.94.0beta:')
    depends_on('boost@1.4:', type=('build', 'link'), when='@1.94.0beta:')
    depends_on('zlib', type=('build', 'link'))
    depends_on('sqlite@3.3.1:', type=('build', 'link'), when='@1.94.0beta:')
    depends_on('zstd@1.4.4:', type=('build', 'link'), when='@1.94.0beta:')
    depends_on('spectra', type=('build', 'link'), when='@1.94.0beta:')
    depends_on('gsl', type=('build', 'link'), when='@1.94.0beta:')

    def patch(self):
        # allow us to specify the locations with cmake_args
        strings = [
            'SET(EIGEN3_INCLUDE_DIR "$ENV{EIGEN3_INCLUDE_DIR}")',
            'SET(SPECTRA_LIB "$ENV{SPECTRA_LIB}")',
            'SET(BOOST_LIB "$ENV{BOOST_LIB}")',
            'SET(OPENBLAS "$ENV{OPENBLAS}")',
            'SET(MKLROOT "$ENV{MKLROOT}")'
        ]
        for s in strings:
            filter_file(s, '', 'CMakeLists.txt', string=True)

    def cmake_args(self):
        eigen = self.spec['eigen'].prefix.include
        args = [self.define('EIGEN3_INCLUDE_DIR', eigen)]
        if self.spec.satisfies('@1.94.0beta:'):
            spectra = self.spec['spectra'].prefix.include
            boost = self.spec['boost'].prefix.include
            deps = [
                self.define('SPECTRA_LIB', spectra),
                self.define('BOOST_LIB', boost),
            ]
            args.extend(deps)

        if self.spec.satisfies('target=x86_64:'):
            mkl = self.spec['intel-mkl'].prefix
            args.append(self.define('MKLROOT', mkl))
        elif self.spec.satisfies('target=aarch64:'):
            openblas = self.spec['openblas'].prefix
            args.append(self.define('OPENBLAS', openblas))

        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('gcta64', join_path(prefix.bin, 'gcta64'))

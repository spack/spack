# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Votca(CMakePackage):
    """VOTCA is a software package which focuses on the analysis of molecular
       dynamics data, the development of systematic coarse-graining techniques
       as well as methods used for simulating microscopic charge (and exciton)
       transport in disordered semiconductors.
    """
    homepage = "https://www.votca.org"
    url      = "https://github.com/votca/votca/tarball/v2022-rc.1"
    git      = "https://github.com/votca/xtp.git"
    maintainers = ['junghans']

    version('master', branch='master')
    version('stable', branch='stable')
    version('2022-rc.2', sha256='eefde51470ec1437d0127fb02c2745f33e434deff53cdaee97691c36ce447fb1')
    version('2022-rc.1', sha256='d53ca9fde364a97d91bf3bed15223536ffa598b2dec7bccd459accae265391b1')

    variant('mkl', default=False, description='Build with MKL support')
    variant('new-gmx', default=False, description='Build against gromacs>2019 - no tabulated kernels')
    conflicts('votca-tools')
    conflicts('votca-csg')
    conflicts('votca-xtp')

    depends_on("cmake@3.13:", type='build')
    depends_on("expat")
    depends_on("fftw-api@3")
    depends_on("eigen@3.3:")
    depends_on("boost")
    depends_on('mkl', when='+mkl')
    depends_on("libxc")
    depends_on("hdf5+cxx~mpi")
    depends_on("libint@2.6.0:")
    depends_on("libecpint")
    depends_on("py-h5py")
    depends_on("py-lxml")
    depends_on("gromacs~mpi@5.1:")
    depends_on("gromacs~mpi@5.1:2019", when="~new-gmx")
    depends_on('lammps', type='test')
    depends_on('py-espresso', type='test')
    depends_on('py-pytest', type='test')

    def cmake_args(self):
        args = [
            '-DINSTALL_RC_FILES=OFF',
            '-DBUILD_XTP=ON',
            '-DBUILD_CSGAPPS=ON',
        ]

        if '~mkl' in self.spec:
            args.append('-DCMAKE_DISABLE_FIND_PACKAGE_MKL=ON')

        if self.run_tests:
            args.append('-DENABLE_TESTING=ON')
            args.append('-DENABLE_REGRESSION_TESTING=ON')

        return args

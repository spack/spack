# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
    git      = "https://github.com/votca/votca.git"
    maintainers = ['junghans']

    version('master', branch='master')
    version('stable', branch='stable')
    version('2022', sha256='7991137098ff4511f4ca2c6f1b6c45f53d92d9f84e5c0d0e32fbc31768f73a83')

    variant('mkl', default=False, description='Build with MKL support')
    variant('new-gmx', default=False, description='Build against gromacs>2019 - no tabulated kernels')
    variant('xtp', default=True, description='Build xtp parts of votca')
    conflicts('votca-tools')
    conflicts('votca-csg')
    conflicts('votca-xtp')

    depends_on("cmake@3.13:", type='build')
    depends_on("expat")
    depends_on("fftw-api@3")
    depends_on("eigen@3.3:")
    depends_on("boost")
    depends_on('mkl', when='+mkl')
    depends_on("hdf5+cxx~mpi")
    depends_on("gromacs~mpi@5.1:")
    depends_on("gromacs~mpi@5.1:2019", when="~new-gmx")

    with when('+xtp'):
        depends_on("libxc")
        depends_on("libint@2.6.0:")
        depends_on("libecpint")
        depends_on("py-h5py")
        depends_on("py-lxml")

    depends_on('lammps', type='test')
    depends_on('py-espresso', type='test')
    depends_on('py-pytest', type='test')

    def cmake_args(self):
        args = [
            '-DINSTALL_RC_FILES=OFF',
            self.define_from_variant('BUILD_XTP', 'xtp'),
            '-DBUILD_CSGAPPS=ON',
        ]

        if '~mkl' in self.spec:
            args.append('-DCMAKE_DISABLE_FIND_PACKAGE_MKL=ON')

        if self.run_tests:
            args.append('-DENABLE_TESTING=ON')
            args.append('-DENABLE_REGRESSION_TESTING=ON')

        return args

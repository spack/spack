# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Casacore(CMakePackage):
    """A suite of c++ libraries for radio astronomy data processing."""

    homepage = "https://github.com/casacore/casacore"
    url      = "https://github.com/casacore/casacore/archive/v2.4.1.tar.gz"

    maintainers = ['mpokorny']

    version('3.2.0', sha256='ae5d3786cb6dfdd7ebc5eecc0c724ff02bbf6929720bc23be43a027978e79a5f')
    version('3.1.2', sha256='ac94f4246412eb45d503f1019cabe2bb04e3861e1f3254b832d9b1164ea5f281')
    version('3.1.1', sha256='85d2b17d856592fb206b17e0a344a29330650a4269c80b87f8abb3eaf3dadad4')
    version('3.1.0', sha256='a6adf2d77ad0d6f32995b1e297fd88d31ded9c3e0bb8f28966d7b35a969f7897')
    version('3.0.0', sha256='6f0e68fd77b5c96299f7583a03a53a90980ec347bff9dfb4c0abb0e2933e6bcb')
    version('2.4.1', sha256='58eccc875053b2c6fe44fe53b6463030ef169597ec29926936f18d27b5087d63')

    variant('openmp', default=False, description='Build OpenMP support')
    variant('shared', default=True, description='Build shared libraries')
    # see note below about the reason for disabling the "sofa" variant
    # variant('sofa', default=False, description='Build SOFA support')
    variant('fftw', default=False, description='Build FFTW3 support')
    variant('hdf5', default=False, description='Build HDF5 support')
    variant('python', default=False, description='Build python support')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('blas')
    depends_on('lapack')
    depends_on('cfitsio@3.181:')
    depends_on('wcslib@4.20:+cfitsio')
    depends_on('fftw~mpi@3.0.0:', when='+fftw')
    # SOFA dependency suffers the same problem in CMakeLists.txt as readline;
    # however, as SOFA is far less likely to be present on most systems, and as
    # it's an unneeded dependency except for testing, for now we leave out the
    # option for a dependency on SOFA.
    # depends_on('sofa-c', when='+sofa')
    depends_on('hdf5', when='+hdf5')
    # Force dependency on readline. Although the presence of readline is tested
    # in CMakeLists.txt, and casacore can be built without it, there's no way
    # to control that dependency at build time; since many systems come with
    # readline, it's better to explicitly depend on it here always.
    depends_on('readline')
    depends_on('python@2.6:', when='+python')
    depends_on('boost+python', when='+python')
    depends_on('py-numpy', when='+python')

    def cmake_args(self):
        args = []
        spec = self.spec

        if '+shared' in spec:
            args.append('-DENABLE_SHARED=YES')
        else:
            args.append('-DENABLE_SHARED=NO')

        if '+openmp' in spec:
            args.append('-DUSE_OPENMP=YES')
        else:
            args.append('-DUSE_OPENMP=NO')

        if '+hdf5' in spec:
            args.append('-DUSE_HDF5=YES')
        else:
            args.append('-DUSE_HDF5=NO')

        if '+fftw' in spec:
            args.append('-DUSE_FFTW3=YES')
        else:
            args.append('-DUSE_FFTW3=NO')

        # Python2 and Python3 binding
        if('+python' not in spec):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=NO'])
        elif(spec['python'].version >= Version('3.0.0')):
            args.extend(['-DBUILD_PYTHON=NO', '-DBUILD_PYTHON3=YES'])
        else:
            args.extend(['-DBUILD_PYTHON=YES', '-DBUILD_PYTHON3=NO'])

        return args

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Med(CMakePackage):
    """The MED file format is a specialization of the HDF5 standard."""

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url = "https://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz"

    maintainers = ['likask']

    # 4.1.0 does not compile in static mode
    version('4.1.0', sha256='847db5d6fbc9ce6924cb4aea86362812c9a5ef6b9684377e4dd6879627651fce')
    version('4.0.0', sha256='a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004', preferred=True)
    version('3.2.0', sha256='d52e9a1bdd10f31aa154c34a5799b48d4266dc6b4a5ee05a9ceda525f2c6c138')

    variant('api23', default=True, description='Enable API2.3')
    variant('mpi', default=True, description='Enable MPI')
    variant('shared', default=False,
            description='Builds a shared version of the library')
    variant('fortran', default=False, description='Enable Fortran support')

    depends_on('mpi', when='+mpi')
    depends_on('hdf5@:1.8.22+mpi', when='@3.2.0+mpi')
    depends_on('hdf5@1.10.2:1.10.7+mpi', when='@4.0.0:+mpi')
    depends_on('hdf5@:1.8.22~mpi', when='@3.2.0~mpi')
    depends_on('hdf5@1.10.2:1.10.7~mpi', when='@4.0.0:~mpi')
    # the "TARGET hdf5" patch below only works with HDF5 shared library builds
    depends_on('hdf5+shared', when='@4.0.0:4.1.99')

    conflicts("@4.1.0", when="~shared", msg="Link error when static")

    # C++11 requires a space between literal and identifier
    patch('add_space.patch', when='@3.2.0')
    # fix problem where CMake "could not find TARGET hdf5"
    patch('med-4.1.0-hdf5-target.patch', when='@4.0.0:4.1.99')

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define('HDF5_ROOT_DIR', spec['hdf5'].prefix),
            self.define('MEDFILE_BUILD_TESTS', self.run_tests),
            self.define('MEDFILE_BUILD_PYTHON', False),
            self.define('MEDFILE_INSTALL_DOC', False),
        ]
        if '~fortran' in spec:
            options.append('-DCMAKE_Fortran_COMPILER=')

        if '+api23' in spec:
            options.extend([
                '-DCMAKE_CXX_FLAGS:STRING=-DMED_API_23=1',
                '-DCMAKE_C_FLAGS:STRING=-DMED_API_23=1',
                '-DMED_API_23=1'])

        if '+shared' in spec:
            options.extend([
                '-DMEDFILE_BUILD_SHARED_LIBS=ON',
                '-DMEDFILE_BUILD_STATIC_LIBS=OFF',
            ])
        else:
            options.extend([
                '-DMEDFILE_BUILD_SHARED_LIBS=OFF',
                '-DMEDFILE_BUILD_STATIC_LIBS=ON',
            ])

        if '+mpi' in spec:
            options.extend(['-DMEDFILE_USE_MPI=YES',
                            '-DMPI_ROOT_DIR=%s' % spec['mpi'].prefix])

        return options

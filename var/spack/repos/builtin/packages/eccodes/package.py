# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = 'https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home'
    url = 'https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2'
    list_url = 'https://software.ecmwf.int/wiki/display/ECC/Releases'

    maintainers = ['skosukhin']

    version('2.13.0', sha256='c5ce1183b5257929fc1f1c8496239e52650707cfab24f4e0e1f1a471135b8272')
    version('2.5.0', sha256='18ab44bc444168fd324d07f7dea94f89e056f5c5cd973e818c8783f952702e4e')
    version('2.2.0', sha256='1a4112196497b8421480e2a0a1164071221e467853486577c4f07627a702f4c3')

    variant('netcdf', default=False,
            description='Enable GRIB to NetCDF conversion tool')
    variant('jp2k', default='openjpeg', values=('openjpeg', 'jasper', 'none'),
            description='Specify JPEG2000 decoding/encoding backend')
    variant('png', default=False,
            description='Enable PNG support for decoding/encoding')
    variant('aec', default=False,
            description='Enable Adaptive Entropy Coding for decoding/encoding')
    variant('pthreads', default=False,
            description='Enable POSIX threads')
    variant('openmp', default=False,
            description='Enable OpenMP threads')
    variant('memfs', default=False,
            description='Enable memory based access to definitions/samples')
    variant('python', default=False,
            description='Enable the Python interface')
    variant('fortran', default=False, description='Enable the Fortran support')
    variant('examples', default=True,
            description='Build the examples (part of the full test suite)')
    variant('test', default=True, description='Enable the tests')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    # The building script tries to find an optional package valgrind when
    # tests are enabled but the testing scripts don't use it.
    # depends_on('valgrind', type='test', when='+test')

    depends_on('netcdf-c', when='+netcdf')
    depends_on('openjpeg@1.5.0:1.5.999,2.1.0:2.1.999', when='jp2k=openjpeg')
    depends_on('jasper', when='jp2k=jasper')
    depends_on('libpng', when='+png')
    depends_on('libaec', when='+aec')
    # Can be built with Python2 or Python3.
    depends_on('python', when='+memfs', type='build')
    # The interface works only for Python2.
    # Python 3 support was added in 2.13.0:
    # https://confluence.ecmwf.int/display/ECC/Python+3+interface+for+ecCodes
    depends_on('python@2.6:2.999', when='@:2.12+python',
               type=('build', 'link', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    extends('python', when='+python')

    conflicts('+openmp', when='+pthreads',
              msg='Cannot enable both POSIX threads and OMP')

    # The following enforces linking against the specified JPEG2000 backend.
    patch('enable_only_openjpeg.patch', when='jp2k=openjpeg')
    patch('enable_only_jasper.patch', when='jp2k=jasper')

    # CMAKE_INSTALL_RPATH must be a semicolon-separated list.
    patch('cmake_install_rpath.patch', when='@:2.10')

    @run_before('cmake')
    def check_fortran(self):
        if '+fortran' in self.spec and self.compiler.fc is None:
            raise InstallError(
                'Fortran interface requires a Fortran compiler!')

    def cmake_args(self):
        var_opt_list = [('+pthreads', 'ECCODES_THREADS'),
                        ('+openmp', 'ECCODES_OMP_THREADS'),
                        ('+memfs', 'MEMFS'),
                        ('+python', 'PYTHON'),
                        ('+fortran', 'FORTRAN'),
                        ('+examples', 'EXAMPLES'),
                        ('+test', 'TESTS'),
                        ('+test', 'EXTRA_TESTS')]

        args = ['-DENABLE_%s=%s' % (opt, 'ON' if var in self.spec else 'OFF')
                for var, opt in var_opt_list]

        if '+netcdf' in self.spec:
            args.extend(['-DENABLE_NETCDF=ON',
                         # Prevent overriding by environment variable
                         # HDF5_ROOT.
                         '-DHDF5_ROOT=' + self.spec['hdf5'].prefix,
                         # Prevent possible overriding by environment variables
                         # NETCDF_ROOT, NETCDF_DIR, and NETCDF_PATH.
                         '-DNETCDF_PATH=' + self.spec['netcdf-c'].prefix])
        else:
            args.append('-DENABLE_NETCDF=OFF')

        if self.spec.variants['jp2k'].value == 'none':
            args.append('-DENABLE_JPG=OFF')
        else:
            args.append('-DENABLE_JPG=ON')

        if self.spec.variants['jp2k'].value == 'openjpeg':
            args.append('-DOPENJPEG_PATH=' + self.spec['openjpeg'].prefix)

        if '+png' in self.spec:
            args.extend(['-DENABLE_PNG=ON',
                         '-DZLIB_ROOT=' + self.spec['zlib'].prefix])
        else:
            args.append('-DENABLE_PNG=OFF')

        if '+aec' in self.spec:
            args.extend(['-DENABLE_AEC=ON',
                         # Prevent overriding by environment variables
                         # AEC_DIR and AEC_PATH.
                         '-DAEC_DIR=' + self.spec['libaec'].prefix])
        else:
            args.append('-DENABLE_AEC=OFF')

        if '^python' in self.spec:
            args.append('-DPYTHON_EXECUTABLE:FILEPATH=' + python.path)

        return args

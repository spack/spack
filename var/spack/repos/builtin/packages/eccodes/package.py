# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = 'https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home'
    url = 'https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2'
    list_url = 'https://confluence.ecmwf.int/display/ECC/Releases'

    maintainers = ['skosukhin']

    version('2.24.2', sha256='c60ad0fd89e11918ace0d84c01489f21222b11d6cad3ff7495856a0add610403')
    version('2.23.0', sha256='cbdc8532537e9682f1a93ddb03440416b66906a4cc25dec3cbd73940d194bf0c')
    version('2.22.1', sha256='75c7ee96469bb30b0c8f7edbdc4429ece4415897969f75c36173545242bc9e85')
    version('2.21.0', sha256='da0a0bf184bb436052e3eae582defafecdb7c08cdaab7216780476e49b509755')
    version('2.20.0', sha256='207a3d7966e75d85920569b55a19824673e8cd0b50db4c4dac2d3d52eacd7985')
    version('2.19.1', sha256='9964bed5058e873d514bd4920951122a95963128b12f55aa199d9afbafdd5d4b')
    version('2.18.0', sha256='d88943df0f246843a1a062796edbf709ef911de7269648eef864be259e9704e3')
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
            description='Enable the Python 2 interface')
    variant('fortran', default=False, description='Enable the Fortran support')
    variant('shared', default=True,
            description='Build shared versions of the libraries')

    depends_on('netcdf-c', when='+netcdf')
    # Cannot be built with openjpeg@2.0.x.
    depends_on('openjpeg@1.5.0:1.5,2.1.0:2.3', when='jp2k=openjpeg')
    # Additional constraint for older versions.
    depends_on('openjpeg@:2.1', when='@:2.16 jp2k=openjpeg')
    depends_on('jasper', when='jp2k=jasper')
    depends_on('libpng', when='+png')
    depends_on('libaec', when='+aec')
    # Can be built with Python 2 or Python 3.
    depends_on('python', when='+memfs', type='build')
    # The interface is available only for Python 2.
    # Python 3 interface is available as a separate packages:
    # https://confluence.ecmwf.int/display/ECC/Python+3+interface+for+ecCodes
    depends_on('python@2.6:2', when='+python',
               type=('build', 'link', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    extends('python', when='+python')

    depends_on('cmake@3.6:', type='build')
    depends_on('cmake@3.12:', when='@2.19:', type='build')
    conflicts('+openmp', when='+pthreads',
              msg='Cannot enable both POSIX threads and OMP')

    # Enforce linking against the specified JPEG2000 backend, see also
    # https://github.com/ecmwf/eccodes/commit/2c10828495900ff3d80d1e570fe96c1df16d97fb
    patch('openjpeg_jasper.patch', when='@:2.16')

    # CMAKE_INSTALL_RPATH must be a semicolon-separated list.
    patch('cmake_install_rpath.patch', when='@:2.10')

    # Fix a bug preventing cmake from finding NetCDF:
    patch('https://github.com/ecmwf/ecbuild/commit/3916c7d22575c45166fcc89edcbe02a6e9b81aa2.patch',
          sha256='857454528b666c52eb36ef3aa5d40ae018981b44e129bb8df3c2d3d560e3fa03',
          when='@:2.4.0+netcdf')

    @run_before('cmake')
    def check_fortran(self):
        if '+fortran' in self.spec and self.compiler.fc is None:
            raise InstallError(
                'Fortran interface requires a Fortran compiler!')

    def cmake_args(self):
        jp2k = self.spec.variants['jp2k'].value

        args = [
            self.define_from_variant('ENABLE_NETCDF', 'netcdf'),
            self.define('ENABLE_JPG', jp2k != 'none'),
            self.define('ENABLE_JPG_LIBJASPER', jp2k == 'jasper'),
            self.define('ENABLE_JPG_LIBOPENJPEG', jp2k == 'openjpeg'),
            self.define_from_variant('ENABLE_PNG', 'png'),
            self.define_from_variant('ENABLE_AEC', 'aec'),
            self.define_from_variant('ENABLE_ECCODES_THREADS', 'pthreads'),
            self.define_from_variant('ENABLE_ECCODES_OMP_THREADS', 'openmp'),
            self.define_from_variant('ENABLE_MEMFS', 'memfs'),
            self.define_from_variant(
                'ENABLE_PYTHON{0}'.format(
                    '2' if self.spec.satisfies('@2.20.0:') else ''),
                'python'),
            self.define_from_variant('ENABLE_FORTRAN', 'fortran'),
            self.define('BUILD_SHARED_LIBS',
                        'BOTH' if '+shared' in self.spec else 'OFF'),
            self.define('ENABLE_TESTS', self.run_tests),
            # Examples are not installed and are just part of the test suite:
            self.define('ENABLE_EXAMPLES', self.run_tests),
            # Unconditionally disable the extended regression tests, since they
            # download additional data (~134MB):
            self.define('ENABLE_EXTRA_TESTS', False)
        ]

        if '+netcdf' in self.spec:
            args.extend([
                # Prevent possible overriding by environment variables
                # NETCDF_ROOT, NETCDF_DIR, and NETCDF_PATH:
                self.define('NETCDF_PATH', self.spec['netcdf-c'].prefix),
                # Prevent overriding by environment variable HDF5_ROOT:
                self.define('HDF5_ROOT', self.spec['hdf5'].prefix)])

        if jp2k == 'openjpeg':
            args.append(self.define('OPENJPEG_PATH',
                                    self.spec['openjpeg'].prefix))

        if '+png' in self.spec:
            args.append(self.define('ZLIB_ROOT', self.spec['zlib'].prefix))

        if '+aec' in self.spec:
            # Prevent overriding by environment variables AEC_DIR and AEC_PATH:
            args.append(self.define('AEC_DIR', self.spec['libaec'].prefix))

        if '^python' in self.spec:
            args.append(self.define('PYTHON_EXECUTABLE', python.path))

        return args

    def check(self):
        # https://confluence.ecmwf.int/display/ECC/ecCodes+installation
        with working_dir(self.build_directory):
            ctest()

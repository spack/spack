# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ParallelNetcdf(AutotoolsPackage):
    """PnetCDF (Parallel netCDF) is a high-performance parallel I/O
    library for accessing files in format compatibility with Unidata's
    NetCDF, specifically the formats of CDF-1, 2, and 5.
    """

    homepage = "https://parallel-netcdf.github.io/"
    git      = "https://github.com/Parallel-NetCDF/PnetCDF"
    url      = "https://parallel-netcdf.github.io/Release/pnetcdf-1.11.0.tar.gz"
    list_url = "https://parallel-netcdf.github.io/wiki/Download.html"

    def url_for_version(self, version):
        if version >= Version('1.11.0'):
            url = "https://parallel-netcdf.github.io/Release/pnetcdf-{0}.tar.gz"
        else:
            url = "https://parallel-netcdf.github.io/Release/parallel-netcdf-{0}.tar.gz"

        return url.format(version.dotted)

    version('master', branch='master')
    version('1.12.1', sha256='56f5afaa0ddc256791c405719b6436a83b92dcd5be37fe860dea103aee8250a2')
    version('1.11.2', sha256='d2c18601b364c35b5acb0a0b46cd6e14cae456e0eb854e5c789cf65f3cd6a2a7')
    version('1.11.1', sha256='0c587b707835255126a23c104c66c9614be174843b85b897b3772a590be45779')
    version('1.11.0', sha256='a18a1a43e6c4fd7ef5827dbe90e9dcf1363b758f513af1f1356ed6c651195a9f')
    version('1.10.0', sha256='ed189228b933cfeac3b7b4f8944eb00e4ff2b72cf143365b1a77890980663a09')
    version('1.9.0',  sha256='356e1e1fae14bc6c4236ec11435cfea0ff6bde2591531a4a329f9508a01fbe98')
    version('1.8.1',  sha256='8d7d4c9c7b39bb1cbbcf087e0d726551c50f0cc30d44aed3df63daf3772c9043')
    version('1.8.0',  sha256='ac00bb2333bee96354de9d9c32d3dfdaa919d878098762f146996578b7f0ede9')
    version('1.7.0',  sha256='52f0d106c470a843c6176318141f74a21e6ece3f70ee8fe261c6b93e35f70a94')
    version('1.6.1',  sha256='8cf1af7b640475e3cc931e5fbcfe52484c5055f2fab526691933c02eda388aae')

    variant('cxx', default=True, description='Build the C++ Interface')
    variant('fortran', default=True, description='Build the Fortran Interface')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True, description='Enable shared library')

    depends_on('mpi')

    depends_on('m4', type='build')
    depends_on('autoconf', when='@master', type='build')
    depends_on('automake', when='@master', type='build')
    depends_on('libtool', when='@master', type='build')

    conflicts('+shared', when='@:1.9%nag+fortran')
    conflicts('+shared', when='@:1.8')

    patch('nag_libtool.patch', when='@1.9:1.12.1%nag')

    @property
    def libs(self):
        libraries = ['libpnetcdf']

        query_parameters = self.spec.last_query.extra_parameters

        if 'shared' in query_parameters:
            shared = True
        elif 'static' in query_parameters:
            shared = False
        else:
            shared = '+shared' in self.spec

        libs = find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

        if libs:
            return libs

        msg = 'Unable to recursively locate {0} {1} libraries in {2}'
        raise spack.error.NoLibrariesError(
            msg.format('shared' if shared else 'static',
                       self.spec.name,
                       self.spec.prefix))

    @when('@master')
    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            # We do not specify '-f' because we need to use libtool files from
            # the repository.
            autoreconf('-iv')

    def configure_args(self):
        args = ['--with-mpi=%s' % self.spec['mpi'].prefix,
                'SEQ_CC=%s' % spack_cc]

        args += self.enable_or_disable('cxx')
        args += self.enable_or_disable('fortran')

        flags = {
            'CFLAGS': [],
            'CXXFLAGS': [],
            'FFLAGS': [],
            'FCFLAGS': [],
        }

        if '+pic' in self.spec:
            flags['CFLAGS'].append(self.compiler.cc_pic_flag)
            flags['CXXFLAGS'].append(self.compiler.cxx_pic_flag)
            flags['FFLAGS'].append(self.compiler.f77_pic_flag)
            flags['FCFLAGS'].append(self.compiler.fc_pic_flag)

        # https://github.com/Parallel-NetCDF/PnetCDF/issues/61
        if self.spec.satisfies('%gcc@10:'):
            flags['FFLAGS'].append('-fallow-argument-mismatch')
            flags['FCFLAGS'].append('-fallow-argument-mismatch')

        for key, value in sorted(flags.items()):
            if value:
                args.append('{0}={1}'.format(key, ' '.join(value)))

        if self.version >= Version('1.8'):
            args.append('--enable-relax-coord-bound')

        if self.version >= Version('1.9'):
            args += self.enable_or_disable('shared')
            args.extend(['--enable-static',
                         '--disable-silent-rules'])

        if self.spec.satisfies('%nag+fortran+shared'):
            args.extend(['ac_cv_prog_fc_v=-Wl,-v',
                         'ac_cv_prog_f77_v=-Wl,-v'])

        return args

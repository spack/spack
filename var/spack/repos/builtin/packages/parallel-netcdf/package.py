# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('develop', branch='develop')
    version('master', branch='master')
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

    depends_on('mpi')

    depends_on('m4', type='build')

    # See:
    # https://trac.mcs.anl.gov/projects/parallel-netcdf/browser/trunk/INSTALL
    def configure_args(self):
        spec = self.spec

        args = ['--with-mpi={0}'.format(spec['mpi'].prefix)]
        args.append('MPICC={0}'.format(spec['mpi'].mpicc))
        args.append('MPICXX={0}'.format(spec['mpi'].mpicxx))
        args.append('MPIF77={0}'.format(spec['mpi'].mpifc))
        args.append('MPIF90={0}'.format(spec['mpi'].mpifc))
        args.append('SEQ_CC={0}'.format(spack_cc))

        if '+pic' in spec:
            args.extend([
                'CFLAGS={0}'.format(self.compiler.pic_flag),
                'CXXFLAGS={0}'.format(self.compiler.pic_flag),
                'FFLAGS={0}'.format(self.compiler.pic_flag)
            ])

        if '~cxx' in spec:
            args.append('--disable-cxx')

        if '~fortran' in spec:
            args.append('--disable-fortran')

        if spec.satisfies('@1.8.0:'):
            args.append('--enable-relax-coord-bound')

        return args

    def install(self, spec, prefix):
        # Installation fails in parallel
        make('install', parallel=False)

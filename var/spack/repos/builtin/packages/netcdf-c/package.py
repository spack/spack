# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class NetcdfC(AutotoolsPackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    git      = "https://github.com/Unidata/netcdf-c.git"
    url      = "https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.8.1.tar.gz"

    maintainers = ['skosukhin', 'WardF']

    version('main', branch='main')
    version('4.8.1',   sha256='bc018cc30d5da402622bf76462480664c6668b55eb16ba205a0dfb8647161dd0')
    version('4.8.0',   sha256='aff58f02b1c3e91dc68f989746f652fe51ff39e6270764e484920cb8db5ad092')
    version('4.7.4',   sha256='99930ad7b3c4c1a8e8831fb061cb02b2170fc8e5ccaeda733bd99c3b9d31666b')
    version('4.7.3',   sha256='05d064a2d55147b83feff3747bea13deb77bef390cb562df4f9f9f1ce147840d')
    version('4.7.2',   sha256='7648db7bd75fdd198f7be64625af7b276067de48a49dcdfd160f1c2ddff8189c')
    version('4.7.1',   sha256='583e6b89c57037293fc3878c9181bb89151da8c6015ecea404dd426fea219b2c')
    version('4.7.0',   sha256='26d03164074363b3911ed79b7cddd045c22adf5ebaf978943db11a1d9f15e9d3')
    version('4.6.3',   sha256='734a629cdaed907201084d003cfa091806d6080eeffbd4204e7c7f73ff9d3564')
    version('4.6.2',   sha256='673936c76ae0c496f6dde7e077f5be480afc1e300adb2c200bf56fbe22e5a82a')
    version('4.6.1',   sha256='a2fabf27c72a5ee746e3843e1debbaad37cd035767eaede2045371322211eebb')
    version('4.6.0',   sha256='6d740356399aac12290650325a05aec2fe92c1905df10761b2b0100994197725')
    version('4.5.0',   sha256='f7d1cb2a82100b9bf9a1130a50bc5c7baf0de5b5022860ac3e09a0a32f83cf4a')
    # Version 4.4.1.1 is having problems in tests
    #    https://github.com/Unidata/netcdf-c/issues/343
    version('4.4.1.1', sha256='7f040a0542ed3f6d27f3002b074e509614e18d6c515b2005d1537fec01b24909')
    # Version 4.4.1 can crash on you (in real life and in tests).  See:
    #    https://github.com/Unidata/netcdf-c/issues/282
    version('4.4.1',   sha256='17599385fd76ccdced368f448f654de2ed000fece44dece9fb5d598798b4c9d6')
    version('4.4.0',   sha256='09b78b152d3fd373bee4b5738dc05c7b2f5315fe34aa2d94ee9256661119112f')
    version('4.3.3.1', sha256='f2ee78eb310637c007f001e7c18e2d773d23f3455242bde89647137b7344c2e2')
    version('4.3.3',   sha256='3f16e21bc3dfeb3973252b9addf5defb48994f84fc9c9356081f871526a680e7')

    # configure fails if curl is not installed.
    # See https://github.com/Unidata/netcdf-c/issues/1390
    patch('https://github.com/Unidata/netcdf-c/commit/e5315da1e748dc541d50796fb05233da65e86b6b.patch?full_index=1',
          sha256='c551ca2f5b6bcefa07dd7f8b7bac426a5df9861e091df1ab99167d8d401f963f',
          when='@4.7.0')
    # fix headers
    patch('https://github.com/Unidata/netcdf-c/pull/1505.patch?full_index=1',
          sha256='495b3e5beb7f074625bcec2ca76aebd339e42719e9c5ccbedbdcc4ffb81a7450',
          when='@4.7.2')
    patch('https://github.com/Unidata/netcdf-c/pull/1508.patch?full_index=1',
          sha256='19e7f31b96536928621b1c29bb6d1a57bcb7aa672cea8719acf9ac934cdd2a3e',
          when='@4.7.2')

    # See https://github.com/Unidata/netcdf-c/pull/1752
    patch('4.7.3-spectrum-mpi-pnetcdf-detect.patch', when='@4.7.3:4.7.4 +parallel-netcdf')

    # See https://github.com/Unidata/netcdf-c/pull/2293
    patch('4.8.1-no-strict-aliasing-config.patch', when='@4.8.1:')

    variant('mpi', default=True,
            description='Enable parallel I/O for netcdf-4')
    variant('parallel-netcdf', default=False,
            description='Enable parallel I/O for classic files')
    variant('hdf4', default=False, description='Enable HDF4 support')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    variant('shared', default=True, description='Enable shared library')
    variant('dap', default=False, description='Enable DAP support')
    variant('jna', default=False, description='Enable JNA support')
    variant('fsync', default=False, description='Enable fsync support')

    # It's unclear if cdmremote can be enabled if '--enable-netcdf-4' is passed
    # to the configure script. Since netcdf-4 support is mandatory we comment
    # this variant out.
    # variant('cdmremote', default=False,
    #         description='Enable CDM Remote support')

    # The patch for 4.7.0 touches configure.ac. See force_autoreconf below.
    depends_on('autoconf', type='build', when='@4.7.0,main')
    depends_on('automake', type='build', when='@4.7.0,main')
    depends_on('libtool', type='build', when='@4.7.0,main')

    depends_on("m4", type='build')
    depends_on("hdf~netcdf", when='+hdf4')

    # curl 7.18.0 or later is required:
    # http://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
    depends_on("curl@7.18.0:", when='+dap')
    # depends_on("curl@7.18.0:", when='+cdmremote')

    depends_on('parallel-netcdf', when='+parallel-netcdf')

    # We need to build with MPI wrappers if any of the two
    # parallel I/O features is enabled:
    # http://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html#build_parallel
    depends_on('mpi', when='+mpi')
    depends_on('mpi', when='+parallel-netcdf')

    # zlib 1.2.5 or later is required for netCDF-4 compression:
    # http://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
    depends_on("zlib@1.2.5:")

    # High-level API of HDF5 1.8.9 or later is required for netCDF-4 support:
    # http://www.unidata.ucar.edu/software/netcdf/docs/getting_and_building_netcdf.html
    depends_on('hdf5@1.8.9:+hl')

    # Starting version 4.4.0, it became possible to disable parallel I/O even
    # if HDF5 supports it. For previous versions of the library we need
    # HDF5 without mpi support to disable parallel I/O:
    depends_on('hdf5~mpi', when='@:4.3~mpi')

    # We need HDF5 with mpi support to enable parallel I/O.
    depends_on('hdf5+mpi', when='+mpi')

    # NetCDF 4.4.0 and prior have compatibility issues with HDF5 1.10 and later
    # https://github.com/Unidata/netcdf-c/issues/250
    depends_on('hdf5@:1.8', when='@:4.4.0')

    # The feature was introduced in version 4.1.2
    # and was removed in version 4.4.0
    # conflicts('+cdmremote', when='@:4.1.1,4.4:')

    # The features were introduced in version 4.1.0
    conflicts('+parallel-netcdf', when='@:4.0')
    conflicts('+hdf4', when='@:4.0')

    @property
    def force_autoreconf(self):
        # The patch for 4.7.0 touches configure.ac.
        return self.spec.satisfies('@4.7.0')

    @when('@4.6.3:')
    def autoreconf(self, spec, prefix):
        if not os.path.exists(self.configure_abs_path):
            Executable('./bootstrap')()

    def configure_args(self):
        cflags = []
        cppflags = []
        ldflags = []
        libs = []

        config_args = ['--enable-v2',
                       '--enable-utilities',
                       '--enable-static',
                       '--enable-largefile',
                       '--enable-netcdf-4']

        config_args.extend(self.enable_or_disable('fsync'))

        # The flag was introduced in version 4.3.1
        if self.spec.satisfies('@4.3.1:'):
            config_args.append('--enable-dynamic-loading')

        config_args += self.enable_or_disable('shared')

        if '~shared' in self.spec or '+pic' in self.spec:
            # We don't have shared libraries but we still want it to be
            # possible to use this library in shared builds
            cflags.append(self.compiler.cc_pic_flag)

        config_args += self.enable_or_disable('dap')
        # config_args += self.enable_or_disable('cdmremote')

        # if '+dap' in self.spec or '+cdmremote' in self.spec:
        if '+dap' in self.spec:
            # Make sure Netcdf links against Spack's curl, otherwise it may
            # pick up system's curl, which can give link errors, e.g.:
            # undefined reference to `SSL_CTX_use_certificate_chain_file
            curl = self.spec['curl']
            curl_libs = curl.libs
            libs.append(curl_libs.link_flags)
            ldflags.append(curl_libs.search_flags)
            # TODO: figure out how to get correct flags via headers.cpp_flags
            cppflags.append('-I' + curl.prefix.include)
        elif self.spec.satisfies('@4.8.0:'):
            # Prevent overlinking to a system installation of libcurl:
            config_args.append('ac_cv_lib_curl_curl_easy_setopt=no')

        if self.spec.satisfies('@4.4:'):
            if '+mpi' in self.spec:
                config_args.append('--enable-parallel4')
            else:
                config_args.append('--disable-parallel4')

        if self.spec.satisfies('@4.3.2:'):
            config_args += self.enable_or_disable('jna')

        # Starting version 4.1.3, --with-hdf5= and other such configure options
        # are removed. Variables CPPFLAGS, LDFLAGS, and LD_LIBRARY_PATH must be
        # used instead.
        hdf5_hl = self.spec['hdf5:hl']
        cppflags.append(hdf5_hl.headers.cpp_flags)
        ldflags.append(hdf5_hl.libs.search_flags)
        if hdf5_hl.satisfies('~shared'):
            libs.append(hdf5_hl.libs.link_flags)

        if '+parallel-netcdf' in self.spec:
            config_args.append('--enable-pnetcdf')
            pnetcdf = self.spec['parallel-netcdf']
            cppflags.append(pnetcdf.headers.cpp_flags)
            # TODO: change to pnetcdf.libs.search_flags once 'parallel-netcdf'
            # package gets custom implementation of 'libs'
            ldflags.append('-L' + pnetcdf.prefix.lib)
        else:
            config_args.append('--disable-pnetcdf')

        if '+mpi' in self.spec or '+parallel-netcdf' in self.spec:
            config_args.append('CC=%s' % self.spec['mpi'].mpicc)

        config_args += self.enable_or_disable('hdf4')
        if '+hdf4' in self.spec:
            hdf4 = self.spec['hdf']
            cppflags.append(hdf4.headers.cpp_flags)
            # TODO: change to hdf4.libs.search_flags once 'hdf'
            # package gets custom implementation of 'libs' property.
            ldflags.append('-L' + hdf4.prefix.lib)
            # TODO: change to self.spec['jpeg'].libs.link_flags once the
            # implementations of 'jpeg' virtual package get 'jpeg_libs'
            # property.
            libs.append('-ljpeg')
            if '+szip' in hdf4:
                # This should also come from hdf4.libs
                libs.append('-lsz')
            if '+external-xdr' in hdf4 and hdf4['rpc'].name != 'libc':
                libs.append(hdf4['rpc'].libs.link_flags)

        # Fortran support
        # In version 4.2+, NetCDF-C and NetCDF-Fortran have split.
        # Use the netcdf-fortran package to install Fortran support.

        config_args.append('CFLAGS=' + ' '.join(cflags))
        config_args.append('CPPFLAGS=' + ' '.join(cppflags))
        config_args.append('LDFLAGS=' + ' '.join(ldflags))
        config_args.append('LIBS=' + ' '.join(libs))

        return config_args

    def check(self):
        # h5_test fails when run in parallel
        make('check', parallel=False)

    @property
    def libs(self):
        shared = '+shared' in self.spec
        return find_libraries(
            'libnetcdf', root=self.prefix, shared=shared, recursive=True
        )

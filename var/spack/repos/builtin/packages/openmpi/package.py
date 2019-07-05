# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys
import llnl.util.tty as tty


def _verbs_dir():
    """Try to find the directory where the OpenFabrics verbs package is
    installed. Return None if not found.
    """
    try:
        # Try to locate Verbs by looking for a utility in the path
        ibv_devices = which("ibv_devices")
        # Run it (silently) to ensure it works
        ibv_devices(output=str, error=str)
        # Get path to executable
        path = ibv_devices.exe[0]
        # Remove executable name and "bin" directory
        path = os.path.dirname(path)
        path = os.path.dirname(path)
        # There's usually no "/include" on Unix; use "/usr/include" instead
        if path == "/":
            path = "/usr"
        return path
    except TypeError:
        return None
    except ProcessError:
        return None


def _mxm_dir():
    """Look for default directory where the Mellanox package is
    installed. Return None if not found.
    """
    # Only using default directory; make this more flexible in the future
    path = "/opt/mellanox/mxm"
    if os.path.isdir(path):
        return path
    else:
        return None


def _tm_dir():
    """Look for default directory where the PBS/TM package is
    installed. Return None if not found.
    """
    # /opt/pbs from PBS 18+; make this more flexible in the future
    paths_list = ("/opt/pbs", )
    for path in paths_list:
        if os.path.isdir(path) and os.path.isfile(path + "/include/tm.h"):
            return path
    return None


class Openmpi(AutotoolsPackage):
    """An open source Message Passing Interface implementation.

    The Open MPI Project is an open source Message Passing Interface
    implementation that is developed and maintained by a consortium
    of academic, research, and industry partners. Open MPI is
    therefore able to combine the expertise, technologies, and
    resources from all across the High Performance Computing
    community in order to build the best MPI library available.
    Open MPI offers advantages for system and software vendors,
    application developers and computer science researchers.
    """

    homepage = "http://www.open-mpi.org"
    url = "https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.0.tar.bz2"
    list_url = "http://www.open-mpi.org/software/ompi/"
    git = "https://github.com/open-mpi/ompi.git"

    version('develop', branch='master')

    # Current
    version('4.0.1', sha256='cce7b6d20522849301727f81282201d609553103ac0b09162cf28d102efb9709')  # libmpi.so.40.20.1

    # Still supported
    version('4.0.0', sha256='2f0b8a36cfeb7354b45dda3c5425ef8393c9b04115570b615213faaa3f97366b')  # libmpi.so.40.20.0
    version('3.1.4', preferred=True, sha256='957b5547bc61fd53d08af0713d0eaa5cd6ee3d58')  # libmpi.so.40.10.4
    version('3.1.3', sha256='8be04307c00f51401d3fb9d837321781ea7c79f2a5a4a2e5d4eaedc874087ab6')  # libmpi.so.40.10.3
    version('3.1.2', sha256='c654ed847f34a278c52a15c98add40402b4a90f0c540779f1ae6c489af8a76c5')  # libmpi.so.40.10.2
    version('3.1.1', sha256='3f11b648dd18a8b878d057e9777f2c43bf78297751ad77ae2cef6db0fe80c77c')  # libmpi.so.40.10.1
    version('3.1.0', sha256='b25c044124cc859c0b4e6e825574f9439a51683af1950f6acda1951f5ccdf06c')  # libmpi.so.40.10.0
    version('3.0.4', sha256='2ff4db1d3e1860785295ab95b03a2c0f23420cda7c1ae845c419401508a3c7b5')  # libmpi.so.40.00.5
    version('3.0.3', sha256='fb228e42893fe6a912841a94cd8a0c06c517701ae505b73072409218a12cf066')  # libmpi.so.40.00.4
    version('3.0.2', sha256='d2eea2af48c1076c53cabac0a1f12272d7470729c4e1cb8b9c2ccd1985b2fb06')  # libmpi.so.40.00.2
    version('3.0.1', sha256='663450d1ee7838b03644507e8a76edfb1fba23e601e9e0b5b2a738e54acd785d')  # libmpi.so.40.00.1
    version('3.0.0', sha256='f699bff21db0125d8cccfe79518b77641cd83628725a1e1ed3e45633496a82d7')  # libmpi.so.40.00.0

    version('2.1.6', sha256='98b8e1b8597bbec586a0da79fcd54a405388190247aa04d48e8c40944d4ca86e')  # libmpi.so.20.10.3
    version('2.1.5', sha256='b807ccab801f27c3159a5edf29051cd3331d3792648919f9c4cee48e987e7794')  # libmpi.so.20.10.3
    version('2.1.4', sha256='3e03695ca8bd663bc2d89eda343c92bb3d4fc79126b178f5ddcb68a8796b24e2')  # libmpi.so.20.10.3
    version('2.1.3', sha256='285b3e2a69ed670415524474496043ecc61498f2c63feb48575f8469354d79e8')  # libmpi.so.20.10.2
    version('2.1.2', sha256='3cc5804984c5329bdf88effc44f2971ed244a29b256e0011b8deda02178dd635')  # libmpi.so.20.10.2
    version('2.1.1', sha256='bd7badd4ff3afa448c0d7f3ca0ee6ce003b957e9954aa87d8e4435759b5e4d16')  # libmpi.so.20.10.1
    version('2.1.0', sha256='b169e15f5af81bf3572db764417670f508c0df37ce86ff50deb56bd3acb43957')  # libmpi.so.20.10.0

    # Retired
    version('2.0.4', sha256='4f82d5f7f294becbd737319f74801206b08378188a95b70abe706fdc77a0c20b')  # libmpi.so.20.0.4
    version('2.0.3', sha256='b52c0204c0e5954c9c57d383bb22b4181c09934f97783292927394d29f2a808a')  # libmpi.so.20.0.3
    version('2.0.2', sha256='cae396e643f9f91f0a795f8d8694adf7bacfb16f967c22fb39e9e28d477730d3')  # libmpi.so.20.0.2
    version('2.0.1', sha256='fed74f4ae619b7ebcc18150bb5bdb65e273e14a8c094e78a3fea0df59b9ff8ff')  # libmpi.so.20.0.1
    version('2.0.0', sha256='08b64cf8e3e5f50a50b4e5655f2b83b54653787bd549b72607d9312be44c18e0')  # libmpi.so.20.0.0

    version('1.10.7', 'c87c613f9acb1a4eee21fa1ac8042579')  # libmpi.so.12.0.7
    version('1.10.6', '2e65008c1867b1f47c32f9f814d41706')  # libmpi.so.12.0.6
    version('1.10.5', 'd32ba9530a869d9c1eae930882ea1834')  # libmpi.so.12.0.5
    version('1.10.4', '9d2375835c5bc5c184ecdeb76c7c78ac')  # libmpi.so.12.0.4
    version('1.10.3', 'e2fe4513200e2aaa1500b762342c674b')  # libmpi.so.12.0.3
    version('1.10.2', 'b2f43d9635d2d52826e5ef9feb97fd4c')  # libmpi.so.12.0.2
    version('1.10.1', 'f0fcd77ed345b7eafb431968124ba16e')  # libmpi.so.12.0.1
    version('1.10.0', '280cf952de68369cebaca886c5ce0304')  # libmpi.so.12.0.0

    version('1.8.8', '0dab8e602372da1425e9242ae37faf8c')  # libmpi.so.1.6.3
    version('1.8.7', '2485ed6fa0fab9bb5b4e7a9f63718630')  # libmpi.so.1.6.2
    version('1.8.6', 'eb569e7dc97eeaa5b1876cccf114f377')  # libmpi.so.1.6.1
    version('1.8.5', '93e958914ff0e4d9634d668d2d48c793')  # libmpi.so.1.6.0
    version('1.8.4', '93b7ea2c4ebae76947f942579608ae4a')  # libmpi.so.1.6.0
    version('1.8.3', '2067d00853e0c33d498153fc7d268d2b')  # libmpi.so.1.6.0
    version('1.8.2', '339a9fc199563bacbb359875ce8c9e20')  # libmpi.so.1.5.2
    version('1.8.1', '0e12c24a28a605f681ff9a19a1aca2f1')  # libmpi.so.1.5.0
    version('1.8',   '5999cfb177a50c480b5d0bced379aff1')  # libmpi.so.1.5.0

    version('1.7.5', '321ab81147ac69a5bbca72652fb3b468')  # libmpi.so.1.4.0
    version('1.7.4', '4aea4fb00f8956dd56ccf50e5784e03f')  # libmpi.so.1.3.0
    version('1.7.3', '7d0779f73c43eb1d098ad037d60649bc')  # libmpi.so.1.2.0
    version('1.7.2', 'b897b92100bd13b367e651df483421d5')  # libmpi.so.1.1.2
    version('1.7.1', 'f25b446a9dcbbd6a105a99d926d34441')  # libmpi.so.1.1.1
    version('1.7',   'c0e3c4b3bfcd8b8bbd027f6f4c164acb')  # libmpi.so.1.1.0

    version('1.6.5', '03aed2a4aa4d0b27196962a2a65fc475')  # libmpi.so.1.0.8
    version('1.6.4', '62119579ab92b2592cd96b6a9d2a8cc3')  # libmpi.so.1.0.7
    version('1.6.3', 'eedb73155a7a40b0b07718494298fb25')  # libmpi.so.1.0.6
    version('1.6.2', '219754715a8e40beb468bbc8f0b3251a')  # libmpi.so.1.0.3
    version('1.6.1', '33d2782c20ff6be79130a703b85da8f0')  # libmpi.so.1.0.3
    version('1.6',   'dd6f5bd4b3cb14d93bbf530e50e46e60')  # libmpi.so.1.0.3

    # Ancient
    version('1.5.5', 'f882fd61ff89db856bfd8f0dfa42e1bd')  # libmpi.so.1.0.3
    version('1.5.4', '51153d794c49ce6d275dba2793ab0c68')  # libmpi.so.1.0.2
    version('1.5.3', '0eb8ec2aa05c74a4bc7602b01847131e')  # libmpi.so.1.0.1
    version('1.5.2', 'faaee6a2777bf607d7fa1297c0b3a9ed')  # libmpi.so.1.0.1
    version('1.5.1', '3f9409f5d3b617c04dea48ba8fbd703a')  # libmpi.so.1.0.0
    version('1.5',   '86bf5f9ef7337231abbca3350b31f112')  # libmpi.so.1.0.0

    version('1.4.5', '84ddd2772f46d35da79e1db8a274c99d')  # libmpi.so.0.0.4
    version('1.4.4', 'e58a1ea7b8af62453aaa0ddaee5f26a0')  # libmpi.so.0.0.3
    version('1.4.3', 'd2ead141c43b915343f5c5a18f3b5016')  # libmpi.so.0.0.2
    version('1.4.2', '53b26fa2586aedaf73cf40effbfcc2f3')  # libmpi.so.0.0.2
    version('1.4.1', '28a820c85e02973809df881fdeddd15e')  # libmpi.so.0.0.1
    version('1.4',   '9786ec0698afed9498ce43dc3978a435')  # libmpi.so.0.0.1

    version('1.3.4', '978c29f3b671856daa0fc67459b73e01')  # libmpi.so.0.0.1
    version('1.3.3', 'f6cdc9c195daa8571b2e509e952d6755')  # libmpi.so.0.0.0
    version('1.3.2', '75781dc31255cd841701c065e239d994')  # libmpi.so.0.0.0
    version('1.3.1', 'd759523b0752139872c534714d641d64')  # libmpi.so.0.0.0
    version('1.3',   'efbba7d652d1e430d456f65d7a2e339b')  # libmpi.so.0.0.0

    version('1.2.9', '78c2aebbb746610ed12bdedcc2b6ec0e')  # libmpi.so.0.0.0
    version('1.2.8', '7f2d5af02101c5f01173f4f6de296549')  # libmpi.so.0.0.0
    version('1.2.7', 'b5ae3059fba71eba4a89a2923da8223f')  # libmpi.so.0.0.0
    version('1.2.6', 'f126793b68e71f5ec4a192c40675af2d')  # libmpi.so.0.0.0
    version('1.2.5', 'c6e82aab6cdcd425bf29217e8317d7dc')  # libmpi.so.0.0.0
    version('1.2.4', '311b38c597f54d8d6b277225ef458666')  # libmpi.so.0.0.0
    version('1.2.3', 'ae980bb00f9686934a1143701cc041e4')  # libmpi.so.0.0.0
    version('1.2.2', '7f553317e388c4efe479e908b66f910d')  # libmpi.so.0.0.0
    version('1.2.1', 'ceaa42891edba2324a94fdd0b87e46ca')  # libmpi.so.0.0.0
    version('1.2',   '37e8d4edad54a8d8c3127fbef87ebda1')  # libmpi.so.0.0.0

    version('1.1.5', '6aada92896a1830ece6d3ba1e66a17fa')  # libmpi.so.0.0.0
    version('1.1.4', '28940b182156478fa442397b0c9660e1')  # libmpi.so.0.0.0
    version('1.1.3', 'bbaa7fe9d556212d877d872544a31569')  # libmpi.so.0.0.0
    version('1.1.2', '53877ec8bca5f6e505496b6b94b1d850')  # libmpi.so.0.0.0
    version('1.1.1', '498b9322ae0ad512026a008a30c7e0b5')  # libmpi.so.0.0.0
    version('1.1',   '821af8bbb7a8e85ec707cb4c3b6bcbf6')  # libmpi.so.0.0.0

    version('1.0.2', 'fd32861d643f9fe539a01d0d5b836f41')  # libmpi.so.0.0.0
    version('1.0.1', '8abccca5cdddc81a6d9d9e22b3bb6db9')  # libmpi.so.0.0.0
    version('1.0',   'f5dcb5d3a98f2e5a9c2a0caaef54d806')  # libmpi.so.0.0.0

    patch('ad_lustre_rwcontig_open_source.patch', when="@1.6.5")
    patch('llnl-platforms.patch', when="@1.6.5")
    patch('configure.patch', when="@1.10.1")
    patch('fix_multidef_pmi_class.patch', when="@2.0.0:2.0.1")

    # Vader Bug: https://github.com/open-mpi/ompi/issues/5375
    # Haven't release fix for 2.1.x
    patch('btl_vader.patch', when='@2.1.3:2.1.5')

    # Fixed in 3.0.3 and 3.1.3
    patch('btl_vader.patch', when='@3.0.1:3.0.2')
    patch('btl_vader.patch', when='@3.1.0:3.1.2')

    variant(
        'fabrics',
        values=disjoint_sets(
            ('auto',), ('psm', 'psm2', 'verbs', 'mxm', 'ucx', 'libfabric')
        ).with_non_feature_values('auto', 'none'),
        description="List of fabrics that are enabled; "
        "'auto' lets openmpi determine",
    )

    variant(
        'schedulers',
        values=disjoint_sets(
            ('auto',), ('alps', 'lsf', 'tm', 'slurm', 'sge', 'loadleveler')
        ).with_non_feature_values('auto', 'none'),
        description="List of schedulers for which support is enabled; "
        "'auto' lets openmpi determine",
    )

    # Additional support options
    variant('java', default=False, description='Build Java support')
    variant('sqlite3', default=False, description='Build SQLite3 support')
    variant('vt', default=True, description='Build VampirTrace support')
    variant('thread_multiple', default=False,
            description='Enable MPI_THREAD_MULTIPLE support')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('pmi', default=False, description='Enable PMI support')
    variant('cxx_exceptions', default=True, description='Enable C++ Exception support')
    # Adding support to build a debug version of OpenMPI that activates
    # Memchecker, as described here:
    #
    # https://www.open-mpi.org/faq/?category=debugging#memchecker_what
    #
    # This option degrades run-time support, and thus is disabled by default
    variant(
        'memchecker',
        default=False,
        description='Memchecker support for debugging [degrades performance]'
    )

    variant(
        'legacylaunchers',
        default=False,
        description='Do not remove mpirun/mpiexec when building with slurm'
    )

    provides('mpi')
    provides('mpi@:2.2', when='@1.6.5')
    provides('mpi@:3.0', when='@1.7.5:')
    provides('mpi@:3.1', when='@2.0.0:')

    if sys.platform != 'darwin':
        depends_on('numactl')

    depends_on('autoconf', type='build', when='@develop')
    depends_on('automake', type='build', when='@develop')
    depends_on('libtool',  type='build', when='@develop')
    depends_on('m4',       type='build', when='@develop')
    depends_on('perl',     type='build', when='@develop')

    depends_on('hwloc')
    # ompi@:3.0.0 doesn't support newer hwloc releases:
    # "configure: error: OMPI does not currently support hwloc v2 API"
    # Future ompi releases may support it, needs to be verified.
    # See #7483 for context.
    depends_on('hwloc@:1.999')

    depends_on('hwloc +cuda', when='+cuda')
    depends_on('java', when='+java')
    depends_on('sqlite', when='+sqlite3@:1.11')
    depends_on('zlib', when='@3.0.0:')
    depends_on('valgrind~mpi', when='+memchecker')
    depends_on('ucx', when='fabrics=ucx')
    depends_on('libfabric', when='fabrics=libfabric')
    depends_on('slurm', when='schedulers=slurm')
    depends_on('lsf', when='schedulers=lsf')
    depends_on('binutils+libiberty', when='fabrics=mxm')

    conflicts('+cuda', when='@:1.6')  # CUDA support was added in 1.7
    conflicts('fabrics=psm2', when='@:1.8')  # PSM2 support was added in 1.10.0
    conflicts('fabrics=mxm', when='@:1.5.3')  # MXM support was added in 1.5.4
    conflicts('+pmi', when='@:1.5.4')  # PMI support was added in 1.5.5
    conflicts('schedulers=slurm ~pmi', when='@1.5.4:',
              msg='+pmi is required for openmpi(>=1.5.5) to work with SLURM.')
    conflicts('schedulers=loadleveler', when='@3.0.0:',
              msg='The loadleveler scheduler is not supported with '
              'openmpi(>=3.0.0).')

    filter_compiler_wrappers('openmpi/*-wrapper-data*', relative_root='share')
    conflicts('fabrics=libfabric', when='@:1.8')  # libfabric support was added in 1.10.0
    # It may be worth considering making libfabric an exclusive fabrics choice

    def url_for_version(self, version):
        url = "http://www.open-mpi.org/software/ompi/v{0}/downloads/openmpi-{1}.tar.bz2"
        return url.format(version.up_to(2), version)

    @property
    def headers(self):
        hdrs = HeaderList(find(self.prefix.include, 'mpi.h', recursive=False))
        if not hdrs:
            hdrs = HeaderList(find(self.prefix, 'mpi.h', recursive=True))
        return hdrs or None

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpi_cxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpic++')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            join_path(self.prefix.lib, 'libmpi_cxx.{0}'.format(dso_suffix)),
            join_path(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def with_or_without_verbs(self, activated):
        # Up through version 1.6, this option was previously named
        # --with-openib
        opt = 'openib'
        # In version 1.7, it was renamed to be --with-verbs
        if self.spec.satisfies('@1.7:'):
            opt = 'verbs'
        # If the option has not been activated return
        # --without-openib or --without-verbs
        if not activated:
            return '--without-{0}'.format(opt)
        line = '--with-{0}'.format(opt)
        path = _verbs_dir()
        if (path is not None) and (path not in ('/usr', '/usr/local')):
            line += '={0}'.format(path)
        return line

    def with_or_without_mxm(self, activated):
        opt = 'mxm'
        # If the option has not been activated return --without-mxm
        if not activated:
            return '--without-{0}'.format(opt)
        line = '--with-{0}'.format(opt)
        path = _mxm_dir()
        if path is not None:
            line += '={0}'.format(path)
        return line

    def with_or_without_tm(self, activated):
        opt = 'tm'
        # If the option has not been activated return --without-tm
        if not activated:
            return '--without-{0}'.format(opt)
        line = '--with-{0}'.format(opt)
        path = _tm_dir()
        if path is not None:
            line += '={0}'.format(path)
        return line

    @run_before('autoreconf')
    def die_without_fortran(self):
        # Until we can pass variants such as +fortran through virtual
        # dependencies depends_on('mpi'), require Fortran compiler to
        # avoid delayed build errors in dependents.
        if (self.compiler.f77 is None) or (self.compiler.fc is None):
            raise InstallError(
                'OpenMPI requires both C and Fortran compilers!'
            )

    @when('@develop')
    def autoreconf(self, spec, prefix):
        perl = which('perl')
        perl('autogen.pl')

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-shared',
        ]

        # Add extra_rpaths dirs from compilers.yaml into link wrapper
        rpaths = [self.compiler.cc_rpath_arg + path
                  for path in self.compiler.extra_rpaths]
        config_args.extend([
            '--with-wrapper-ldflags={0}'.format(' '.join(rpaths))
        ])

        # According to this comment on github:
        #
        # https://github.com/open-mpi/ompi/issues/4338#issuecomment-383982008
        #
        # adding --enable-static silently disables slurm support via pmi/pmi2
        # for versions older than 3.0.3,3.1.3,4.0.0
        # Presumably future versions after 11/2018 should support slurm+static
        if spec.satisfies('schedulers=slurm'):
            config_args.append('--with-pmi={0}'.format(spec['slurm'].prefix))
            if spec.satisfies('@3.1.3:') or spec.satisfies('@3.0.3'):
                config_args.append('--enable-static')
        else:
            config_args.append('--enable-static')
            config_args.extend(self.with_or_without('pmi'))

        if spec.satisfies('@2.0:'):
            # for Open-MPI 2.0:, C++ bindings are disabled by default.
            config_args.extend(['--enable-mpi-cxx'])

        if spec.satisfies('@3.0.0:', strict=True):
            config_args.append('--with-zlib={0}'.format(spec['zlib'].prefix))

        # some scientific packages ignore deprecated/remove symbols. Re-enable
        # them for now, for discussion see
        # https://github.com/open-mpi/ompi/issues/6114#issuecomment-446279495
        if spec.satisfies('@4.0.1:'):
            config_args.append('--enable-mpi1-compatibility')

        # Fabrics
        if 'fabrics=auto' not in spec:
            config_args.extend(self.with_or_without('fabrics'))
        # Schedulers
        if 'schedulers=auto' not in spec:
            config_args.extend(self.with_or_without('schedulers'))

        config_args.extend(self.enable_or_disable('memchecker'))
        if spec.satisfies('+memchecker', strict=True):
            config_args.extend([
                '--enable-debug',
                '--with-valgrind={0}'.format(spec['valgrind'].prefix),
            ])

        # Hwloc support
        if spec.satisfies('@1.5.2:'):
            config_args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))

        # Java support
        if spec.satisfies('@1.7.4:'):
            if '+java' in spec:
                config_args.extend([
                    '--enable-java',
                    '--enable-mpi-java',
                    '--with-jdk-dir={0}'.format(spec['java'].home)
                ])
            else:
                config_args.extend([
                    '--disable-java',
                    '--disable-mpi-java'
                ])

        # SQLite3 support
        if spec.satisfies('@1.7.3:1.999'):
            if '+sqlite3' in spec:
                config_args.append('--with-sqlite3')
            else:
                config_args.append('--without-sqlite3')

        # VampirTrace support
        if spec.satisfies('@1.3:1.999'):
            if '+vt' not in spec:
                config_args.append('--enable-contrib-no-build=vt')

        # Multithreading support
        if spec.satisfies('@1.5.4:2.999'):
            if '+thread_multiple' in spec:
                config_args.append('--enable-mpi-thread-multiple')
            else:
                config_args.append('--disable-mpi-thread-multiple')

        # CUDA support
        # See https://www.open-mpi.org/faq/?category=buildcuda
        if spec.satisfies('@1.7:'):
            if '+cuda' in spec:
                # OpenMPI dynamically loads libcuda.so, requires dlopen
                config_args.append('--enable-dlopen')
                # Searches for header files in DIR/include
                config_args.append('--with-cuda={0}'.format(
                    spec['cuda'].prefix))
                if spec.satisfies('@1.7:1.7.2'):
                    # This option was removed from later versions
                    config_args.append('--with-cuda-libdir={0}'.format(
                        spec['cuda'].libs.directories[0]))
                if spec.satisfies('@1.7.2'):
                    # There was a bug in 1.7.2 when --enable-static is used
                    config_args.append('--enable-mca-no-build=pml-bfo')
                if spec.satisfies('%pgi^cuda@7.0:7.999'):
                    # OpenMPI has problems with CUDA 7 and PGI
                    config_args.append(
                        '--with-wrapper-cflags=-D__LP64__ -ta:tesla')
                    if spec.satisfies('%pgi@:15.8'):
                        # With PGI 15.9 and later compilers, the
                        # CFLAGS=-D__LP64__ is no longer needed.
                        config_args.append('CFLAGS=-D__LP64__')
            else:
                config_args.append('--without-cuda')

        if '+cxx_exceptions' in spec:
            config_args.append('--enable-cxx-exceptions')
        else:
            config_args.append('--disable-cxx-exceptions')
        return config_args

    @run_after('install')
    def delete_mpirun_mpiexec(self):
        # The preferred way to run an application when Slurm is the
        # scheduler is to let Slurm manage process spawning via PMI.
        #
        # Deleting the links to orterun avoids users running their
        # applications via mpirun or mpiexec, and leaves srun as the
        # only sensible choice (orterun is still present, but normal
        # users don't know about that).
        if '@1.6: ~legacylaunchers schedulers=slurm' in self.spec:
            exe_list = [self.prefix.bin.mpirun,
                        self.prefix.bin.mpiexec,
                        self.prefix.bin.shmemrun,
                        self.prefix.bin.oshrun
                        ]
            script_stub = join_path(os.path.dirname(__file__),
                                    "nolegacylaunchers.sh")
            for exe in exe_list:
                try:
                    os.remove(exe)
                except OSError:
                    tty.debug("File not present: " + exe)
                else:
                    copy(script_stub, exe)

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack import *


class Hpctoolkit(AutotoolsPackage):
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"
    git      = "https://github.com/HPCToolkit/hpctoolkit.git"
    maintainers = ['mwkrentel']

    tags = ['e4s']

    test_requires_compiler = True

    version('develop', branch='develop')
    version('master',  branch='master')

    version('2022.04.00', commit='ac18918d5038f7da30031e8e6cc23f1859d142b0')

    version('2022.01.15', commit='0238e9a052a696707e4e65b2269f342baad728ae')
    version('2021.10.15', commit='a8f289e4dc87ff98e05cfc105978c09eb2f5ea16')
    version('2021.05.15', commit='004ea0c2aea6a261e7d5d216c24f8a703fc6c408')
    version('2021.03.01', commit='68a051044c952f0f4dac459d9941875c700039e7')
    version('2020.08.03', commit='d9d13c705d81e5de38e624254cf0875cce6add9a')
    version('2020.07.21', commit='4e56c780cffc53875aca67d6472a2fb3678970eb')
    version('2020.06.12', commit='ac6ae1156e77d35596fea743ed8ae768f7222f19')
    version('2020.03.01', commit='94ede4e6fa1e05e6f080be8dc388240ea027f769')
    version('2019.12.28', commit='b4e1877ff96069fd8ed0fdf0e36283a5b4b62240')
    version('2019.08.14', commit='6ea44ed3f93ede2d0a48937f288a2d41188a277c', deprecated=True)
    version('2018.12.28', commit='8dbf0d543171ffa9885344f32f23cc6f7f6e39bc', deprecated=True)
    version('2018.11.05', commit='d0c43e39020e67095b1f1d8bb89b75f22b12aee9', deprecated=True)

    # Options for MPI and hpcprof-mpi.  We always support profiling
    # MPI applications.  These options add hpcprof-mpi, the MPI
    # version of hpcprof.  Cray and Blue Gene need separate options
    # because an MPI module in packages.yaml doesn't work on these
    # systems.
    variant('cray', default=False,
            description='Build for Cray compute nodes, including '
            'hpcprof-mpi.')

    variant('mpi', default=False,
            description='Build hpcprof-mpi, the MPI version of hpcprof.')

    # We can't build with both PAPI and perfmon for risk of segfault
    # from mismatched header files (unless PAPI installs the perfmon
    # headers).
    variant('papi', default=True,
            description='Use PAPI instead of perfmon for access to '
            'the hardware performance counters.')

    variant('all-static', default=False,
            description='Needed when MPICXX builds static binaries '
            'for the compute nodes.')

    variant('cuda', default=False,
            description='Support CUDA on NVIDIA GPUs (2020.03.01 or later).')

    variant('rocm', default=False,
            description='Support ROCM on AMD GPUs (2022.04.15 or later).')

    variant('debug', default=False,
            description='Build in debug (develop) mode.')

    variant('viewer', default=True, description='Include hpcviewer.')

    boost_libs = (
        '+atomic +chrono +date_time +filesystem +system +thread +timer'
        ' +graph +regex +shared +multithreaded visibility=global'
    )

    depends_on('binutils +libiberty', type='link', when='@2021.00:')
    depends_on('binutils +libiberty~nls', type='link', when='@2020.04:2020')
    depends_on('binutils@:2.33.1 +libiberty~nls', type='link', when='@:2020.03')
    depends_on('boost' + boost_libs)
    depends_on('bzip2+shared', type='link')
    depends_on('dyninst@12.1.0:', when='@2022.0:')
    depends_on('dyninst@10.2.0:', when='@2021.0:2021.12')
    depends_on('dyninst@9.3.2:', when='@:2020')
    depends_on('elfutils+bzip2+xz~nls', type='link')
    depends_on('gotcha@1.0.3:', when='@:2020.09')
    depends_on('intel-tbb+shared')
    depends_on('libdwarf')
    depends_on('libmonitor+hpctoolkit~dlopen', when='@2021.00:')
    depends_on('libmonitor+hpctoolkit+dlopen', when='@:2020')
    depends_on('libmonitor@2021.11.08:', when='@2022.01:')
    depends_on('libunwind@1.4: +xz+pic')
    depends_on('mbedtls+pic', when='@:2022.03')
    depends_on('xerces-c transcoder=iconv')
    depends_on('xz+pic', type='link')
    depends_on('zlib+shared')

    depends_on('cuda', when='+cuda')
    depends_on('intel-xed', when='target=x86_64:')
    depends_on('memkind', type=('build', 'run'), when='@2021.05.01:')
    depends_on('papi', when='+papi')
    depends_on('libpfm4', when='~papi')
    depends_on('mpi', when='+mpi')
    depends_on('hpcviewer', type='run', when='+viewer')

    depends_on('hip@4.5:', when='+rocm')
    depends_on('hsa-rocr-dev@4.5:', when='+rocm')
    depends_on('roctracer-dev@4.5:', when='+rocm')
    depends_on('rocprofiler-dev@4.5:', when='+rocm')

    conflicts('%gcc@:4.7', when='^dyninst@10.0.0:',
              msg='hpctoolkit requires gnu gcc 4.8.x or later')

    conflicts('%gcc@:4', when='@2020.03:2020',
              msg='hpctoolkit requires gnu gcc 5.x or later')

    conflicts('%gcc@:6', when='@2021.00:',
              msg='hpctoolkit requires gnu gcc 7.x or later')

    conflicts('+cuda', when='@:2019',
              msg='cuda requires 2020.03.01 or later')

    conflicts('+rocm', when='@:2022.03',
              msg='rocm requires 2022.04.15 or later')

    conflicts('^binutils@2.35:2.35.1',
              msg='avoid binutils 2.35 and 2.35.1 (spews errors)')

    # Fix the build for old revs with gcc 10.x.
    patch('gcc10-enum.patch', when='@2020.01.01:2020.08 %gcc@10.0:')

    patch('https://github.com/HPCToolkit/hpctoolkit/commit/511afd95b01d743edc5940c84e0079f462b2c23e.patch?full_index=1',
          sha256='c8371b929f45dafae37d2ef17880fcfb86de893beebaec501a282bc04b61ef64',
          when='@2019.08.01:2021.03 %gcc@11.0:')

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec

        args = [
            '--with-binutils=%s'     % spec['binutils'].prefix,
            '--with-boost=%s'        % spec['boost'].prefix,
            '--with-bzip=%s'         % spec['bzip2'].prefix,
            '--with-dyninst=%s'      % spec['dyninst'].prefix,
            '--with-elfutils=%s'     % spec['elfutils'].prefix,
            '--with-tbb=%s'          % spec['intel-tbb'].prefix,
            '--with-libdwarf=%s'     % spec['libdwarf'].prefix,
            '--with-libmonitor=%s'   % spec['libmonitor'].prefix,
            '--with-libunwind=%s'    % spec['libunwind'].prefix,
            '--with-xerces=%s'       % spec['xerces-c'].prefix,
            '--with-lzma=%s'         % spec['xz'].prefix,
            '--with-zlib=%s'         % spec['zlib'].prefix,
        ]

        if '+cuda' in spec:
            args.append('--with-cuda=%s' % spec['cuda'].prefix)

        if spec.satisfies('@:2020.09'):
            args.append('--with-gotcha=%s' % spec['gotcha'].prefix)

        if spec.target.family == 'x86_64':
            args.append('--with-xed=%s' % spec['intel-xed'].prefix)

        if spec.satisfies('@:2022.03'):
            args.append('--with-mbedtls=%s' % spec['mbedtls'].prefix)

        if spec.satisfies('@2021.05.01:'):
            args.append('--with-memkind=%s' % spec['memkind'].prefix)

        if spec.satisfies('+papi'):
            args.append('--with-papi=%s' % spec['papi'].prefix)
        else:
            args.append('--with-perfmon=%s' % spec['libpfm4'].prefix)

        if spec.satisfies('+rocm'):
            args.extend([
                '--with-rocm-hip=%s'    % spec['hip'].prefix,
                '--with-rocm-hsa=%s'    % spec['hsa-rocr-dev'].prefix,
                '--with-rocm-tracer=%s' % spec['roctracer-dev'].prefix,
                '--with-rocm-profiler=%s' % spec['rocprofiler-dev'].prefix,
            ])

        # MPI options for hpcprof-mpi.
        if '+cray' in spec:
            args.extend([
                '--enable-mpi-search=cray',
                '--enable-all-static',
            ])
        elif '+mpi' in spec:
            args.append('MPICXX=%s' % spec['mpi'].mpicxx)

        if '+all-static' in spec:
            args.append('--enable-all-static')

        if spec.satisfies('+debug'):
            args.append('--enable-develop')

        return args

    # We only want hpctoolkit and hpcviewer paths and man paths in the
    # module file.  The run dependencies are all curried into hpctoolkit
    # and we don't want to risk exposing a package if the application
    # uses a different version of the same package.
    def setup_run_environment(self, env):
        spec = self.spec
        env.clear()
        env.prepend_path('PATH', spec.prefix.bin)
        env.prepend_path('MANPATH', spec.prefix.share.man)
        if '+viewer' in spec:
            env.prepend_path('PATH', spec['hpcviewer'].prefix.bin)
            env.prepend_path('MANPATH', spec['hpcviewer'].prefix.share.man)

    # Build tests (spack install --run-tests).  Disable the default
    # spack tests and run autotools 'make check', but only from the
    # tests directory.
    build_time_test_callbacks = []
    install_time_test_callbacks = []

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        if self.spec.satisfies('@2022:'):
            with working_dir('tests'):
                make('check')
        else:
            tty.warn('spack test for hpctoolkit requires 2022.01.15 or later')

    # Post-Install tests (spack test run).  These are the same tests
    # but with a different Makefile that works outside the build
    # directory.
    @run_after('install')
    def copy_test_files(self):
        if self.spec.satisfies('@2022:'):
            self.cache_extra_test_sources(['tests'])

    def test(self):
        test_dir = join_path(self.test_suite.current_test_cache_dir, 'tests')
        if self.spec.satisfies('@2022:'):
            with working_dir(test_dir):
                make('-f', 'Makefile.spack', 'all')
                self.run_test('./run-sort', status=[0], installed=False,
                              purpose='selection sort unit test')
        else:
            tty.warn('spack test for hpctoolkit requires 2022.01.15 or later')

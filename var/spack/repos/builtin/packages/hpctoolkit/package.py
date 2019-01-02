# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

    version('develop', branch='master')
    version('2018.11.05', commit='d0c43e39020e67095b1f1d8bb89b75f22b12aee9')

    # We can't build with both PAPI and perfmon for risk of segfault
    # from mismatched header files (unless PAPI installs the perfmon
    # headers).
    variant('papi', default=False,
            description='Use PAPI instead of perfmon for access to '
            'the hardware performance counters.')

    # We always support profiling MPI applications.  +mpi builds
    # hpcprof-mpi, the MPI version of hpcprof.
    variant('mpi', default=False,
            description='Build hpcprof-mpi, the MPI version of hpcprof.')

    variant('all-static', default=False,
            description='Needed when MPICXX builds static binaries '
            'for the compute nodes.')

    boost_libs = '+atomic +graph +regex +serialization'  \
        '+shared +multithreaded'

    depends_on('binutils+libiberty~nls')
    depends_on('boost' + boost_libs)
    depends_on('bzip2')
    depends_on('dyninst')
    depends_on('elfutils~nls')
    depends_on('intel-tbb')
    depends_on('libdwarf')
    depends_on('libmonitor+hpctoolkit')
    depends_on('libunwind@2018.10.0:')
    depends_on('xerces-c transcoder=iconv')
    depends_on('xz')
    depends_on('zlib')

    depends_on('intel-xed', when='target=x86_64')
    depends_on('papi', when='+papi')
    depends_on('libpfm4', when='~papi')
    depends_on('mpi', when='+mpi')

    flag_handler = AutotoolsPackage.build_system_flags

    def configure_args(self):
        spec = self.spec
        target = spec.architecture.target

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

        if target == 'x86_64':
            args.append('--with-xed=%s' % spec['intel-xed'].prefix)

        if '+papi' in spec:
            args.append('--with-papi=%s' % spec['papi'].prefix)
        else:
            args.append('--with-perfmon=%s' % spec['libpfm4'].prefix)

        if '+mpi' in spec:
            args.append('MPICXX=%s' % spec['mpi'].mpicxx)

        if '+all-static' in spec:
            args.append('--enable-all-static')

        return args

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class DarshanRuntime(AutotoolsPackage):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "https://www.mcs.anl.gov/research/projects/darshan/"
    url      = "https://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"
    git      = "https://github.com/darshan-hpc/darshan.git"

    maintainers = ['shanedsnyder', 'carns']

    tags = ['e4s']
    test_requires_compiler = True

    version('main', branch='main', submodules=True)
    version('3.3.1', sha256='281d871335977d0592a49d053df93d68ce1840f6fdec27fea7a59586a84395f7')
    version('3.3.0', sha256='2e8bccf28acfa9f9394f2084ec18122c66e45d966087fa2e533928e824fcb57a')
    version('3.3.0-pre2', sha256='0fc09f86f935132b7b05df981b05cdb3796a1ea02c7acd1905323691df65e761')
    version('3.3.0-pre1', sha256='1c655359455b5122921091bab9961491be58a5f0158f073d09fe8cc772bd0812')
    version('3.2.1', sha256='d63048b7a3d1c4de939875943e3e7a2468a9034fcb68585edbc87f57f622e7f7')
    version('3.2.0', sha256='4035435bdc0fa2a678247fbf8d5a31dfeb3a133baf06577786b1fe8d00a31b7e')
    version('3.1.8', sha256='3ed51c8d5d93b4a8cbb7d53d13052140a9dffe0bc1a3e1ebfc44a36a184b5c82')
    version('3.1.7', sha256='9ba535df292727ac1e8025bdf2dc42942715205cad8319d925723fd88709e8d6')
    version('3.1.6', sha256='21cb24e2a971c45e04476e00441b7fbea63d2afa727a5cf8b7a4a9d9004dd856')
    version('3.1.0', sha256='b847047c76759054577823fbe21075cfabb478cdafad341d480274fb1cef861c')
    version('3.0.0', sha256='95232710f5631bbf665964c0650df729c48104494e887442596128d189da43e0')

    depends_on('mpi', when='+mpi')
    depends_on('zlib')
    depends_on('hdf5', when='+hdf5')
    depends_on('papi', when='+apxc')
    depends_on('autoconf', type='build', when='@main')
    depends_on('automake', type='build', when='@main')
    depends_on('libtool',  type='build', when='@main')
    depends_on('m4',       type='build', when='@main')

    variant('mpi', default=True, description='Compile with MPI support')
    variant('hdf5', default=False, description='Compile with HDF5 module')
    variant('apmpi', default=False, description='Compile with AutoPerf MPI module')
    variant('apmpi_sync', default=False, description='Compile with AutoPerf MPI module (with collective synchronization timing)')
    variant('apxc', default=False, description='Compile with AutoPerf XC module')
    variant(
        'scheduler',
        default='NONE',
        description='queue system scheduler JOB ID',
        values=('NONE', 'cobalt', 'pbs', 'sge', 'slurm'),
        multi=False
    )

    conflicts('+hdf5', when='@:3.1.8',
              msg='+hdf5 variant only available starting from version 3.2.0')
    conflicts('+apmpi', when='@:3.2.1',
              msg='+apmpi variant only available starting from version 3.3.0')
    conflicts('+apmpi_sync', when='@:3.2.1',
              msg='+apmpi variant only available starting from version 3.3.0')
    conflicts('+apxc', when='@:3.2.1',
              msg='+apxc variant only available starting from version 3.3.0')

    @property
    def configure_directory(self):
        return 'darshan-runtime'

    def configure_args(self):
        spec = self.spec
        extra_args = []

        job_id = 'NONE'
        if '+slurm' in spec:
            job_id = 'SLURM_JOBID'
        if '+cobalt' in spec:
            job_id = 'COBALT_JOBID'
        if '+pbs' in spec:
            job_id = 'PBS_JOBID'
        if '+sge' in spec:
            job_id = 'JOB_ID'

        if '+hdf5' in spec:
            if self.version < Version('3.3.2'):
                extra_args.append('--enable-hdf5-mod=%s' % spec['hdf5'].prefix)
            else:
                extra_args.append('--enable-hdf5-mod')
        if '+apmpi' in spec:
            extra_args.append('--enable-apmpi-mod')
        if '+apmpi_sync' in spec:
            extra_args.append(['--enable-apmpi-mod',
                               '--enable-apmpi-coll-sync'])
        if '+apxc' in spec:
            extra_args.append(['--enable-apxc-mod'])

        extra_args.append('--with-mem-align=8')
        extra_args.append('--with-log-path-by-env=DARSHAN_LOG_DIR_PATH')
        extra_args.append('--with-jobid-env=%s' % job_id)
        extra_args.append('--with-zlib=%s' % spec['zlib'].prefix)

        if '+mpi' in spec:
            extra_args.append('CC=%s' % self.spec['mpi'].mpicc)
        else:
            extra_args.append('CC=%s' % self.compiler.cc)
            extra_args.append('--without-mpi')

        return extra_args

    def setup_run_environment(self, env):
        # default path for log file, could be user or site specific setting
        darshan_log_dir = os.environ['HOME']
        env.set('DARSHAN_LOG_DIR_PATH', darshan_log_dir)

    @property
    def basepath(self):
        return join_path('darshan-test',
                         join_path('regression',
                                   join_path('test-cases', 'src')))

    @run_after('install')
    def _copy_test_inputs(self):
        test_inputs = [
            join_path(self.basepath, 'mpi-io-test.c')]
        self.cache_extra_test_sources(test_inputs)

    def _test_intercept(self):
        testdir = "intercept-test"
        with working_dir(testdir, create=True):
            if '+mpi' in self.spec:
                # compile a test program
                logname = join_path(os.getcwd(), "test.darshan")
                fname = join_path(self.test_suite.current_test_cache_dir,
                                  join_path(self.basepath, 'mpi-io-test.c'))
                cc = Executable(self.spec['mpi'].mpicc)
                compile_opt = ['-c', fname]
                link_opt = ['-o', "mpi-io-test", 'mpi-io-test.o']
                cc(*(compile_opt))
                cc(*(link_opt))

                # run test program and intercept
                purpose = "Test running code built against darshan"
                exe = "./mpi-io-test"
                options = ['-f', 'tmp.dat']
                status = [0]
                installed = False
                expected_output = [r"Write bandwidth = \d+.\d+ Mbytes/sec",
                                   r"Read bandwidth = \d+.\d+ Mbytes/sec"]
                env['LD_PRELOAD'] = 'libdarshan.so'
                env['DARSHAN_LOGFILE'] = logname
                self.run_test(exe,
                              options,
                              expected_output,
                              status,
                              installed,
                              purpose,
                              skip_missing=False,
                              work_dir=None)
                env.pop('LD_PRELOAD')

                import llnl.util.tty as tty

                # verify existence of log and size is > 0
                tty.msg("Test for existince of log:")
                if os.path.exists(logname):
                    sr = os.stat(logname)
                    print("PASSED")
                    tty.msg("Test for size of log:")
                    if not sr.st_size > 0:
                        exc = BaseException('log size is 0')
                        m = None
                        if spack.config.get('config:fail_fast', False):
                            raise TestFailure([(exc, m)])
                        else:
                            self.test_failures.append((exc, m))
                    else:
                        print("PASSED")
                else:
                    exc = BaseException('log does not exist')
                    m = None
                    if spack.config.get('config:fail_fast', False):
                        raise TestFailure([(exc, m)])
                    else:
                        self.test_failures.append((exc, m))

    def test(self):
        self._test_intercept()

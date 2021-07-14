# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class DarshanRuntime(Package):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url      = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"
    git      = "https://github.com/darshan-hpc/darshan.git"

    maintainers = ['shanedsnyder', 'carns']

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

    def install(self, spec, prefix):

        job_id = 'NONE'
        if '+slurm' in spec:
            job_id = 'SLURM_JOBID'
        if '+cobalt' in spec:
            job_id = 'COBALT_JOBID'
        if '+pbs' in spec:
            job_id = 'PBS_JOBID'
        if '+sge' in spec:
            job_id = 'JOB_ID'

        # TODO: BG-Q and other platform configure options
        options = []
        if '+mpi' in spec:
            options = ['CC=%s' % spec['mpi'].mpicc]
        else:
            options = ['--without-mpi']

        if '+hdf5' in spec:
            options.extend(['--enable-hdf5-mod=%s' % spec['hdf5'].prefix])

        if '+apmpi' in spec:
            options.extend(['--enable-apmpi-mod'])
        if '+apmpi_sync' in spec:
            options.extend(['--enable-apmpi-mod',
                            '--enable-apmpi-coll-sync'])
        if '+apxc' in spec:
            options.extend(['--enable-apxc-mod'])

        options.extend(['--with-mem-align=8',
                        '--with-log-path-by-env=DARSHAN_LOG_DIR_PATH',
                        '--with-jobid-env=%s' % job_id,
                        '--with-zlib=%s' % spec['zlib'].prefix])

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-runtime/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')

    def setup_run_environment(self, env):
        # default path for log file, could be user or site specific setting
        darshan_log_dir = os.environ['HOME']
        env.set('DARSHAN_LOG_DIR_PATH', darshan_log_dir)

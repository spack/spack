# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class DarshanRuntime(Package):
    """Darshan (runtime) is a scalable HPC I/O characterization tool
    designed to capture an accurate picture of application I/O behavior,
    including properties such as patterns of access within files, with
    minimum overhead. DarshanRuntime package should be installed on
    systems where you intend to instrument MPI applications."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"

    version('3.1.6', 'ce5b8f1e69d602edd4753b57258b57c1')
    version('3.1.0', '439d717323e6265b2612ed127886ae52')
    version('3.0.0', '732577fe94238936268d74d7d74ebd08')

    depends_on('mpi')
    depends_on('zlib')

    variant('slurm', default=False, description='Use Slurm Job ID')
    variant('cobalt', default=False, description='Use Coblat Job Id')
    variant('pbs', default=False, description='Use PBS Job Id')

    def install(self, spec, prefix):

        job_id = 'NONE'
        if '+slurm' in spec:
            job_id = 'SLURM_JOBID'
        if '+cobalt' in spec:
            job_id = 'COBALT_JOBID'
        if '+pbs' in spec:
            job_id = 'PBS_JOBID'

        # TODO: BG-Q and other platform configure options
        options = ['CC=%s' % spec['mpi'].mpicc,
                   '--with-mem-align=8',
                   '--with-log-path-by-env=DARSHAN_LOG_DIR_PATH',
                   '--with-jobid-env=%s' % job_id,
                   '--with-zlib=%s' % spec['zlib'].prefix]

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-runtime/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')

    def setup_environment(self, spack_env, run_env):
        # default path for log file, could be user or site specific setting
        darshan_log_dir = '%s' % os.environ['HOME']
        run_env.set('DARSHAN_LOG_DIR_PATH', darshan_log_dir)

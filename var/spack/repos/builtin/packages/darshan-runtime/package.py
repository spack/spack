##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import re


def detect_batch_system(package, make_jobs):
    """Detect from the environment if Python is running under a known batch
    system. Returns a dictionary with the following keys: 'name', 'mpiexec',
    'mpiexec_numproc_flag', and 'num_cpus'. The currently returned values for
    'name' are: 'slurm', 'lsf', or None.
    """

    bsys = {'name': None, 'mpiexec': 'mpirun',
            'mpiexec_numproc_flag': '-np', 'num_cpus': 1}

    # Check for Slurm (sbatch, srun)
    if 'SLURM_JOB_CPUS_PER_NODE' in os.environ:
        # Assert we are running on one node:
        assert('SLURM_NNODES' in os.environ)
        assert(os.environ['SLURM_NNODES'] == '1')
        bsys['name'] = 'slurm'
        bsys['mpiexec'] = 'srun'
        bsys['mpiexec_numproc_flag'] = '-n'
        # Parse SLURM_JOB_CPUS_PER_NODE which has the format:
        #    <num-cpus>{(x<num-nodes>}{,<num-cpus>{(x<num-nodes>}}
        cpn = os.environ['SLURM_JOB_CPUS_PER_NODE'].split(',')
        cpn = [re.split('(\d*)(\(x(\d*)\))?', grp) for grp in cpn]
        cpn = [int(g[1]) * (int(g[3]) if g[3] else 1) for g in cpn]
        bsys['num_cpus'] = sum(cpn)

    # Check for Moab (msub, ?)
    # TODO

    # Check for LSF (bsub, mpirun/jsrun)
    elif 'LSB_DJOB_NUMPROC' in os.environ:
        # Assert we are running on one node:
        # LSB_MCPU_HOSTS has the form: 'host01 20 host02 20 ...'
        assert('LSB_MCPU_HOSTS' in os.environ)
        assert(len(os.environ['LSB_MCPU_HOSTS'].split()) == 2)
        bsys['name'] = 'lsf'
        bsys['num_cpus'] = int(os.environ['LSB_DJOB_NUMPROC'])

    # No batch system found. Return defaults based on 'package'.
    else:
        # Another option: check for 'mpi' in package.spec and if true, set the
        # 'mpiexec' entry accordingly - e.g. we can set the full path of the
        # mpirun/mpiexec command using package.spec['mpi'].prefix.bin.
        bsys['num_cpus'] = make_jobs

    return bsys

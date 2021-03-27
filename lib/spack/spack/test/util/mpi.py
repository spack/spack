# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.filesystem as fs
import spack.util.mpi as mpi


def test_mpirunner(tmpdir):
    tmpdir_str = str(tmpdir)
    os.environ["PATH"] = tmpdir_str
    assert mpi.MPIRunner.query_mgr_pref('srun', tmpdir_str) is None

    with tmpdir.as_cwd():
        fs.touch("srun")
        fs.set_executable('srun')
        runner = mpi.MPIRunner.query_mgr_pref('srun', tmpdir_str)
        assert runner.manager == 'slurm'
        assert runner.exe is not None

        fs.touch("mpirun")
        fs.set_executable('mpirun')
        runner = mpi.MPIRunner.query_mpi_pref(tmpdir_str)
        assert runner.manager == 'mpirun'
        assert runner.exe is not None

        fs.touch("mpiexec")
        fs.set_executable('mpiexec')
        runner = mpi.MPIRunner.query_mpi_pref(tmpdir_str)
        assert runner.manager == 'mpiexec'
        assert runner.exe is not None

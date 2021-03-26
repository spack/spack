# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.util.executable import Executable, which
from llnl.util.filesystem import join_path


class MPIRunner(object):
    """ Class representing a resource manager command to run MPI-based code."""

    def __init__(self, cmd, mgr_type):
        self.exe = Executable(cmd)
        self.manager = mgr_type

    @property
    def command(self):
        """The command-line string for the resource manager.

        Returns:
            str: The executable and default arguments
        """
        return self.exe.command

    @staticmethod
    def query_mpi_pref(mpi_bin_dir):
        """Constructs a new MPIRunner object by querying the given path.

        Returns:
            MPIRunner: MPIRunner object
        """
        runner_cmd = which(join_path(mpi_bin_dir, 'mpiexec'),
                           join_path(mpi_bin_dir, 'mpirun'))
        if not runner_cmd:
            return None
        else:
            return MPIRunner(runner_cmd.command, runner_cmd.name)

    @staticmethod
    def query_mgr_pref(mgr, mpi_bin_dir):
        """Constructs a new MPIRunner object by first querying the given resource
        manager and if unsuccessful querying the given mpi path.

        Returns:
            MPIRunner: MPIRunner object
        """
        mgr_names = ['slurm']   # Add other process managers in the future
        mgr_exes = ['srun']
        mgr_sel = [p[1] for p in zip(mgr_exes, mgr_names) if p[0] == mgr][0]

        mgr_cmd = which(mgr)
        if mgr_cmd:
            return MPIRunner(mgr_cmd.command, mgr_sel)
        else:
            return MPIRunner.query_mpi_pref(mpi_bin_dir)

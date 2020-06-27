# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import os

import llnl.util.filesystem as fs

from spack.operating_systems.linux_distro import LinuxDistro
from spack.util.environment import get_path
from spack.util.module_cmd import module


@contextlib.contextmanager
def unload_programming_environment():
    """Context manager that unloads Cray Programming Environments."""
    env_bu = None

    # We rely on the fact that the PrgEnv-* modules set the PE_ENV
    # environment variable.
    if 'PE_ENV' in os.environ:
        # Copy environment variables to restore them after the compiler
        # detection. We expect that the only thing PrgEnv-* modules do is
        # the environment variables modifications.
        env_bu = os.environ.copy()

        # Get the name of the module from the environment variable.
        prg_env = 'PrgEnv-' + os.environ['PE_ENV'].lower()

        # Unload the PrgEnv-* module. By doing this we intentionally
        # provoke errors when the Cray's compiler wrappers are executed
        # (Error: A PrgEnv-* modulefile must be loaded.) so they will not
        # be detected as valid compilers by the overridden method. We also
        # expect that the modules that add the actual compilers' binaries
        # into the PATH environment variable (i.e. the following modules:
        # 'intel', 'cce', 'gcc', etc.) will also be unloaded since they are
        # specified as prerequisites in the PrgEnv-* modulefiles.
        module('unload', prg_env)

    yield

    # Restore the environment.
    if env_bu is not None:
        os.environ.clear()
        os.environ.update(env_bu)


class CrayFrontend(LinuxDistro):
    """Represents OS that runs on login and service nodes of the Cray platform.
    It acts as a regular Linux without Cray-specific modules and compiler
    wrappers."""

    @property
    def compiler_search_paths(self):
        """Calls the default function but unloads Cray's programming
        environments first.

        This prevents from detecting Cray compiler wrappers and avoids
        possible false detections.
        """
        with unload_programming_environment():
            search_paths = fs.search_paths_for_executables(*get_path('PATH'))
        return search_paths

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.operating_systems.linux_distro import LinuxDistro
from spack.util.module_cmd import module


class CrayFrontend(LinuxDistro):
    """Represents OS that runs on login and service nodes of the Cray platform.
    It acts as a regular Linux without Cray-specific modules and compiler
    wrappers."""

    def find_compilers(self, *paths):
        """Calls the overridden method but prevents it from detecting Cray
        compiler wrappers to avoid possible false detections. The detected
        compilers come into play only if a user decides to work with the Cray's
        frontend OS as if it was a regular Linux environment."""

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

        # Call the overridden method.
        clist = super(CrayFrontend, self).find_compilers(*paths)

        # Restore the environment.
        if env_bu is not None:
            os.environ.clear()
            os.environ.update(env_bu)

        return clist

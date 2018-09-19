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

from spack.operating_systems.linux_distro import LinuxDistro
from spack.util.module_cmd import get_module_cmd


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
            modulecmd = get_module_cmd()
            exec(compile(
                modulecmd('unload', prg_env, output=str, error=os.devnull),
                '<string>', 'exec'))

        # Call the overridden method.
        clist = super(CrayFrontend, self).find_compilers(*paths)

        # Restore the environment.
        if env_bu is not None:
            os.environ.clear()
            os.environ.update(env_bu)

        return clist

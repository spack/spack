# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import contextlib
import os
import re

import llnl.util.filesystem as fs
import llnl.util.lang
import llnl.util.tty as tty

from spack.util.environment import get_path
from spack.util.module_cmd import module

from .linux_distro import LinuxDistro


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
        import spack.compilers

        with unload_programming_environment():
            search_paths = get_path('PATH')

        extract_path_re = re.compile(r'prepend-path[\s]*PATH[\s]*([/\w\.:-]*)')

        for compiler_cls in spack.compilers.all_compiler_types():
            # Check if the compiler class is supported on Cray
            prg_env = getattr(compiler_cls, 'PrgEnv', None)
            compiler_module = getattr(compiler_cls, 'PrgEnv_compiler', None)
            if not (prg_env and compiler_module):
                continue

            # It is supported, check which versions are available
            output = module('avail', compiler_cls.PrgEnv_compiler)
            version_regex = r'({0})/([\d\.]+[\d]-?[\w]*)'.format(
                compiler_cls.PrgEnv_compiler
            )
            matches = re.findall(version_regex, output)
            versions = tuple(version for _, version in matches
                             if 'classic' not in version)

            # Now inspect the modules and add to paths
            msg = "[CRAY FE] Detected FE compiler [name={0}, versions={1}]"
            tty.debug(msg.format(compiler_module, versions))
            for v in versions:
                try:
                    current_module = compiler_module + '/' + v
                    out = module('show', current_module)
                    match = extract_path_re.search(out)
                    search_paths += match.group(1).split(':')
                except Exception as e:
                    msg = ("[CRAY FE] An unexpected error occurred while "
                           "detecting FE compiler [compiler={0}, "
                           " version={1}, error={2}]")
                    tty.debug(msg.format(compiler_cls.name, v, str(e)))

        search_paths = list(llnl.util.lang.dedupe(search_paths))
        return fs.search_paths_for_executables(*search_paths)

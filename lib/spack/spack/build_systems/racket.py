# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from typing import Optional

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir

from spack.build_environment import SPACK_NO_PARALLEL_MAKE, determine_number_of_jobs
from spack.directives import extends
from spack.package_base import PackageBase
from spack.util.environment import env_flag
from spack.util.executable import Executable, ProcessError


class RacketPackage(PackageBase):
    """Specialized class for packages that are built using Racket's
    `raco pkg install` and `raco setup` commands.

    This class provides the following phases that can be overridden:

    * install
    * setup
    """
    #: Package name, version, and extension on PyPI
    maintainers = ['elfprince13']

    # Default phases
    phases = ['install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'RacketPackage'

    extends('racket')

    pkgs = False
    subdirectory = None  # type: Optional[str]
    name = None  # type: Optional[str]
    parallel = True

    @property
    def homepage(self):
        if self.pkgs:
            return 'https://pkgs.racket-lang.org/package/{0}'.format(self.name)

    @property
    def build_directory(self):
        ret = os.getcwd()
        if self.subdirectory:
            ret = os.path.join(ret, self.subdirectory)
        return ret

    def install(self, spec, prefix):
        """Install everything from build directory."""
        raco = Executable("raco")
        with working_dir(self.build_directory):
            allow_parallel = self.parallel and (not env_flag(SPACK_NO_PARALLEL_MAKE))
            args = ['pkg', 'install', '-t', 'dir', '-n', self.name, '--deps', 'fail',
                    '--ignore-implies', '--copy', '-i', '-j',
                    str(determine_number_of_jobs(allow_parallel)),
                    '--', os.getcwd()]
            try:
                raco(*args)
            except ProcessError:
                args.insert(-2, "--skip-installed")
                raco(*args)
                tty.warn(("Racket package {0} was already installed, uninstalling via "
                          "Spack may make someone unhappy!").format(self.name))

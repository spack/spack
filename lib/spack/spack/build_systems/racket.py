# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import re
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import (
    filter_file,
    find,
    get_filetype,
    path_contains_subdirectory,
    same_path,
    working_dir,
)
from llnl.util.lang import match_predicate

from spack.directives import extends
from spack.package import PackageBase, run_after
from spack.util.executable import Executable, ProcessError
from spack.util.environment import env_flag
from spack.build_environment import determine_number_of_jobs, SPACK_NO_PARALLEL_MAKE


class RacketPackage(PackageBase):
    """Specialized class for packages that are built using Racket's `raco pkg install` and `raco setup` commands.

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
    subdirectory = None
    name = None
    parallel = True

    @property
    def homepage(self):
        if self.pkgs:
            return 'https://pkgs.racket-lang.org/package/{0}'.format(self.name)

    @property
    def build_directory(self):
        return (os.path.join(os.getcwd(), self.subdirectory) if self.subdirectory else os.getcwd())

    def install(self, spec, prefix):
        """Install everything from build directory."""
        raco = Executable("raco")
        with working_dir(self.build_directory):
            args = ['pkg', 'install', '-t', 'dir', '-n', self.name, '--deps', 'fail',
                 '--ignore-implies', '--copy', '-i', '-j', str(determine_number_of_jobs(self.parallel and (not env_flag(SPACK_NO_PARALLEL_MAKE)))),
                 '--', os.getcwd()]
            try:
                raco(*args)
            except ProcessError:
                args.insert(-2, "--skip-installed")
                raco(*args)
                tty.warn("Racket package {0} was already installed, uninstalling via Spack may make someone unhappy!".format(self.name))
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

import inspect

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir
from spack.package import PackageBase, run_after


class MakefilePackage(PackageBase):
    """Specialized class for packages that are built using editable Makefiles

    This class provides three phases that can be overridden:

        1. :py:meth:`~.MakefilePackage.edit`
        2. :py:meth:`~.MakefilePackage.build`
        3. :py:meth:`~.MakefilePackage.install`

    It is usually necessary to override the :py:meth:`~.MakefilePackage.edit`
    phase, while :py:meth:`~.MakefilePackage.build` and
    :py:meth:`~.MakefilePackage.install` have sensible defaults.
    For a finer tuning you may override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.MakefilePackage.build_targets`    | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.MakefilePackage.install_targets`  | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.MakefilePackage.build_directory`  | Directory where the|
        |                                               | Makefile is located|
        +-----------------------------------------------+--------------------+
    """
    #: Phases of a package that is built with an hand-written Makefile
    phases = ['edit', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'MakefilePackage'

    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.build`
    #: phase
    build_targets = []
    #: Targets for ``make`` during the :py:meth:`~.MakefilePackage.install`
    #: phase
    install_targets = ['install']

    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def edit(self, spec, prefix):
        """Edits the Makefile before calling make. This phase cannot
        be defaulted.
        """
        tty.msg('Using default implementation: skipping edit phase.')

    def build(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.build_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Calls make, passing :py:attr:`~.MakefilePackage.install_targets`
        as targets.
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

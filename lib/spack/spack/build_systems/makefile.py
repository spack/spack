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
from spack.package import PackageBase


class MakefilePackage(PackageBase):
    """Specialized class for packages that are built using editable Makefiles

    This class provides three phases that can be overridden:

    * edit
    * build
    * install

    It is necessary to override the 'edit' phase, while 'build' and 'install'
    have sensible defaults.
    """
    phases = ['edit', 'build', 'install']
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'MakefilePackage'

    build_targets = []
    install_targets = ['install']

    def build_directory(self):
        """Directory where the main Makefile is located"""
        return self.stage.source_path

    def edit(self, spec, prefix):
        """This phase cannot be defaulted for obvious reasons..."""
        tty.msg('Using default implementation: skipping edit phase.')

    def build(self, spec, prefix):
        """Make the build targets"""
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.install_targets)

    # Check that self.prefix is there after installation
    PackageBase.sanity_check('install')(PackageBase.sanity_check_prefix)

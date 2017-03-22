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

from spack.directives import extends
from spack.package import PackageBase, run_after, InstallError
from spack.util.executable import Executable

import os


class PerlPackage(PackageBase):
    """Specialized class for packages that are built using Perl

    This class provides a single phase that can be overridden:

        1. :py:meth:`~.PerlPackage.install`

    It has sensible defaults, and for many packages the only thing
    necessary will be to add dependencies
    """
    phases = ['install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'PerlPackage'

    extends('perl')

    def install(self, spec, prefix):
        """Installs a Perl package."""
        perlx = inspect.getmodule(self).perl
        if os.path.isfile('Makefile.PL'):
            makex = inspect.getmodule(self).make
            perlx('Makefile.PL', 'INSTALL_BASE=%s' % self.prefix)
            makex()
            if self.run_tests:
                makex('test')
            makex('install')
        elif os.path.isfile('Build.PL'):
            perlx('Build.PL', '--install_base', '%s' % self.prefix)
            Buildx = Executable('./Build')
            Buildx()
            if self.run_tests:
                Buildx('test')
            Buildx('install')
        else:
            raise InstallError('Unknown install method for perl package')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

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
from spack.package import PackageBase, run_after


class RPackage(PackageBase):
    """Specialized class for packages that are built using R

    This class provides a single phase that can be overridden:

        1. :py:meth:`~.RPackage.install`

    It has sensible defaults, and for many packages the only thing
    necessary will be to add dependencies
    """
    phases = ['install']

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'RPackage'

    extends('r')

    def install(self, spec, prefix):
        """Installs an R package."""
        inspect.getmodule(self).R(
            'CMD', 'INSTALL',
            '--library={0}'.format(self.module.r_lib_dir),
            self.stage.source_path)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

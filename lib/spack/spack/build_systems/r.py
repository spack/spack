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

import inspect

from spack.directives import depends_on, extends
from spack.package import PackageBase, run_after


class RPackage(PackageBase):
    """Specialized class for packages that are built using R.

    For more information on the R build system, see:
    https://stat.ethz.ch/R-manual/R-devel/library/utils/html/INSTALL.html

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

    depends_on('r', type=('build', 'run'))

    def configure_args(self):
        """Arguments to pass to install via ``--configure-args``."""
        return []

    def configure_vars(self):
        """Arguments to pass to install via ``--configure-vars``."""
        return []

    def install(self, spec, prefix):
        """Installs an R package."""

        config_args = self.configure_args()
        config_vars = self.configure_vars()

        args = [
            'CMD',
            'INSTALL'
        ]

        if config_args:
            args.append('--configure-args={0}'.format(' '.join(config_args)))

        if config_vars:
            args.append('--configure-vars={0}'.format(' '.join(config_vars)))

        args.extend([
            '--library={0}'.format(self.module.r_lib_dir),
            self.stage.source_path
        ])

        inspect.getmodule(self).R(*args)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

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


class OctavePackage(PackageBase):
    """Specialized class for Octave packages. See
    https://www.gnu.org/software/octave/doc/v4.2.0/Installing-and-Removing-Packages.html
    for more information.

    This class provides the following phases that can be overridden:

    1. :py:meth:`~.OctavePackage.install`

    """
    # Default phases
    phases = ['install']

    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'OctavePackage'

    extends('octave')
    depends_on('octave', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""
        # octave does not like those environment variables to be set:
        spack_env.unset('CC')
        spack_env.unset('CXX')
        spack_env.unset('FC')

    def install(self, spec, prefix):
        """Install the package from the archive file"""
        inspect.getmodule(self).octave(
            '--quiet',
            '--norc',
            '--built-in-docstrings-file=/dev/null',
            '--texi-macros-file=/dev/null',
            '--eval', 'pkg prefix %s; pkg install %s' %
            (prefix, self.stage.archive_file))

    # Testing

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

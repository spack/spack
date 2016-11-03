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
import os.path

import llnl.util.tty as tty
from spack.package import PackageBase


class AutotoolsPackage(PackageBase):
    """Specialized class for packages that are built using GNU Autotools

    This class provides four phases that can be overridden:
    - autoreconf
    - configure
    - build
    - install

    They all have sensible defaults and for many packages the only thing
    necessary will be to override `configure_args`
    """
    phases = ['autoreconf', 'configure', 'build', 'install']
    # To be used in UI queries that require to know which
    # build-system class we are using
    build_system_class = 'AutotoolsPackage'

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        pass

    @PackageBase.sanity_check('autoreconf')
    def is_configure_or_die(self):
        """Checks the presence of a `configure` file after the
        autoreconf phase"""
        if not os.path.exists('configure'):
            raise RuntimeError(
                'configure script not found in {0}'.format(os.getcwd()))

    def configure_args(self):
        """Method to be overridden. Should return an iterable containing
        all the arguments that must be passed to configure, except --prefix
        """
        return []

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in `configure_args`
        and an appropriately set prefix
        """
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()
        inspect.getmodule(self).configure(*options)

    def build(self, spec, prefix):
        """The usual `make` after configure"""
        inspect.getmodule(self).make()

    def install(self, spec, prefix):
        """...and the final `make install` after configure"""
        inspect.getmodule(self).make('install')

    @PackageBase.sanity_check('build')
    @PackageBase.on_package_attributes(run_tests=True)
    def _run_default_function(self):
        """This function is run after build if self.run_tests == True

        It will search for a method named `check` and run it. A sensible
        default is provided in the base class.
        """
        try:
            fn = getattr(self, 'check')
            tty.msg('Trying default sanity checks [check]')
            fn()
        except AttributeError:
            tty.msg('Skipping default sanity checks [method `check` not implemented]')  # NOQA: ignore=E501

    def check(self):
        """Default test : search the Makefile for targets `test` and `check`
        and run them if found.
        """
        self._if_make_target_execute('test')
        self._if_make_target_execute('check')

    # Check that self.prefix is there after installation
    PackageBase.sanity_check('install')(PackageBase.sanity_check_prefix)

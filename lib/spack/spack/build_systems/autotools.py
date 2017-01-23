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
import os
import os.path
import shutil
from subprocess import PIPE
from subprocess import check_call

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir
from spack.package import PackageBase


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools.

    This class provides four phases that can be overridden:

        1. :py:meth:`~.AutotoolsPackage.autoreconf`
        2. :py:meth:`~.AutotoolsPackage.configure`
        3. :py:meth:`~.AutotoolsPackage.build`
        4. :py:meth:`~.AutotoolsPackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override the helper method :py:meth:`.configure_args`.
    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.AutotoolsPackage.build_targets`   | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.AutotoolsPackage.install_targets` | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.AutotoolsPackage.check`           | Run  build time    |
        |                                               | tests if required  |
        +-----------------------------------------------+--------------------+

    """
    #: Phases of a GNU Autotools package
    phases = ['autoreconf', 'configure', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'AutotoolsPackage'
    #: Whether or not to update ``config.guess`` on old architectures
    patch_config_guess = True

    #: Targets for ``make`` during the :py:meth:`~.AutotoolsPackage.build`
    #: phase
    build_targets = []
    #: Targets for ``make`` during the :py:meth:`~.AutotoolsPackage.install`
    #: phase
    install_targets = ['install']

    def _do_patch_config_guess(self):
        """Some packages ship with an older config.guess and need to have
        this updated when installed on a newer architecture."""

        my_config_guess = None
        config_guess = None
        if os.path.exists('config.guess'):
            # First search the top-level source directory
            my_config_guess = 'config.guess'
        else:
            # Then search in all sub directories.
            # We would like to use AC_CONFIG_AUX_DIR, but not all packages
            # ship with their configure.in or configure.ac.
            d = '.'
            dirs = [os.path.join(d, o) for o in os.listdir(d)
                    if os.path.isdir(os.path.join(d, o))]
            for dirname in dirs:
                path = os.path.join(dirname, 'config.guess')
                if os.path.exists(path):
                    my_config_guess = path

        if my_config_guess is not None:
            try:
                check_call([my_config_guess], stdout=PIPE, stderr=PIPE)
                # The package's config.guess already runs OK, so just use it
                return True
            except Exception:
                pass
        else:
            return True

        # Look for a spack-installed automake package
        if 'automake' in self.spec:
            automake_path = os.path.join(self.spec['automake'].prefix, 'share',
                                         'automake-' +
                                         str(self.spec['automake'].version))
            path = os.path.join(automake_path, 'config.guess')
            if os.path.exists(path):
                config_guess = path
        if config_guess is not None:
            try:
                check_call([config_guess], stdout=PIPE, stderr=PIPE)
                shutil.copyfile(config_guess, my_config_guess)
                return True
            except Exception:
                pass

        # Look for the system's config.guess
        if os.path.exists('/usr/share'):
            automake_dir = [s for s in os.listdir('/usr/share') if
                            "automake" in s]
            if automake_dir:
                automake_path = os.path.join('/usr/share', automake_dir[0])
                path = os.path.join(automake_path, 'config.guess')
                if os.path.exists(path):
                    config_guess = path
        if config_guess is not None:
            try:
                check_call([config_guess], stdout=PIPE, stderr=PIPE)
                shutil.copyfile(config_guess, my_config_guess)
                return True
            except Exception:
                pass

        return False

    def build_directory(self):
        """Override to provide another place to build the package"""
        return self.stage.source_path

    def patch(self):
        """Patches config.guess if
        :py:attr:``~.AutotoolsPackage.patch_config_guess`` is True

        :raise RuntimeError: if something goes wrong when patching
            ``config.guess``
        """

        if self.patch_config_guess and self.spec.satisfies(
                'arch=linux-rhel7-ppc64le'
        ):
            if not self._do_patch_config_guess():
                raise RuntimeError('Failed to find suitable config.guess')

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        pass

    @PackageBase.sanity_check('autoreconf')
    def is_configure_or_die(self):
        """Checks the presence of a `configure` file after the
        :py:meth:`.autoreconf` phase.

        :raise RuntimeError: if the ``configure`` script does not exist.
        """
        with working_dir(self.build_directory()):
            if not os.path.exists('configure'):
                raise RuntimeError(
                    'configure script not found in {0}'.format(os.getcwd()))

    def configure_args(self):
        """Produces a list containing all the arguments that must be passed to
        configure, except ``--prefix`` which will be pre-pended to the list.

        :return: list of arguments for configure
        """
        return []

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in :py:meth:`.configure_args`
        and an appropriately set prefix.
        """
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()

        with working_dir(self.build_directory()):
            inspect.getmodule(self).configure(*options)

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Makes the install targets specified by
        :py:attr:``~.AutotoolsPackage.install_targets``
        """
        with working_dir(self.build_directory()):
            inspect.getmodule(self).make(*self.install_targets)

    @PackageBase.sanity_check('build')
    @PackageBase.on_package_attributes(run_tests=True)
    def _run_default_function(self):
        """This function is run after build if ``self.run_tests == True``

        It will search for a method named :py:meth:`.check` and run it. A
        sensible default is provided in the base class.
        """
        try:
            fn = getattr(self, 'check')
            tty.msg('Trying default sanity checks [check]')
            fn()
        except AttributeError:
            tty.msg('Skipping default sanity checks [method `check` not implemented]')  # NOQA: ignore=E501

    def check(self):
        """Searches the Makefile for targets ``test`` and ``check``
        and runs them if found.
        """
        with working_dir(self.build_directory()):
            self._if_make_target_execute('test')
            self._if_make_target_execute('check')

    # Check that self.prefix is there after installation
    PackageBase.sanity_check('install')(PackageBase.sanity_check_prefix)

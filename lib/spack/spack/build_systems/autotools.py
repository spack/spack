##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os
import os.path
import shutil
from os import stat
from stat import *
from subprocess import PIPE
from subprocess import check_call

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir, join_path, force_remove
from spack.package import PackageBase, run_after, run_before
from spack.util.executable import Executable


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools.

    This class provides four phases that can be overridden:

        1. :py:meth:`~.AutotoolsPackage.autoreconf`
        2. :py:meth:`~.AutotoolsPackage.configure`
        3. :py:meth:`~.AutotoolsPackage.build`
        4. :py:meth:`~.AutotoolsPackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override the helper method
    :py:meth:`~.AutotoolsPackage.configure_args`.
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

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    #: Callback names for install-time test
    install_time_test_callbacks = ['installcheck']

    #: Set to true to force the autoreconf step even if configure is present
    force_autoreconf = False
    #: Options to be passed to autoreconf when using the default implementation
    autoreconf_extra_args = []

    @run_after('autoreconf')
    def _do_patch_config_guess(self):
        """Some packages ship with an older config.guess and need to have
        this updated when installed on a newer architecture. In particular,
        config.guess fails for PPC64LE for version prior to a 2013-06-10
        build date (automake 1.13.4)."""

        if not self.patch_config_guess or not self.spec.satisfies(
                'target=ppc64le'
        ):
            return
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
                return
            except Exception:
                pass
        else:
            return

        # Look for a spack-installed automake package
        if 'automake' in self.spec:
            automake_path = os.path.join(self.spec['automake'].prefix, 'share',
                                         'automake-' +
                                         str(self.spec['automake'].version))
            path = os.path.join(automake_path, 'config.guess')
            if os.path.exists(path):
                config_guess = path
        # Look for the system's config.guess
        if config_guess is None and os.path.exists('/usr/share'):
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
                mod = stat(my_config_guess).st_mode & 0o777 | S_IWUSR
                os.chmod(my_config_guess, mod)
                shutil.copyfile(config_guess, my_config_guess)
                return
            except Exception:
                pass

        raise RuntimeError('Failed to find suitable config.guess')

    @property
    def configure_directory(self):
        """Returns the directory where 'configure' resides.

        :return: directory where to find configure
        """
        return self.stage.source_path

    @property
    def configure_abs_path(self):
        # Absolute path to configure
        configure_abs_path = join_path(
            os.path.abspath(self.configure_directory), 'configure'
        )
        return configure_abs_path

    @property
    def build_directory(self):
        """Override to provide another place to build the package"""
        return self.configure_directory

    def default_flag_handler(self, spack_env, flag_val):
        # Relies on being the first thing that can affect the spack_env
        # EnvironmentModification after it is instantiated or no other
        # method trying to affect these variables. Currently both are true
        # flag_val is a tuple (flag, value_list).
        spack_env.set(flag_val[0].upper(),
                      ' '.join(flag_val[1]))
        return []

    @run_before('autoreconf')
    def delete_configure_to_force_update(self):
        if self.force_autoreconf:
            force_remove(self.configure_abs_path)

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else try to regenerate it
        autotools = ['m4', 'autoconf', 'automake', 'libtool']
        missing = [x for x in autotools if x not in spec]
        if missing:
            msg = 'Cannot generate configure: missing dependencies {0}'
            raise RuntimeError(msg.format(missing))
        tty.msg('Configure script not found: trying to generate it')
        tty.warn('*********************************************************')
        tty.warn('* If the default procedure fails, consider implementing *')
        tty.warn('*        a custom AUTORECONF phase in the package       *')
        tty.warn('*********************************************************')
        with working_dir(self.configure_directory):
            m = inspect.getmodule(self)
            # This part should be redundant in principle, but
            # won't hurt
            m.libtoolize()
            m.aclocal()
            # This line is what is needed most of the time
            # --install, --verbose, --force
            autoreconf_args = ['-ivf']
            if 'pkg-config' in spec:
                autoreconf_args += [
                    '-I',
                    join_path(spec['pkg-config'].prefix, 'share', 'aclocal'),
                ]
            autoreconf_args += self.autoreconf_extra_args
            m.autoreconf(*autoreconf_args)

    @run_after('autoreconf')
    def set_configure_or_die(self):
        """Checks the presence of a ``configure`` file after the
        autoreconf phase. If it is found sets a module attribute
        appropriately, otherwise raises an error.

        :raises RuntimeError: if a configure script is not found in
            :py:meth:`~AutotoolsPackage.configure_directory`
        """
        # Check if a configure script is there. If not raise a RuntimeError.
        if not os.path.exists(self.configure_abs_path):
            msg = 'configure script not found in {0}'
            raise RuntimeError(msg.format(self.configure_directory))

        # Monkey-patch the configure script in the corresponding module
        inspect.getmodule(self).configure = Executable(
            self.configure_abs_path
        )

    def configure_args(self):
        """Produces a list containing all the arguments that must be passed to
        configure, except ``--prefix`` which will be pre-pended to the list.

        :return: list of arguments for configure
        """
        return []

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :py:meth:`~.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Makes the install targets specified by
        :py:attr:``~.AutotoolsPackage.install_targets``
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the Makefile for targets ``test`` and ``check``
        and runs them if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('test')
            self._if_make_target_execute('check')

    def _activate_or_not(self, active, inactive, name, active_parameters=None):
        spec = self.spec
        args = []
        # For each allowed value in the list of values
        for value in self.variants[name].values:
            # Check if the value is active in the current spec
            condition = '{name}={value}'.format(name=name, value=value)
            activated = condition in spec
            # Search for an override in the package for this value
            override_name = '{0}_or_{1}_{2}'.format(active, inactive, value)
            line_generator = getattr(self, override_name, None)
            # If not available use a sensible default
            if line_generator is None:
                def _default_generator(is_activated):
                    if is_activated:
                        line = '--{0}-{1}'.format(active, value)
                        if active_parameters is not None and active_parameters(value):  # NOQA=ignore=E501
                            line += '={0}'.format(active_parameters(value))
                        return line
                    return '--{0}-{1}'.format(inactive, value)
                line_generator = _default_generator
            args.append(line_generator(activated))
        return args

    def with_or_without(self, name, active_parameters=None):
        """Inspects the multi-valued variant 'name' and returns the configure
        arguments that activate / deactivate the selected feature.

        :param str name: name of a valid multi-valued variant
        :param callable active_parameters: if present accepts a single value
            and returns the parameter to be used leading to an entry of the
            type '--with-{name}={parameter}
        """
        return self._activate_or_not(
            'with', 'without', name, active_parameters
        )

    def enable_or_disable(self, name, active_parameters=None):
        """Inspects the multi-valued variant 'name' and returns the configure
        arguments that activate / deactivate the selected feature.
        """
        return self._activate_or_not(
            'enable', 'disable', name, active_parameters
        )

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    def installcheck(self):
        """Searches the Makefile for an ``installcheck`` target
        and runs it if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('installcheck')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

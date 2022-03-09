# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import os.path
import stat
from subprocess import PIPE, check_call
from typing import List  # novm

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.filesystem import force_remove, working_dir

from spack.build_environment import InstallError
from spack.directives import depends_on
from spack.operating_systems.mac_os import macos_version
from spack.package import PackageBase, run_after, run_before
from spack.util.executable import Executable
from spack.version import Version


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools.

    This class provides four phases that can be overridden:

        1. :py:meth:`~.AutotoolsPackage.autoreconf`
        2. :py:meth:`~.AutotoolsPackage.configure`
        3. :py:meth:`~.AutotoolsPackage.build`
        4. :py:meth:`~.AutotoolsPackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override the helper method
    :meth:`~spack.build_systems.autotools.AutotoolsPackage.configure_args`.
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

    @property
    def patch_config_files(self):
        """
        Whether or not to update old ``config.guess`` and ``config.sub`` files
        distributed with the tarball. This currently only applies to
        ``ppc64le:``, ``aarch64:``, and ``riscv64`` target architectures. The
        substitutes are taken from the ``gnuconfig`` package, which is
        automatically added as a build dependency for these architectures. In
        case system versions of these config files are required, the
        ``gnuconfig`` package can be marked external with a prefix pointing to
        the directory containing the system ``config.guess`` and ``config.sub``
        files.
        """
        return (self.spec.satisfies('target=ppc64le:')
                or self.spec.satisfies('target=aarch64:')
                or self.spec.satisfies('target=riscv64:'))

    #: Whether or not to update ``libtool``
    #: (currently only for Arm/Clang/Fujitsu compilers)
    patch_libtool = True

    #: Targets for ``make`` during the :py:meth:`~.AutotoolsPackage.build`
    #: phase
    build_targets = []  # type: List[str]
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
    autoreconf_extra_args = []  # type: List[str]

    #: If False deletes all the .la files in the prefix folder
    #: after the installation. If True instead it installs them.
    install_libtool_archives = False

    depends_on('gnuconfig', type='build', when='target=ppc64le:')
    depends_on('gnuconfig', type='build', when='target=aarch64:')
    depends_on('gnuconfig', type='build', when='target=riscv64:')

    @property
    def _removed_la_files_log(self):
        """File containing the list of remove libtool archives"""
        build_dir = self.build_directory
        if not os.path.isabs(self.build_directory):
            build_dir = os.path.join(self.stage.path, build_dir)
        return os.path.join(build_dir, 'removed_la_files.txt')

    @property
    def archive_files(self):
        """Files to archive for packages based on autotools"""
        files = [os.path.join(self.build_directory, 'config.log')]
        if not self.install_libtool_archives:
            files.append(self._removed_la_files_log)
        return files

    @run_after('autoreconf')
    def _do_patch_config_files(self):
        """Some packages ship with older config.guess/config.sub files and
        need to have these updated when installed on a newer architecture.
        In particular, config.guess fails for PPC64LE for version prior
        to a 2013-06-10 build date (automake 1.13.4) and for ARM (aarch64) and
        RISC-V (riscv64).
        """
        if not self.patch_config_files:
            return

        # TODO: Expand this to select the 'config.sub'-compatible architecture
        # for each platform (e.g. 'config.sub' doesn't accept 'power9le', but
        # does accept 'ppc64le').
        if self.spec.satisfies('target=ppc64le:'):
            config_arch = 'ppc64le'
        elif self.spec.satisfies('target=aarch64:'):
            config_arch = 'aarch64'
        elif self.spec.satisfies('target=riscv64:'):
            config_arch = 'riscv64'
        else:
            config_arch = 'local'

        def runs_ok(script_abs_path):
            # Construct the list of arguments for the call
            additional_args = {
                'config.sub': [config_arch]
            }
            script_name = os.path.basename(script_abs_path)
            args = [script_abs_path] + additional_args.get(script_name, [])

            try:
                check_call(args, stdout=PIPE, stderr=PIPE)
            except Exception as e:
                tty.debug(e)
                return False

            return True

        # Get the list of files that needs to be patched
        to_be_patched = fs.find(self.stage.path, files=['config.sub', 'config.guess'])
        to_be_patched = [f for f in to_be_patched if not runs_ok(f)]

        # If there are no files to be patched, return early
        if not to_be_patched:
            return

        # Otherwise, require `gnuconfig` to be a build dependency
        self._require_build_deps(
            pkgs=['gnuconfig'],
            spec=self.spec,
            err="Cannot patch config files")

        # Get the config files we need to patch (config.sub / config.guess).
        to_be_found = list(set(os.path.basename(f) for f in to_be_patched))
        gnuconfig = self.spec['gnuconfig']
        gnuconfig_dir = gnuconfig.prefix

        # An external gnuconfig may not not have a prefix.
        if gnuconfig_dir is None:
            raise InstallError("Spack could not find substitutes for GNU config "
                               "files because no prefix is available for the "
                               "`gnuconfig` package. Make sure you set a prefix "
                               "path instead of modules for external `gnuconfig`.")

        candidates = fs.find(gnuconfig_dir, files=to_be_found, recursive=False)

        # For external packages the user may have specified an incorrect prefix.
        # otherwise the installation is just corrupt.
        if not candidates:
            msg = ("Spack could not find `config.guess` and `config.sub` "
                   "files in the `gnuconfig` prefix `{0}`. This means the "
                   "`gnuconfig` package is broken").format(gnuconfig_dir)
            if gnuconfig.external:
                msg += (" or the `gnuconfig` package prefix is misconfigured as"
                        " an external package")
            raise InstallError(msg)

        # Filter working substitutes
        candidates = [f for f in candidates if runs_ok(f)]
        substitutes = {}
        for candidate in candidates:
            config_file = os.path.basename(candidate)
            substitutes[config_file] = candidate
            to_be_found.remove(config_file)

        # Check that we found everything we needed
        if to_be_found:
            msg = """\
Spack could not find working replacements for the following autotools config
files: {0}.

To resolve this problem, please try the following:
1. Try to rebuild with `patch_config_files = False` in the package `{1}`, to
   rule out that Spack tries to replace config files not used by the build.
2. Verify that the `gnuconfig` package is up-to-date.
3. On some systems you need to use system-provided `config.guess` and `config.sub`
   files. In this case, mark `gnuconfig` as an non-buildable external package,
   and set the prefix to the directory containing the `config.guess` and
   `config.sub` files.
"""
            raise InstallError(msg.format(', '.join(to_be_found), self.name))

        # Copy the good files over the bad ones
        for abs_path in to_be_patched:
            name = os.path.basename(abs_path)
            mode = os.stat(abs_path).st_mode
            os.chmod(abs_path, stat.S_IWUSR)
            fs.copy(substitutes[name], abs_path)
            os.chmod(abs_path, mode)

    @run_before('configure')
    def _set_autotools_environment_variables(self):
        """Many autotools builds use a version of mknod.m4 that fails when
        running as root unless FORCE_UNSAFE_CONFIGURE is set to 1.

        We set this to 1 and expect the user to take responsibility if
        they are running as root. They have to anyway, as this variable
        doesn't actually prevent configure from doing bad things as root.
        Without it, configure just fails halfway through, but it can
        still run things *before* this check. Forcing this just removes a
        nuisance -- this is not circumventing any real protection.

        """
        os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"

    @run_after('configure')
    def _do_patch_libtool(self):
        """If configure generates a "libtool" script that does not correctly
        detect the compiler (and patch_libtool is set), patch in the correct
        flags for the Arm, Clang/Flang, and Fujitsu compilers."""

        # Exit early if we are required not to patch libtool
        if not self.patch_libtool:
            return

        for libtool_path in fs.find(
                self.build_directory, 'libtool', recursive=True):
            self._patch_libtool(libtool_path)

    def _patch_libtool(self, libtool_path):
        if self.spec.satisfies('%arm')\
                or self.spec.satisfies('%clang')\
                or self.spec.satisfies('%fj'):
            fs.filter_file('wl=""\n', 'wl="-Wl,"\n', libtool_path)
            fs.filter_file('pic_flag=""\n',
                           'pic_flag="{0}"\n'
                           .format(self.compiler.cc_pic_flag),
                           libtool_path)
        if self.spec.satisfies('%fj'):
            fs.filter_file('-nostdlib', '', libtool_path)
            rehead = r'/\S*/'
            objfile = ['fjhpctag.o', 'fjcrt0.o', 'fjlang08.o', 'fjomp.o',
                       'crti.o', 'crtbeginS.o', 'crtendS.o']
            for o in objfile:
                fs.filter_file(rehead + o, '', libtool_path)

    @property
    def configure_directory(self):
        """Returns the directory where 'configure' resides.

        :return: directory where to find configure
        """
        return self.stage.source_path

    @property
    def configure_abs_path(self):
        # Absolute path to configure
        configure_abs_path = os.path.join(
            os.path.abspath(self.configure_directory), 'configure'
        )
        return configure_abs_path

    @property
    def build_directory(self):
        """Override to provide another place to build the package"""
        return self.configure_directory

    @run_before('autoreconf')
    def delete_configure_to_force_update(self):
        if self.force_autoreconf:
            force_remove(self.configure_abs_path)

    def _require_build_deps(self, pkgs, spec, err):
        """Require `pkgs` to be direct build dependencies of `spec`. Raises a
        RuntimeError with a helpful error messages when any dep is missing."""

        build_deps = [d.name for d in spec.dependencies(deptype='build')]
        missing_deps = [x for x in pkgs if x not in build_deps]

        if not missing_deps:
            return

        # Raise an exception on missing deps.
        msg = ("{0}: missing dependencies: {1}.\n\nPlease add "
               "the following lines to the package:\n\n"
               .format(err, ", ".join(missing_deps)))

        for dep in missing_deps:
            msg += ("    depends_on('{0}', type='build', when='@{1}')\n"
                    .format(dep, spec.version))

        msg += "\nUpdate the version (when='@{0}') as needed.".format(spec.version)
        raise RuntimeError(msg)

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""

        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return

        # Else try to regenerate it, which reuquires a few build dependencies
        self._require_build_deps(
            pkgs=['autoconf', 'automake', 'libtool'],
            spec=spec,
            err="Cannot generate configure")

        tty.msg('Configure script not found: trying to generate it')
        tty.warn('*********************************************************')
        tty.warn('* If the default procedure fails, consider implementing *')
        tty.warn('*        a custom AUTORECONF phase in the package       *')
        tty.warn('*********************************************************')
        with working_dir(self.configure_directory):
            m = inspect.getmodule(self)
            # This line is what is needed most of the time
            # --install, --verbose, --force
            autoreconf_args = ['-ivf']
            autoreconf_args += self.autoreconf_search_path_args
            autoreconf_args += self.autoreconf_extra_args
            m.autoreconf(*autoreconf_args)

    @property
    def autoreconf_search_path_args(self):
        """Arguments to autoreconf to modify the search paths"""
        search_path_args = []
        for dep in self.spec.dependencies(deptype='build'):
            if os.path.exists(dep.prefix.share.aclocal):
                search_path_args.extend(['-I', dep.prefix.share.aclocal])
        return search_path_args

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

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass specified
        compiler flags to configure."""
        # Has to be dynamic attribute due to caching.
        setattr(self, 'configure_flag_args', [])
        for flag, values in flags.items():
            if values:
                values_str = '{0}={1}'.format(flag.upper(), ' '.join(values))
                self.configure_flag_args.append(values_str)
        # Spack's fflags are meant for both F77 and FC, therefore we
        # additionaly set FCFLAGS if required.
        values = flags.get('fflags', None)
        if values:
            values_str = 'FCFLAGS={0}'.format(' '.join(values))
            self.configure_flag_args.append(values_str)

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        options = getattr(self, 'configure_flag_args', [])
        options += ['--prefix={0}'.format(prefix)]
        options += self.configure_args()

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)

    def setup_build_environment(self, env):
        if (self.spec.platform == 'darwin'
                and macos_version() >= Version('11')):
            # Many configure files rely on matching '10.*' for macOS version
            # detection and fail to add flags if it shows as version 11.
            env.set('MACOSX_DEPLOYMENT_TARGET', '10.16')

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        # See https://autotools.io/automake/silent.html
        params = ['V=1']
        params += self.build_targets
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*params)

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

    def _activate_or_not(
            self,
            name,
            activation_word,
            deactivation_word,
            activation_value=None,
            variant=None
    ):
        """This function contains the current implementation details of
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.with_or_without` and
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.enable_or_disable`.

        Args:
            name (str): name of the option that is being activated or not
            activation_word (str): the default activation word ('with' in the
                case of ``with_or_without``)
            deactivation_word (str): the default deactivation word ('without'
                in the case of ``with_or_without``)
            activation_value (typing.Callable): callable that accepts a single
                value. This value is either one of the allowed values for a
                multi-valued variant or the name of a bool-valued variant.
                Returns the parameter to be used when the value is activated.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.
            variant (str): name of the variant that is being processed
                           (if different from option name)

        Examples:

            Given a package with:

            .. code-block:: python

                variant('foo', values=('x', 'y'), description='')
                variant('bar', default=True, description='')
                variant('ba_z', default=True, description='')

            calling this function like:

            .. code-block:: python

                _activate_or_not(
                    'foo', 'with', 'without', activation_value='prefix'
                )
                _activate_or_not('bar', 'with', 'without')
                _activate_or_not('ba-z', 'with', 'without', variant='ba_z')

            will generate the following configuration options:

            .. code-block:: console

                --with-x=<prefix-to-x> --without-y --with-bar --with-ba-z

            for ``<spec-name> foo=x +bar``

        Note: returns an empty list when the variant is conditional and its condition
              is not met.

        Returns:
            list: list of strings that corresponds to the activation/deactivation
            of the variant that has been processed

        Raises:
            KeyError: if name is not among known variants
        """
        spec = self.spec
        args = []

        if activation_value == 'prefix':
            activation_value = lambda x: spec[x].prefix

        variant = variant or name

        # Defensively look that the name passed as argument is among
        # variants
        if variant not in self.variants:
            msg = '"{0}" is not a variant of "{1}"'
            raise KeyError(msg.format(variant, self.name))

        if variant not in spec.variants:
            return []

        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        variant_desc, _ = self.variants[variant]
        if set(variant_desc.values) == set((True, False)):
            # BoolValuedVariant carry information about a single option.
            # Nonetheless, for uniformity of treatment we'll package them
            # in an iterable of one element.
            condition = '+{name}'.format(name=variant)
            options = [(name, condition in spec)]
        else:
            condition = '{variant}={value}'
            # "feature_values" is used to track values which correspond to
            # features which can be enabled or disabled as understood by the
            # package's build system. It excludes values which have special
            # meanings and do not correspond to features (e.g. "none")
            feature_values = getattr(
                variant_desc.values, 'feature_values', None
            ) or variant_desc.values

            options = [
                (value,
                 condition.format(variant=variant,
                                  value=value) in spec)
                for value in feature_values
            ]

        # For each allowed value in the list of values
        for option_value, activated in options:
            # Search for an override in the package for this value
            override_name = '{0}_or_{1}_{2}'.format(
                activation_word, deactivation_word, option_value
            )
            line_generator = getattr(self, override_name, None)
            # If not available use a sensible default
            if line_generator is None:
                def _default_generator(is_activated):
                    if is_activated:
                        line = '--{0}-{1}'.format(
                            activation_word, option_value
                        )
                        if activation_value is not None and activation_value(option_value):  # NOQA=ignore=E501
                            line += '={0}'.format(
                                activation_value(option_value)
                            )
                        return line
                    return '--{0}-{1}'.format(deactivation_word, option_value)
                line_generator = _default_generator
            args.append(line_generator(activated))
        return args

    def with_or_without(self, name, activation_value=None, variant=None):
        """Inspects a variant and returns the arguments that activate
        or deactivate the selected feature(s) for the configure options.

        This function works on all type of variants. For bool-valued variants
        it will return by default ``--with-{name}`` or ``--without-{name}``.
        For other kinds of variants it will cycle over the allowed values and
        return either ``--with-{value}`` or ``--without-{value}``.

        If activation_value is given, then for each possible value of the
        variant, the option ``--with-{value}=activation_value(value)`` or
        ``--without-{value}`` will be added depending on whether or not
        ``variant=value`` is in the spec.

        Args:
            name (str): name of a valid multi-valued variant
            activation_value (typing.Callable): callable that accepts a single
                value and returns the parameter to be used leading to an entry
                of the type ``--with-{name}={parameter}``.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(name, 'with', 'without', activation_value,
                                     variant)

    def enable_or_disable(self, name, activation_value=None, variant=None):
        """Same as
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.with_or_without`
        but substitute ``with`` with ``enable`` and ``without`` with ``disable``.

        Args:
            name (str): name of a valid multi-valued variant
            activation_value (typing.Callable): if present accepts a single value
                and returns the parameter to be used leading to an entry of the
                type ``--enable-{name}={parameter}``

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(
            name, 'enable', 'disable', activation_value, variant
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

    @run_after('install')
    def remove_libtool_archives(self):
        """Remove all .la files in prefix sub-folders if the package sets
        ``install_libtool_archives`` to be False.
        """
        # If .la files are to be installed there's nothing to do
        if self.install_libtool_archives:
            return

        # Remove the files and create a log of what was removed
        libtool_files = fs.find(str(self.prefix), '*.la', recursive=True)
        with fs.safe_remove(*libtool_files):
            fs.mkdirp(os.path.dirname(self._removed_la_files_log))
            with open(self._removed_la_files_log, mode='w') as f:
                f.write('\n'.join(libtool_files))

    # On macOS, force rpaths for shared library IDs and remove duplicate rpaths
    run_after('install')(PackageBase.apply_macos_rpath_fixups)

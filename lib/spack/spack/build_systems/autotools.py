# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import itertools
import os
import os.path
import stat
import re
import six  # used for string types checking
from copy import deepcopy
from subprocess import PIPE
from subprocess import check_call
from typing import List  # novm

import llnl.util.tty as tty
import llnl.util.filesystem as fs
from llnl.util.filesystem import working_dir, force_remove
from spack.package import PackageBase, run_after, run_before
from spack.util.executable import Executable
# enable build_type interface for autotools (will add default
# variants to Autotools Packages)
from spack.directives import variant


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
    #: Whether or not to update ``config.guess`` and ``config.sub`` on old
    #: architectures
    patch_config_files = True
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

    # provide a means for setting optimization or debug flags consistently
    # across autotools packages. Model it after CMake.

    # to preserve existing behavior, define 'undefined' as the default,
    # which will set nothing.
    _desc = ['Allow parity with CMake projects. '
             'Flags will be applied to all compilers (CFLAGS, CXXFLAGS,...)'
             '  Release (-O3)',
             '  RelWithDebug (-O3 -g)',
             '  Debug (-g)',
             '  MinSizeRel (-Os)',
             '  Undefined (do nothing, preserving existing behavior)',
             ]
    variant('build_type',
            default='Undefined',
            values=('Release', 'RelWithDebug',
                    'Debug', 'MinSizeRel', 'Undefined'),
            multi=False,
            description=os.linesep.join(_desc))

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
        to a 2013-06-10 build date (automake 1.13.4) and for ARM (aarch64).
        """
        if not self.patch_config_files or (
                not self.spec.satisfies('target=ppc64le:') and
                not self.spec.satisfies('target=aarch64:')
        ):
            return

        # TODO: Expand this to select the 'config.sub'-compatible architecture
        # for each platform (e.g. 'config.sub' doesn't accept 'power9le', but
        # does accept 'ppc64le').
        if self.spec.satisfies('target=ppc64le:'):
            config_arch = 'ppc64le'
        elif self.spec.satisfies('target=aarch64:'):
            config_arch = 'aarch64'
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

        # Compute the list of files that needs to be patched
        search_dir = self.stage.path
        to_be_patched = fs.find(
            search_dir, files=['config.sub', 'config.guess'], recursive=True
        )
        to_be_patched = [f for f in to_be_patched if not runs_ok(f)]

        # If there are no files to be patched, return early
        if not to_be_patched:
            return

        # Directories where to search for files to be copied
        # over the failing ones
        good_file_dirs = ['/usr/share']
        if 'automake' in self.spec:
            good_file_dirs.insert(0, self.spec['automake'].prefix)

        # List of files to be found in the directories above
        to_be_found = list(set(os.path.basename(f) for f in to_be_patched))
        substitutes = {}
        for directory in good_file_dirs:
            candidates = fs.find(directory, files=to_be_found, recursive=True)
            candidates = [f for f in candidates if runs_ok(f)]
            for name, good_files in itertools.groupby(
                    candidates, key=os.path.basename
            ):
                substitutes[name] = next(good_files)
                to_be_found.remove(name)

        # Check that we found everything we needed
        if to_be_found:
            msg = 'Failed to find suitable substitutes for {0}'
            raise RuntimeError(msg.format(', '.join(to_be_found)))

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

    def _configure_check_flags(self, spec, configure_args, arg_src):
        '''Check a list of configure args from `arg_src` for logical
        errors (such as variables set multiple times). Enforce that
        user provided flags are respected See `_enforce_user_flags`

        Args:
            spec (Spec): the spec being evaluated
            configure_args (list): configure args
            arg_src (str): Identify where the `var_map` came from. AutoTools
                uses two places to generate configure args. One assembles
                `build_environment` variables to pass to the configure line,
                and `configure_args` which the packager may directly set.
                This parameter is used to provide meaningful feedback in
                the event of error.

        Return:
            flag_map (dict): dictionary of VAR : VALUE where VAR is variable
                Autotools respects (and spack allows the user to set).
                See `_get_spack_autotool_flag_map`. Examples are `CFLAGS` and
                `cflags`
                The flags may be modified as passed in from `configure_args`.
                (user flags may be prepended)
                Moroever, if the package erroneously sets variables multiple
                times, this state is revolved by combining the values.

            reg_args (list): the other args from `configure_args` that are
                not `VAR=`. (unmodified)

            This method may throw a ValueError if it fails to parse
            `VAR=VAL`, this should be impossible because the values are
            from `_split_configure_args`, which only returns values that
            sucessfuly match `VAR=` format.
        '''
        pre = '{s.name}@{s.version} [{src}]:'.format(s=spec, src=arg_src)
        # a mapping of VAR to spack names (CFLAGS->cflags)
        flag_var_names = AutotoolsPackage._get_spack_autotool_flag_map()

        # split the args into VAR=VAL and all others
        # we only consider names for VAR in `flag_var_names`
        flag_args, reg_args = self._split_configure_args(configure_args,
                                                         flag_var_names)
        # flag args is a list, which could have duplicate variables, e.g.,
        # CFLAGS twice convert to a map, and report problems...
        var_re = re.compile(r'^(?P<env>[^=]+)=(?P<value>.*)$')
        flag_map = {}
        for arg in flag_args:
            # we should have the proper format
            m = var_re.match(arg)
            if not m:
                # this shouldn't be possible..
                tty.debug("Split configure args into variables, but {0} does"
                          " not satisfy the format VAR=VALUE".format(arg))
                raise ValueError
            var_name = m.group("env")
            var_value = m.group("value")

            # if we already have the var in flag_map, then the package has
            # set this variable multiple times!
            if var_name in flag_map:
                tty.warn('**************************************************')
                tty.warn("* {0} has set variable {1} multiple times,"
                         " values will be concatenated".format(pre, var_name))
                tty.warn("*  {0} = {1}".format(var_name, var_value))
                tty.warn("*  Prior: {0} = {1}".format(var_name,
                                                      flag_map[var_name]))
                tty.warn('**************************************************')
                flag_map[var_name] += ' {0}'.format(var_value)
            else:
                # The expected case, with the package behaving as expected
                flag_map[var_name] = var_value

        # now enforce that any user provided flags are set
        flag_map = self._enforce_user_flags(spec,
                                            var_map=flag_map,
                                            var_to_spack_map=flag_var_names,
                                            arg_src=arg_src)
        # optional: Dedupe flags... be careful though!
        return flag_map, reg_args

    def _enforce_user_flags_when_package_does_not_declare(
            self,
            spec,
            flag_map,
            add_if_var_undefined=True):
        '''Handle the case the user has defined some flag variables,
        but the package does not set the similar AutoTools ENV variable.

        Args:
            spec (Spec): The spec being evaluated
            flag_map (dict): Modified in-place.
                Dictionary of VAR=VAL of flag variables and their values
            add_if_var_undefined (bool): Whether to add flag variables if
                the package has not defined them.
        Discussion!
         The problem is that if a package does not set VAR at all,
         then a user defined flag will never get added

         You don't want to do this detection in either the build_flags
         or `configure_args` because it breaks detecting bad behavior if
         the package defines flags in both places

         The correct place to do this is *after* you have a uniform set of
         flags the package has declared.

         This is a bit involved... Some flags (fortran) spack expects
         a common set of flags... this is actually bug imo
         To be consistent (if spack expects a uniform fortran flags)
         then we need to make sure that FCFLAGS / F90FLAGS / F77FLAGS are
         set in a consistent way (or not set - but in some consistent fashion)

         For example: pnetcdf sets FCFLAGS and FFLAGS, but not F90/F77 flags
         if fflags=-g , the package is adding -fpic
         this isn't something we can trivially resolve

        ==> Setting FFLAGS=-g -fPIC (from configure_args)
        ==> Setting FCFLAGS=-g -fPIC (from configure_args)
        ==> Adding flag VAR that package does not:  adding F77FLAGS=-g to configure args
        ==> Adding flag VAR that package does not:  adding F90FLAGS=-g to configure args

         These modifications *are* enforcing user flags
         IMO, a fix for SPACK would be to require packages to declare the
         flag variables they respect. Or have spack impose a policy on all
         packages.
        '''
        # a mapping of VAR to spack names (CFLAGS->cflags)
        var_to_spack_map = AutotoolsPackage._get_spack_autotool_flag_map()

        # fix the package not declaring the variable but the user defining one
        for env_flag_var_name in var_to_spack_map:
            # if the existing AutoTools var_map has the name (key)
            # then do nothing
            if env_flag_var_name in flag_map:
                continue
            # otherwise, add this VAR with the user specified flags

            # collect the spack flags from the spec
            spack_flag_name = var_to_spack_map[env_flag_var_name]
            spack_flags = spec.compiler_flags[spack_flag_name]
            # now check that there is a spack variable to set
            if not spack_flags:
                tty.debug("{0} NOT adding: {1}={2} to configure args"
                          "".format("enforce_user_flags: ",
                                    env_flag_var_name,
                                    ' '.join(spack_flags)))
                continue
            # should be a list, but be safe
            if isinstance(spack_flags, six.string_types):
                spack_flags = [spack_flags]
            spack_flags = ' '.join(spack_flags)
            tty.debug("{0} Adding {1}={2} to configure args"
                      "".format("enforce_user_flags: ",
                                env_flag_var_name,
                                spack_flags))
            flag_map[env_flag_var_name] = spack_flags

    def _enforce_user_flags(self,
                            spec,
                            var_map,
                            var_to_spack_map,
                            arg_src):
        ''' Given a dict of variables and values, determine if the package
        respected user provided flags and add user provided flags.

        Args:
            spec (Spec): spec being evaluated
            var_map (dict): a map of VAR : VALUE where the keys are also
                keys in the var_to_spack_map. See `_configure_check_flags`,
                which returns a flag_map suitable for use.
            var_to_spack_map (dict): dictionary mapping VARs to spack.
                See `_get_spack_autotool_flag_map` for a means to generate
                var_to_spack_map.
            arg_src (str): Identify where the `var_map` came from. AutoTools
                uses two places to generate configure args. One assembles
                `build_environment` variables to pass to the configure line,
                and `configure_args` which the packager may directly set.
                This parameter is used to provide meaningful feedback in
                the event of error.
        Return:
            var_map (dict): modified `var_map` with user provided flags
                added if omitted
        '''
        new_var_map = deepcopy(var_map)

        # be careful about reordering flags
        for var_name, var_value in var_map.items():

            # collect the spack flags from the spec
            spack_flag_name = var_to_spack_map[var_name]
            spack_flags = spec.compiler_flags[spack_flag_name]
            # should be a list, but be safe
            if isinstance(spack_flags, six.string_types):
                spack_flags = [spack_flags]
            user_flags = var_value.split()

            spack_set = set(spack_flags)
            user_set = set(user_flags)

            if spack_set.issubset(user_set):
                continue

            # User provided flags are not in the package's provided
            # flags... warn the user
            tty.warn("{0} Package set {1} but did not include user flags ({2})"
                     "".format("enforce_user_flags: ",
                               var_name, spack_flag_name))
            tty.warn("Spack    Flags: {0}".format(' '.join(spack_flags)))
            tty.warn("Packgage Flags: {0}".format(' '.join(user_flags)))

            # The safest method could be to simply prepend spack + package
            # flags compilers typically will respect the final flag if
            # contradictory ones are present... this is messy (and the
            # package) should fix this stuff
            new_var_map[var_name] = ' '.join(spack_flags + user_flags)
        # return the new map with spack flags added
        return new_var_map

    def _split_configure_args(self, configure_args, env_var_names):
        '''Given a list of args for configure and an iterable of variables
        that spack provides interfaces to provide, e.g., ldflags => LDFLAGS

        Split the list of configure args into 2 lists. One containing all args
        that have VAR= format (where VAR is defined in env_var_names). The
        second list containing the other args.

        Args:
            configure_args (list): configure args
            env_var_names (iterable): List of VARs that will be split from the
                other args.

        Returns:
            env_args (list): any args that startwith `VAR=` format
            reg_args (list): all other args
        '''
        env_args = []
        reg_args = []

        pre = tuple(['{0}='.format(e) for e in env_var_names])
        env_args = [arg for arg in configure_args if arg.startswith(pre)]
        reg_args = [arg for arg in configure_args if not arg.startswith(pre)]

        # tty.debug("sizes {0} (env) + {1} (reg) = {2} , orig size: {3}"
        #           "".format(len(env_args), len(reg_args),
        #                     len(env_args) + len(reg_args),
        #                     len(configure_args)))

        # tty.debug("env_args [{0}]: {1}".format(len(env_args),
        #                                        os.linesep.join(env_args)))
        # tty.debug("reg_args [{0}]: {1}".format(len(reg_args),
        #                                        os.linesep.join(reg_args)))
        return env_args, reg_args

    @staticmethod
    def _get_spack_autotool_flag_map():
        '''Provide mapping between autotool's ENV variables and spack's
           variable names.

           Return: [dict] of autotool to spack mapping
        '''
        # the API code path for setting flags
        flag_names = {'CFLAGS':   'cflags',
                      'CXXFLAGS': 'cxxflags',
                      'F77FLAGS': 'fflags',
                      'F90FLAGS': 'fflags',
                      'FCFLAGS':  'fflags',
                      'FFLAGS':   'fflags',
                      'LDFLAGS':  'ldflags',
                      }
        return flag_names

    def _reconcile_var_args(self,
                            spec,
                            build_var_flag_map,
                            configure_var_flag_map):
        '''Given two dicts of VAR=VAL,
            1. determine if the package sets VAR in both setup_build_env
               and configure_args.
            2. resolve the conflict above if needed
               Policy: combine the values as well (could be weird!)
            3. Unify the build and configure_args variable setting
               arguments. This entails taking the non-duplciated args
               from both and placing them into a single dict of VAR : VAL
               Step (2) ensures we will not have any conflicts
        '''
        # this is returning keys to a dict, which are
        # the env variable names for setting these flags
        # we need to be careful with ordering.
        # A goal is to preserver the flag order in the early phases
        # ( that means no set -> list -> string (join) )
        be_var_names = set(build_var_flag_map)
        conf_var_names = set(configure_var_flag_map)
        duplicate_vars_names_set = be_var_names.intersection(conf_var_names)
        unified_flags = {}
        # Handle point #1 above. This ensures that we have only one variable
        # We resolve conflicts using combine
        if duplicate_vars_names_set:
            pre = '{s.name}@{s.version} :'.format(s=spec)
            tty.warn("{0} Detected flags set in both build environment "
                     " AND passed to configure. This is a bug in the"
                     " package.".format(pre))
            for dupe_flag in duplicate_vars_names_set:
                tty.warn("{0} {1} ".format(pre, dupe_flag))
                tty.warn("    setup_build_environment: {0}"
                         "".format(build_var_flag_map[dupe_flag]))
                tty.warn("    configure_args         : {0}"
                         "".format(configure_var_flag_map[dupe_flag]))
                # define some policy... combine both ...
                unified_flags[dupe_flag] = configure_var_flag_map[dupe_flag]
                unified_flags[dupe_flag] += ' '
                unified_flags[dupe_flag] += build_var_flag_map[dupe_flag]

        # handle the build enviroment flags
        for flag in be_var_names.difference(duplicate_vars_names_set):
            tty.debug("Setting {0}={1} (from setup_build_environment)"
                      .format(flag, build_var_flag_map[flag]))
            unified_flags[flag] = build_var_flag_map[flag]

        # handle the package provided flags
        for flag in conf_var_names.difference(duplicate_vars_names_set):
            tty.debug("Setting {0}={1} (from configure_args)"
                      .format(flag, configure_var_flag_map[flag]))
            unified_flags[flag] = configure_var_flag_map[flag]

        return unified_flags

    def _configure_apply_build_type(self,
                                    spec,
                                    flag_map,
                                    add_if_var_undefined=True):
        '''Support a CMake-like build_tyle
        Caveats: an autotools package may define **NO** flag variables
        E.g., CFLAGS and friends.  In that case, we will not have these
        variables defined i the `flag_map`.

        This will result in the flags never getting applied... which is
        exactly what we want to avoid - we *want* consistent application of
        said flags.

        The parameter: `add_if_var_undefined` defines the policy for adding
        flag variables if the package does not. A reasonable question is posed
        in `_enforce_user_flags_when_package_does_not_declare` about setting
        user provided flags.

        I feel we *should* set these variables if they do not. That makes it
        explicit. An alternative method would be modifying the spack wrappers
        to enforce a policy of setting - but that is not clear when evaluating
        e.g., config.log or even the `./configure` as displayed.

        Args:
            spec (Spec): the spec being evaluated
            flag_map (dict) [IN/OUT]: Dictionary of VAR=VAL.
                Will be modified in place to add build_type flags
                and potentially add flag varaibles
            add_if_var_undefined (bool): Whether to add flag variables if
                the package has not defined them.

        Returns:
            Nothing
        '''
        # Mimic cmake
        # 'Release', 'RelWithDebug', 'Debug', 'MinSizeRel'
        #
        # we could expose variants that are defaults to each...
        # but that bloats up the variant list. E.g.,
        # build_type_release_flags with default='-O3'
        #
        # You would have to define all 4 to enable full coverage
        # These seem like well defined basic flags - so maybe we can get
        # away with defaults... Windows compilers or odd ball machines
        # I am not familiar with is what bothers me.
        build_type_flags_map = {'release'      : '-O3',
                                'relwithdebug' : '-O3 -g',
                                'debug'        : '-g',
                                'minsizerel'   : '-Os',
                                'undefined'    : '',
                                }
        # get the build type as lower case
        build_type = spec.variants['build_type'].value.lower()
        # create a list from the string
        build_type_flags = build_type_flags_map[build_type].split()

        flag_variables = ['CFLAGS',
                          'CXXFLAGS',
                          'FFLAGS',
                          'FCFLAGS',
                          'F90FLAGS',
                          'F77FLAGS']

        # apply these flags if the variable is defined (see
        # `_enforce_user_flags_when_package_does_not_declare`
        # for a discussion on whether to set the flags if the variable
        # is not declared.
        for flag_env_var_name in flag_variables:
            # add the variable and flags if it doens't exist.
            # subject to `add_if_var_undefined`
            if flag_env_var_name not in flag_map and add_if_var_undefined:
                flag_map[flag_env_var_name] = ' '.join(build_type_flags)

            # the case the flag var is set
            elif flag_env_var_name in flag_map:
                existing_flags = flag_map[flag_env_var_name]
                existing_flags_set = set(existing_flags.split())
                new_flags = set(build_type_flags)
                # prepend if they don't exist already
                for new_flag in new_flags:
                    if new_flag not in existing_flags_set:
                        existing_flags = new_flag + ' ' + existing_flags
                        flag_map[flag_env_var_name] = existing_flags

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :py:meth:`~.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        options = ['--prefix={0}'.format(prefix)]

        # tty.debug("Testing configure_flag_args for user provided flags")
        build_env_flag_args = getattr(self, 'configure_flag_args', [])
        # given some args to configure, test them for bad flag behavior
        # return a split list of args for configure:
        #   The flag args (fargs) and the non-flag configure args (cargs)
        # Return value is a dict for fargs and list for others
        arg_src = 'setup_build_environment'
        be_fargs, be_cargs = self._configure_check_flags(spec,
                                                         build_env_flag_args,
                                                         arg_src)

        # tty.debug("Testing configure_args for user provided flags")
        # gather the package defined configured args
        pkg_configure_args = self.configure_args()
        # Test the package configure_args for bad flag behavior
        # return a split list of args for configure
        # Return value is a dict for flag args (fargs), and list for others
        arg_src = 'configure_args'
        pkg_fargs, pkg_cargs = self._configure_check_flags(spec,
                                                           pkg_configure_args,
                                                           arg_src)

        # reconcile build env flags and pkg configure_args ... better not
        # exist in both! It would mean setup_build_environment defined an
        # ENV, then configure was passed something else
        unified_flags = self._reconcile_var_args(
            spec,
            build_var_flag_map=be_fargs,
            configure_var_flag_map=pkg_fargs)

        # Now that we know all flag variables set (and their values)
        # handle the case the user declared a some flags (cflags=foo),
        # but the package never set CFLAGS
        # this modifies the `unified_flags` dict in place
        self._enforce_user_flags_when_package_does_not_declare(spec,
                                                               unified_flags)

        # this is where we can apply uniform flags (such as build_system)
        # DISABLED initially - included to demostrate why the prior effort
        # make this clean to implement
        #
        # self._configure_apply_build_type(spec, unified_flags)

        # we could apply some deduplication (but that is tricky)
        # for now, flatten the dict of VAR : VAL to a list of [ "VAR=VAL" ]
        flag_args = ['{0}={1}'.format(k, v) for k, v in unified_flags.items()]
        options += be_cargs + pkg_cargs + flag_args

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

    def _activate_or_not(
            self,
            name,
            activation_word,
            deactivation_word,
            activation_value=None
    ):
        """This function contains the current implementation details of
        :py:meth:`~.AutotoolsPackage.with_or_without` and
        :py:meth:`~.AutotoolsPackage.enable_or_disable`.

        Args:
            name (str): name of the variant that is being processed
            activation_word (str): the default activation word ('with' in the
                case of ``with_or_without``)
            deactivation_word (str): the default deactivation word ('without'
                in the case of ``with_or_without``)
            activation_value (callable): callable that accepts a single
                value. This value is either one of the allowed values for a
                multi-valued variant or the name of a bool-valued variant.
                Returns the parameter to be used when the value is activated.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Examples:

            Given a package with:

            .. code-block:: python

                variant('foo', values=('x', 'y'), description='')
                variant('bar', default=True, description='')

            calling this function like:

            .. code-block:: python

                _activate_or_not(
                    'foo', 'with', 'without', activation_value='prefix'
                )
                _activate_or_not('bar', 'with', 'without')

            will generate the following configuration options:

            .. code-block:: console

                --with-x=<prefix-to-x> --without-y --with-bar

            for ``<spec-name> foo=x +bar``

        Returns:
            list of strings that corresponds to the activation/deactivation
            of the variant that has been processed

        Raises:
            KeyError: if name is not among known variants
        """
        spec = self.spec
        args = []

        if activation_value == 'prefix':
            activation_value = lambda x: spec[x].prefix

        # Defensively look that the name passed as argument is among
        # variants
        if name not in self.variants:
            msg = '"{0}" is not a variant of "{1}"'
            raise KeyError(msg.format(name, self.name))

        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        if set(self.variants[name].values) == set((True, False)):
            # BoolValuedVariant carry information about a single option.
            # Nonetheless, for uniformity of treatment we'll package them
            # in an iterable of one element.
            condition = '+{name}'.format(name=name)
            options = [(name, condition in spec)]
        else:
            condition = '{name}={value}'
            # "feature_values" is used to track values which correspond to
            # features which can be enabled or disabled as understood by the
            # package's build system. It excludes values which have special
            # meanings and do not correspond to features (e.g. "none")
            feature_values = getattr(
                self.variants[name].values, 'feature_values', None
            ) or self.variants[name].values

            options = [
                (value, condition.format(name=name, value=value) in spec)
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

    def with_or_without(self, name, activation_value=None):
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
            activation_value (callable): callable that accepts a single
                value and returns the parameter to be used leading to an entry
                of the type ``--with-{name}={parameter}``.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(name, 'with', 'without', activation_value)

    def enable_or_disable(self, name, activation_value=None):
        """Same as :py:meth:`~.AutotoolsPackage.with_or_without` but substitute
        ``with`` with ``enable`` and ``without`` with ``disable``.

        Args:
            name (str): name of a valid multi-valued variant
            activation_value (callable): if present accepts a single value
                and returns the parameter to be used leading to an entry of the
                type ``--enable-{name}={parameter}``

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(
            name, 'enable', 'disable', activation_value
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

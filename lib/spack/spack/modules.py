##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""
This module contains code for creating environment modules, which can include dotkits, tcl modules, lmod, and others.

The various types of modules are installed by post-install hooks and removed after an uninstall by post-uninstall hooks.
This class consolidates the logic for creating an abstract description of the information that module systems need.
Currently that includes a number of directories to be appended to paths in the user's environment:

  * /bin directories to be appended to PATH
  * /lib* directories for LD_LIBRARY_PATH
  * /include directories for CPATH
  * /man* and /share/man* directories for MANPATH
  * the package prefix for CMAKE_PREFIX_PATH

This module also includes logic for coming up with unique names for the module files so that they can be found by the
various shell-support files in $SPACK/share/spack/setup-env.*.

Each hook in hooks/ implements the logic for writing its specific type of module file.
"""
import os
import os.path
import re
import shutil
import textwrap

import llnl.util.tty as tty
import spack
import spack.config
from llnl.util.filesystem import join_path, mkdirp
from spack.build_environment import parent_class_modules, set_module_variables_for_package
from spack.environment import *

__all__ = ['EnvModule', 'Dotkit', 'TclModule']

# Registry of all types of modules.  Entries created by EnvModule's metaclass
module_types = {}

CONFIGURATION = spack.config.get_config('modules')


def print_help():
    """For use by commands to tell user how to activate shell support."""

    tty.msg("This command requires spack's shell integration.",
            "",
            "To initialize spack's shell commands, you must run one of",
            "the commands below.  Choose the right command for your shell.",
            "",
            "For bash and zsh:",
            "    . %s/setup-env.sh" % spack.share_path,
            "",
            "For csh and tcsh:",
            "    setenv SPACK_ROOT %s"    % spack.prefix,
            "    source %s/setup-env.csh" % spack.share_path,
            "")


def inspect_path(prefix):
    """
    Inspects the prefix of an installation to search for common layouts. Issues a request to modify the environment
    accordingly when an item is found.

    Args:
        prefix: prefix of the installation

    Returns:
        instance of EnvironmentModifications containing the requested modifications
    """
    env = EnvironmentModifications()
    # Inspect the prefix to check for the existence of common directories
    prefix_inspections = {
        'bin': ('PATH',),
        'man': ('MANPATH',),
        'lib': ('LIBRARY_PATH', 'LD_LIBRARY_PATH'),
        'lib64': ('LIBRARY_PATH', 'LD_LIBRARY_PATH'),
        'include': ('CPATH',)
    }
    for attribute, variables in prefix_inspections.items():
        expected = getattr(prefix, attribute)
        if os.path.isdir(expected):
            for variable in variables:
                env.prepend_path(variable, expected)
    # PKGCONFIG
    for expected in (join_path(prefix.lib, 'pkgconfig'), join_path(prefix.lib64, 'pkgconfig')):
        if os.path.isdir(expected):
            env.prepend_path('PKG_CONFIG_PATH', expected)
    # CMake related variables
    env.prepend_path('CMAKE_PREFIX_PATH', prefix)
    return env


class EnvModule(object):
    name = 'env_module'
    formats = {}

    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if cls.name != 'env_module' and cls.name in CONFIGURATION['enable']:
                module_types[cls.name] = cls

    def __init__(self, spec=None):
        self.spec = spec
        self.pkg = spec.package  # Just stored for convenience

        # short description default is just the package + version
        # packages can provide this optional attribute
        self.short_description = spec.format("$_ $@")
        if hasattr(self.pkg, 'short_description'):
            self.short_description = self.pkg.short_description

        # long description is the docstring with reduced whitespace.
        self.long_description = None
        if self.spec.package.__doc__:
            self.long_description = re.sub(r'\s+', ' ', self.spec.package.__doc__)


    @property
    def category(self):
        # Anything defined at the package level takes precedence
        if hasattr(self.pkg, 'category'):
            return self.pkg.category
        # Extensions
        for extendee in self.pkg.extendees:
            return '{extendee} extension'.format(extendee=extendee)
        # Not very descriptive fallback
        return 'spack installed package'


    def write(self):
        """Write out a module file for this object."""
        module_dir = os.path.dirname(self.file_name)
        if not os.path.exists(module_dir):
            mkdirp(module_dir)

        # Environment modifications guessed by inspecting the
        # installation prefix
        env = inspect_path(self.spec.prefix)

        # Let the extendee/dependency modify their extensions/dependencies before asking for
        # package-specific modifications
        spack_env = EnvironmentModifications()

        def dependencies():
            # FIXME : during module file creation nodes seem to be visited multiple times even if cover='nodes'
            # FIXME : is given. This work around permits to get a unique list of spec anyhow.
            # FIXME : Possibly we miss a merge step among nodes that refer to the same package.
            l = [x for x in sorted(self.spec.traverse(order='post', depth=True, cover='nodes'),reverse=True)]
            seen = set()
            return [x for ii, x in l if not (x in seen or seen.add(x))]

        for item in dependencies():
            try:
                package = self.spec[item.name].package
                modules = parent_class_modules(package.__class__)
                for mod in modules:
                    set_module_variables_for_package(package, mod)
                set_module_variables_for_package(package, package.module)
                package.setup_dependent_package(self.pkg.module, self.spec)
                package.setup_dependent_environment(spack_env, env, self.spec)
            except KeyError as e:
                # The extends was conditional, so it doesn't count here
                # eg: extends('python', when='+python')
                tty.debug(str(e))

        # Package-specific environment modifications
        set_module_variables_for_package(self.pkg, self.pkg.module)
        self.spec.package.setup_environment(spack_env, env)

        # TODO : implement site-specific modifications and filters
        if not env:
            return

        # Filter modifications to the environment according to configuration files
        try:
            filter_list = CONFIGURATION[self.name]['filter']['environment_modifications']
        except KeyError:
            filter_list = []

        with open(self.file_name, 'w') as f:
            self.write_header(f)
            for line in self.process_environment_command(
                    filter_environment_modifications(env, filter_list)
            ):
                f.write(line)

    def write_header(self, stream):
        raise NotImplementedError()

    def process_environment_command(self, env):
        for command in env:
            try:
                yield self.formats[type(command)].format(**command.args)
            except KeyError:
                tty.warn('Cannot handle command of type {command} : skipping request'.format(command=type(command)))
                tty.warn('{context} at {filename}:{lineno}'.format(**command.args))


    @property
    def file_name(self):
        """Subclasses should implement this to return the name of the file
           where this module lives."""
        raise NotImplementedError()

    @property
    def use_name(self):
        """Subclasses should implement this to return the name the
           module command uses to refer to the package."""
        raise NotImplementedError()

    def remove(self):
        mod_file = self.file_name
        if os.path.exists(mod_file):
            shutil.rmtree(mod_file, ignore_errors=True)


class Dotkit(EnvModule):
    name = 'dotkit'
    path = join_path(spack.share_path, "dotkit")

    formats = {
        PrependPath: 'dk_alter {name} {value}\n',
        SetEnv: 'dk_setenv {name} {value}\n'
    }

    @property
    def file_name(self):
        return join_path(Dotkit.path, self.spec.architecture, '%s.dk' % self.use_name)

    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version,
                                 self.spec.dag_hash())

    def write_header(self, dk_file):
        # Category
        if self.category:
            dk_file.write('#c %s\n' % self.category)

        # Short description
        if self.short_description:
            dk_file.write('#d %s\n' % self.short_description)

        # Long description
        if self.long_description:
            for line in textwrap.wrap(self.long_description, 72):
                dk_file.write("#h %s\n" % line)


class TclModule(EnvModule):
    name = 'tcl'
    path = join_path(spack.share_path, "modules")

    formats = {
        PrependPath: 'prepend-path {name} \"{value}\"\n',
        AppendPath: 'append-path {name} \"{value}\"\n',
        RemovePath: 'remove-path {name} \"{value}\"\n',
        SetEnv: 'setenv {name} \"{value}\"\n',
        UnsetEnv: 'unsetenv {name}\n'
    }

    @property
    def file_name(self):
        return join_path(TclModule.path, self.spec.architecture, self.use_name)

    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version,
                                 self.spec.dag_hash())

    def write_header(self, module_file):
        # TCL Modulefile header
        module_file.write('#%Module1.0\n')
        # TODO : category ?
        # Short description
        if self.short_description:
            module_file.write('module-whatis \"%s\"\n\n' % self.short_description)

        # Long description
        if self.long_description:
            module_file.write('proc ModulesHelp { } {\n')
            for line in textwrap.wrap(self.long_description, 72):
                module_file.write("puts stderr \"%s\"\n" % line)
            module_file.write('}\n\n')

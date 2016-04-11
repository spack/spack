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
import copy

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


def dependencies(spec, request='all'):
    if request == 'none':
        return []

    l = [xx for xx in
         sorted(spec.traverse(order='post', depth=True, cover='nodes', root=False), reverse=True)]

    if request == 'direct':
        return [xx for ii, xx in l if ii == 1]

    # FIXME : during module file creation nodes seem to be visited multiple times even if cover='nodes'
    # FIXME : is given. This work around permits to get a unique list of spec anyhow.
    # FIXME : Possibly we miss a merge step among nodes that refer to the same package.
    seen = set()
    seen_add = seen.add
    return [xx for ii, xx in l if not (xx in seen or seen_add(xx))]


def parse_config_options(module_generator):
    autoloads, prerequisites, filters = [], [], []
    env = EnvironmentModifications()
    # Get the configuration for this kind of generator
    try:
        module_configuration = copy.copy(CONFIGURATION[module_generator.name])
    except KeyError:
        return autoloads, prerequisites, filters, env

    # Get the defaults for all packages
    all_conf = module_configuration.pop('all', {})

    update_single(module_generator.spec, all_conf, autoloads, prerequisites, filters, env)

    for spec, conf in module_configuration.items():
        override = False
        if spec.endswith(':'):
            spec = spec.strip(':')
            override = True
        if module_generator.spec.satisfies(spec):
            if override:
                autoloads, prerequisites, filters = [], [], []
                env = EnvironmentModifications()
            update_single(module_generator.spec, conf, autoloads, prerequisites, filters, env)

    return autoloads, prerequisites, filters, env


def update_single(spec, configuration, autoloads, prerequisites, filters, env):
    # Get list of modules that will be loaded automatically
    try:
        autoloads.extend(dependencies(spec, configuration['autoload']))
    except KeyError:
        pass
    try:
        prerequisites.extend(dependencies(spec, configuration['prerequisites']))
    except KeyError:
        pass

    # Filter modifications to environment variables
    try:
        filters.extend(configuration['filter']['environment_blacklist'])
    except KeyError:
        pass

    try:
        for method, arglist in configuration['environment'].items():
            for item in arglist:
                if method == 'unset':
                    args = [item]
                else:
                    args = item.split(',')
                getattr(env, method)(*args)
    except KeyError:
        pass


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
        """
        Writes out a module file for this object.

        This method employs a template pattern and expects derived classes to:
        - override the header property
        - provide formats for autoload, prerequisites and environment changes
        """
        module_dir = os.path.dirname(self.file_name)
        if not os.path.exists(module_dir):
            mkdirp(module_dir)

        # Environment modifications guessed by inspecting the
        # installation prefix
        env = inspect_path(self.spec.prefix)

        # Let the extendee/dependency modify their extensions/dependencies before asking for
        # package-specific modifications
        spack_env = EnvironmentModifications()
        # TODO : the code down below is quite similar to build_environment.setup_package and needs to be
        # TODO : factored out to a single place
        for item in dependencies(self.spec, 'All'):
            package = self.spec[item.name].package
            modules = parent_class_modules(package.__class__)
            for mod in modules:
                set_module_variables_for_package(package, mod)
            set_module_variables_for_package(package, package.module)
            package.setup_dependent_package(self.pkg.module, self.spec)
            package.setup_dependent_environment(spack_env, env, self.spec)

        # Package-specific environment modifications
        set_module_variables_for_package(self.pkg, self.pkg.module)
        self.spec.package.setup_environment(spack_env, env)

        # Parse configuration file
        autoloads, prerequisites, filters, conf_env = parse_config_options(self)
        env.extend(conf_env)

        # Build up the module file content
        module_file_content = self.header
        for x in autoloads:
            module_file_content += self.autoload(x)
        for x in prerequisites:
            module_file_content += self.prerequisite(x)
        for line in self.process_environment_command(filter_environment_blacklist(env, filters)):
            module_file_content += line

        # Dump to file
        with open(self.file_name, 'w') as f:
            f.write(module_file_content)

    @property
    def header(self):
        raise NotImplementedError()

    def autoload(self, spec):
        m = TclModule(spec)
        return self.autoload_format.format(module_file=m.use_name)

    def prerequisite(self, spec):
        m = TclModule(spec)
        return self.prerequisite_format.format(module_file=m.use_name)

    def process_environment_command(self, env):
        for command in env:
            try:
                yield self.environment_modifications_formats[type(command)].format(**command.args)
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
            try:
                os.remove(mod_file)  # Remove the module file
                os.removedirs(os.path.dirname(mod_file))  # Remove all the empty directories from the leaf up
            except OSError:
                pass  # removedirs throws OSError on first non-empty directory found


class Dotkit(EnvModule):
    name = 'dotkit'
    path = join_path(spack.share_path, "dotkit")

    environment_modifications_formats = {
        PrependPath: 'dk_alter {name} {value}\n',
        SetEnv: 'dk_setenv {name} {value}\n'
    }

    autoload_format = 'dk_op {module_file}\n'  # TODO : Check this line

    prerequisite_format = None  # TODO : does something like prerequisite exist for dotkit?

    @property
    def file_name(self):
        return join_path(Dotkit.path, self.spec.architecture, '%s.dk' % self.use_name)

    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version,
                                 self.spec.dag_hash())

    @property
    def header(self):
        # Category
        header = ''
        if self.category:
            header += '#c %s\n' % self.category

        # Short description
        if self.short_description:
            header += '#d %s\n' % self.short_description

        # Long description
        if self.long_description:
            for line in textwrap.wrap(self.long_description, 72):
                header += '#h %s\n' % line
        return header


class TclModule(EnvModule):
    name = 'tcl'
    path = join_path(spack.share_path, "modules")

    environment_modifications_formats = {
        PrependPath: 'prepend-path {name} \"{value}\"\n',
        AppendPath: 'append-path {name} \"{value}\"\n',
        RemovePath: 'remove-path {name} \"{value}\"\n',
        SetEnv: 'setenv {name} \"{value}\"\n',
        UnsetEnv: 'unsetenv {name}\n'
    }

    autoload_format = ('if ![ is-loaded {module_file} ] {{\n'
                       '    puts stderr "Autoloading {module_file}"\n'
                       '    module load {module_file}\n'
                       '}}\n')

    prerequisite_format = 'prereq {module_file}\n'

    @property
    def file_name(self):
        return join_path(TclModule.path, self.spec.architecture, self.use_name)

    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version,
                                 self.spec.dag_hash())

    @property
    def header(self):
        # TCL Modulefile header
        header = '#%Module1.0\n'
        # TODO : category ?
        # Short description
        if self.short_description:
            header += 'module-whatis \"%s\"\n\n' % self.short_description

        # Long description
        if self.long_description:
            header += 'proc ModulesHelp { } {\n'
            for line in textwrap.wrap(self.long_description, 72):
                header += 'puts stderr "%s"\n' % line
            header += '}\n\n'
        return header

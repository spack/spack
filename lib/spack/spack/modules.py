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
"""
This module contains code for creating environment modules, which can include
dotkits, tcl modules, lmod, and others.

The various types of modules are installed by post-install hooks and removed
after an uninstall by post-uninstall hooks. This class consolidates the logic
for creating an abstract description of the information that module systems
need.

This module also includes logic for coming up with unique names for the module
files so that they can be found by the various shell-support files in
$SPACK/share/spack/setup-env.*.

Each hook in hooks/ implements the logic for writing its specific type of
module file.
"""
import copy
import datetime
import itertools
import os
import os.path
import re
import string
import textwrap

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack
import spack.compilers  # Needed by LmodModules
import spack.config
from spack.util.path import canonicalize_path
from spack.build_environment import parent_class_modules
from spack.build_environment import set_module_variables_for_package
from spack.environment import *

__all__ = ['EnvModule', 'Dotkit', 'TclModule']

"""Registry of all types of modules.  Entries created by EnvModule's
   metaclass."""
module_types = {}

"""Module install roots are in config.yaml."""
_roots = spack.config.get_config('config').get('module_roots', {})

"""Specifics about modules are in modules.yaml"""
_module_config = spack.config.get_config('modules')


def print_help():
    """
    For use by commands to tell user how to activate shell support.
    """
    tty.msg("This command requires spack's shell integration.", "",
            "To initialize spack's shell commands, you must run one of",
            "the commands below.  Choose the right command for your shell.",
            "", "For bash and zsh:",
            "    . %s/setup-env.sh" % spack.share_path, "",
            "For csh and tcsh:", "    setenv SPACK_ROOT %s" % spack.prefix,
            "    source %s/setup-env.csh" % spack.share_path, "")


def inspect_path(prefix):
    """
    Inspects the prefix of an installation to search for common layouts. Issues
    a request to modify the environment accordingly when an item is found.

    Args:
        prefix: prefix of the installation

    Returns:
        instance of EnvironmentModifications containing the requested
        modifications
    """
    env = EnvironmentModifications()
    # Inspect the prefix to check for the existence of common directories
    prefix_inspections = _module_config.get('prefix_inspections', {})
    for relative_path, variables in prefix_inspections.items():
        expected = join_path(prefix, relative_path)
        if os.path.isdir(expected):
            for variable in variables:
                env.prepend_path(variable, expected)
    return env


def dependencies(spec, request='all'):
    """
    Returns the list of dependent specs for a given spec, according to the
    given request

    Args:
        spec: target spec
        request: either 'none', 'direct' or 'all'

    Returns:
        empty list if 'none', direct dependency list if 'direct', all
        dependencies if 'all'
    """
    if request not in ('none', 'direct', 'all'):
        message = "Wrong value for argument 'request' : "
        message += "should be one of ('none', 'direct', 'all')"
        raise tty.error(message + " [current value is '%s']" % request)

    if request == 'none':
        return []

    if request == 'direct':
        return spec.dependencies(deptype=('link', 'run'))

    # FIXME : during module file creation nodes seem to be visited multiple
    # FIXME : times even if cover='nodes' is given. This work around permits
    # FIXME : to get a unique list of spec anyhow. Do we miss a merge
    # FIXME : step among nodes that refer to the same package?
    seen = set()
    seen_add = seen.add
    l = sorted(
        spec.traverse(order='post',
                      cover='nodes',
                      deptype=('link', 'run'),
                      root=False),
        reverse=True)
    return [x for x in l if not (x in seen or seen_add(x))]


def update_dictionary_extending_lists(target, update):
    for key in update:
        value = target.get(key, None)
        if isinstance(value, list):
            target[key].extend(update[key])
        elif isinstance(value, dict):
            update_dictionary_extending_lists(target[key], update[key])
        else:
            target[key] = update[key]


def parse_config_options(module_generator):
    """
    Parse the configuration file and returns a bunch of items that will be
    needed during module file generation

    Args:
        module_generator: module generator for a given spec

    Returns:
        autoloads: list of specs to be autoloaded
        prerequisites: list of specs to be marked as prerequisite
        filters: list of environment variables whose modification is
        blacklisted in module files
        env: list of custom environment modifications to be applied in the
        module file
    """
    # Get the configuration for this kind of generator
    module_configuration = copy.deepcopy(_module_config.get(
        module_generator.name, {}))

    #####
    # Merge all the rules
    #####
    module_file_actions = module_configuration.pop('all', {})
    for spec, conf in module_configuration.items():
        override = False
        if spec.endswith(':'):
            spec = spec.strip(':')
            override = True
        if module_generator.spec.satisfies(spec):
            if override:
                module_file_actions = {}
            update_dictionary_extending_lists(module_file_actions, conf)

    #####
    # Process the common rules
    #####

    # Automatic loading loads
    module_file_actions['hash_length'] = module_configuration.get(
        'hash_length', 7)
    module_file_actions['autoload'] = dependencies(
        module_generator.spec, module_file_actions.get('autoload', 'none'))
    # Prerequisites
    module_file_actions['prerequisites'] = dependencies(
        module_generator.spec, module_file_actions.get('prerequisites',
                                                       'none'))
    # Environment modifications
    environment_actions = module_file_actions.pop('environment', {})
    env = EnvironmentModifications()

    def process_arglist(arglist):
        if method == 'unset':
            for x in arglist:
                yield (x, )
        else:
            for x in arglist.iteritems():
                yield x

    for method, arglist in environment_actions.items():
        for args in process_arglist(arglist):
            getattr(env, method)(*args)

    return module_file_actions, env


def filter_blacklisted(specs, module_name):
    """
    Given a sequence of specs, filters the ones that are blacklisted in the
    module configuration file.

    Args:
        specs: sequence of spec instances
        module_name: type of module file objects

    Yields:
        non blacklisted specs
    """
    for x in specs:
        if module_types[module_name](x).blacklisted:
            tty.debug('\tFILTER : %s' % x)
            continue
        yield x


def format_env_var_name(name):
    return name.replace('-', '_').upper()


class EnvModule(object):
    name = 'env_module'
    formats = {}

    class __metaclass__(type):

        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if cls.name != 'env_module' and cls.name in _module_config[
                    'enable']:
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
            self.long_description = re.sub(r'\s+', ' ',
                                           self.spec.package.__doc__)

    @property
    def naming_scheme(self):
        try:
            naming_scheme = _module_config[self.name]['naming_scheme']
        except KeyError:
            naming_scheme = self.default_naming_format
        return naming_scheme

    @property
    def use_name(self):
        """
        Subclasses should implement this to return the name the module command
        uses to refer to the package.
        """
        name = self.spec.format(self.naming_scheme)
        # Not everybody is working on linux...
        parts = name.split('/')
        name = join_path(*parts)
        # Add optional suffixes based on constraints
        path_elements = [name] + self._get_suffixes()
        return '-'.join(path_elements)

    def _get_suffixes(self):
        configuration, _ = parse_config_options(self)
        suffixes = []
        for constraint, suffix in configuration.get('suffixes', {}).items():
            if constraint in self.spec:
                suffixes.append(suffix)
        hash_length = configuration.get('hash_length', 7)
        if hash_length != 0:
            suffixes.append(self.spec.dag_hash(length=hash_length))
        return suffixes

    @property
    def category(self):
        # Anything defined at the package level takes precedence
        if hasattr(self.pkg, 'category'):
            return self.pkg.category
        # Extensions
        for extendee in self.pkg.extendees:
            return '{extendee}_extension'.format(extendee=extendee)
        # Not very descriptive fallback
        return 'spack'

    @property
    def blacklisted(self):
        configuration = _module_config.get(self.name, {})
        whitelist_matches = [x
                             for x in configuration.get('whitelist', [])
                             if self.spec.satisfies(x)]
        blacklist_matches = [x
                             for x in configuration.get('blacklist', [])
                             if self.spec.satisfies(x)]
        blacklist_implicits = configuration.get('blacklist_implicits')
        installed_implicitly = not self.spec._installed_explicitly()
        blacklisted_as_implicit = blacklist_implicits and installed_implicitly

        if whitelist_matches:
            message = '\tWHITELIST : %s [matches : ' % self.spec.cshort_spec
            for rule in whitelist_matches:
                message += '%s ' % rule
            message += ' ]'
            tty.debug(message)

        if blacklist_matches:
            message = '\tBLACKLIST : %s [matches : ' % self.spec.cshort_spec
            for rule in blacklist_matches:
                message += '%s ' % rule
            message += ' ]'
            tty.debug(message)

        if blacklisted_as_implicit:
            message = '\tBLACKLISTED_AS_IMPLICIT : %s' % \
                      self.spec.cshort_spec
            tty.debug(message)

        is_blacklisted = blacklist_matches or blacklisted_as_implicit
        if not whitelist_matches and is_blacklisted:
            return True

        return False

    def write(self, overwrite=False):
        """
        Writes out a module file for this object.

        This method employs a template pattern and expects derived classes to:
        - override the header property
        - provide formats for autoload, prerequisites and environment changes
        """
        if self.blacklisted:
            return
        tty.debug("\tWRITE : %s [%s]" %
                  (self.spec.cshort_spec, self.file_name))

        module_dir = os.path.dirname(self.file_name)
        if not os.path.exists(module_dir):
            mkdirp(module_dir)

        # Environment modifications guessed by inspecting the
        # installation prefix
        env = inspect_path(self.spec.prefix)

        # Let the extendee/dependency modify their extensions/dependencies
        # before asking for package-specific modifications
        spack_env = EnvironmentModifications()
        # TODO : the code down below is quite similar to
        # TODO : build_environment.setup_package and needs to be factored out
        # TODO : to a single place
        for item in dependencies(self.spec, 'all'):
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
        module_configuration, conf_env = parse_config_options(self)
        env.extend(conf_env)
        filters = module_configuration.get('filter', {}).get(
            'environment_blacklist', {})
        # Build up the module file content
        module_file_content = self.header
        for x in filter_blacklisted(
                module_configuration.pop('autoload', []), self.name):
            module_file_content += self.autoload(x)
        for x in module_configuration.pop('load', []):
            module_file_content += self.autoload(x)
        for x in filter_blacklisted(
                module_configuration.pop('prerequisites', []), self.name):
            module_file_content += self.prerequisite(x)
        for line in self.process_environment_command(
                filter_environment_blacklist(env, filters)):
            module_file_content += line
        for line in self.module_specific_content(module_configuration):
            module_file_content += line

        # Print a warning in case I am accidentally overwriting
        # a module file that is already there (name clash)
        if not overwrite and os.path.exists(self.file_name):
            message = 'Module file already exists : skipping creation\n'
            message += 'file : {0.file_name}\n'
            message += 'spec : {0.spec}'
            tty.warn(message.format(self))
            return

        # Dump to file
        with open(self.file_name, 'w') as f:
            f.write(module_file_content)

    @property
    def header(self):
        raise NotImplementedError()

    def module_specific_content(self, configuration):
        return tuple()

    # Subclasses can return a fragment of module code that prints out
    # a warning that modules are being autoloaded.
    def autoload_warner(self):
        return ''

    def autoload(self, spec):
        if not isinstance(spec, str):
            m = type(self)(spec)
            module_file = m.use_name
        else:
            module_file = spec
        return self.autoload_format.format(
            module_file=module_file,
            warner=self.autoload_warner().format(module_file=module_file))

    def prerequisite(self, spec):
        m = type(self)(spec)
        return self.prerequisite_format.format(module_file=m.use_name)

    def process_environment_command(self, env):
        for command in env:
            # Token expansion from configuration file
            name = format_env_var_name(
                self.spec.format(command.args.get('name', '')))
            value = self.spec.format(str(command.args.get('value', '')))
            command.update_args(name=name, value=value)
            # Format the line int the module file
            try:
                yield self.environment_modifications_formats[type(
                    command)].format(**command.args)
            except KeyError:
                message = ('Cannot handle command of type {command}: '
                           'skipping request')
                details = '{context} at {filename}:{lineno}'
                tty.warn(message.format(command=type(command)))
                tty.warn(details.format(**command.args))

    @property
    def file_name(self):
        """Subclasses should implement this to return the name of the file
           where this module lives."""
        raise NotImplementedError()

    def remove(self):
        mod_file = self.file_name
        if os.path.exists(mod_file):
            try:
                os.remove(mod_file)  # Remove the module file
                os.removedirs(
                    os.path.dirname(mod_file)
                )  # Remove all the empty directories from the leaf up
            except OSError:
                # removedirs throws OSError on first non-empty directory found
                pass

    def verbose_autoload(self):
        configuration = _module_config.get(self.name, {})
        return configuration.get('verbose_autoload', True)


class Dotkit(EnvModule):
    name = 'dotkit'
    path = canonicalize_path(
        _roots.get(name, join_path(spack.share_path, name)))

    environment_modifications_formats = {
        PrependPath: 'dk_alter {name} {value}\n',
        RemovePath: 'dk_unalter {name} {value}\n',
        SetEnv: 'dk_setenv {name} {value}\n'
    }

    autoload_format = 'dk_op {module_file}\n'

    default_naming_format = \
        '${PACKAGE}-${VERSION}-${COMPILERNAME}-${COMPILERVER}'

    @property
    def file_name(self):
        return join_path(self.path, self.spec.architecture,
                         '%s.dk' % self.use_name)

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

    def prerequisite(self, spec):
        tty.warn('prerequisites:  not supported by dotkit module files')
        tty.warn('\tYou may want to check %s/modules.yaml'
                 % spack.user_config_path)
        return ''


class TclModule(EnvModule):
    name = 'tcl'
    path = canonicalize_path(
        _roots.get(name, join_path(spack.share_path, 'modules')))

    def autoload_warner(self):
        if self.verbose_autoload():
            return 'puts stderr "Autoloading {module_file}"\n'
        return ''

    autoload_format = ('if ![ is-loaded {module_file} ] {{\n'
                       '    {warner}'
                       '    module load {module_file}\n'
                       '}}\n\n')

    prerequisite_format = 'prereq {module_file}\n'

    default_naming_format = \
        '${PACKAGE}-${VERSION}-${COMPILERNAME}-${COMPILERVER}'

    @property
    def file_name(self):
        return join_path(self.path, self.spec.architecture, self.use_name)

    @property
    def header(self):
        timestamp = datetime.datetime.now()
        # TCL Modulefile header
        header = """\
#%%Module1.0
## Module file created by spack (https://github.com/LLNL/spack) on %s
##
## %s
##
""" % (timestamp, self.spec.short_spec)

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

    def process_environment_command(self, env):
        environment_modifications_formats_colon = {
            PrependPath: 'prepend-path {name} \"{value}\"\n',
            AppendPath: 'append-path   {name} \"{value}\"\n',
            RemovePath: 'remove-path   {name} \"{value}\"\n',
            SetEnv: 'setenv {name} \"{value}\"\n',
            UnsetEnv: 'unsetenv {name}\n'
        }
        environment_modifications_formats_general = {
            PrependPath:
            'prepend-path --delim "{separator}" {name} \"{value}\"\n',
            AppendPath:
            'append-path   --delim "{separator}" {name} \"{value}\"\n',
            RemovePath:
            'remove-path   --delim "{separator}" {name} \"{value}\"\n',
            SetEnv: 'setenv {name} \"{value}\"\n',
            UnsetEnv: 'unsetenv {name}\n'
        }
        for command in env:
            # Token expansion from configuration file
            name = format_env_var_name(
                self.spec.format(command.args.get('name', '')))
            value = self.spec.format(str(command.args.get('value', '')))
            command.update_args(name=name, value=value)
            # Format the line int the module file
            try:
                if command.args.get('separator', ':') == ':':
                    yield environment_modifications_formats_colon[type(
                        command)].format(**command.args)
                else:
                    yield environment_modifications_formats_general[type(
                        command)].format(**command.args)
            except KeyError:
                message = ('Cannot handle command of type {command}: '
                           'skipping request')
                details = '{context} at {filename}:{lineno}'
                tty.warn(message.format(command=type(command)))
                tty.warn(details.format(**command.args))

    def module_specific_content(self, configuration):
        # Conflict
        conflict_format = configuration.get('conflict', [])
        f = string.Formatter()
        for item in conflict_format:
            line = 'conflict ' + item + '\n'
            if len([x for x in f.parse(line)
                    ]) > 1:  # We do have placeholder to substitute
                for naming_dir, conflict_dir in zip(
                        self.naming_scheme.split('/'), item.split('/')):
                    if naming_dir != conflict_dir:
                        message = 'conflict scheme does not match naming '
                        message += 'scheme [{spec}]\n\n'
                        message += 'naming scheme   : "{nformat}"\n'
                        message += 'conflict scheme : "{cformat}"\n\n'
                        message += '** You may want to check your '
                        message += '`modules.yaml` configuration file **\n'
                        tty.error(message.format(spec=self.spec,
                                                 nformat=self.naming_scheme,
                                                 cformat=item))
                        raise SystemExit('Module generation aborted.')
                line = self.spec.format(line)
            yield line

# To construct an arbitrary hierarchy of module files:
# 1. Parse the configuration file and check that all the items in
#    hierarchical_scheme are indeed virtual packages
#    This needs to be done only once at start-up
# 2. Order the stack as `hierarchical_scheme + ['mpi, 'compiler']
# 3. Check which of the services are provided by the package
#    -> may be more than one
# 4. Check which of the services are needed by the package
#    -> this determines where to write the module file
# 5. For each combination of services in which we have at least one provider
#    here add the appropriate conditional MODULEPATH modifications


class LmodModule(EnvModule):
    name = 'lmod'
    path = canonicalize_path(
        _roots.get(name, join_path(spack.share_path, name)))

    environment_modifications_formats = {
        PrependPath: 'prepend_path("{name}", "{value}")\n',
        AppendPath: 'append_path("{name}", "{value}")\n',
        RemovePath: 'remove_path("{name}", "{value}")\n',
        SetEnv: 'setenv("{name}", "{value}")\n',
        UnsetEnv: 'unsetenv("{name}")\n'
    }

    def autoload_warner(self):
        if self.verbose_autoload():
            return 'LmodMessage("Autoloading {module_file}")\n'
        return ''

    autoload_format = ('if not isloaded("{module_file}") then\n'
                       '    {warner}'
                       '    load("{module_file}")\n'
                       'end\n\n')

    prerequisite_format = 'prereq("{module_file}")\n'

    family_format = 'family("{family}")\n'

    path_part_without_hash = join_path('{token.name}', '{token.version}')

    # TODO : Check that extra tokens specified in configuration file
    # TODO : are actually virtual dependencies
    configuration = _module_config.get('lmod', {})
    hierarchy_tokens = configuration.get('hierarchical_scheme', [])
    hierarchy_tokens = hierarchy_tokens + ['mpi', 'compiler']

    def __init__(self, spec=None):
        super(LmodModule, self).__init__(spec)

        self.configuration = _module_config.get('lmod', {})
        hierarchy_tokens = self.configuration.get('hierarchical_scheme', [])
        # TODO : Check that the extra hierarchy tokens specified in the
        # TODO : configuration file are actually virtual dependencies
        self.hierarchy_tokens = hierarchy_tokens + ['mpi', 'compiler']

        # Sets the root directory for this architecture
        self.modules_root = join_path(LmodModule.path, self.spec.architecture)

        # Retrieve core compilers
        self.core_compilers = self.configuration.get('core_compilers', [])
        # Keep track of the requirements that this package has in terms
        # of virtual packages that participate in the hierarchical structure
        self.requires = {'compiler': self.spec.compiler}
        # For each virtual dependency in the hierarchy
        for x in self.hierarchy_tokens:
            if x in self.spec and not self.spec.package.provides(
                    x):  # if I depend on it
                self.requires[x] = self.spec[x]  # record the actual provider
        # Check what are the services I need (this will determine where the
        # module file will be written)
        self.substitutions = {}
        self.substitutions.update(self.requires)
        # TODO : complete substitutions
        # Check what service I provide to others
        self.provides = {}
        # If it is in the list of supported compilers family -> compiler
        if self.spec.name in spack.compilers.supported_compilers():
            self.provides['compiler'] = spack.spec.CompilerSpec(str(self.spec))
        # Special case for llvm
        if self.spec.name == 'llvm':
            self.provides['compiler'] = spack.spec.CompilerSpec(str(self.spec))
            self.provides['compiler'].name = 'clang'

        for x in self.hierarchy_tokens:
            if self.spec.package.provides(x):
                self.provides[x] = self.spec[x]

    def _hierarchy_token_combinations(self):
        """
        Yields all the relevant combinations that could appear in the hierarchy
        """
        for ii in range(len(self.hierarchy_tokens) + 1):
            for item in itertools.combinations(self.hierarchy_tokens, ii):
                if 'compiler' in item:
                    yield item

    def _hierarchy_to_be_provided(self):
        """
        Filters a list of hierarchy tokens and yields only the one that we
        need to provide
        """
        for item in self._hierarchy_token_combinations():
            if any(x in self.provides for x in item):
                yield item

    def token_to_path(self, name, value):
        # If we are dealing with a core compiler, return 'Core'
        if name == 'compiler' and str(value) in self.core_compilers:
            return 'Core'
        # CompilerSpec does not have an hash
        if name == 'compiler':
            return self.path_part_without_hash.format(token=value)
        # In this case the hierarchy token refers to a virtual provider
        path = self.path_part_without_hash.format(token=value)
        path = '-'.join([path, value.dag_hash(length=7)])
        return path

    @property
    def file_name(self):
        parts = [self.token_to_path(x, self.requires[x])
                 for x in self.hierarchy_tokens if x in self.requires]
        hierarchy_name = join_path(*parts)
        fullname = join_path(self.modules_root, hierarchy_name,
                             self.use_name + '.lua')
        return fullname

    @property
    def use_name(self):
        path_elements = [self.spec.format("${PACKAGE}/${VERSION}")]
        # The remaining elements are filename suffixes
        path_elements.extend(self._get_suffixes())
        return '-'.join(path_elements)

    def modulepath_modifications(self):
        # What is available is what we require plus what we provide
        entry = ''
        available = {}
        available.update(self.requires)
        available.update(self.provides)
        available_parts = [self.token_to_path(x, available[x])
                           for x in self.hierarchy_tokens if x in available]
        # Missing parts
        missing = [x for x in self.hierarchy_tokens if x not in available]
        # Direct path we provide on top of compilers
        modulepath = join_path(self.modules_root, *available_parts)
        env = EnvironmentModifications()
        env.prepend_path('MODULEPATH', modulepath)
        for line in self.process_environment_command(env):
            entry += line

        def local_variable(x):
            lower, upper = x.lower(), x.upper()
            fmt = 'local {lower}_name = os.getenv("LMOD_{upper}_NAME")\n'
            fmt += 'local {lower}_version = os.getenv("LMOD_{upper}_VERSION")\n'  # NOQA: ignore=501
            return fmt.format(lower=lower, upper=upper)

        def set_variables_for_service(env, x):
            upper = x.upper()
            s = self.provides[x]
            name, version = os.path.split(self.token_to_path(x, s))

            env.set('LMOD_{upper}_NAME'.format(upper=upper), name)
            env.set('LMOD_{upper}_VERSION'.format(upper=upper), version)

        def conditional_modulepath_modifications(item):
            entry = 'if '
            needed = []
            for x in self.hierarchy_tokens:
                if x in missing:
                    needed.append('{x}_name '.format(x=x))
            entry += 'and '.join(needed) + 'then\n'
            entry += '  local t = pathJoin("{root}"'.format(
                root=self.modules_root)
            for x in item:
                if x in missing:
                    entry += ', {lower}_name, {lower}_version'.format(
                        lower=x.lower())
                else:
                    entry += ', "{x}"'.format(
                        x=self.token_to_path(x, available[x]))
            entry += ')\n'
            entry += '  prepend_path("MODULEPATH", t)\n'
            entry += 'end\n\n'
            return entry

        if 'compiler' not in self.provides:
            # Retrieve variables
            entry += '\n'
            for x in missing:
                entry += local_variable(x)
            entry += '\n'
            # Conditional modifications
            conditionals = [x
                            for x in self._hierarchy_to_be_provided()
                            if any(t in missing for t in x)]
            for item in conditionals:
                entry += conditional_modulepath_modifications(item)

            # Set environment variables for the services we provide
            env = EnvironmentModifications()
            for x in self.provides:
                set_variables_for_service(env, x)
            for line in self.process_environment_command(env):
                entry += line

        return entry

    @property
    def header(self):
        timestamp = datetime.datetime.now()
        # Header as in
        # https://www.tacc.utexas.edu/research-development/tacc-projects/lmod/advanced-user-guide/more-about-writing-module-files
        header = "-- -*- lua -*-\n"
        header += '-- Module file created by spack (https://github.com/LLNL/spack) on %s\n' % timestamp  # NOQA: ignore=E501
        header += '--\n'
        header += '-- %s\n' % self.spec.short_spec
        header += '--\n'

        # Short description -> whatis()
        if self.short_description:
            header += "whatis([[Name : {name}]])\n".format(name=self.spec.name)
            header += "whatis([[Version : {version}]])\n".format(
                version=self.spec.version)

        # Long description -> help()
        if self.long_description:
            doc = re.sub(r'"', '\"', self.long_description)
            header += "help([[{documentation}]])\n".format(documentation=doc)

        # Certain things need to be done only if we provide a service
        if self.provides:
            # Add family directives
            header += '\n'
            for x in self.provides:
                header += self.family_format.format(family=x)
            header += '\n'
            header += '-- MODULEPATH modifications\n'
            header += '\n'
            # Modify MODULEPATH
            header += self.modulepath_modifications()
            # Set environment variables for services we provide
            header += '\n'
            header += '-- END MODULEPATH modifications\n'
            header += '\n'

        return header

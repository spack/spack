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
"""Here we consolidate the logic for creating an abstract description
of the information that module systems need.

This information maps **a single spec** to:

  * a unique module filename
  * the module file content

and is divided among four classes:

  * a configuration class that provides a convenient interface to query
    configuration for the spec under consideration.

  * a layout class that provides the information associated with module
    file names and directories

  * a context class that provides the dictionary used byt the template engine
    to generate the module file

  * a writer that collects and uses the information above to either write
    or remove the module file

Each of the four classes needs to be sub-classed when implementing a new
module type.
"""
import copy
import datetime
import inspect
import os.path
import re

import llnl.util.filesystem
import llnl.util.tty as tty
import spack
import spack.build_environment as build_environment
import spack.environment
import spack.tengine as tengine
import spack.util.path

#: Root folders where the various module files should be written
roots = spack.config.get_config('config').get('module_roots', {})

#: Merged modules.yaml as a dictionary
configuration = spack.config.get_config('modules')

#: Inspections that needs to be done on spec prefixes
prefix_inspections = configuration.get('prefix_inspections', {})


def update_dictionary_extending_lists(target, update):
    """Updates a dictionary, but extends lists instead of overriding them.

    :param target: dictionary to be updated
    :param update: update to be applied
    """
    for key in update:
        value = target.get(key, None)
        if isinstance(value, list):
            target[key].extend(update[key])
        elif isinstance(value, dict):
            update_dictionary_extending_lists(target[key], update[key])
        else:
            target[key] = update[key]


def dependencies(spec, request='all'):
    """Returns the list of dependent specs for a given spec, according to the
    request passed as parameter.

    :param spec: spec to be analyzed
    :param request: either 'none', 'direct' or 'all'

    :return: empty list if 'none', direct dependency list if 'direct',
        all dependencies if 'all'
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


def merge_config_rules(configuration, spec):
    """Parses the module specific part of a configuration and returns a
    dictionary containing the actions to be performed on the spec passed as
    an argument.

    :param configuration: module specific configuration (e.g. entries under
        the top-level 'tcl' key
    :param spec: spec for which we need to generate a module file

    :return: dictionary with the actions to be taken on the spec passed
        as an argument
    """

    # Get the top-level configuration for the module type we are using
    module_specific_configuration = copy.deepcopy(configuration)

    # Construct a dictionary with the actions we need to perform on the spec
    # passed as a parameter

    # The keyword 'all' is always evaluated first, all the others are
    # evaluated in order of appearance in the module file
    spec_configuration = module_specific_configuration.pop('all', {})
    for constraint, action in module_specific_configuration.items():
        override = False
        if constraint.endswith(':'):
            constraint = constraint.strip(':')
            override = True
        if spec.satisfies(constraint):
            if override:
                spec_configuration = {}
            update_dictionary_extending_lists(spec_configuration, action)

    # Attach options that are spec-independent to the spec-specific
    # configuration

    # Hash length in module files
    hash_length = module_specific_configuration.get('hash_length', 7)
    spec_configuration['hash_length'] = hash_length

    # Which modulefiles we want to autoload
    autoload_strategy = spec_configuration.get('autoload', 'none')
    spec_configuration['autoload'] = dependencies(spec, autoload_strategy)

    # Which instead we want to mark as prerequisites
    prerequisite_strategy = spec_configuration.get('prerequisites', 'none')
    l = dependencies(spec, prerequisite_strategy)
    spec_configuration['prerequisites'] = l

    return spec_configuration


def root_path(name):
    """Returns the root folder for module file installation.

    :param name: name of the module system t be used (e.g. 'tcl')
    :return: root folder for module file installation
    """
    path = roots.get(name, os.path.join(spack.share_path, name))
    return spack.util.path.canonicalize_path(path)


class BaseConfiguration(object):
    """Manipulates the information needed to generate a module file to make
    querying easier. It needs to be sub-classed for specific module types.
    """

    #: naming scheme suitable for non-hierarchical layouts
    naming_scheme = configuration.get(
        'naming_scheme', '${PACKAGE}-${VERSION}-${COMPILERNAME}-${COMPILERVER}'
    )

    def __init__(self, spec):
        # Module where type(self) is defined
        self.module = inspect.getmodule(self)
        # Spec for which we want to generate a module file
        self.spec = spec
        # Dictionary of configuration options that should be applied
        # to the spec
        self.conf = merge_config_rules(self.module.configuration, self.spec)

    @property
    def env(self):
        """List of environment modifications that should be done in the
        module.
        """
        l = spack.environment.EnvironmentModifications()
        actions = self.conf.get('environment', {})

        def process_arglist(arglist):
            if method == 'unset':
                for x in arglist:
                    yield (x,)
            else:
                for x in arglist.iteritems():
                    yield x

        for method, arglist in actions.items():
            for args in process_arglist(arglist):
                getattr(l, method)(*args)

        return l

    @property
    def suffixes(self):
        """List of suffixes that should be appended to the module
        file name.
        """
        suffixes = []
        for constraint, suffix in self.conf.get('suffixes', {}).items():
            if constraint in self.spec:
                suffixes.append(suffix)
        if self.hash:
            suffixes.append(self.hash)
        return suffixes

    @property
    def hash(self):
        """Hash tag for the module or None"""
        hash_length = self.conf.get('hash_length', 7)
        if hash_length != 0:
            return self.spec.dag_hash(length=hash_length)
        return None

    @property
    def blacklisted(self):
        """Returns True if the module has been blacklisted,
        False otherwise.
        """
        # A few variables for convenience of writing the method
        spec = self.spec
        conf = self.module.configuration

        # Compute the list of whitelist rules that match
        wlrules = conf.get('whitelist', [])
        whitelist_matches = [x for x in wlrules if spec.satisfies(x)]

        # Compute the list of blacklist rules that match
        blrules = conf.get('blacklist', [])
        blacklist_matches = [x for x in blrules if spec.satisfies(x)]

        # Should I blacklist the module because it's implicit?
        blacklist_implicits = conf.get('blacklist_implicits')
        installed_implicitly = not spec._installed_explicitly()
        blacklisted_as_implicit = blacklist_implicits and installed_implicitly

        def debug_info(line_header, match_list):
            if match_list:
                msg = '\t{0} : {1}'.format(line_header, spec.cshort_spec)
                tty.debug(msg)
                for rule in match_list:
                    tty.debug('\t\tmatches rule: {0}'.format(rule))

        debug_info('WHITELIST', whitelist_matches)
        debug_info('BLACKLIST', blacklist_matches)

        if blacklisted_as_implicit:
            msg = '\tBLACKLISTED_AS_IMPLICIT : {0}'.format(spec.cshort_spec)
            tty.debug(msg)

        is_blacklisted = blacklist_matches or blacklisted_as_implicit
        if not whitelist_matches and is_blacklisted:
            return True

        return False

    @property
    def specs_to_load(self):
        """List of specs that should be loaded in the module file."""
        return self._create_list_for('autoload')

    @property
    def literals_to_load(self):
        """List of literal modules to be loaded."""
        return self.conf.get('load', [])

    @property
    def specs_to_prereq(self):
        """List of specs that should be prerequisite of the module file."""
        return self._create_list_for('prerequisites')

    @property
    def environment_blacklist(self):
        """List of variables that should be left unmodified."""
        return self.conf.get('filter', {}).get('environment_blacklist', {})

    def _create_list_for(self, what):
        l = []
        for item in self.conf[what]:
            conf = type(self)(item)
            if not conf.blacklisted:
                l.append(item)
        return l

    @property
    def verbose(self):
        """Returns True if the module file needs to be verbose, False
        otherwise
        """
        return self.conf.get('verbose')


class BaseFileLayout(object):
    """Provides information on the layout of module files. Needs to be
    sub-classed for specific module types.
    """

    #: This needs to be redefined
    extension = None

    def __init__(self, configuration):
        self.conf = configuration

    @property
    def spec(self):
        """Spec under consideration"""
        return self.conf.spec

    @classmethod
    def dirname(cls):
        """Root folder for module files of this type."""
        module_system = str(inspect.getmodule(cls).__name__).split('.')[-1]
        return root_path(module_system)

    @property
    def use_name(self):
        """Returns the 'use' name of the module i.e. the name you have to type
        to console to use it. This implementation fits the needs of most
        non-hierarchical layouts.
        """
        name = self.spec.format(self.conf.naming_scheme)
        # Not everybody is working on linux...
        parts = name.split('/')
        name = os.path.join(*parts)
        # Add optional suffixes based on constraints
        path_elements = [name] + self.conf.suffixes
        return '-'.join(path_elements)

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = self.use_name
        if self.extension:
            filename = '{0}.{1}'.format(self.use_name, self.extension)
        # Architecture sub-folder
        arch_folder = str(self.spec.architecture)
        # Return the absolute path
        return os.path.join(self.dirname(), arch_folder, filename)


class BaseContext(tengine.ContextClass):
    """Provides the context needed for template rendering.

    This class needs to be sub-classed for specific module types. The
    following attributes need to be implemented:

    - fields

    """

    # FIXME: check autoload_warning

    def __init__(self, configuration):
        self.conf = configuration

    @property
    def spec(self):
        return self.conf.spec

    @property
    def timestamp(self):
        return datetime.datetime.now()

    @property
    def category(self):
        return getattr(self.spec, 'category', 'spack')

    @property
    def short_description(self):
        # short description default is just the package + version
        # packages can provide this optional attribute
        return getattr(
            self.spec.package, 'short_description', self.spec.format("$_ $@")
        )

    @property
    def long_description(self):
        # long description is the docstring with reduced whitespace.
        if self.spec.package.__doc__:
            return re.sub(r'\s+', ' ', self.spec.package.__doc__)
        return None

    @property
    def environment_modifications(self):
        """List of environment modifications to be processed."""
        # Modifications guessed inspecting the spec prefix
        env = spack.environment.inspect_path(
            self.spec.prefix, prefix_inspections
        )

        # Modifications that are coded at package level
        _ = spack.environment.EnvironmentModifications()
        # TODO : the code down below is quite similar to
        # TODO : build_environment.setup_package and needs to be factored out
        # TODO : to a single place
        # Let the extendee/dependency modify their extensions/dependencies
        # before asking for package-specific modifications
        for item in dependencies(self.spec, 'all'):
            package = self.spec[item.name].package
            modules = build_environment.parent_class_modules(package.__class__)
            for mod in modules:
                build_environment.set_module_variables_for_package(
                    package, mod
                )
            build_environment.set_module_variables_for_package(
                package, package.module
            )
            package.setup_dependent_package(
                self.spec.package.module, self.spec
            )
            package.setup_dependent_environment(_, env, self.spec)
        # Package specific modifications
        build_environment.set_module_variables_for_package(
            self.spec.package, self.spec.package.module
        )
        self.spec.package.setup_environment(_, env)

        # Modifications required from modules.yaml
        env.extend(self.conf.env)

        # List of variables that are blacklisted in modules.yaml
        blacklist = self.conf.environment_blacklist

        # We may have tokens to substitute in environment commands
        for x in env:
            x.name = self.spec.format(x.name)
            try:
                # Not every command has a value
                x.value = self.spec.format(x.value)
            except AttributeError:
                pass
            x.name = str(x.name).replace('-', '_').upper()

        return [(type(x).__name__, x) for x in env if x.name not in blacklist]

    @property
    def autoload(self):
        """List of modules that needs to be loaded automatically."""
        # From 'autoload' configuration option
        specs = self._create_module_list_of('specs_to_load')
        # From 'load' configuration option
        literals = self.conf.literals_to_load
        return specs + literals

    def _create_module_list_of(self, what):
        m = self.conf.module
        l = getattr(self.conf, what)
        return [m.make_layout(x).use_name for x in l]

    @property
    def verbose(self):
        """Verbosity level."""
        return self.conf.verbose


class BaseModuleFileWriter(object):
    def __init__(self, spec):
        self.spec = spec
        m = inspect.getmodule(self)
        self.conf = m.make_configuration(spec)
        self.layout = m.make_layout(spec)
        self.context = m.make_context(spec)

    def write(self, overwrite=False):
        """Writes the module file.

        :param bool overwrite: if True it is fine to overwrite an already
            existing file. If False the operation is skipped an we print
            a warning to the user.
        """
        # Return immediately if the module is blacklisted
        if self.conf.blacklisted:
            msg = '\tNOT WRITING: {0} [BLACKLISTED]'
            tty.debug(msg.format(self.spec.cshort_spec))
            return

        # Print a warning in case I am accidentally overwriting
        # a module file that is already there (name clash)
        if not overwrite and os.path.exists(self.layout.filename):
            message = 'Module file already exists : skipping creation\n'
            message += 'file : {0.filename}\n'
            message += 'spec : {0.spec}'
            tty.warn(message.format(self.layout))
            return

        # If we are here it means it's ok to write the module file
        msg = '\tWRITE: {0} [{1}]'
        tty.debug(msg.format(self.spec.cshort_spec, self.layout.filename))

        # If the directory where the module should reside does not exist
        # create it
        module_dir = os.path.dirname(self.layout.filename)
        if not os.path.exists(module_dir):
            llnl.util.filesystem.mkdirp(module_dir)

        # Get the template for the module
        # TODO: decide on a policy for extensions
        template = None
        for x in self.templates:
            try:
                template = tengine.env.get_template(x)
                break
            except tengine.TemplateNotFound:
                # FIXME: do something
                # FIXME: in case template is not found
                pass

        # Render the template
        text = template.render(self.context.as_dict())
        # Write it to file
        with open(self.layout.filename, 'w') as f:
            f.write(text)

    def remove(self):
        """Deletes the module file."""
        mod_file = self.layout.filename
        if os.path.exists(mod_file):
            try:
                os.remove(mod_file)  # Remove the module file
                os.removedirs(
                    os.path.dirname(mod_file)
                )  # Remove all the empty directories from the leaf up
            except OSError:
                # removedirs throws OSError on first non-empty directory found
                pass

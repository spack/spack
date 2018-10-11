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
from __future__ import print_function

"""This module implements Spack's configuration file handling.

This implements Spack's configuration system, which handles merging
multiple scopes with different levels of precedence.  See the
documentation on :ref:`configuration-scopes` for details on how Spack's
configuration system behaves.  The scopes are:

  #. ``default``
  #. ``system``
  #. ``site``
  #. ``user``

And corresponding :ref:`per-platform scopes <platform-scopes>`. Important
functions in this module are:

* :py:func:`get_config`
* :py:func:`update_config`

``get_config`` reads in YAML data for a particular scope and returns
it. Callers can then modify the data and write it back with
``update_config``.

When read in, Spack validates configurations with jsonschemas.  The
schemas are in submodules of :py:mod:`spack.schema`.

"""

import copy
import os
import re
import sys
import multiprocessing
from contextlib import contextmanager
from six import string_types
from six import iteritems
from ordereddict_backport import OrderedDict

import ruamel.yaml as yaml
from ruamel.yaml.error import MarkedYAMLError

import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack.paths
import spack.architecture
import spack.schema
from spack.error import SpackError

# Hacked yaml for configuration files preserves line numbers.
import spack.util.spack_yaml as syaml


#: Dict from section names -> schema for that section
section_schemas = {
    'compilers': spack.schema.compilers.schema,
    'mirrors': spack.schema.mirrors.schema,
    'repos': spack.schema.repos.schema,
    'packages': spack.schema.packages.schema,
    'modules': spack.schema.modules.schema,
    'config': spack.schema.config.schema,
}

#: Builtin paths to configuration files in Spack
configuration_paths = (
    # Default configuration scope is the lowest-level scope. These are
    # versioned with Spack and can be overridden by systems, sites or users
    ('defaults', os.path.join(spack.paths.etc_path, 'spack', 'defaults')),

    # System configuration is per machine.
    # No system-level configs should be checked into spack by default
    ('system', os.path.join(spack.paths.system_etc_path, 'spack')),

    # Site configuration is per spack instance, for sites or projects
    # No site-level configs should be checked into spack by default.
    ('site', os.path.join(spack.paths.etc_path, 'spack')),

    # User configuration can override both spack defaults and site config
    ('user', spack.paths.user_config_path)
)

#: Hard-coded default values for some key configuration options.
#: This ensures that Spack will still work even if config.yaml in
#: the defaults scope is removed.
config_defaults = {
    'config': {
        'debug': False,
        'verify_ssl': True,
        'checksum': True,
        'dirty': False,
        'build_jobs': multiprocessing.cpu_count(),
    }
}

#: metavar to use for commands that accept scopes
#: this is shorter and more readable than listing all choices
scopes_metavar = '{defaults,system,site,user}[/PLATFORM]'


def _extend_with_default(validator_class):
    """Add support for the 'default' attr for properties and patternProperties.

       jsonschema does not handle this out of the box -- it only
       validates.  This allows us to set default values for configs
       where certain fields are `None` b/c they're deleted or
       commented out.

    """
    import jsonschema
    validate_properties = validator_class.VALIDATORS["properties"]
    validate_pattern_properties = validator_class.VALIDATORS[
        "patternProperties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                instance.setdefault(
                    property, copy.deepcopy(subschema["default"]))
        for err in validate_properties(
                validator, properties, instance, schema):
            yield err

    def set_pp_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in iteritems(instance):
                        if re.match(property, key) and val is None:
                            instance[key] = copy.deepcopy(subschema["default"])

        for err in validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

    return jsonschema.validators.extend(validator_class, {
        "properties": set_defaults,
        "patternProperties": set_pp_defaults
    })


class ConfigScope(object):
    """This class represents a configuration scope.

       A scope is one directory containing named configuration files.
       Each file is a config "section" (e.g., mirrors, compilers, etc).
    """

    def __init__(self, name, path):
        self.name = name           # scope name.
        self.path = path           # path to directory containing configs.
        self.sections = syaml.syaml_dict()  # sections read from config files.

    def get_section_filename(self, section):
        _validate_section_name(section)
        return os.path.join(self.path, "%s.yaml" % section)

    def get_section(self, section):
        if section not in self.sections:
            path   = self.get_section_filename(section)
            schema = section_schemas[section]
            data   = _read_config_file(path, schema)
            self.sections[section] = data
        return self.sections[section]

    def write_section(self, section):
        filename = self.get_section_filename(section)
        data = self.get_section(section)
        try:
            mkdirp(self.path)
            with open(filename, 'w') as f:
                _validate_section(data, section_schemas[section])
                syaml.dump(data, stream=f, default_flow_style=False)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError(
                "Error writing to config file: '%s'" % str(e))

    def clear(self):
        """Empty cached config information."""
        self.sections = syaml.syaml_dict()

    def __repr__(self):
        return '<ConfigScope: %s: %s>' % (self.name, self.path)


class ImmutableConfigScope(ConfigScope):
    """A configuration scope that cannot be written to.

    This is used for ConfigScopes passed on the command line.
    """

    def write_section(self, section):
        raise ConfigError("Cannot write to immutable scope %s" % self)

    def __repr__(self):
        return '<ImmutableConfigScope: %s: %s>' % (self.name, self.path)


class InternalConfigScope(ConfigScope):
    """An internal configuration scope that is not persisted to a file.

    This is for spack internal use so that command-line options and
    config file settings are accessed the same way, and Spack can easily
    override settings from files.
    """
    def __init__(self, name, data=None):
        self.name = name
        self.sections = syaml.syaml_dict()

        if data:
            for section in data:
                dsec = data[section]
                _validate_section({section: dsec}, section_schemas[section])
                self.sections[section] = _mark_internal(
                    syaml.syaml_dict({section: dsec}), name)

    def get_section_filename(self, section):
        raise NotImplementedError(
            "Cannot get filename for InternalConfigScope.")

    def get_section(self, section):
        """Just reads from an internal dictionary."""
        if section not in self.sections:
            self.sections[section] = None
        return self.sections[section]

    def write_section(self, section):
        """This only validates, as the data is already in memory."""
        data = self.get_section(section)
        if data is not None:
            _validate_section(data, section_schemas[section])
        self.sections[section] = _mark_internal(data, self.name)

    def __repr__(self):
        return '<InternalConfigScope: %s>' % self.name


class Configuration(object):
    """A full Spack configuration, from a hierarchy of config files.

    This class makes it easy to add a new scope on top of an existing one.
    """

    def __init__(self, *scopes):
        """Initialize a configuration with an initial list of scopes.

        Args:
            scopes (list of ConfigScope): list of scopes to add to this
                Configuration, ordered from lowest to highest precedence

        """
        self.scopes = OrderedDict()
        for scope in scopes:
            self.push_scope(scope)

    def push_scope(self, scope):
        """Add a higher precedence scope to the Configuration."""
        self.scopes[scope.name] = scope

    def pop_scope(self):
        """Remove the highest precedence scope and return it."""
        name, scope = self.scopes.popitem(last=True)
        return scope

    @property
    def file_scopes(self):
        """List of writable scopes with an associated file."""
        return [s for s in self.scopes.values() if type(s) == ConfigScope]

    def highest_precedence_scope(self):
        """Non-internal scope with highest precedence."""
        return next(reversed(self.file_scopes), None)

    def _validate_scope(self, scope):
        """Ensure that scope is valid in this configuration.

        This should be used by routines in ``config.py`` to validate
        scope name arguments, and to determine a default scope where no
        scope is specified.

        Raises:
            ValueError: if ``scope`` is not valid

        Returns:
            ConfigScope: a valid ConfigScope if ``scope`` is ``None`` or valid
        """
        if scope is None:
            # default to the scope with highest precedence.
            return self.highest_precedence_scope()

        elif scope in self.scopes:
            return self.scopes[scope]

        else:
            raise ValueError("Invalid config scope: '%s'.  Must be one of %s"
                             % (scope, self.scopes.keys()))

    def get_config_filename(self, scope, section):
        """For some scope and section, get the name of the configuration file.
        """
        scope = self._validate_scope(scope)
        return scope.get_section_filename(section)

    def clear_caches(self):
        """Clears the caches for configuration files,

        This will cause files to be re-read upon the next request."""
        for scope in self.scopes.values():
            scope.clear()

    def update_config(self, section, update_data, scope=None):
        """Update the configuration file for a particular scope.

        Overwrites contents of a section in a scope with update_data,
        then writes out the config file.

        update_data should have the top-level section name stripped off
        (it will be re-added).  Data itself can be a list, dict, or any
        other yaml-ish structure.
        """
        _validate_section_name(section)  # validate section name
        scope = self._validate_scope(scope)  # get ConfigScope object

        # read only the requested section's data.
        scope.sections[section] = {section: update_data}
        scope.write_section(section)

    def get_config(self, section, scope=None):
        """Get configuration settings for a section.

        If ``scope`` is ``None`` or not provided, return the merged contents
        of all of Spack's configuration scopes.  If ``scope`` is provided,
        return only the confiugration as specified in that scope.

        This off the top-level name from the YAML section.  That is, for a
        YAML config file that looks like this::

           config:
             install_tree: $spack/opt/spack
             module_roots:
               lmod:   $spack/share/spack/lmod

        ``get_config('config')`` will return::

           { 'install_tree': '$spack/opt/spack',
             'module_roots: {
                 'lmod': '$spack/share/spack/lmod'
             }
           }

        """
        _validate_section_name(section)

        if scope is None:
            scopes = self.scopes.values()
        else:
            scopes = [self._validate_scope(scope)]

        merged_section = syaml.syaml_dict()
        for scope in scopes:
            # read potentially cached data from the scope.

            data = scope.get_section(section)

            # Skip empty configs
            if not data or not isinstance(data, dict):
                continue

            if section not in data:
                continue

            merged_section = _merge_yaml(merged_section, data)

        # no config files -- empty config.
        if section not in merged_section:
            return {}

        # take the top key off before returning.
        return merged_section[section]

    def get(self, path, default=None, scope=None):
        """Get a config section or a single value from one.

        Accepts a path syntax that allows us to grab nested config map
        entries.  Getting the 'config' section would look like::

            spack.config.get('config')

        and the ``dirty`` section in the ``config`` scope would be::

            spack.config.get('config:dirty')

        We use ``:`` as the separator, like YAML objects.
    """
        # TODO: Currently only handles maps. Think about lists if neded.
        section, _, rest = path.partition(':')

        value = self.get_config(section, scope=scope)
        if not rest:
            return value

        parts = rest.split(':')
        while parts:
            key = parts.pop(0)
            value = value.get(key, default)

        return value

    def set(self, path, value, scope=None):
        """Convenience function for setting single values in config files.

        Accepts the path syntax described in ``get()``.
        """
        section, _, rest = path.partition(':')

        if not rest:
            self.update_config(section, value, scope=scope)
        else:
            section_data = self.get_config(section, scope=scope)

            parts = rest.split(':')
            data = section_data
            while len(parts) > 1:
                key = parts.pop(0)
                data = data[key]
            data[parts[0]] = value

            self.update_config(section, section_data, scope=scope)

    def __iter__(self):
        """Iterate over scopes in this configuration."""
        for scope in self.scopes.values():
            yield scope

    def print_section(self, section, blame=False):
        """Print a configuration to stdout."""
        try:
            data = syaml.syaml_dict()
            data[section] = self.get_config(section)
            syaml.dump(
                data, stream=sys.stdout, default_flow_style=False, blame=blame)
        except (yaml.YAMLError, IOError):
            raise ConfigError("Error reading configuration: %s" % section)


@contextmanager
def override(path_or_scope, value=None):
    """Simple way to override config settings within a context.

    Arguments:
        path_or_scope (ConfigScope or str): scope or single option to override
        value (object, optional): value for the single option

    Temporarily push a scope on the current configuration, then remove it
    after the context completes. If a single option is provided, create
    an internal config scope for it and push/pop that scope.

    """
    if isinstance(path_or_scope, ConfigScope):
        config.push_scope(path_or_scope)
        yield config
        config.pop_scope(path_or_scope)

    else:
        overrides = InternalConfigScope('overrides')

        config.push_scope(overrides)
        config.set(path_or_scope, value, scope='overrides')

        yield config

        scope = config.pop_scope()
        assert scope is overrides


#: configuration scopes added on the command line
#: set by ``spack.main.main()``.
command_line_scopes = []


def _add_platform_scope(cfg, scope_type, name, path):
    """Add a platform-specific subdirectory for the current platform."""
    platform = spack.architecture.platform().name
    plat_name = '%s/%s' % (name, platform)
    plat_path = os.path.join(path, platform)
    cfg.push_scope(scope_type(plat_name, plat_path))


def _add_command_line_scopes(cfg, command_line_scopes):
    """Add additional scopes from the --config-scope argument.

    Command line scopes are named after their position in the arg list.
    """
    for i, path in enumerate(command_line_scopes):
        # We ensure that these scopes exist and are readable, as they are
        # provided on the command line by the user.
        if not os.path.isdir(path):
            raise ConfigError("config scope is not a directory: '%s'" % path)
        elif not os.access(path, os.R_OK):
            raise ConfigError("config scope is not readable: '%s'" % path)

        # name based on order on the command line
        name = 'cmd_scope_%d' % i
        cfg.push_scope(ImmutableConfigScope(name, path))
        _add_platform_scope(cfg, ImmutableConfigScope, name, path)


def _config():
    """Singleton Configuration instance.

    This constructs one instance associated with this module and returns
    it. It is bundled inside a function so that configuratoin can be
    initialized lazily.

    Return:
        (Configuration): object for accessing spack configuration

    """
    cfg = Configuration()

    # first do the builtin, hardcoded defaults
    defaults = InternalConfigScope('_builtin', config_defaults)
    cfg.push_scope(defaults)

    # add each scope and its platform-specific directory
    for name, path in configuration_paths:
        cfg.push_scope(ConfigScope(name, path))

        # Each scope can have per-platfom overrides in subdirectories
        _add_platform_scope(cfg, ConfigScope, name, path)

    # add command-line scopes
    _add_command_line_scopes(cfg, command_line_scopes)

    # we make a special scope for spack commands so that they can
    # override configuration options.
    cfg.push_scope(InternalConfigScope('command_line'))

    return cfg


#: This is the singleton configuration instance for Spack.
config = llnl.util.lang.Singleton(_config)


def get(path, default=None, scope=None):
    """Module-level wrapper for ``Configuration.get()``."""
    return config.get(path, default, scope)


def set(path, value, scope=None):
    """Convenience function for getting single values in config files.

    Accepts the path syntax described in ``get()``.
    """
    return config.set(path, value, scope)


def scopes():
    """Convenience function to get list of configuration scopes."""
    return config.scopes


def _validate_section_name(section):
    """Exit if the section is not a valid section."""
    if section not in section_schemas:
        raise ConfigSectionError(
            "Invalid config section: '%s'. Options are: %s"
            % (section, " ".join(section_schemas.keys())))


def _validate_section(data, schema):
    """Validate data read in from a Spack YAML file.

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.

    """
    import jsonschema
    if not hasattr(_validate_section, 'validator'):
        default_setting_validator = _extend_with_default(
            jsonschema.Draft4Validator)
        _validate_section.validator = default_setting_validator

    try:
        _validate_section.validator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise ConfigFormatError(e, data)


def _read_config_file(filename, schema):
    """Read a YAML configuration file."""
    # Ignore nonexisting files.
    if not os.path.exists(filename):
        return None

    elif not os.path.isfile(filename):
        raise ConfigFileError(
            "Invalid configuration. %s exists but is not a file." % filename)

    elif not os.access(filename, os.R_OK):
        raise ConfigFileError("Config file is not readable: %s" % filename)

    try:
        tty.debug("Reading config file %s" % filename)
        with open(filename) as f:
            data = _mark_overrides(syaml.load(f))

        if data:
            _validate_section(data, schema)
        return data

    except MarkedYAMLError as e:
        raise ConfigFileError(
            "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

    except IOError as e:
        raise ConfigFileError(
            "Error reading configuration file %s: %s" % (filename, str(e)))


def _override(string):
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `::`,
    and if they do, their values completely replace lower-precedence
    configs instead of merging into them.

    """
    return hasattr(string, 'override') and string.override


def _mark_overrides(data):
    if isinstance(data, list):
        return syaml.syaml_list(_mark_overrides(elt) for elt in data)

    elif isinstance(data, dict):
        marked = syaml.syaml_dict()
        for key, val in iteritems(data):
            if isinstance(key, string_types) and key.endswith(':'):
                key = syaml.syaml_str(key[:-1])
                key.override = True
            marked[key] = _mark_overrides(val)
        return marked

    else:
        return data


def _mark_internal(data, name):
    """Add a simple name mark to raw YAML/JSON data.

    This is used by `spack config blame` to show where config lines came from.
    """
    if isinstance(data, dict):
        d = syaml.syaml_dict((_mark_internal(k, name), _mark_internal(v, name))
                             for k, v in data.items())
    elif isinstance(data, list):
        d = syaml.syaml_list(_mark_internal(e, name) for e in data)
    else:
        d = syaml.syaml_type(data)

    if syaml.markable(d):
        d._start_mark = yaml.Mark(name, None, None, None, None, None)
        d._end_mark = yaml.Mark(name, None, None, None, None, None)

    return d


def _merge_yaml(dest, source):
    """Merges source into dest; entries in source take precedence over dest.

    This routine may modify dest and should be assigned to dest, in
    case dest was None to begin with, e.g.:

       dest = _merge_yaml(dest, source)

    Config file authors can optionally end any attribute in a dict
    with `::` instead of `:`, and the key will override that of the
    parent instead of merging.

    """
    def they_are(t):
        return isinstance(dest, t) and isinstance(source, t)

    # If both are None, handle specially and return None.
    if source is None and dest is None:
        return None

    # If source is None, overwrite with source.
    elif source is None:
        return None

    # Source list is prepended (for precedence)
    if they_are(list):
        dest[:] = source + [x for x in dest if x not in source]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        # track keys for marking
        key_marks = {}

        for sk, sv in iteritems(source):
            if _override(sk) or sk not in dest:
                # if sk ended with ::, or if it's new, completely override
                dest[sk] = copy.copy(sv)
            else:
                # otherwise, merge the YAML
                dest[sk] = _merge_yaml(dest[sk], source[sk])

            # this seems unintuitive, but see below. We need this because
            # Python dicts do not overwrite keys on insert, and we want
            # to copy mark information on source keys to dest.
            key_marks[sk] = sk

        # ensure that keys are marked in the destination.  the key_marks dict
        # ensures we can get the actual source key objects from dest keys
        for dk in dest.keys():
            if dk in key_marks:
                syaml.mark(dk, key_marks[dk])

        return dest

    # In any other case, overwrite with a copy of the source value.
    else:
        return copy.copy(source)


#
# Settings for commands that modify configuration
#
def default_modify_scope():
    """Return the config scope that commands should modify by default.

    Commands that modify configuration by default modify the *highest*
    priority scope.
    """
    return spack.config.config.highest_precedence_scope().name


def default_list_scope():
    """Return the config scope that is listed by default.

    Commands that list configuration list *all* scopes (merged) by default.
    """
    return None


class ConfigError(SpackError):
    """Superclass for all Spack config related errors."""


class ConfigSectionError(ConfigError):
    """Error for referring to a bad config section name in a configuration."""


class ConfigFileError(ConfigError):
    """Issue reading or accessing a configuration file."""


class ConfigFormatError(ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data):
        location = '<unknown file>'
        mark = self._get_mark(validation_error, data)
        if mark:
            location = '%s' % mark.name
            if mark.line is not None:
                location += ':%d' % (mark.line + 1)

        message = '%s: %s' % (location, validation_error.message)
        super(ConfigError, self).__init__(message)

    def _get_mark(self, validation_error, data):
        """Get the file/line mark fo a validation error from a Spack YAML file.
        """
        def _get_mark_or_first_member_mark(obj):
            # mark of object itelf
            mark = getattr(obj, '_start_mark', None)
            if mark:
                return mark

            # mark of first member if it is a container
            if isinstance(obj, (list, dict)):
                first_member = next(iter(obj), None)
                if first_member:
                    mark = getattr(first_member, '_start_mark', None)
                    if mark:
                        return mark

        # Try various places, starting with instance and parent
        for obj in (validation_error.instance, validation_error.parent):
            mark = _get_mark_or_first_member_mark(obj)
            if mark:
                return mark

        def get_path(path, data):
            if path:
                return get_path(path[1:], data[path[0]])
            else:
                return data

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        path = validation_error.path
        if path:
            parent = get_path(list(path)[:-1], data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = list(parent.keys())
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                mark = getattr(keylist[idx], '_start_mark', None)
                if mark:
                    return mark

        # give up and return None if nothing worked
        return None

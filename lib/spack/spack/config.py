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
"""This module implements Spack's configuration file handling.

This implements Spack's configuration system, which handles merging
multiple scopes with different levels of precedence.  See the
documentation on :ref:`configuration-scopes` for details on how Spack's
configuration system behaves.  The scopes are:

  #. ``default``
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
from six import string_types
from six import iteritems

import yaml
import jsonschema
from yaml.error import MarkedYAMLError
from jsonschema import Draft4Validator, validators
from ordereddict_backport import OrderedDict

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
import spack.architecture
from spack.error import SpackError
import spack.schema

# Hacked yaml for configuration files preserves line numbers.
import spack.util.spack_yaml as syaml


"""Dict from section names -> schema for that section."""
section_schemas = {
    'compilers': spack.schema.compilers.schema,
    'mirrors': spack.schema.mirrors.schema,
    'repos': spack.schema.repos.schema,
    'packages': spack.schema.packages.schema,
    'modules': spack.schema.modules.schema,
    'config': spack.schema.config.schema,
}

"""OrderedDict of config scopes keyed by name.
   Later scopes will override earlier scopes.
"""
config_scopes = OrderedDict()


def validate_section_name(section):
    """Exit if the section is not a valid section."""
    if section not in section_schemas:
        tty.die("Invalid config section: '%s'. Options are: %s"
                % (section, " ".join(section_schemas.keys())))


def extend_with_default(validator_class):
    """Add support for the 'default' attr for properties and patternProperties.

       jsonschema does not handle this out of the box -- it only
       validates.  This allows us to set default values for configs
       where certain fields are `None` b/c they're deleted or
       commented out.

    """
    validate_properties = validator_class.VALIDATORS["properties"]
    validate_pattern_properties = validator_class.VALIDATORS[
        "patternProperties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])
        for err in validate_properties(
                validator, properties, instance, schema):
            yield err

    def set_pp_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in iteritems(instance):
                        if re.match(property, key) and val is None:
                            instance[key] = subschema["default"]

        for err in validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

    return validators.extend(validator_class, {
        "properties": set_defaults,
        "patternProperties": set_pp_defaults
    })


DefaultSettingValidator = extend_with_default(Draft4Validator)


def validate_section(data, schema):
    """Validate data read in from a Spack YAML file.

    This leverages the line information (start_mark, end_mark) stored
    on Spack YAML structures.

    """
    try:
        DefaultSettingValidator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise ConfigFormatError(e, data)


class ConfigScope(object):
    """This class represents a configuration scope.

       A scope is one directory containing named configuration files.
       Each file is a config "section" (e.g., mirrors, compilers, etc).
    """

    def __init__(self, name, path):
        self.name = name           # scope name.
        self.path = path           # path to directory containing configs.
        self.sections = {}         # sections read from config files.

        # Register in a dict of all ConfigScopes
        # TODO: make this cleaner.  Mocking up for testing is brittle.
        global config_scopes
        config_scopes[name] = self

    def get_section_filename(self, section):
        validate_section_name(section)
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
                validate_section(data, section_schemas[section])
                syaml.dump(data, stream=f, default_flow_style=False)
        except jsonschema.ValidationError as e:
            raise ConfigSanityError(e, data)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError(
                "Error writing to config file: '%s'" % str(e))

    def clear(self):
        """Empty cached config information."""
        self.sections = {}

    def __repr__(self):
        return '<ConfigScope: %s: %s>' % (self.name, self.path)


#
# Below are configuration scopes.
#
# Each scope can have per-platfom overrides in subdirectories of the
# configuration directory.
#
_platform = spack.architecture.platform().name

"""Default configuration scope is the lowest-level scope. These are
   versioned with Spack and can be overridden by sites or users."""
_defaults_path = os.path.join(spack.etc_path, 'spack', 'defaults')
ConfigScope('defaults', _defaults_path)
ConfigScope('defaults/%s' % _platform, os.path.join(_defaults_path, _platform))

"""Site configuration is per spack instance, for sites or projects.
   No site-level configs should be checked into spack by default."""
_site_path = os.path.join(spack.etc_path, 'spack')
ConfigScope('site', _site_path)
ConfigScope('site/%s' % _platform, os.path.join(_site_path, _platform))

"""User configuration can override both spack defaults and site config."""
_user_path = spack.user_config_path
ConfigScope('user', _user_path)
ConfigScope('user/%s' % _platform, os.path.join(_user_path, _platform))


def highest_precedence_scope():
    """Get the scope with highest precedence (prefs will override others)."""
    return config_scopes.values()[-1]


def validate_scope(scope):
    """Ensure that scope is valid, and return a valid scope if it is None.

       This should be used by routines in ``config.py`` to validate
       scope name arguments, and to determine a default scope where no
       scope is specified.

    """
    if scope is None:
        # default to the scope with highest precedence.
        return highest_precedence_scope()

    elif scope in config_scopes:
        return config_scopes[scope]

    else:
        raise ValueError("Invalid config scope: '%s'.  Must be one of %s"
                         % (scope, config_scopes.keys()))


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
            validate_section(data, schema)
        return data

    except MarkedYAMLError as e:
        raise ConfigFileError(
            "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

    except IOError as e:
        raise ConfigFileError(
            "Error reading configuration file %s: %s" % (filename, str(e)))


def clear_config_caches():
    """Clears the caches for configuration files, which will cause them
       to be re-read upon the next request"""
    for scope in config_scopes.values():
        scope.clear()


def override(string):
    """Test if a spack YAML string is an override.

    See ``spack_yaml`` for details.  Keys in Spack YAML can end in `::`,
    and if they do, their values completely replace lower-precedence
    configs instead of merging into them.

    """
    return hasattr(string, 'override') and string.override


def _mark_overrides(data):
    if isinstance(data, list):
        return [_mark_overrides(elt) for elt in data]

    elif isinstance(data, dict):
        marked = {}
        for key, val in iteritems(data):
            if isinstance(key, string_types) and key.endswith(':'):
                key = syaml.syaml_str(key[:-1])
                key.override = True
            marked[key] = _mark_overrides(val)
        return marked

    else:
        return data


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
        for sk, sv in iteritems(source):
            if override(sk) or sk not in dest:
                # if sk ended with ::, or if it's new, completely override
                dest[sk] = copy.copy(sv)
            else:
                # otherwise, merge the YAML
                dest[sk] = _merge_yaml(dest[sk], source[sk])
        return dest

    # In any other case, overwrite with a copy of the source value.
    else:
        return copy.copy(source)


def get_config(section, scope=None):
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
    validate_section_name(section)
    merged_section = syaml.syaml_dict()

    if scope is None:
        scopes = config_scopes.values()
    else:
        scopes = [validate_scope(scope)]

    for scope in scopes:
        # read potentially cached data from the scope.
        data = scope.get_section(section)

        # Skip empty configs
        if not data or not isinstance(data, dict):
            continue

        if section not in data:
            tty.warn("Skipping bad configuration file: '%s'" % scope.path)
            continue

        merged_section = _merge_yaml(merged_section, data)

    # no config files -- empty config.
    if section not in merged_section:
        return {}

    # take the top key off before returning.
    return merged_section[section]


def get_config_filename(scope, section):
    """For some scope and section, get the name of the configuration file"""
    scope = validate_scope(scope)
    return scope.get_section_filename(section)


def update_config(section, update_data, scope=None):
    """Update the configuration file for a particular scope.

       Overwrites contents of a section in a scope with update_data,
       then writes out the config file.

       update_data should have the top-level section name stripped off
       (it will be re-added).  Data itself can be a list, dict, or any
       other yaml-ish structure.

    """
    validate_section_name(section)  # validate section name
    scope = validate_scope(scope)  # get ConfigScope object from string.

    # read in the config to ensure we've got current data
    configuration = get_config(section)

    if isinstance(update_data, list):
        configuration = update_data
    else:
        configuration.update(update_data)

    # read only the requested section's data.
    scope.sections[section] = {section: configuration}
    scope.write_section(section)


def print_section(section):
    """Print a configuration to stdout."""
    try:
        data = syaml.syaml_dict()
        data[section] = get_config(section)
        syaml.dump(data, stream=sys.stdout, default_flow_style=False)
    except (yaml.YAMLError, IOError):
        raise ConfigError("Error reading configuration: %s" % section)


class ConfigError(SpackError):
    pass


class ConfigFileError(ConfigError):
    pass


def get_path(path, data):
    if path:
        return get_path(path[1:], data[path[0]])
    else:
        return data


class ConfigFormatError(ConfigError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data):
        # Try to get line number from erroneous instance and its parent
        instance_mark = getattr(validation_error.instance, '_start_mark', None)
        parent_mark = getattr(validation_error.parent, '_start_mark', None)
        path = [str(s) for s in getattr(validation_error, 'path', None)]

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        if path and not parent_mark:
            parent_path = list(path)[:-1]
            parent = get_path(parent_path, data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = parent.keys()
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                parent_mark = getattr(keylist[idx], '_start_mark', None)

        if instance_mark:
            location = '%s:%d' % (instance_mark.name, instance_mark.line + 1)
        elif parent_mark:
            location = '%s:%d' % (parent_mark.name, parent_mark.line + 1)
        elif path:
            location = 'At ' + ':'.join(path)
        else:
            location = '<unknown line>'

        message = '%s: %s' % (location, validation_error.message)
        super(ConfigError, self).__init__(message)


class ConfigSanityError(ConfigFormatError):
    """Same as ConfigFormatError, raised when config is written by Spack."""

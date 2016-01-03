##############################################################################
# Copyright (c) 2013-2015, Lawrence Livermore National Security, LLC.
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
"""This module implements Spack's configuration file handling.

Configuration file scopes
===============================

When Spack runs, it pulls configuration data from several config
directories, each of which contains configuration files.  In Spack,
there are two configuration scopes:

 1. ``site``: Spack loads site-wide configuration options from
   ``$(prefix)/etc/spack/``.

 2. ``user``: Spack next loads per-user configuration options from
    ~/.spack/.

Spack may read configuration files from both of these locations.  When
configurations conflict, the user config options take precedence over
the site configurations.  Each configuration directory may contain
several configuration files, such as compilers.yaml or mirrors.yaml.

Configuration file format
===============================

Configuration files are formatted using YAML syntax.  This format is
implemented by libyaml (included with Spack as an external module),
and it's easy to read and versatile.

Config files are structured as trees, like this ``compiler`` section::

     compilers:
       chaos_5_x86_64_ib:
          gcc@4.4.7:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            f77: /usr/bin/gfortran
            fc: /usr/bin/gfortran
       bgqos_0:
          xlc@12.1:
            cc: /usr/local/bin/mpixlc
            ...

In this example, entries like ''compilers'' and ''xlc@12.1'' are used to
categorize entries beneath them in the tree.  At the root of the tree,
entries like ''cc'' and ''cxx'' are specified as name/value pairs.

``config.get_config()`` returns these trees as nested dicts, but it
strips the first level off.  So, ``config.get_config('compilers')``
would return something like this for the above example:

   { 'chaos_5_x86_64_ib' :
       { 'gcc@4.4.7' :
           { 'cc' : '/usr/bin/gcc',
             'cxx' : '/usr/bin/g++'
             'f77' : '/usr/bin/gfortran'
             'fc' : '/usr/bin/gfortran' }
           }
       { 'bgqos_0' :
          { 'cc' : '/usr/local/bin/mpixlc' } }

Likewise, the ``mirrors.yaml`` file's first line must be ``mirrors:``,
but ``get_config()`` strips that off too.

Precedence
===============================

``config.py`` routines attempt to recursively merge configuration
across scopes.  So if there are ``compilers.py`` files in both the
site scope and the user scope, ``get_config('compilers')`` will return
merged dictionaries of *all* the compilers available.  If a user
compiler conflicts with a site compiler, Spack will overwrite the site
configuration wtih the user configuration.  If both the user and site
``mirrors.yaml`` files contain lists of mirrors, then ``get_config()``
will return a concatenated list of mirrors, with the user config items
first.

Sometimes, it is useful to *completely* override a site setting with a
user one.  To accomplish this, you can use *two* colons at the end of
a key in a configuration file.  For example, this:

     compilers::
       chaos_5_x86_64_ib:
          gcc@4.4.7:
            cc: /usr/bin/gcc
            cxx: /usr/bin/g++
            f77: /usr/bin/gfortran
            fc: /usr/bin/gfortran
       bgqos_0:
          xlc@12.1:
            cc: /usr/local/bin/mpixlc
            ...

Will make Spack take compilers *only* from the user configuration, and
the site configuration will be ignored.

"""
import os
import sys
import copy

import yaml
from yaml.error import MarkedYAMLError
from ordereddict_backport import OrderedDict

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
from spack.error import SpackError

# Hacked yaml for configuration files preserves line numbers.
import spack.util.spack_yaml as syaml


"""Dict from section names -> function to check section YAML format."""
valid_sections = ['compilers', 'mirrors', 'repos']

"""OrderedDict of config scopes keyed by name.
   Later scopes will override earlier scopes.
"""
config_scopes = OrderedDict()


def validate_section(section):
    """Raise a ValueError if the section is not a valid section."""
    if section not in valid_sections:
        raise ValueError("Invalid config section: '%s'.  Options are %s."
                         % (section, valid_sections))


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
        validate_section(section)
        return os.path.join(self.path, "%s.yaml" % section)


    def get_section(self, section):
        if not section in self.sections:
            path = self.get_section_filename(section)
            data = _read_config_file(path)
            if data is None:
                self.sections[section] = {}
            else:
                self.sections[section] = data
        return self.sections[section]


    def write_section(self, section):
        filename = self.get_section_filename(section)
        data = self.get_section(section)
        try:
            mkdirp(self.path)
            with open(filename, 'w') as f:
                syaml.dump(data, stream=f, default_flow_style=False)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError("Error writing to config file: '%s'" % str(e))


    def clear(self):
        """Empty cached config information."""
        self.sections = {}


ConfigScope('site', os.path.join(spack.etc_path, 'spack')),
ConfigScope('user', os.path.expanduser('~/.spack'))


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
        raise ValueError("Invalid config scope: '%s'.  Must be one of %s."
                         % (scope, config_scopes.keys()))


def _read_config_file(filename):
    """Read a YAML configuration file."""
    # Ignore nonexisting files.
    if not os.path.exists(filename):
        return None

    elif not os.path.isfile(filename):
        raise ConfigFileError(
            "Invlaid configuration. %s exists but is not a file." % filename)

    elif not os.access(filename, os.R_OK):
        raise ConfigFileError("Config file is not readable: %s." % filename)

    try:
        with open(filename) as f:
            return syaml.load(f)

    except MarkedYAMLError, e:
        raise ConfigFileError(
            "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

    except IOError, e:
        raise ConfigFileError(
            "Error reading configuration file %s: %s" % (filename, str(e)))


def clear_config_caches():
    """Clears the caches for configuration files, which will cause them
       to be re-read upon the next request"""
    for scope in config_scopes.values():
        scope.clear()


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
        seen = set(source)
        dest[:] = source + [x for x in dest if x not in seen]
        return dest

    # Source dict is merged into dest.
    elif they_are(dict):
        for sk, sv in source.iteritems():
            if not sk in dest:
                dest[sk] = copy.copy(sv)
            else:
                dest[sk] = _merge_yaml(dest[sk], source[sk])
        return dest

    # In any other case, overwrite with a copy of the source value.
    else:
        return copy.copy(source)


def get_config(section, scope=None):
    """Get configuration settings for a section.

       Strips off the top-level section name from the YAML dict.
    """
    validate_section(section)
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

        # Allow complete override of site config with '<section>::'
        override_key = section + ':'
        if not (section in data or override_key in data):
            tty.warn("Skipping bad configuration file: '%s'" % scope.path)
            continue

        if override_key in data:
            merged_section = data[override_key]
        else:
            merged_section = _merge_yaml(merged_section, data[section])

    return merged_section


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
    # read in the config to ensure we've got current data
    get_config(section)

    validate_section(section)       # validate section name
    scope = validate_scope(scope)   # get ConfigScope object from string.

    # read only the requested section's data.
    scope.sections[section] = { section : update_data }
    scope.write_section(section)


"""Print a configuration to stdout"""
def print_section(section):
    try:
        yaml.dump(get_config(section), stream=sys.stdout, default_flow_style=False)
    except (yaml.YAMLError, IOError) as e:
        raise ConfigError("Error reading configuration: %s" % section)


class ConfigError(SpackError): pass
class ConfigFileError(ConfigError): pass
class ConfigFormatError(ConfigError): pass

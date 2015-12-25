##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
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
from external import yaml
from external.yaml.error import MarkedYAMLError

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

import spack
from spack.error import SpackError

"""List of valid config sections."""
valid_sections = ('compilers', 'mirrors', 'repos')


def check_section(section):
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


    def get_section_filename(self, section):
        check_section(section)
        return os.path.join(self.path, "%s.yaml" % section)


    def get_section(self, section):
        if not section in self.sections:
            path = self.get_section_filename(section)
            data = _read_config_file(path)
            self.sections[section] = {} if data is None else data
        return self.sections[section]


    def write_section(self, section):
        filename = self.get_section_filename(section)
        data = self.get_section(section)
        try:
            mkdirp(self.path)
            with open(filename, 'w') as f:
                yaml.dump(data, stream=f, default_flow_style=False)
        except (yaml.YAMLError, IOError) as e:
            raise ConfigFileError("Error writing to config file: '%s'" % str(e))


    def clear(self):
        """Empty cached config information."""
        self.sections = {}


"""List of config scopes by name.
   Later scopes in the list will override earlier scopes.
"""
config_scopes = [
    ConfigScope('site', os.path.join(spack.etc_path, 'spack')),
    ConfigScope('user', os.path.expanduser('~/.spack'))]

"""List of valid scopes, for convenience."""
valid_scopes = (s.name for s in config_scopes)


def check_scope(scope):
    if scope is None:
        return 'user'
    elif scope not in valid_scopes:
        raise ValueError("Invalid config scope: '%s'.  Must be one of %s."
                         % (scope, valid_scopes))
    return scope


def get_scope(scope):
    scope = check_scope(scope)
    return next(s for s in config_scopes if s.name == scope)


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
            return yaml.load(f)

    except MarkedYAMLError, e:
        raise ConfigFileError(
            "Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))

    except IOError, e:
        raise ConfigFileError(
            "Error reading configuration file %s: %s" % (filename, str(e)))


def clear_config_caches():
    """Clears the caches for configuration files, which will cause them
       to be re-read upon the next request"""
    for scope in config_scopes:
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

    # Source dict is merged into dest. Extra ':' means overwrite.
    elif they_are(dict):
        for sk, sv in source.iteritems():
            # allow total override with, e.g., repos::
            override = sk.endswith(':')
            if override:
                sk = sk.rstrip(':')

            if override or not sk in dest:
                dest[sk] = copy.copy(sv)
            else:
                dest[sk] = _merge_yaml(dest[sk], source[sk])
        return dest

    # In any other case, overwrite with a copy of the source value.
    else:
        return copy.copy(source)


def substitute_spack_prefix(path):
    """Replaces instances of $spack with Spack's prefix."""
    return path.replace('$spack', spack.prefix)


def get_config(section):
    """Get configuration settings for a section.

       Strips off the top-level section name from the YAML dict.
    """
    check_section(section)
    merged_section = {}

    for scope in config_scopes:
        # read potentially cached data from the scope.
        data = scope.get_section(section)
        if not data or not section in data:
            continue

        # extract data under the section name header
        data = data[section]

        # ignore empty sections for easy commenting of single-line configs.
        if not data:
            continue

        # merge config data from scopes.
        merged_section = _merge_yaml(merged_section, data)

    return merged_section


def get_repos_config():
    repo_list = get_config('repos')
    if repo_list is None:
        return []

    if not isinstance(repo_list, list):
        tty.die("Bad repository configuration. 'repos' element does not contain a list.")

    def expand_repo_path(path):
        path = substitute_spack_prefix(path)
        path = os.path.expanduser(path)
        return path
    return [expand_repo_path(repo) for repo in repo_list]


def get_config_filename(scope, section):
    """For some scope and section, get the name of the configuration file"""
    scope = get_scope(scope)
    return scope.get_section_filename(section)


def update_config(section, update_data, scope=None):
    """Update the configuration file for a particular scope.

       Merges contents of update_data into the scope's data for the
       specified section, then writes out the config file.

       update_data shoudl contain only the section's data, with the
       top-level name stripped off.  This can be a list, dict, or any
       other yaml-ish structure.

    """
    # read in the config to ensure we've got current data
    get_config(section)

    check_section(section)     # validate section name
    scope = get_scope(scope)   # get ConfigScope object from string.

    # read only the requested section's data.
    data = scope.get_section(section)
    data = _merge_yaml(data, { section : update_data })
    scope.write_section(section)


def remove_from_config(section, key_to_rm, scope=None):
    """Remove a configuration key and write updated configuration to disk.

       Return True if something was removed, False otherwise.

    """
    # ensure configs are current by reading in.
    get_config(section)

    # check args and get the objects we need.
    scope = get_scope(scope)
    data = scope.get_section(section)
    filename = scope.get_section_filename(section)

    # do some checks
    if not data:
        return False

    if not section in data:
        raise ConfigFileError("Invalid configuration file: '%s'" % filename)

    if key_to_rm not in section[section]:
        return False

    # remove the key from the section's configuration
    del data[section][key_to_rm]
    scope.write_section(section)


"""Print a configuration to stdout"""
def print_section(section):
    try:
        yaml.dump(get_config(section), stream=sys.stdout, default_flow_style=False)
    except (yaml.YAMLError, IOError) as e:
        raise ConfigError("Error reading configuration: %s" % section)


class ConfigError(SpackError): pass
class ConfigFileError(ConfigError): pass

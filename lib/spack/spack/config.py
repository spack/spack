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

Configuration files are formatted using YAML syntax.
This format is implemented by Python's
yaml class, and it's easy to read and versatile.

The config files are structured as trees, like this ``compiler`` section::

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

Spack returns these trees as nested dicts.  The dict for the above example
would looks like:

  { 'compilers' :
      { 'chaos_5_x86_64_ib' :
         { 'gcc@4.4.7' :
             { 'cc' : '/usr/bin/gcc',
               'cxx' : '/usr/bin/g++'
               'f77' : '/usr/bin/gfortran'
               'fc' : '/usr/bin/gfortran' }
         }
     { 'bgqos_0' :
         { 'cc' : '/usr/local/bin/mpixlc' }
     }
  }

Some routines, like get_mirrors_config and get_compilers_config may strip
off the top-levels of the tree and return subtrees.
"""
import os
import exceptions
import sys

from ordereddict_backport import OrderedDict
from llnl.util.lang import memoized
import spack.error

import yaml
from yaml.error import MarkedYAMLError
import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp

_config_sections = {}
class _ConfigCategory:
    name = None
    filename = None
    merge = True
    def __init__(self, n, f, m):
        self.name = n
        self.filename = f
        self.merge = m
        self.files_read_from = []
        self.result_dict = {}
        _config_sections[n] = self

_ConfigCategory('compilers', 'compilers.yaml', True)
_ConfigCategory('mirrors', 'mirrors.yaml', True)
_ConfigCategory('view', 'views.yaml', True)
_ConfigCategory('order', 'orders.yaml', True)

"""Names of scopes and their corresponding configuration files."""
config_scopes = [('site', os.path.join(spack.etc_path, 'spack')),
                 ('user', os.path.expanduser('~/.spack'))]

_compiler_by_arch = {}
_read_config_file_result = {}
def _read_config_file(filename):
    """Read a given YAML configuration file"""
    global _read_config_file_result
    if filename in _read_config_file_result:
        return _read_config_file_result[filename]

    try:
        with open(filename) as f:
            ydict = yaml.load(f)
    except MarkedYAMLError, e:
        tty.die("Error parsing yaml%s: %s" % (str(e.context_mark), e.problem))
    except exceptions.IOError, e:
        _read_config_file_result[filename] = None
        return None
    _read_config_file_result[filename] = ydict
    return ydict


def clear_config_caches():
    """Clears the caches for configuration files, which will cause them
       to be re-read upon the next request"""
    for key,s in _config_sections.iteritems():
        s.files_read_from = []
        s.result_dict = {}
    spack.config._read_config_file_result = {}
    spack.config._compiler_by_arch = {}
    spack.compilers._cached_default_compiler = None


def _merge_dicts(d1, d2):
    """Recursively merges two configuration trees, with entries
       in d2 taking precedence over d1"""
    if not d1:
        return d2.copy()
    if not d2:
        return d1

    for key2, val2 in d2.iteritems():
        if not key2 in d1:
            d1[key2] = val2
            continue
        val1 = d1[key2]
        if isinstance(val1, dict) and isinstance(val2, dict):
            d1[key2] = _merge_dicts(val1, val2)
            continue
        if isinstance(val1, list) and isinstance(val2, list):
            val1.extend(val2)
            seen = set()
            d1[key2] = [ x for x in val1 if not (x in seen or seen.add(x)) ]
            continue
        d1[key2] = val2
    return d1


def get_config(category_name):
    """Get the confguration tree for the names category.  Strips off the
       top-level category entry from the dict"""
    global config_scopes
    category = _config_sections[category_name]
    if category.result_dict:
        return category.result_dict

    category.result_dict = {}
    for scope, scope_path in config_scopes:
        path = os.path.join(scope_path, category.filename)
        result = _read_config_file(path)
        if not result:
            continue
        if not category_name in result:
            continue
        category.files_read_from.insert(0, path)
        result = result[category_name]
        if category.merge:
            category.result_dict = _merge_dicts(category.result_dict, result)
        else:
            category.result_dict = result
    return category.result_dict


def get_compilers_config(arch=None):
    """Get the compiler configuration from config files for the given
       architecture.  Strips off the architecture component of the
       configuration"""
    global _compiler_by_arch
    if not arch:
        arch = spack.architecture.sys_type()
    if arch in _compiler_by_arch:
        return _compiler_by_arch[arch]

    cc_config = get_config('compilers')
    if arch in cc_config and 'all' in cc_config:
        arch_compiler = dict(cc_config[arch])
        _compiler_by_arch[arch] = _merge_dict(arch_compiler, cc_config['all'])
    elif arch in cc_config:
        _compiler_by_arch[arch] = cc_config[arch]
    elif 'all' in cc_config:
        _compiler_by_arch[arch] = cc_config['all']
    else:
        _compiler_by_arch[arch] = {}
    return _compiler_by_arch[arch]


def get_mirror_config():
    """Get the mirror configuration from config files"""
    return get_config('mirrors')


def get_config_scope_dirname(scope):
    """For a scope return the config directory"""
    global config_scopes
    for s,p in config_scopes:
        if s == scope:
            return p
    tty.die("Unknown scope %s.  Valid options are %s" %
            (scope, ", ".join([s for s,p in config_scopes])))


def get_config_scope_filename(scope, category_name):
    """For some scope and category, get the name of the configuration file"""
    if not category_name in _config_sections:
        tty.die("Unknown config category %s.  Valid options are: %s" %
                (category_name, ", ".join([s for s in _config_sections])))
    return os.path.join(get_config_scope_dirname(scope), _config_sections[category_name].filename)


def add_to_config(category_name, addition_dict, scope=None):
    """Merge a new dict into a configuration tree and write the new
       configuration to disk"""
    global _read_config_file_result
    get_config(category_name)
    category = _config_sections[category_name]

    #If scope is specified, use it.  Otherwise use the last config scope that
    #we successfully parsed data from.
    file = None
    path = None
    if not scope and not category.files_read_from:
        scope = 'user'
    if scope:
        try:
            dir = get_config_scope_dirname(scope)
            if not os.path.exists(dir):
                mkdirp(dir)
            path = os.path.join(dir, category.filename)
            file = open(path, 'w')
        except exceptions.IOError, e:
            pass
    else:
        for p in category.files_read_from:
            try:
                file = open(p, 'w')
            except exceptions.IOError, e:
                pass
            if file:
                path = p
                break;
    if not file:
        tty.die('Unable to write to config file %s' % path)

    #Merge the new information into the existing file info, then write to disk
    new_dict = _read_config_file_result[path]
    if new_dict and category_name in new_dict:
        new_dict = new_dict[category_name]
    new_dict = _merge_dicts(new_dict, addition_dict)
    new_dict = { category_name : new_dict }
    _read_config_file_result[path] = new_dict
    yaml.dump(new_dict, stream=file, default_flow_style=False)
    file.close()

    #Merge the new information into the cached results
    category.result_dict = _merge_dicts(category.result_dict, addition_dict)


def add_to_mirror_config(addition_dict, scope=None):
    """Add mirrors to the configuration files"""
    add_to_config('mirrors', addition_dict, scope)


def add_to_compiler_config(addition_dict, scope=None, arch=None):
    """Add compilerss to the configuration files"""
    if not arch:
        arch = spack.architecture.sys_type()
    add_to_config('compilers', { arch : addition_dict }, scope)
    clear_config_caches()


def remove_from_config(category_name, key_to_rm, scope=None):
    """Remove a configuration key and write a new configuration to disk"""
    global config_scopes
    get_config(category_name)
    scopes_to_rm_from = [scope] if scope else [s for s,p in config_scopes]
    category = _config_sections[category_name]

    rmd_something = False
    for s in scopes_to_rm_from:
        path = get_config_scope_filename(scope, category_name)
        result = _read_config_file(path)
        if not result:
            continue
        if not key_to_rm in result[category_name]:
            continue
        with open(path, 'w') as f:
            result[category_name].pop(key_to_rm, None)
            yaml.dump(result, stream=f, default_flow_style=False)
            category.result_dict.pop(key_to_rm, None)
            rmd_something = True
    return rmd_something


"""Print a configuration to stdout"""
def print_category(category_name):
    if not category_name in _config_sections:
        tty.die("Unknown config category %s.  Valid options are: %s" %
                (category_name, ", ".join([s for s in _config_sections])))
    yaml.dump(get_config(category_name), stream=sys.stdout, default_flow_style=False)

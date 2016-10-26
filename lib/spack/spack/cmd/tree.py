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
import spack
from llnl.util.filesystem import join_path

import argparse

from collections import defaultdict
import itertools

description = "Project Spack's fully-qualified names to a tree of simplified symlinks"

def setup_parser(subparser):
    subparser.add_argument('--root', dest='root')
    subparser.add_argument(
        '--transitive', dest='transitive', action='store_true')
    subparser.add_argument('action')
    subparser.add_argument('target', nargs=argparse.REMAINDER)

class PackageConfig(object):
    def __init__(self, descriptor=None, compiler_descriptor=None,
            multiply=None):
        self.descriptor = descriptor
        self.compiler_descriptor = compiler_descriptor
        self.multiply = multiply or {}

    def project(self, spec):
        starter_path = spec.format(self.descriptor)
        elements = starter_path.split('/')
        path = Path(elements[:-1], elements[-1])
        for dep, action, dep_cfg in self.multiply:
            if dep in spec and not dep == spec.name:
                dep_path = dep_cfg.project(spec[dep])
                action(path, str(dep_path))

        if self.compiler_descriptor:
            path.prepend(spec.format(self.compiler_descriptor))
        return str(path)

class FallbackSection(object):
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary
    
    def __getitem__(self, key):
        if key in self.primary:
            return self.primary[key]
        elif key in self.secondary:
            return self.secondary[key]

class Path(object):
    def __init__(self, dir_elements, basename):
        self.dir_elements = dir_elements
        self.basename = basename

    def prepend(self, element):
        self.dir_elements.insert(0, element)

    def append(self, element):
        self.dir_elements.append(element)

    def append_basename(self, element):
        self.basename = '-'.join([self.basename, element])

    def __str__(self):
        elements = list(self.dir_elements)
        if self.basename:
            elements.append(self.basename)
        return join_path(*elements)

class PathAction(object):
    PREPEND = 'prepend'
    APPEND = 'append'
    BASENAME = 'basename'
    ACTIONS = set([PREPEND, APPEND, BASENAME])

    def __init__(self, action):
        if action not in PathAction.ACTIONS:
            raise ValueError(
                "Action must be one of {{{0}}}, check configuration".format(
                    ', '.join(PathActions.ACTIONS)))
        self.action = action

    def __call__(self, path, element):
        if self.action == PathAction.PREPEND:
            path.prepend(element)
        elif self.action == PathAction.APPEND:
            path.append(element)
        else:
            path.append_basename(element)

    @staticmethod
    def reorder(items, actionFn):
        appends = list()
        prepends = list()
        for item in items:
            path_action = actionFn(item).action
            if path_action == PathAction.PREPEND:
                prepends.append(item)
            else:
                appends.append(item)
        return list(reversed(prepends)) + appends

def get_package_config(name, config, exclude_multiply=None,
        force_path_action=None):
    """
    Notes:
    
    - siblings may reuse multipliers, but children never reuse multipliers
      which were used by their parents
    - (implied) parent multiplier actions override child multiplier actions
    - always append to basename for multipliers of multipliers
    - elements appear in the order listed: if a prepend action for Y follows
      a prepend action for X, the result will appear as X/Y
    """
    section = FallbackSection(config.get(name, {}), config.get('all'))    

    multipliers = list()
    exclude_multiply = set(exclude_multiply) if exclude_multiply else set()
    for item in section['multiply']:
        t = item.strip().split(':')
        if len(t) == 3:
            action, pkg, cfg_id = t
        else:
            action, pkg = t
            cfg_id = pkg
        
        action = force_path_action or action

        if pkg not in exclude_multiply:
            multipliers.append((action, pkg, cfg_id))
            exclude_multiply.add(pkg)

    multiply = list()
    for action, pkg, cfg_id in multipliers:
        pkg_cfg = get_package_config(cfg_id, config, exclude_multiply,
            force_path_action=PathAction.BASENAME)
        multiply.append((pkg, PathAction(action), pkg_cfg))
    
    multiply = PathAction.reorder(multiply, lambda t: t[1])
    
    return PackageConfig(section['descriptor'], section['compiler_descriptor'],
        multiply)

def project_all(specs, config):
    def keyFn(spec):
        pkg_cfg = get_package_config(spec.name, config)
        return pkg_cfg.project(spec)
        
    link_to_specs = map_specs(specs, keyFn)
    
    return dict(
        (x, resolve_conflict(y)) for x, y in link_to_specs.iteritems())

def map_specs(specs, keyFn):
    key_to_specs = defaultdict(set)
    for spec in specs:
        key = keyFn(spec)
        key_to_specs[key].add(spec)
    return key_to_specs

def resolve_conflict(specs):
    #TODO: optionally omit build dependencies when ordering packages
    return max(specs)

def update_install(specs, config):
    projection = config.projection

    touched = set()
    for spec in specs:
        touched.update(x.name for x in spec.traverse())
    
    # All specs associated with all packages affected, along with the specs
    # associated with their dependencies
    related_specs = set(itertools.chain.from_iterable(
        spack.installed_db.query(name) for name in touched))

    link_to_spec = projection.project_all(related_specs)
    
    config.update_links(link_to_spec)
    
    #TODO: what to do if the installed specs arent the chosen specs?

def update_uninstall(specs, config):
    projection = config.projection
    link_to_spec = projection.project_all(specs)
    config.remove_links(set(link_to_spec))

    # If all instances of a package are uninstalled, there may be no entries
    # for it here.
    related_specs = set(itertools.chain.from_iterable(
        spack.installed_db.query(s.name) for s in specs))
    link_to_spec = projection.project_all(related_specs)
    config.add_links(link_to_spec)

def get_or_set(d, key, val):
    if key in d:
        return d[key]
    else:
        d[key] = val
        return val

def tree(parser, args):
    root = args.root
    action = args.action

    tree_config = spack.config.get_config('trees')
    projections_config = spack.config.get_config('projections')

    if action == 'add':
        tree_id, query_spec = args.target
            
        tree = get_or_set(projections_config, tree_id, {})
        update = get_or_set(
            tree, 'transitive' if args.transitive else 'single', [])
        update.append(query_spec)
        spack.config.update_config('projections', projections_config, 'user')
    elif action == 'project':
        tree_id, = args.target

        if tree_id == 'all':
            specs_to_project = spack.install_layout.all_specs()
        else:
            specs_to_project = list()
            tree = projections_config[tree_id]
            single = tree['single']
            transitive = tree['transitive']
            for query_spec in single:
                specs_to_project.extend(
                    spack.installed_db.query(query_spec))
            for query_spec in transitive:
                specs_to_project.extend(
                    itertools.chain.from_iterable(spec.traverse() for spec in
                        spack.installed_db.query(query_spec)))

        for link_path, spec in project_all(
                specs_to_project, tree_config).iteritems():
            print join_path(root, link_path), spec.prefix
    else:
        raise ValueError("Unknown action: " + action)


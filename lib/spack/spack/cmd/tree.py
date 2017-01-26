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
from spack.projections import *
from llnl.util.filesystem import join_path, mkdirp

import argparse

import os
import errno

description = "Project package prefixes"


def setup_parser(subparser):
    subparser.add_argument('--relative-root', dest='relative_root')
    subparser.add_argument(
        '--show-only', dest="show_only", action="store_true")
    subparser.add_argument(
        '--transitive', dest='transitive', action='store_true')
    subparser.add_argument('action')
    subparser.add_argument('--root', dest='root')
    subparser.add_argument('--projection', dest='projection')
    subparser.add_argument('target', nargs=argparse.REMAINDER)


def create_softlinks(link_to_target, root):
    link_path_to_target = dict(
        (join_path(root, link.lstrip('/')).rstrip('/'), target)
        for link, target in link_to_target.iteritems())

    for link_path, target in link_path_to_target.iteritems():
        try:
            mkdirp(os.path.dirname(link_path))
            os.symlink(target, link_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            else:
                print "Collision: ", link
                raise


def print_links(link_to_target, root):
    for link, target in link_to_target.iteritems():
        print join_path(root, link), '--->', target


def update_install(installed_specs, tree, config=None):
    config = config or UpdateConfig()
    # TODO: must get all specs here because an installed spec may be a
    # dependency of a transitive spec in the tree
    tree_specs = set(config.relevant_specs(tree))
    specs_for_update = tree_specs & installed_specs

    root = tree['root']
    projection_id = tree['projection']
    projections_config = spack.config.get_config(
        'projections')[projection_id]

    link_to_spec = project_packages(
        specs_for_update, projections_config, resolve_conflict)
    update = dict()
    rm_links = list()
    for link, spec in link_to_spec.iteritems():
        link_path = join_path(root, link)
        prev_spec = config.spec_from_prefix(link_path)
        if prev_spec:
            if spec == prev_spec:
                continue
            # TODO? highlight details which differ between the two specs
            chosen = resolve_conflict([spec, prev_spec])
            if chosen == spec:
                update[link] = spec.prefix
                rm_links.append(link_path)
                print (
                    "The following spec will be replaced for {0}:".format(
                        link_path) +
                    "\n{0}".format(str(prev_spec)))
            else:
                print (
                    "Existing spec for {0}".format(link_path) +
                    " is preferred over newly-installed spec {0}".format(
                        str(spec)))
        else:
            update[link] = spec.prefix

    for link_path in rm_links:
        config.delete(link_path)

    check_for_prefix_collisions(set(update), root)
    config.link_action(update, root)

    link_to_target = project_targets(
        specs_for_update, projections_config, resolve_target_conflict)
    update = dict()
    rm_links = list()
    for link, (spec, target) in link_to_target.iteritems():
        prev_spec = config.spec_from_target(link, target)
        if prev_spec:
            if prev_spec == spec:
                continue
            chosen = resolve_conflict([spec, prev_spec])
            if chosen == prev_spec:
                continue
            else:
                rm_links.append(link)
        target_path = join_path(spec.prefix, target)
        update[link] = target_path

    for link_path in rm_links:
        # TODO: make sure rm_links has link paths vs. relative paths
        config.delete(link_path)

    check_for_target_collisions(set(update))
    config.link_action(update, relative_root)


def read_spec_from_prefix(path):
    # Here path is expected to be a package prefix
    spec_yaml_path = join_path(path, '.spack', 'spec.yaml')
    return spack.store.layout.read_spec(spec_yaml_path)


def read_spec_from_target(link, target):
    relative_depth = len(x for x in target.split(os.sep) if x) - 1
    real_target_path = os.path.realpath(link)
    target_dir = os.path.dirname(real_target_path)
    prefix_path = join_path(target_dir, *([os.pardir] * relative_depth))
    return read_spec_from_prefix(prefix_path)


class UpdateConfig(object):
    def __init__(
            self, relevant_specs=None, link_action=None, delete=None,
            spec_from_prefix=None, spec_from_target=None):
        self.relevant_specs = relevant_specs or get_relevant_specs
        self.link_action = link_action or create_softlinks
        self.delete = delete or os.remove
        self.spec_from_prefix = spec_from_prefix or read_spec_from_prefix
        self.spec_from_target = spec_from_target or read_spec_from_target


def update_uninstall(uninstalled_specs, tree, config=None):
    config = config or UpdateConfig()
    affected_pkgs = set(x.name for x in uninstalled_specs)
    # TODO: must get all specs here because an installed spec may be a
    # dependency of a transitive spec in the tree
    tree_specs = set(config.relevant_specs(tree))
    touched_specs = set(x for x in tree_specs if x.name in affected_pkgs)

    root = tree['root']
    projection_id = tree['projection']
    projections_config = spack.config.get_config(
        'projections')[projection_id]

    link_to_spec = project_packages(
        touched_specs, projections_config, resolve_conflict)

    # TODO: should only project specs that are relevant to the tree
    uninstalled_links = project_packages(
        uninstalled_specs, projections_config, resolve_conflict)
    uninstalled_prefixes = set(x.prefix for x in uninstalled_specs)

    # Check realpath of each link, if the link points to the prefix of an
    # uninstalled spec, then update the link
    update = dict()
    for link, spec in link_to_spec.iteritems():
        link_path = join_path(root, link)
        if (os.path.exists(link_path) and
                os.path.realpath(link_path) in uninstalled_prefixes):
            update[link] = spec

    # In case the uninstalled links were not touched: you have to project them
    # as well and delete. You should only delete if the link refers to the
    # prefix of an uninstalled spec
    rm_links = list()
    for link, spec in uninstalled_links.iteritems():
        link_path = join_path(root, link)
        if link not in update and os.path.exists(link):
            rm_links.append(link)

    for link_path in rm_links:
        # TODO: make sure rm_links has link paths vs. relative paths
        config.delete(link_path)
    config.link_action(update, relative_root)


def resolve_conflict(specs):
    return max(specs)


def resolve_target_conflict(spec_target_pairs):
    return max(spec_target_pairs, key=lambda (spec, target): spec)


def get_or_set(d, key, val):
    if key in d:
        return d[key]
    else:
        d[key] = val
        return val


def softlink_command(target_path, link_path):
    return "ln -s {0} {1}".format(target_path, link_path)


def tree(parser, args):
    relative_root = args.relative_root or '/'
    action = args.action
    link_action = print_links if args.show_only else create_softlinks

    tree_config = spack.config.get_config('trees')

    if action == 'add':
        tree_id, query_spec = args.target

        tree = get_or_set(tree_config, tree_id, {})
        update = get_or_set(
            tree, 'transitive' if args.transitive else 'single', [])
        update.append(query_spec)
        spack.config.update_config('trees', tree_config, 'user')
    elif action in ['create', 'set']:
        tree_id, = args.target
        tree = get_or_set(tree_config, tree_id, {})
        if args.root:
            tree['root'] = args.root
        if args.projection:
            tree['projection'] = args.projection
        spack.config.update_config('trees', tree_config, 'user')
    elif action == 'project':
        tree_id, = args.target

        if tree_id == 'all':
            root = args.root
            projection_id = args.projection
            specs_to_project = spack.store.layout.all_specs()
        else:
            tree = tree_config[tree_id]
            root = args.root or tree['root']
            projection_id = args.projection or tree['projection']

            specs_to_project = get_relevant_specs(tree)

        projections_config = spack.config.get_config(
            'projections')[projection_id]

        link_to_spec = project_packages(
            specs_to_project, projections_config, resolve_conflict)
        link_to_prefix = dict(
            (link, spec.prefix) for link, spec in link_to_spec.iteritems())
        pkg_root = join_path(relative_root, root.lstrip('/'))
        check_for_prefix_collisions(
            set(link_to_prefix), pkg_root, os.path.islink)
        link_action(link_to_prefix, pkg_root)

        link_to_target = project_targets(
            specs_to_project, projections_config, resolve_target_conflict)
        link_to_target_path = dict(
            (link, join_path(spec.prefix, target))
            for link, (spec, target) in link_to_target.iteritems())
        check_for_target_collisions(set(link_to_target_path))
        link_action(link_to_target_path, relative_root)
    else:
        raise ValueError("Unknown action: " + action)

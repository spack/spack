###########################################################################
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
import llnl.util.tty as tty

from collections import defaultdict
import itertools
import os


class PackageProjection(object):
    def __init__(self, element_groups, dep=None):
        self.element_groups = element_groups
        self.dep = dep

    def project(self, spec):
        # TODO: keep track of the instantiations of virtual deps to avoid
        # including them twice in the projection
        if self.dep:
            if self.dep == spec.name or self.dep not in spec:
                return
            spec = spec[self.dep]
        projected_groups = list()
        for element_group in self.element_groups:
            projected = list(x.project(spec) for x in element_group)
            projected = list(x for x in projected if x)
            if projected:
                projected_groups.append(projected)

        if projected_groups:
            return join_path(*('-'.join(x) for x in projected_groups))


def get_package_projection(name, config, exclude_multiply=None,
                           force_basename=False, dep=None):
    """
    Notes:

    - siblings may reuse multipliers, but children never reuse multipliers
      which were used by their parents
    - (implied) parent multiplier actions override child multiplier actions
    - always append to basename for multipliers of multipliers
    """
    primary_section = config.get(name, {})
    all_section = config.get('all', {})
    if primary_section.get('descriptor', None):
        return PackageProjection(
            [[PackageDetailProjection(primary_section['descriptor'])]],
            dep)
    elif primary_section.get('components', None):
        components = primary_section['components']
    elif all_section.get('descriptor', None):
        return PackageProjection(
            [[PackageDetailProjection(all_section['descriptor'])]],
            dep)
    elif all_section.get('components', None):
        components = all_section['components']

    components = list(components)
    components.extend(primary_section.get('extra-components', []))

    element_groups = list()
    element_group = list()
    exclude_multiply = set(exclude_multiply) if exclude_multiply else set()

    base = (
        primary_section.get('top-level-basedir', None) or
        all_section.get('top-level-basedir', None))
    if base and not dep:
        element_groups.append([PackageDetailProjection(base)])

    parent_exclude = set(exclude_multiply)
    for item in components:
        t = item.strip().split(':')
        if t[0] == 'dep':
            parent_exclude.add(t[1])
        elif t[0] == 'once':
            parent_exclude.add(t[1])

    for item in components:
        t = item.strip().split(':')
        if t[0] == '/':
            if force_basename:
                continue
            element_groups.append(element_group)
            element_group = list()
        else:
            if t[0] == 'dep':
                pkg = t[1]
                if pkg in exclude_multiply:
                    continue
                cfg_id = pkg if len(t) < 3 else t[2]
                element = get_package_projection(
                    cfg_id, config, parent_exclude,
                    force_basename=True, dep=pkg)
            elif t[0] == 'once':
                cfg_id = t[1]
                if cfg_id in exclude_multiply:
                    continue
                element = process_this(t[2:])
            elif t[0] in ['this', 'this?']:
                element = process_this(t)
            element_group.append(element)

    if element_group:
        element_groups.append(element_group)
    return PackageProjection(element_groups, dep=dep)


class PackageDetailProjection(object):
    def __init__(self, true_fmt, query_spec=None, false_fmt=None):
        self.query_spec = query_spec
        self.true_fmt = true_fmt
        self.false_fmt = false_fmt

    def project(self, spec):
        if not self.query_spec or spec.satisfies(self.query_spec):
            return spec.format(self.true_fmt)
        elif self.false_fmt:
            return spec.format(self.false_fmt)


def process_this(t):
    if t[0] == 'this':
        _, true_fmt = t
        query_spec, false_fmt = None, None
    elif t[0] == 'this?':
        _, query_spec, true_fmt = t[:3]
        false_fmt = t[3] if len(t) > 3 else None
    return PackageDetailProjection(true_fmt, query_spec, false_fmt)


def get_target_projections(pkg, config):
    targets = config.get(pkg, {}).get('targets', [])
    return list(
        TargetProjection(t['match'], t['target'], t['output'])
        for t in targets)


class TargetProjection(object):
    def __init__(self, match, target, output):
        self.match = match
        self.target = target
        self.output = output

    def matches(self, spec):
        return spec.satisfies(self.match)

    def project(self, spec):
        target_path = join_path(spec.prefix, self.target)
        if not os.path.exists(target_path):
            raise ValueError(
                "{0} does not exist in {1}".format(self.target, spec.prefix))
        return spec.format(self.output)


def get_relevant_specs(tree):
    relevant_specs = list()
    single = tree['single']
    transitive = tree['transitive']
    for query_spec in single:
        relevant_specs.extend(
            spack.store.db.query(query_spec))
    for query_spec in transitive:
        relevant_specs.extend(
            itertools.chain.from_iterable(
                spec.traverse() for spec in
                spack.store.db.query(query_spec)))
    return relevant_specs


def project_packages(specs, config, resolve_conflict):
    def keyFn(spec):
        pkg_cfg = get_package_projection(spec.name, config)
        return pkg_cfg.project(spec)

    path_to_specs = map_specs(specs, keyFn)

    path_to_spec = dict()
    for path, specs in path_to_specs.iteritems():
        if len(specs) > 1:
            tty.warn(
                "{0} has {1} conflicting specs".format(path, str(len(specs))))
        path_to_spec[path] = resolve_conflict(specs)
    return path_to_spec


def check_for_prefix_collisions(relative_paths, root, prefix_used):
    """Ensure that the given paths (which are relative to root) are
    distinct from one another and from any existing paths.
    """
    # Check for conflicts between planned prefixes
    for path1, path2 in itertools.combinations(relative_paths, 2):
        if path1.startswith(path2) or path2.startswith(path1):
            smaller, larger = sorted([path1, path2], key=lambda x: len(x))
            raise ValueError(
                "Prefix collision:\n\t{0}\n\t{1}".format(smaller, larger))

    # Check for conflicts between planned and existing prefixes
    for path in relative_paths:
        prefix = path
        while prefix:
            full_prefix = join_path(root, prefix.lstrip('/'))
            if os.path.exists(full_prefix) and prefix_used(full_prefix):
                raise ValueError(
                    "Path {0} collides with existing prefix".format(path))
            prefix = os.path.dirname(prefix)


def check_for_target_collisions(paths):
    # Targets can share prefixes; the only constraint is that they are unique
    seen = set()
    for path in paths:
        if path in seen:
            raise ValueError("Target collision: {0}".format(path))
        elif os.path.exists(path):
            raise ValueError("Path already exists: {0}".format(link))
        seen.add(path)


def project_targets(specs, config, resolve_target_conflict):
    output_to_targets = defaultdict(set)
    for spec in specs:
        target_projections = get_target_projections(spec.name, config)
        for tp in target_projections:
            if tp.matches(spec):
                output = tp.project(spec)
                output_to_targets[output].add((spec, tp))
    output_to_target = {}
    for output, spec_keys in output_to_targets.iteritems():
        spec, tp = resolve_target_conflict(spec_keys)
        output_to_target[output] = (spec, tp.target)
    return output_to_target


def map_specs(specs, keyFn):
    key_to_specs = defaultdict(set)
    for spec in specs:
        key = keyFn(spec)
        key_to_specs[key].add(spec)
    return key_to_specs

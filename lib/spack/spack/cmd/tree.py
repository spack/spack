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

from collections import defaultdict
import itertools

description = "Project Spack's fully-qualified names to a tree of simplified symlinks"

def setup_parser(subparser):
    subparser.add_argument(
        '--default-projection', dest='default_projection')
    subparser.add_argument(
        'root')

class PackageConfig(object):
    def __init__(self, descriptor=None, compiler_descriptor=None,
            multiply=None):
        self.descriptor = descriptor
        self.compiler_descriptor = compiler_descriptor
        self.multiply = multiply or {}

    def project(self, spec):
        elements = list()
        elements.append(spec.format(self.descriptor))
        if self.compiler_descriptor:
            elements.append(spec.format(self.compiler_descriptor))
        elements.extend(spec[dep].format(descriptor)
            for dep, descriptor in self.multiply.iteritems()
            if dep in spec and not dep == spec.name)
        return join_path(*elements)

class FallbackSection(object):
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary
    
    def __getitem__(self, key):
        if key in self.primary:
            return self.primary[key]
        elif key in self.secondary:
            return self.secondary[key]

def get_package_config(name, config):
    section = FallbackSection(config.get(name, {}), config.get('all'))
    return PackageConfig(section['descriptor'], section['compiler_descriptor'],
        section['multiply'])

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


def tree(parser, args):
    root = args.root

    all_specs = spack.install_layout.all_specs()

    config = spack.config.get_config('trees')

    for link_path, spec in project_all(all_specs, config).iteritems():
        print join_path(root, link_path), spec.prefix


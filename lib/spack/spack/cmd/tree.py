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

class UniversalProjection(object):
    def __init__(self, projection):
        self.projection = projection
    
    def _project(self, spec):
        return spec.format(self.projection)

    def project_all(self, specs):
        link_to_specs = map_specs(specs, self._project)
        
        return dict(
            (x, resolve_conflict(y)) for x, y in link_to_specs.iteritems())

def map_specs(specs, keyFn):
    key_to_specs = defaultdict(set)
    for spec in specs:
        key = keyFn(spec)
        key_to_specs[key].add(spec)
    return key_to_specs

def resolve_conflict(specs):
    return max(specs, 
               key=lambda s: (s.compiler, s.version,
                              get_versions(s), s.dag_hash()))
    
def get_versions(spec):
    return tuple(x.version for x in spec.dependencies(deptype=('link', 'run')))

#To be called after install or uninstall
def update_install(specs, projection):
    touched = set()
    for spec in specs:
        touched.update(x.name for x in spec.traverse())
    
    # All specs associated with all packages affected, along with the specs
    # associated with dependency packages
    related_specs = set(itertools.chain.from_iterable(
        spack.installed_db.query(name) for name in touched))

    link_to_spec = projection.project_all(related_specs)
    
    #TODO: delete the existing links
    #TODO: add in the new links
    #TODO: what to do if the installed specs arent the chosen specs?
    
    return link_to_spec

def update_uninstall(specs, projection):
    link_to_spec = projection.project_all(specs)

    #TODO: remove existing links

    # If all instances of a package are uninstalled, there may be no entries
    # for it here.
    related_specs = set(itertools.chain.from_iterable(
        spack.installed_db.query(s.name) for s in specs))
    
    link_to_spec = projection.project_all(related_specs)
    
    return link_to_spec

#TODO: allow removing all links associated with a given package
#TODO: store spec to link so that if link scheme changes you can still remove
#    (then again you should totally regenerate if scheme changes)
#TODO: projection which optionally includes details if they apply (e.g. mention
#    the MPI implementation if there is a dependency on MPI)
#TODO: if a projection automatically adds details to disambiguate specs, then
#    the installation of a new spec could lead to several symlinks being updated
#TODO: when a user installs a package allow adding symlinks, when they uninstall
#    allow removing symlinks (and potentially replacing with a conflicting spec)

def tree(parser, args):
    root = args.root

    all_specs = spack.install_layout.all_specs()
    projection = UniversalProjection(args.default_projection)
    
    link_to_chosen = projection.project_all(all_specs)
    
    for link, spec in link_to_chosen.iteritems():
        link_path = join_path(root, link)
        print link_path, spec.prefix

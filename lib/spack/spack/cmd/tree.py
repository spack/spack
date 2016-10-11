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
    def __init__(self, formatStr):
        self.formatStr = formatStr
    
    def _project(self, spec):
        return spec.format(self.formatStr)

    def project_all(self, specs):
        link_to_specs = map_specs(specs, self._project)
        
        return dict(
            (x, resolve_conflict(y)) for x, y in link_to_specs.iteritems())

#TODO: there may be conflict resolution schemes which don't just need all instances
#    of a given package but rather all instances of their dependents as well (if
#    it is desirable to ensure that you link a dependency when you link its
#    parent).

#First do an initial sort. Then for each package, choose it if its dependent
#was chosen. Note that you could have X->Z and Y->Z', then which one do you pick?

class AutoProjection(object):
    def __init__(self, format_str, spec_to_format):
        self.base_format = format_str
        self.spec_to_format = spec_to_format
        
    def _project(self, spec):
        elements = [spec.format(self.base_format)]
        for extra_spec, format_str in self.spec_to_format.iteritems():
            if extra_spec in spec:
                elements.append(spec[extra_spec].format(format_str))
        #TODO: actually I think this needs to be reversed, because the path
        #    without augmentations may refer to an existing prefix, so I can't
        #    later append more things to it.
        return join_path(elements)

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

#TODO: should there be any attempt to pick the dependencies of a package when
#    you pick the package? e.g. if X->Y and there is also Y', should I always
#    choose Y?

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

#TODO: store spec to link so that if link scheme changes you can still remove
#    (then again you should totally regenerate if scheme changes)
#TODO: projection which optionally includes details if they apply (e.g. mention
#    the MPI implementation if there is a dependency on MPI)
#TODO: if a projection automatically adds details to disambiguate specs, then
#    the installation of a new spec could lead to several symlinks being updated

def tree(parser, args):
    root = args.root

    all_specs = spack.install_layout.all_specs()
    projection = UniversalProjection(args.default_projection)
    
    link_to_chosen = projection.project_all(all_specs)
    
    for link, spec in link_to_chosen.iteritems():
        link_path = join_path(root, link)
        print link_path, spec.prefix

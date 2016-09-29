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

description = "Project Spack's fully-qualified names to a tree of simplified symlinks"

def setup_parser(subparser):
    subparser.add_argument(
        '--default-projection', dest='default_projection')
    subparser.add_argument(
        'root')

class ProjectionSelector(object):
    def projection_for(self, spec):
        raise NotImplementedError(self.__class__.__name__ + " does not implement select")

class UniversalProjection(object):
    def __init__(self, projection):
        self.projection = projection
    
    def projection_for(self, spec):
        return self.projection

def user_projection(all_specs, selector):
    link_to_specs = defaultdict(set)
    for spec in all_specs:
        projection = selector.projection_for(spec)
        link_name = spec.format(projection)
        link_to_specs[link_name].add(spec)
    
    link_to_chosen = {}
    for link, specs in link_to_specs.iteritems():
        chosen = max(specs, key=lambda s: (s.compiler, s.version))
        link_to_chosen[link] = chosen

    return link_to_chosen

def tree(parser, args):
    root = args.root

    all_specs = spack.install_layout.all_specs()
    selector = UniversalProjection(args.default_projection)
    
    link_to_chosen = user_projection(all_specs, selector)
    
    for link, spec in link_to_chosen.iteritems():
        link_path = join_path(root, link)
        print link_path, spec.prefix

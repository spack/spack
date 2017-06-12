##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import argparse

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack
import spack.store
import spack.cmd

description = "show installed packages that depend on another"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        '-a', '--all', action='store_true', default=False,
        help="List all potential dependents of the package instead of actual "
        "dependents of an installed spec")
    subparser.add_argument(
        'spec', nargs=argparse.REMAINDER,
        help="specs to list dependencies of")


def inverted_dag():
    """Returns inverted package DAG as adjacency lists."""
    dag = {}
    for pkg in spack.repo.all_packages():
        dag.setdefault(pkg.name, set())
        for dep in pkg.dependencies:
            deps = [dep]

            # expand virtuals if necessary
            if spack.repo.is_virtual(dep):
                deps = [s.name for s in spack.repo.providers_for(dep)]

            for d in deps:
                dag.setdefault(d, set()).add(pkg.name)
    return dag


def all_dependents(name, inverted_dag, dependents=None):
    if dependents is None:
        dependents = set()

    if name in dependents:
        return set()
    dependents.add(name)

    direct = inverted_dag[name]
    for dname in direct:
        all_dependents(dname, inverted_dag, dependents)
    dependents.update(direct)
    return dependents


def dependents(parser, args):
    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) != 1:
        tty.die("spack dependents takes only one spec.")

    if args.all:
        spec = specs[0]
        idag = inverted_dag()

        dependents = all_dependents(spec.name, idag)
        dependents.remove(spec.name)
        if dependents:
            colify(sorted(dependents))
        else:
            print("No dependents")

    else:
        spec = spack.cmd.disambiguate_spec(specs[0])

        tty.msg("Dependents of %s" % spec.cformat('$_$@$%@$/'))
        deps = spack.store.db.installed_dependents(spec)
        if deps:
            spack.cmd.display_specs(deps)
        else:
            print("No dependents")

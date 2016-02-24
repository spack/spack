##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os
import argparse

import spack
import spack.cmd
import llnl.util.tty as tty

description = "Produce a single-rooted directory view of a spec."

def setup_parser(subparser):
    setup_parser.parser = subparser

    subparser.add_argument('prefix', nargs=1,
                           help="Path to top-level directory for the view.")
    subparser.add_argument('specs', nargs=argparse.REMAINDER,
                           help="specs of packages to expose in the view.")

def assuredir(path):
    'Assure path exists as a directory'
    if not os.path.exists(path):
        os.makedirs(path)
    
def relative_to(prefix, path):
    assert 0 == path.find(prefix)
    reldir = path[len(prefix):]
    if reldir.startswith('/'):
        reldir = reldir[1:]
    return reldir

def view_one(prefix, spec):
    print spec.name,spec.prefix

    dotspack = os.path.join(prefix, '.spack', spec.name)

    if os.path.exists(os.path.join(dotspack)):
        tty.warn("Skipping previously added package %s"%spec.name)
        return


    for dirpath,dirnames,filenames in os.walk(spec.prefix):
        if not filenames:
            continue        # avoid explicitly making empty dirs

        reldir = relative_to(spec.prefix, dirpath)

        # fixme: assumes .spack has no subdirs
        if dirpath.endswith('.spack'):
            targdir = dotspack
        else:
            targdir = os.path.join(prefix, reldir)

        assuredir(targdir)

        print '\t%s...'%reldir,
        nlinks = 0
        for fname in filenames:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(targdir, fname)
            if os.path.exists(dst):
                tty.warn("Skipping existing file for view: %s" % dst)
                continue
            os.symlink(src,dst)
            nlinks += 1
        print nlinks
    

def view(parser, args):
    # if not args.specs:
    #     tty.die("view creation requires at least one spec argument")

    specs = spack.cmd.parse_specs(args.specs, normalize=True, concretize=True)
    if not specs:
        setup_parser.parser.print_help()
        return 1

    prefix = args.prefix[0]
    assuredir(prefix)

    flat = set()
    for spec in specs:
        flat.update(spec.normalized().traverse())

    for spec in flat:
        view_one(prefix, spec)

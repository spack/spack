'''
Produce a file-system "view" of a Spack DAG.

Concept from Nix, implemented by brett.viren@gmail.com ca 2016.
'''
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
import re
import argparse

import spack
import spack.cmd
import llnl.util.tty as tty

description = "Produce a single-rooted directory view of a spec."

def setup_parser(subparser):
    setup_parser.parser = subparser

    sp = subparser.add_subparsers(metavar='ACTION', dest='action')

    # The action parameterizes the command but in keeping with Spack
    # patterns we make it a subcommand.
    sps = [
        sp.add_parser('link', aliases=['add'],
                      help='Add packages to the view, create view if needed.'),
        sp.add_parser('remove', aliases=['rm'],
                      help='Remove packages from the view, and view if empty.'),
        sp.add_parser('status', aliases=['check'],
                      help='Check status of packages in the view.')
    ]

    # All these options and arguments are common to every action.
    for p in sps:
        p.add_argument('-e','--exclude', action='append', default=[],
                       help="exclude any packages which the given re pattern")
        p.add_argument('--no-dependencies', action='store_true', default=False,
                       help="just operate on named packages and do not follow dependencies")
        p.add_argument('prefix', nargs=1,
                       help="Path to a top-level directory to receive the view.")
        p.add_argument('specs', nargs=argparse.REMAINDER,
                       help="specs of packages to expose in the view.")
        

def assuredir(path):
    'Assure path exists as a directory'
    if not os.path.exists(path):
        os.makedirs(path)
    
def relative_to(prefix, path):
    'Return end of `path` relative to `prefix`'
    assert 0 == path.find(prefix)
    reldir = path[len(prefix):]
    if reldir.startswith('/'):
        reldir = reldir[1:]
    return reldir

    
def transform_path(spec, path, prefix=None):
    'Return the a relative path corresponding to given path spec.prefix'
    if os.path.isabs(path):
        path = relative_to(spec.prefix, path)
    subdirs = path.split(os.path.sep)
    if subdirs[0] == '.spack':
        lst = ['.spack',spec.name]+subdirs[1:]
        path = os.path.join(*lst)
    if prefix:
        path = os.path.join(prefix, path)
    return path

def action_status(spec, prefix):
    'Check status of view in prefix against spec'
    dotspack = os.path.join(prefix, '.spack', spec.name)
    if os.path.exists(os.path.join(dotspack)):
        tty.info("Package added: %s"%spec.name)
        return
    tty.info("Package missing: %s"%spec.name)
    return

def action_remove(spec, prefix):
    'Remove any files found in spec from prefix and purge empty directories.'

    if not os.path.exists(prefix):
        return

    dotspack = transform_path(spec, '.spack', prefix)
    if not os.path.exists(dotspack):
        tty.info("Skipping nonexistent package %s"%spec.name)
        return

    for dirpath,dirnames,filenames in os.walk(spec.prefix):
        if not filenames:
            continue

        targdir = transform_path(spec, dirpath, prefix)
        for fname in filenames:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(targdir, fname)
            if not os.path.exists(dst):
                #tty.warn("Skipping nonexistent file for view: %s" % dst)
                continue
            os.unlink(dst)


def action_link(spec, prefix):
    'Symlink all files in `spec` into directory `prefix`.'

    dotspack = transform_path(spec, '.spack', prefix)
    if os.path.exists(dotspack):
        tty.warn("Skipping previously added package %s"%spec.name)
        return

    for dirpath,dirnames,filenames in os.walk(spec.prefix):
        if not filenames:
            continue        # avoid explicitly making empty dirs

        targdir = transform_path(spec, dirpath, prefix)
        assuredir(targdir)

        for fname in filenames:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(targdir, fname)
            if os.path.exists(dst):
                if '.spack' in dst.split(os.path.sep):
                    continue    # silence these
                tty.warn("Skipping existing file for view: %s" % dst)
                continue
            os.symlink(src,dst)



def purge_empty_directories(path):
    'Ascend up from the leaves accessible from `path` and remove empty directories.'
    for dirpath, subdirs, files in os.walk(path, topdown=False):
        for sd in subdirs:
            sdp = os.path.join(dirpath,sd)
            try:
                os.rmdir(sdp)
            except OSError:
                tty.warn("Not removing directory with contents: %s" % sdp)




def view_action(action, parser, args):
    'The view command.'
    to_exclude = [re.compile(e) for e in args.exclude]
    def exclude(spec):
        for e in to_exclude:
            if e.match(spec.name):
                return True
        return False

    specs = spack.cmd.parse_specs(args.specs, normalize=True, concretize=True)
    if not specs:
        parser.print_help()
        return 1

    prefix = args.prefix
    assuredir(prefix)

    flat = set()
    for spec in specs:
        if args.no_dependencies:
            flat.add(spec)
            continue
        flat.update(spec.normalized().traverse())

    for spec in flat:
        if exclude(spec):
            tty.info('Skipping excluded package: "%s"' % spec.name)
            continue
        if not os.path.exists(spec.prefix):
            tty.warn('Skipping unknown package: %s in %s' % (spec.name, spec.prefix))
            continue
        tty.info("%s %s" % (action, spec.name))
        action(spec, prefix)

    if action in ['remove']:
        purge_empty_directories(prefix)


def view(parser, args):
    action = {
        'add': action_link,
        'link': action_link,
        'remove': action_remove,
        'rm': action_remove,
        'status': action_status,
        'check': action_status
        }[args.action]
    view_action(action, parser, args)

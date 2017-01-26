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
'''Produce a "view" of a Spack DAG.

A "view" is file hierarchy representing the union of a number of
Spack-installed package file hierarchies.  The union is formed from:

- specs resolved from the package names given by the user (the seeds)

- all depenencies of the seeds unless user specifies `--no-depenencies`

- less any specs with names matching the regular expressions given by
  `--exclude`

The `view` can be built and tore down via a number of methods (the "actions"):

- symlink :: a file system view which is a directory hierarchy that is
  the union of the hierarchies of the installed packages in the DAG
  where installed files are referenced via symlinks.

- hardlink :: like the symlink view but hardlinks are used.

- statlink :: a view producing a status report of a symlink or
  hardlink view.

The file system view concept is imspired by Nix, implemented by
brett.viren@gmail.com ca 2016.

'''
# Implementation notes:
#
# This is implemented as a visitor pattern on the set of package specs.
#
# The command line ACTION maps to a visitor_*() function which takes
# the set of package specs and any args which may be specific to the
# ACTION.
#
# To add a new view:
# 1. add a new cmd line args sub parser ACTION
# 2. add any action-specific options/arguments, most likely a list of specs.
# 3. add a visitor_MYACTION() function
# 4. add any visitor_MYALIAS assignments to match any command line aliases

import os
import re
import spack
import spack.cmd
import llnl.util.tty as tty

description = "produce a single-rooted directory view of a spec"


def setup_parser(sp):
    setup_parser.parser = sp

    sp.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help="display verbose output")
    sp.add_argument(
        '-e', '--exclude', action='append', default=[],
        help="exclude packages with names matching the given regex pattern")
    sp.add_argument(
        '-d', '--dependencies', choices=['true', 'false', 'yes', 'no'],
        default='true',
        help="follow dependencies")

    ssp = sp.add_subparsers(metavar='ACTION', dest='action')

    specs_opts = dict(metavar='spec', nargs='+',
                      help="seed specs of the packages to view")

    # The action parameterizes the command but in keeping with Spack
    # patterns we make it a subcommand.
    file_system_view_actions = [
        ssp.add_parser(
            'symlink', aliases=['add', 'soft'],
            help='add package files to a filesystem view via symbolic links'),
        ssp.add_parser(
            'hardlink', aliases=['hard'],
            help='add packages files to a filesystem via via hard links'),
        ssp.add_parser(
            'remove', aliases=['rm'],
            help='remove packages from a filesystem view'),
        ssp.add_parser(
            'statlink', aliases=['status', 'check'],
            help='check status of packages in a filesystem view')
    ]
    # All these options and arguments are common to every action.
    for act in file_system_view_actions:
        act.add_argument('path', nargs=1,
                         help="path to file system view directory")
        act.add_argument('specs', **specs_opts)

    return


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
        lst = ['.spack', spec.name] + subdirs[1:]
        path = os.path.join(*lst)
    if prefix:
        path = os.path.join(prefix, path)
    return path


def purge_empty_directories(path):
    '''Ascend up from the leaves accessible from `path`
    and remove empty directories.'''
    for dirpath, subdirs, files in os.walk(path, topdown=False):
        for sd in subdirs:
            sdp = os.path.join(dirpath, sd)
            try:
                os.rmdir(sdp)
            except OSError:
                pass


def filter_exclude(specs, exclude):
    'Filter specs given sequence of exclude regex'
    to_exclude = [re.compile(e) for e in exclude]

    def exclude(spec):
        for e in to_exclude:
            if e.match(spec.name):
                return True
        return False
    return [s for s in specs if not exclude(s)]


def flatten(seeds, descend=True):
    'Normalize and flattend seed specs and descend hiearchy'
    flat = set()
    for spec in seeds:
        if not descend:
            flat.add(spec)
            continue
        flat.update(spec.normalized().traverse())
    return flat


def check_one(spec, path, verbose=False):
    'Check status of view in path against spec'
    dotspack = os.path.join(path, '.spack', spec.name)
    if os.path.exists(os.path.join(dotspack)):
        tty.info('Package in view: "%s"' % spec.name)
        return
    tty.info('Package not in view: "%s"' % spec.name)
    return


def remove_one(spec, path, verbose=False):
    'Remove any files found in `spec` from `path` and purge empty directories.'

    if not os.path.exists(path):
        return                  # done, short circuit

    dotspack = transform_path(spec, '.spack', path)
    if not os.path.exists(dotspack):
        if verbose:
            tty.info('Skipping nonexistent package: "%s"' % spec.name)
        return

    if verbose:
        tty.info('Removing package: "%s"' % spec.name)
    for dirpath, dirnames, filenames in os.walk(spec.prefix):
        if not filenames:
            continue
        targdir = transform_path(spec, dirpath, path)
        for fname in filenames:
            dst = os.path.join(targdir, fname)
            if not os.path.exists(dst):
                continue
            os.unlink(dst)


def link_one(spec, path, link=os.symlink, verbose=False):
    'Link all files in `spec` into directory `path`.'

    dotspack = transform_path(spec, '.spack', path)
    if os.path.exists(dotspack):
        tty.warn('Skipping existing package: "%s"' % spec.name)
        return

    if verbose:
        tty.info('Linking package: "%s"' % spec.name)
    for dirpath, dirnames, filenames in os.walk(spec.prefix):
        if not filenames:
            continue        # avoid explicitly making empty dirs

        targdir = transform_path(spec, dirpath, path)
        assuredir(targdir)

        for fname in filenames:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(targdir, fname)
            if os.path.exists(dst):
                if '.spack' in dst.split(os.path.sep):
                    continue    # silence these
                tty.warn("Skipping existing file: %s" % dst)
                continue
            link(src, dst)


def visitor_symlink(specs, args):
    'Symlink all files found in specs'
    path = args.path[0]
    assuredir(path)
    for spec in specs:
        link_one(spec, path, verbose=args.verbose)


visitor_add = visitor_symlink
visitor_soft = visitor_symlink


def visitor_hardlink(specs, args):
    'Hardlink all files found in specs'
    path = args.path[0]
    assuredir(path)
    for spec in specs:
        link_one(spec, path, os.link, verbose=args.verbose)


visitor_hard = visitor_hardlink


def visitor_remove(specs, args):
    'Remove all files and directories found in specs from args.path'
    path = args.path[0]
    for spec in specs:
        remove_one(spec, path, verbose=args.verbose)
    purge_empty_directories(path)


visitor_rm = visitor_remove


def visitor_statlink(specs, args):
    'Give status of view in args.path relative to specs'
    path = args.path[0]
    for spec in specs:
        check_one(spec, path, verbose=args.verbose)


visitor_status = visitor_statlink
visitor_check = visitor_statlink


def view(parser, args):
    'Produce a view of a set of packages.'

    # Process common args
    seeds = [spack.cmd.disambiguate_spec(s) for s in args.specs]
    specs = flatten(seeds, args.dependencies.lower() in ['yes', 'true'])
    specs = filter_exclude(specs, args.exclude)

    # Execute the visitation.
    try:
        visitor = globals()['visitor_' + args.action]
    except KeyError:
        tty.error('Unknown action: "%s"' % args.action)
    visitor(specs, args)

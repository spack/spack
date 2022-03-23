# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import re
import sys

import llnl.util.tty as tty
from llnl.util.filesystem import working_dir
from llnl.util.tty.colify import colify

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.paths
import spack.repo
import spack.util.package_hash as ph
from spack.util.executable import which

description = "query packages associated with particular git revisions"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='pkg_command')

    add_parser = sp.add_parser('add', help=pkg_add.__doc__)
    arguments.add_common_arguments(add_parser, ['packages'])

    list_parser = sp.add_parser('list', help=pkg_list.__doc__)
    list_parser.add_argument('rev', default='HEAD', nargs='?',
                             help="revision to list packages for")

    diff_parser = sp.add_parser('diff', help=pkg_diff.__doc__)
    diff_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    diff_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")

    add_parser = sp.add_parser('added', help=pkg_added.__doc__)
    add_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    add_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")

    add_parser = sp.add_parser('changed', help=pkg_changed.__doc__)
    add_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    add_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")
    add_parser.add_argument(
        '-t', '--type', action='store', default='C',
        help="Types of changes to show (A: added, R: removed, "
        "C: changed); default is 'C'")

    rm_parser = sp.add_parser('removed', help=pkg_removed.__doc__)
    rm_parser.add_argument(
        'rev1', nargs='?', default='HEAD^',
        help="revision to compare against")
    rm_parser.add_argument(
        'rev2', nargs='?', default='HEAD',
        help="revision to compare to rev1 (default is HEAD)")

    source_parser = sp.add_parser('source', help=pkg_source.__doc__)
    source_parser.add_argument(
        '-c', '--canonical', action='store_true', default=False,
        help="dump canonical source as used by package hash.")
    arguments.add_common_arguments(source_parser, ['spec'])

    hash_parser = sp.add_parser('hash', help=pkg_hash.__doc__)
    arguments.add_common_arguments(hash_parser, ['spec'])


def packages_path():
    """Get the test repo if it is active, otherwise the builtin repo."""
    try:
        return spack.repo.path.get_repo('builtin.mock').packages_path
    except spack.repo.UnknownNamespaceError:
        return spack.repo.path.get_repo('builtin').packages_path


class GitExe:
    # Wrapper around Executable for git to set working directory for all
    # invocations.
    #
    # Not using -C as that is not supported for git < 1.8.5.
    def __init__(self):
        self._git_cmd = which('git', required=True)

    def __call__(self, *args, **kwargs):
        with working_dir(packages_path()):
            return self._git_cmd(*args, **kwargs)


_git = None


def get_git():
    """Get a git executable that runs *within* the packages path."""
    global _git
    if _git is None:
        _git = GitExe()
    return _git


def list_packages(rev):
    git = get_git()

    # git ls-tree does not support ... merge-base syntax, so do it manually
    if rev.endswith('...'):
        ref = rev.replace('...', '')
        rev = git('merge-base', ref, 'HEAD', output=str).strip()

    output = git('ls-tree', '--name-only', rev, output=str)
    return sorted(line for line in output.split('\n')
                  if line and not line.startswith('.'))


def pkg_add(args):
    """add a package to the git stage with `git add`"""
    git = get_git()

    for pkg_name in args.packages:
        filename = spack.repo.path.filename_for_package_name(pkg_name)
        if not os.path.isfile(filename):
            tty.die("No such package: %s.  Path does not exist:" %
                    pkg_name, filename)

        git('add', filename)


def pkg_list(args):
    """list packages associated with a particular spack git revision"""
    colify(list_packages(args.rev))


def diff_packages(rev1, rev2):
    p1 = set(list_packages(rev1))
    p2 = set(list_packages(rev2))
    return p1.difference(p2), p2.difference(p1)


def pkg_diff(args):
    """compare packages available in two different git revisions"""
    u1, u2 = diff_packages(args.rev1, args.rev2)

    if u1:
        print("%s:" % args.rev1)
        colify(sorted(u1), indent=4)
        if u1:
            print()

    if u2:
        print("%s:" % args.rev2)
        colify(sorted(u2), indent=4)


def pkg_removed(args):
    """show packages removed since a commit"""
    u1, u2 = diff_packages(args.rev1, args.rev2)
    if u1:
        colify(sorted(u1))


def pkg_added(args):
    """show packages added since a commit"""
    u1, u2 = diff_packages(args.rev1, args.rev2)
    if u2:
        colify(sorted(u2))


def get_all_package_diffs(type, rev1='HEAD^1', rev2='HEAD'):
    """Show packages changed, added, or removed (or any combination of those)
       since a commit.

    Arguments:

        type (str): String containing one or more of 'A', 'B', 'C'
        rev1 (str): Revision to compare against, default is 'HEAD^'
        rev2 (str): Revision to compare to rev1, default is 'HEAD'

    Returns:

        A set contain names of affected packages.
    """
    lower_type = type.lower()
    if not re.match('^[arc]*$', lower_type):
        tty.die("Invald change type: '%s'." % type,
                "Can contain only A (added), R (removed), or C (changed)")

    removed, added = diff_packages(rev1, rev2)

    git = get_git()
    out = git('diff', '--relative', '--name-only', rev1, rev2,
              output=str).strip()

    lines = [] if not out else re.split(r'\s+', out)
    changed = set()
    for path in lines:
        pkg_name, _, _ = path.partition(os.sep)
        if pkg_name not in added and pkg_name not in removed:
            changed.add(pkg_name)

    packages = set()
    if 'a' in lower_type:
        packages |= added
    if 'r' in lower_type:
        packages |= removed
    if 'c' in lower_type:
        packages |= changed

    return packages


def pkg_changed(args):
    """show packages changed since a commit"""
    packages = get_all_package_diffs(args.type, args.rev1, args.rev2)

    if packages:
        colify(sorted(packages))


def pkg_source(args):
    """dump source code for a package"""
    specs = spack.cmd.parse_specs(args.spec, concretize=False)
    if len(specs) != 1:
        tty.die("spack pkg source requires exactly one spec")

    spec = specs[0]
    filename = spack.repo.path.filename_for_package_name(spec.name)

    # regular source dump -- just get the package and print its contents
    if args.canonical:
        message = "Canonical source for %s:" % filename
        content = ph.canonical_source(spec)
    else:
        message = "Source for %s:" % filename
        with open(filename) as f:
            content = f.read()

    if sys.stdout.isatty():
        tty.msg(message)
    sys.stdout.write(content)


def pkg_hash(args):
    """dump canonical source code hash for a package spec"""
    specs = spack.cmd.parse_specs(args.spec, concretize=False)

    for spec in specs:
        print(ph.package_hash(spec))


def pkg(parser, args):
    if not spack.cmd.spack_is_git_repo():
        tty.die("This spack is not a git clone. Can't use 'spack pkg'")

    action = {
        'add': pkg_add,
        'diff': pkg_diff,
        'list': pkg_list,
        'removed': pkg_removed,
        'added': pkg_added,
        'changed': pkg_changed,
        'source': pkg_source,
        'hash': pkg_hash,
    }
    action[args.pkg_command](args)

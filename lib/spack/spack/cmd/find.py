# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import llnl.util.tty as tty
import llnl.util.tty.color as color
import llnl.util.lang

import spack.environment as ev
import spack.repo
import spack.cmd.common.arguments as arguments
from spack.cmd import display_specs
from spack.util.string import plural

description = "list and search installed packages"
section = "basic"
level = "short"


def setup_parser(subparser):
    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument('-s', '--short',
                              action='store_const',
                              dest='mode',
                              const='short',
                              default='short',
                              help='show only specs (default)')
    format_group.add_argument('-p', '--paths',
                              action='store_const',
                              dest='mode',
                              const='paths',
                              help='show paths to package install directories')
    format_group.add_argument(
        '-d', '--deps',
        action='store_const',
        dest='mode',
        const='deps',
        help='show full dependency DAG of installed packages')

    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'tags'])

    subparser.add_argument('-c', '--show-concretized',
                           action='store_true',
                           help='show concretized specs in an environment')
    subparser.add_argument('-f', '--show-flags',
                           action='store_true',
                           dest='show_flags',
                           help='show spec compiler flags')
    subparser.add_argument('--show-full-compiler',
                           action='store_true',
                           dest='show_full_compiler',
                           help='show full compiler specs')
    implicit_explicit = subparser.add_mutually_exclusive_group()
    implicit_explicit.add_argument(
        '-x', '--explicit',
        action='store_true',
        help='show only specs that were installed explicitly')
    implicit_explicit.add_argument(
        '-X', '--implicit',
        action='store_true',
        help='show only specs that were installed as dependencies')
    subparser.add_argument(
        '-u', '--unknown',
        action='store_true',
        dest='unknown',
        help='show only specs Spack does not have a package for')
    subparser.add_argument(
        '-m', '--missing',
        action='store_true',
        dest='missing',
        help='show missing dependencies as well as installed specs')
    subparser.add_argument(
        '-v', '--variants',
        action='store_true',
        dest='variants',
        help='show variants in output (can be long)')
    subparser.add_argument('-M', '--only-missing',
                           action='store_true',
                           dest='only_missing',
                           help='show only missing dependencies')
    subparser.add_argument('-N', '--namespace',
                           action='store_true',
                           help='show fully qualified package names')

    subparser.add_argument(
        '--start-date',
        help='earliest date of installation [YYYY-MM-DD]'
    )
    subparser.add_argument(
        '--end-date', help='latest date of installation [YYYY-MM-DD]'
    )

    arguments.add_common_arguments(subparser, ['constraint'])


def query_arguments(args):
    # Set up query arguments.
    installed, known = True, any
    if args.only_missing:
        installed = False
    elif args.missing:
        installed = any
    if args.unknown:
        known = False
    explicit = any
    if args.explicit:
        explicit = True
    if args.implicit:
        explicit = False
    q_args = {'installed': installed, 'known': known, "explicit": explicit}

    # Time window of installation
    for attribute in ('start_date', 'end_date'):
        date = getattr(args, attribute)
        if date:
            q_args[attribute] = llnl.util.lang.pretty_string_to_date(date)

    return q_args


def setup_env(env):
    """Create a function for decorating specs when in an environment."""

    def strip_build(seq):
        return set(s.copy(deps=('link', 'run')) for s in seq)

    added = set(strip_build(env.added_specs()))
    roots = set(strip_build(env.roots()))
    removed = set(strip_build(env.removed_specs()))

    def decorator(spec, fmt):
        # add +/-/* to show added/removed/root specs
        if any(spec.dag_hash() == r.dag_hash() for r in roots):
            return color.colorize('@*{%s}' % fmt)
        elif spec in removed:
            return color.colorize('@K{%s}' % fmt)
        else:
            return '%s' % fmt

    return decorator, added, roots, removed


def find(parser, args):
    q_args = query_arguments(args)
    results = args.specs(**q_args)

    decorator = lambda s, f: f
    added = set()
    removed = set()

    env = ev.get_env(args, 'find')
    if env:
        decorator, added, roots, removed = setup_env(env)

    # Exit early if no package matches the constraint
    if not results and args.constraint:
        msg = "No package matches the query: {0}"
        msg = msg.format(' '.join(args.constraint))
        tty.msg(msg)
        return

    # If tags have been specified on the command line, filter by tags
    if args.tags:
        packages_with_tags = spack.repo.path.packages_with_tags(*args.tags)
        results = [x for x in results if x.name in packages_with_tags]

    # Display the result
    if env:
        tty.msg('In environment %s' % env.name)

        if not env.user_specs:
            tty.msg('No root specs')
        else:
            tty.msg('Root specs')
            display_specs(
                env.user_specs, args,
                decorator=lambda s, f: color.colorize('@*{%s}' % f))
        print()

        if args.show_concretized:
            tty.msg('Concretized roots')
            display_specs(
                env.specs_by_hash.values(), args, decorator=decorator)
            print()

    tty.msg("%s" % plural(len(results), 'installed package'))

    display_specs(results, args, decorator=decorator, all_headers=True)

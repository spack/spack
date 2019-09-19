# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
'''Deprecate one Spack install in favor of another

Spack packages of different configurations cannot be installed to the same
location. However, in some circumstances (e.g. security patches) old
installations should never be used again. In these cases, we will mark the old
installation as deprecated, remove it, and link another installation into its
place.

It is up to the user to ensure binary compatibility between the deprecated
installation and its replacement.
'''
import argparse
import os

import spack.cmd
import spack.store
import spack.cmd.common.arguments as arguments

description = "Replace one package with another via symlinks"
section = "admin"
level = "long"

# Arguments for display_specs when we find ambiguity
display_args = {
    'long': True,
    'show_flags': True,
    'variants': True,
    'indent': 4,
}


def setup_parser(sp):
    setup_parser.parser = sp

    arguments.add_common_arguments(sp, ['yes_to_all'])

    deps = sp.add_mutually_exclusive_group()
    deps.add_argument('-d', '--dependencies', action='store_true',
                      default=True, dest='dependencies',
                      help='Deprecate dependencies (default)')
    deps.add_argument('-D', '--no-dependencies', action='store_false',
                      default=True, dest='dependencies',
                      help='Do not deprecate dependencies')

    install = sp.add_mutually_exclusive_group()
    install.add_argument('-i', '--install-replacement', action='store_true',
                         default=False, dest='install',
                         help='Concretize and install replacement spec')
    install.add_argument('-I', '--no-install-replacement',
                         action='store_false', default=False, dest='install',
                         help='Replacement spec must already be installed (default)')  # noqa 501

    sp.add_argument('-l', '--link-type', type=str,
                    default='soft', choices=['soft', 'hard'],
                    help="Type of filesystem link to use for deprecation (default soft)")  # noqa 501

    sp.add_argument('specs', nargs=argparse.REMAINDER,
                    help="spec to replace and spec to replace with")


def find_single_matching_spec(spec):
    env = ev.get_active_environment()
    hashes = env.all_hashes() if env else None

    specs = spack.store.db.query_local(spec, hashes=hashes)
    if len(specs) > 1:
        tty.error('%s matches multiple packages:' % spec)
        print()
        print spack.cmd.display_specs(deprecated, **display_args)
        print()
        tty.die("Use a more specific spec to refer to %s" % spec)
    elif not specs:
        t = 'package in envrionment %s' % env if env else 'installed package'
        tty.die('%s does not match any %s.' % (spec, t))

    return specs[0]


def deprecate(parser, args):
    """Deprecate one spec in favor of another"""
    specs = spack.cmd.parse_specs(args.specs)

    if len(specs) != 2:
        raise SpackError('spack deprecate requires exactly two specs')

    deprecated = find_single_matching_spec(specs[0])

    if args.install:
        replacement = specs[1].concretized()
        replacement.package.do_install()
    else:
        replacement = find_single_matching_spec(specs[1])

    if not args.yes_to_all:
        tty.msg('The following package will be deprecated:\n')
        spack.cmd.display_specs(deprecated, **display_args)
        tty.msg("In favor of:\n")
        spack.cmd.display_specs(replacement, **display_args)
        answer = tty.get_yes_or_no('Do you want to proceed?', default=False)
        if not answer:
            tty.die('Will not deprecate any packages.')

    link_fn = os.link if args.link_type == 'hard' else os.symlink

    if args.dependencies:
        for dep in deprecated.traverse(type='link', root=False):
            try:
                repl = replacement[dep.name]
                dep.package.do_deprecate(repl, link_fn)
            except KeyError as e:
                if "No spec with name" not in e.message:
                    raise e

    deprecated.package.do_deprecate(replacement, link_fn)


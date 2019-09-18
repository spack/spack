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

description = "Replace one package with another via symlinks"
section = "admin"
level = "long"


def setup_parser(sp):
    setup_parser.parser = sp

    deps = sp.add_mutually_exclusive_group()
    deps.add_argument('-d', '--dependencies', action='store_true',
                      default=True, dest='dependencies',
                      help='Deprecate dependencies')
    deps.add_argument('-D', '--no-dependencies', action='store_false',
                      default=True, dest='dependencies',
                      help='Do not deprecate dependencies')

    install = sp.add_mutually_exclusive_group()
    install.add_argument('-i', '--install-replacement', action='store_true',
                         default=False, dest='install',
                         help='Concretize and install replacement spec')
    install.add_argument('-I', '--no-install-replacement',
                         action='store_false', default=False, dest='install',
                         help='Replacement spec must already be installed')

    sp.add_argument('-l', '--link-type', type=str,
                    default='soft', choices=['soft', 'hard'],
                    help="Type of filesystem link to use for deprecation")

    sp.add_argument('specs', nargs=argparse.REMAINDER,
                    help="spec to replace and spec to replace with")


def deprecate(parser, args):
    """Deprecate one spec in favor of another"""
    specs = spack.cmd.parse_specs(args.specs)

    if len(specs) != 2:
        raise SpackError('spack deprecate requires exactly two specs')

    deprecated = spack.store.db.query_one(specs[0])

    if args.install:
        replacement = specs[1].concretized()
        replacement.package.do_install()
    else:
        replacement = spack.store.db.query_one(specs[1])

    link_fn = os.link if args.link_type == 'hard' else os.symlink

    if args.dependencies:
        for dep in deprecated.traverse(type='link'):
            try:
                repl = replacement[dep.name]
                dep.package.do_deprecate(repl, link_fn)
            except KeyError as e:
                if "No spec with name" not in e.message:
                    raise e

    deprecated.package.do_deprecate(replacement, link_fn)


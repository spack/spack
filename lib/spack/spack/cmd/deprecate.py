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
from __future__ import print_function
import argparse
import os

import llnl.util.tty as tty

import spack.cmd
import spack.store
import spack.cmd.common.arguments as arguments
import spack.environment as ev
from spack.error import SpackError

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


def find_single_matching_spec(spec, env, installed=True):
    hashes = env.all_hashes() if env else None

    specs = spack.store.db.query_local(spec, hashes=hashes,
                                       installed=installed)
    if len(specs) > 1:
        tty.error('%s matches multiple packages:' % spec)
        print()
        print(spack.cmd.display_specs(specs, **display_args))
        print()
        tty.die("Use a more specific spec to refer to %s" % spec)
    elif not specs:
        t = 'package in envrionment %s' % env if env else 'installed package'
        tty.die('%s does not match any %s.' % (spec, t))

    return specs[0]


def deprecate(parser, args):
    """Deprecate one spec in favor of another"""
    env = ev.get_env(args, 'deprecate')
    specs = spack.cmd.parse_specs(args.specs)

    if len(specs) != 2:
        raise SpackError('spack deprecate requires exactly two specs')

    deprecated = find_single_matching_spec(specs[0], env,
                                           installed=['installed',
                                                      'deprecated'])

    if args.install:
        replacement = specs[1].concretized()
        replacement.package.do_install()
    else:
        replacement = find_single_matching_spec(specs[1], env)

    # Check whether package to deprecate has active extensions
    if deprecated.package.extendable:
        view = spack.filesystem_view.YamlFilesystemView(deprecated.prefix,
                                                        spack.store.layout)
        active_exts = view.extensions_layout.extension_map(deprecated).values()
        if active_exts:
            short = deprecated.format('{name}/{hash:7}')
            msg = "Spec %s has active extensions\n" % short
            for active in active_exts:
                msg += '        %s\n' % active.format('{name}/{hash:7}')
                msg += "Deactivate extensions before deprecating %s" % short
            tty.die(msg)

    # Check whether package to deprecate is an active extension
    if deprecated.package.is_extension:
        extendee = deprecated.package.extendee_spec
        view = spack.filesystem_view.YamlFilesystemView(extendee.prefix,
                                                        spack.store.layout)
        if deprecated.package.is_activated(view):
            short = deprecated.format('{name}/{hash:7}')
            short_extendee = extendee.format('{name}/{hash:7}')
            msg = "Spec %s is an active extension of %s\n" % (short,
                                                              short_extendee)
            msg += "Deactivate %s to be able to deprecate it" % short
            tty.die(msg)

    if not args.yes_to_all:
        tty.msg('The following package will be deprecated:\n')
        spack.cmd.display_specs([deprecated], **display_args)
        tty.msg("In favor of:\n")
        spack.cmd.display_specs([replacement], **display_args)
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

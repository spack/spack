# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import six
import sys

import llnl.util.tty.colify as colify

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.repo

description = "list packages that provide a particular virtual package"
section = "basic"
level = "long"


def setup_parser(subparser):
    subparser.epilog = 'If called without argument returns ' \
                       'the list of all valid virtual packages'
    arguments.add_common_arguments(subparser, ['specs'])


def providers(parser, args):
    valid_virtuals = sorted(spack.repo.path.provider_index.providers.keys())

    buffer = six.StringIO()
    isatty = sys.stdout.isatty()
    if isatty:
        buffer.write('Virtual packages:\n')
    colify.colify(valid_virtuals, output=buffer, tty=isatty, indent=4)
    valid_virtuals_str = buffer.getvalue()

    # If called without arguments, list all the virtual packages
    if not args.specs:
        print(valid_virtuals_str)
        return

    # Otherwise, parse the specs from command line
    specs = spack.cmd.parse_specs(args.specs)

    # Check prerequisites
    non_virtual = [
        str(s) for s in specs if not s.virtual or s.name not in valid_virtuals
    ]
    if non_virtual:
        msg = 'non-virtual specs cannot be part of the query '
        msg += '[{0}]\n'.format(', '.join(non_virtual))
        msg += valid_virtuals_str
        raise ValueError(msg)

    # Display providers
    for spec in specs:
        if sys.stdout.isatty():
            print("{0}:".format(spec))
        spack.cmd.display_specs(sorted(spack.repo.path.providers_for(spec)))
        print('')

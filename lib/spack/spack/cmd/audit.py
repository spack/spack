# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import llnl.util.tty.color as cl
import spack.audit


description = "audit configuration files, packages, etc."
section = "system"
level = "short"


def setup_parser(subparser):
    # Top level flags, valid for every audit class
    sp = subparser.add_subparsers(metavar='SUBCOMMAND', dest='subcommand')

    # Audit configuration files
    sp.add_parser(
        'configuration',
        help='audit configuration files'
    )


def audit(parser, args):
    # FIXME: trigger subcommands
    errors = spack.audit.audit_cfgcmp.run()
    if errors:
        msg = '{0}: {1} issue{2} found'.format(
            spack.audit.audit_cfgcmp.tag, len(errors),
            '' if len(errors) == 1 else 's'
        )
        header = '@*b{' + msg + '}'
        print(cl.colorize(header))
        for idx, error in enumerate(errors):
            print(str(idx + 1) + '. ' + str(error))

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os
import argparse

import spack.paths
from spack.util.gpg import Gpg

description = "handle GPG actions for spack"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='GPG sub-commands')

    verify = subparsers.add_parser('verify')
    verify.add_argument('package', type=str,
                        help='the package to verify')
    verify.add_argument('signature', type=str, nargs='?',
                        help='the signature file')
    verify.set_defaults(func=gpg_verify)

    trust = subparsers.add_parser('trust')
    trust.add_argument('keyfile', type=str,
                       help='add a key to the trust store')
    trust.set_defaults(func=gpg_trust)

    untrust = subparsers.add_parser('untrust')
    untrust.add_argument('--signing', action='store_true',
                         help='allow untrusting signing keys')
    untrust.add_argument('keys', nargs='+', type=str,
                         help='remove keys from the trust store')
    untrust.set_defaults(func=gpg_untrust)

    sign = subparsers.add_parser('sign')
    sign.add_argument('--output', metavar='DEST', type=str,
                      help='the directory to place signatures')
    sign.add_argument('--key', metavar='KEY', type=str,
                      help='the key to use for signing')
    sign.add_argument('--clearsign', action='store_true',
                      help='if specified, create a clearsign signature')
    sign.add_argument('package', type=str,
                      help='the package to sign')
    sign.set_defaults(func=gpg_sign)

    create = subparsers.add_parser('create')
    create.add_argument('name', type=str,
                        help='the name to use for the new key')
    create.add_argument('email', type=str,
                        help='the email address to use for the new key')
    create.add_argument('--comment', metavar='COMMENT', type=str,
                        default='GPG created for Spack',
                        help='a description for the intended use of the key')
    create.add_argument('--expires', metavar='EXPIRATION', type=str,
                        default='0', help='when the key should expire')
    create.add_argument('--export', metavar='DEST', type=str,
                        help='export the public key to a file')
    create.set_defaults(func=gpg_create)

    list = subparsers.add_parser('list')
    list.add_argument('--trusted', action='store_true',
                      default=True, help='list trusted keys')
    list.add_argument('--signing', action='store_true',
                      help='list keys which may be used for signing')
    list.set_defaults(func=gpg_list)

    init = subparsers.add_parser('init')
    init.add_argument('--from', metavar='DIR', type=str,
                      dest='import_dir', help=argparse.SUPPRESS)
    init.set_defaults(func=gpg_init)

    export = subparsers.add_parser('export')
    export.add_argument('location', type=str,
                        help='where to export keys')
    export.add_argument('keys', nargs='*',
                        help='the keys to export; '
                             'all secret keys if unspecified')
    export.set_defaults(func=gpg_export)


def gpg_create(args):
    if args.export:
        old_sec_keys = Gpg.signing_keys()
    Gpg.create(name=args.name, email=args.email,
               comment=args.comment, expires=args.expires)
    if args.export:
        new_sec_keys = set(Gpg.signing_keys())
        new_keys = new_sec_keys.difference(old_sec_keys)
        Gpg.export_keys(args.export, *new_keys)


def gpg_export(args):
    keys = args.keys
    if not keys:
        keys = Gpg.signing_keys()
    Gpg.export_keys(args.location, *keys)


def gpg_list(args):
    Gpg.list(args.trusted, args.signing)


def gpg_sign(args):
    key = args.key
    if key is None:
        keys = Gpg.signing_keys()
        if len(keys) == 1:
            key = keys[0]
        elif not keys:
            raise RuntimeError('no signing keys are available')
        else:
            raise RuntimeError('multiple signing keys are available; '
                               'please choose one')
    output = args.output
    if not output:
        output = args.package + '.asc'
    # TODO: Support the package format Spack creates.
    Gpg.sign(key, args.package, output, args.clearsign)


def gpg_trust(args):
    Gpg.trust(args.keyfile)


def gpg_init(args):
    import_dir = args.import_dir
    if import_dir is None:
        import_dir = spack.paths.gpg_keys_path

    for root, _, filenames in os.walk(import_dir):
        for filename in filenames:
            if not filename.endswith('.key'):
                continue
            Gpg.trust(os.path.join(root, filename))


def gpg_untrust(args):
    Gpg.untrust(args.signing, *args.keys)


def gpg_verify(args):
    # TODO: Support the package format Spack creates.
    signature = args.signature
    if signature is None:
        signature = args.package + '.asc'
    Gpg.verify(signature, args.package)


def gpg(parser, args):
    if args.func:
        args.func(args)

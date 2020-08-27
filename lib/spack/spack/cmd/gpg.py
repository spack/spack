# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import argparse

import spack.cmd.common.arguments as arguments
import spack.paths
from spack.util.gpg import Gpg

description = "handle GPG actions for spack"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='GPG sub-commands')

    verify = subparsers.add_parser('verify', help=gpg_verify.__doc__)
    arguments.add_common_arguments(verify, ['installed_spec'])
    verify.add_argument('signature', type=str, nargs='?',
                        help='the signature file')
    verify.set_defaults(func=gpg_verify)

    trust = subparsers.add_parser('trust', help=gpg_trust.__doc__)
    trust.add_argument('keyfile', type=str,
                       help='add a key to the trust store')
    trust.set_defaults(func=gpg_trust)

    untrust = subparsers.add_parser('untrust', help=gpg_untrust.__doc__)
    untrust.add_argument('--signing', action='store_true',
                         help='allow untrusting signing keys')
    untrust.add_argument('keys', nargs='+', type=str,
                         help='remove keys from the trust store')
    untrust.set_defaults(func=gpg_untrust)

    sign = subparsers.add_parser('sign', help=gpg_sign.__doc__)
    sign.add_argument('--output', metavar='DEST', type=str,
                      help='the directory to place signatures')
    sign.add_argument('--key', metavar='KEY', type=str,
                      help='the key to use for signing')
    sign.add_argument('--clearsign', action='store_true',
                      help='if specified, create a clearsign signature')
    arguments.add_common_arguments(sign, ['installed_spec'])
    sign.set_defaults(func=gpg_sign)

    create = subparsers.add_parser('create', help=gpg_create.__doc__)
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

    list = subparsers.add_parser('list', help=gpg_list.__doc__)
    list.add_argument('--trusted', action='store_true',
                      default=True, help='list trusted keys')
    list.add_argument('--signing', action='store_true',
                      help='list keys which may be used for signing')
    list.set_defaults(func=gpg_list)

    init = subparsers.add_parser('init', help=gpg_init.__doc__)
    init.add_argument('--from', metavar='DIR', type=str,
                      dest='import_dir', help=argparse.SUPPRESS)
    init.set_defaults(func=gpg_init)

    export = subparsers.add_parser('export', help=gpg_export.__doc__)
    export.add_argument('location', type=str,
                        help='where to export keys')
    export.add_argument('keys', nargs='*',
                        help='the keys to export; '
                             'all secret keys if unspecified')
    export.set_defaults(func=gpg_export)


def gpg_create(args):
    """create a new key"""
    if args.export:
        old_sec_keys = Gpg.signing_keys()
    Gpg.create(name=args.name, email=args.email,
               comment=args.comment, expires=args.expires)
    if args.export:
        new_sec_keys = set(Gpg.signing_keys())
        new_keys = new_sec_keys.difference(old_sec_keys)
        Gpg.export_keys(args.export, *new_keys)


def gpg_export(args):
    """export a secret key"""
    keys = args.keys
    if not keys:
        keys = Gpg.signing_keys()
    Gpg.export_keys(args.location, *keys)


def gpg_list(args):
    """list keys available in the keyring"""
    Gpg.list(args.trusted, args.signing)


def gpg_sign(args):
    """sign a package"""
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
        output = args.spec[0] + '.asc'
    # TODO: Support the package format Spack creates.
    Gpg.sign(key, ' '.join(args.spec), output, args.clearsign)


def gpg_trust(args):
    """add a key to the keyring"""
    Gpg.trust(args.keyfile)


def gpg_init(args):
    """add the default keys to the keyring"""
    import_dir = args.import_dir
    if import_dir is None:
        import_dir = spack.paths.gpg_keys_path

    for root, _, filenames in os.walk(import_dir):
        for filename in filenames:
            if not filename.endswith('.key'):
                continue
            Gpg.trust(os.path.join(root, filename))


def gpg_untrust(args):
    """remove a key from the keyring"""
    Gpg.untrust(args.signing, *args.keys)


def gpg_verify(args):
    """verify a signed package"""
    # TODO: Support the package format Spack creates.
    signature = args.signature
    if signature is None:
        signature = args.spec[0] + '.asc'
    Gpg.verify(signature, ' '.join(args.spec))


def gpg(parser, args):
    if args.func:
        args.func(args)

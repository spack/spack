# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.paths
from spack.util.executable import Executable


GNUPGHOME = spack.paths.gpg_path


def parse_keys_output(output):
    keys = []
    found_sec = False
    for line in output.split('\n'):
        if found_sec:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_sec = False
            elif line.startswith('ssb'):
                found_sec = False
        elif line.startswith('sec'):
            found_sec = True
    return keys


class Gpg(object):
    @staticmethod
    def gpg():
        # TODO: Support loading up a GPG environment from a built gpg.
        gpg = Executable('gpg2')
        if not os.path.exists(GNUPGHOME):
            os.makedirs(GNUPGHOME)
            os.chmod(GNUPGHOME, 0o700)
        gpg.add_default_env('GNUPGHOME', GNUPGHOME)
        return gpg

    @classmethod
    def create(cls, **kwargs):
        r, w = os.pipe()
        r = os.fdopen(r, 'r')
        w = os.fdopen(w, 'w')
        w.write('''
        Key-Type: rsa
        Key-Length: 4096
        Key-Usage: sign
        Name-Real: %(name)s
        Name-Email: %(email)s
        Name-Comment: %(comment)s
        Expire-Date: %(expires)s
        %%no-protection
        %%commit
        ''' % kwargs)
        w.close()
        cls.gpg()('--gen-key', '--batch', input=r)
        r.close()

    @classmethod
    def signing_keys(cls):
        output = cls.gpg()('--list-secret-keys', '--with-colons',
                           '--fingerprint', '--fingerprint', output=str)
        return parse_keys_output(output)

    @classmethod
    def export_keys(cls, location, *keys):
        cls.gpg()('--armor', '--export', '--output', location, *keys)

    @classmethod
    def trust(cls, keyfile):
        cls.gpg()('--import', keyfile)

    @classmethod
    def untrust(cls, signing, *keys):
        args = [
            '--yes',
            '--batch',
        ]
        if signing:
            signing_args = args + ['--delete-secret-keys'] + list(keys)
            cls.gpg()(*signing_args)
        args.append('--delete-keys')
        args.extend(keys)
        cls.gpg()(*args)

    @classmethod
    def sign(cls, key, file, output, clearsign=False):
        args = [
            '--armor',
            '--default-key', key,
            '--output', output,
            file,
        ]
        if clearsign:
            args.insert(0, '--clearsign')
        else:
            args.insert(0, '--detach-sign')
        cls.gpg()(*args)

    @classmethod
    def verify(cls, signature, file):
        cls.gpg()('--verify', signature, file)

    @classmethod
    def list(cls, trusted, signing):
        if trusted:
            cls.gpg()('--list-public-keys')
        if signing:
            cls.gpg()('--list-secret-keys')

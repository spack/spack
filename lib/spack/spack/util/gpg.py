# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import spack.error
import spack.paths
import spack.version
from spack.util.executable import which

_gnupg_version_re = r"^gpg \(GnuPG\) (.*)$"

GNUPGHOME = os.getenv('SPACK_GNUPGHOME', spack.paths.gpg_path)


def parse_secret_keys_output(output):
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


def parse_public_keys_output(output):
    keys = []
    found_pub = False
    for line in output.split('\n'):
        if found_pub:
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
                found_pub = False
            elif line.startswith('ssb'):
                found_pub = False
        elif line.startswith('pub'):
            found_pub = True
    return keys


class Gpg(object):
    _gpg = None

    @staticmethod
    def gpg():
        # TODO: Support loading up a GPG environment from a built gpg.
        if Gpg._gpg is None:
            gpg = which('gpg2', 'gpg')

            if not gpg:
                raise SpackGPGError("Spack requires gpg version 2 or higher.")

            # ensure that the version is actually >= 2 if we find 'gpg'
            if gpg.name == 'gpg':
                output = gpg('--version', output=str)
                match = re.search(_gnupg_version_re, output, re.M)

                if not match:
                    raise SpackGPGError("Couldn't determine version of gpg")

                v = spack.version.Version(match.group(1))
                if v < spack.version.Version('2'):
                    raise SpackGPGError("Spack requires GPG version >= 2")

            # make the GNU PG path if we need to
            # TODO: does this need to be in the spack directory?
            # we should probably just use GPG's regular conventions
            if not os.path.exists(GNUPGHOME):
                os.makedirs(GNUPGHOME)
                os.chmod(GNUPGHOME, 0o700)
            gpg.add_default_env('GNUPGHOME', GNUPGHOME)

            Gpg._gpg = gpg
        return Gpg._gpg

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
    def signing_keys(cls, *args):
        output = cls.gpg()('--list-secret-keys', '--with-colons',
                           '--fingerprint', *args, output=str)
        return parse_secret_keys_output(output)

    @classmethod
    def public_keys(cls, *args):
        output = cls.gpg()('--list-public-keys', '--with-colons',
                           '--fingerprint', *args, output=str)
        return parse_public_keys_output(output)

    @classmethod
    def export_keys(cls, location, *keys):
        cls.gpg()('--batch', '--yes',
                  '--armor', '--export',
                  '--output', location, *keys)

    @classmethod
    def trust(cls, keyfile):
        cls.gpg()('--import', keyfile)

    @classmethod
    def untrust(cls, signing, *keys):
        if signing:
            cls.gpg()('--batch', '--yes', '--delete-secret-keys',
                      *cls.signing_keys(*keys))

        cls.gpg()('--batch', '--yes', '--delete-keys',
                  *cls.public_keys(*keys))

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
    def verify(cls, signature, file, suppress_warnings=False):
        if suppress_warnings:
            cls.gpg()('--verify', signature, file, error=str)
        else:
            cls.gpg()('--verify', signature, file)

    @classmethod
    def list(cls, trusted, signing):
        if trusted:
            cls.gpg()('--list-public-keys')
        if signing:
            cls.gpg()('--list-secret-keys')


class SpackGPGError(spack.error.SpackError):
    """Class raised when GPG errors are detected."""

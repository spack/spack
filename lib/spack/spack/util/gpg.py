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

import spack.paths
from spack.util.executable import Executable


GNUPGHOME = spack.paths.gpg_path


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
        keys = []
        output = cls.gpg()('--list-secret-keys', '--with-colons',
                           '--fingerprint', output=str)
        for line in output.split('\n'):
            if line.startswith('fpr'):
                keys.append(line.split(':')[9])
        return keys

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

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

import pytest

from spack.paths import mock_gpg_data_path, mock_gpg_keys_path
import spack.util.gpg as gpg_util
from spack.main import SpackCommand
from spack.util.executable import ProcessError


@pytest.fixture(scope='function')
def testing_gpg_directory(tmpdir):
    old_gpg_path = gpg_util.GNUPGHOME
    gpg_util.GNUPGHOME = str(tmpdir.join('gpg'))
    yield
    gpg_util.GNUPGHOME = old_gpg_path


@pytest.fixture(scope='function')
def gpg():
    return SpackCommand('gpg')


def has_gnupg2():
    try:
        gpg_util.Gpg.gpg()('--version', output=os.devnull)
        return True
    except Exception:
        return False


@pytest.mark.maybeslow
@pytest.mark.skipif(not has_gnupg2(),
                    reason='These tests require gnupg2')
def test_gpg(gpg, tmpdir, testing_gpg_directory):
    # Verify a file with an empty keyring.
    with pytest.raises(ProcessError):
        gpg('verify', os.path.join(mock_gpg_data_path, 'content.txt'))

    # Import the default key.
    gpg('init', '--from', mock_gpg_keys_path)

    # List the keys.
    # TODO: Test the output here.
    gpg('list', '--trusted')
    gpg('list', '--signing')

    # Verify the file now that the key has been trusted.
    gpg('verify', os.path.join(mock_gpg_data_path, 'content.txt'))

    # Untrust the default key.
    gpg('untrust', 'Spack testing')

    # Now that the key is untrusted, verification should fail.
    with pytest.raises(ProcessError):
        gpg('verify', os.path.join(mock_gpg_data_path, 'content.txt'))

    # Create a file to test signing.
    test_path = tmpdir.join('to-sign.txt')
    with open(str(test_path), 'w+') as fout:
        fout.write('Test content for signing.\n')

    # Signing without a private key should fail.
    with pytest.raises(RuntimeError) as exc_info:
        gpg('sign', str(test_path))
    assert exc_info.value.args[0] == 'no signing keys are available'

    # Create a key for use in the tests.
    keypath = tmpdir.join('testing-1.key')
    gpg('create',
        '--comment', 'Spack testing key',
        '--export', str(keypath),
        'Spack testing 1',
        'spack@googlegroups.com')
    keyfp = gpg_util.Gpg.signing_keys()[0]

    # List the keys.
    # TODO: Test the output here.
    gpg('list')
    gpg('list', '--trusted')
    gpg('list', '--signing')

    # Signing with the default (only) key.
    gpg('sign', str(test_path))

    # Verify the file we just verified.
    gpg('verify', str(test_path))

    # Export the key for future use.
    export_path = tmpdir.join('export.testing.key')
    gpg('export', str(export_path))

    # Create a second key for use in the tests.
    gpg('create',
        '--comment', 'Spack testing key',
        'Spack testing 2',
        'spack@googlegroups.com')

    # List the keys.
    # TODO: Test the output here.
    gpg('list', '--trusted')
    gpg('list', '--signing')

    test_path = tmpdir.join('to-sign-2.txt')
    with open(str(test_path), 'w+') as fout:
        fout.write('Test content for signing.\n')

    # Signing with multiple signing keys is ambiguous.
    with pytest.raises(RuntimeError) as exc_info:
        gpg('sign', str(test_path))
    assert exc_info.value.args[0] == \
        'multiple signing keys are available; please choose one'

    # Signing with a specified key.
    gpg('sign', '--key', keyfp, str(test_path))

    # Untrusting signing keys needs a flag.
    with pytest.raises(ProcessError):
        gpg('untrust', 'Spack testing 1')

    # Untrust the key we created.
    gpg('untrust', '--signing', keyfp)

    # Verification should now fail.
    with pytest.raises(ProcessError):
        gpg('verify', str(test_path))

    # Trust the exported key.
    gpg('trust', str(export_path))

    # Verification should now succeed again.
    gpg('verify', str(test_path))

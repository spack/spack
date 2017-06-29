##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import argparse
import os

import pytest
import spack
import spack.cmd.gpg as gpg
import spack.util.gpg as gpg_util
from spack.util.executable import ProcessError


@pytest.fixture(scope='function')
def testing_gpg_directory(tmpdir):
    old_gpg_path = gpg_util.GNUPGHOME
    gpg_util.GNUPGHOME = str(tmpdir.join('gpg'))
    yield
    gpg_util.GNUPGHOME = old_gpg_path


def has_gnupg2():
    try:
        gpg_util.Gpg.gpg()('--version', output=os.devnull)
        return True
    except Exception:
        return False


@pytest.mark.usefixtures('testing_gpg_directory')
@pytest.mark.skipif(not has_gnupg2(),
                    reason='These tests require gnupg2')
def test_gpg(tmpdir):
    parser = argparse.ArgumentParser()
    gpg.setup_parser(parser)

    # Verify a file with an empty keyring.
    args = parser.parse_args(['verify', os.path.join(
        spack.mock_gpg_data_path, 'content.txt')])
    with pytest.raises(ProcessError):
        gpg.gpg(parser, args)

    # Import the default key.
    args = parser.parse_args(['init'])
    args.import_dir = spack.mock_gpg_keys_path
    gpg.gpg(parser, args)

    # List the keys.
    # TODO: Test the output here.
    args = parser.parse_args(['list', '--trusted'])
    gpg.gpg(parser, args)
    args = parser.parse_args(['list', '--signing'])
    gpg.gpg(parser, args)

    # Verify the file now that the key has been trusted.
    args = parser.parse_args(['verify', os.path.join(
        spack.mock_gpg_data_path, 'content.txt')])
    gpg.gpg(parser, args)

    # Untrust the default key.
    args = parser.parse_args(['untrust', 'Spack testing'])
    gpg.gpg(parser, args)

    # Now that the key is untrusted, verification should fail.
    args = parser.parse_args(['verify', os.path.join(
        spack.mock_gpg_data_path, 'content.txt')])
    with pytest.raises(ProcessError):
        gpg.gpg(parser, args)

    # Create a file to test signing.
    test_path = tmpdir.join('to-sign.txt')
    with open(str(test_path), 'w+') as fout:
        fout.write('Test content for signing.\n')

    # Signing without a private key should fail.
    args = parser.parse_args(['sign', str(test_path)])
    with pytest.raises(RuntimeError) as exc_info:
        gpg.gpg(parser, args)
    assert exc_info.value.args[0] == 'no signing keys are available'

    # Create a key for use in the tests.
    keypath = tmpdir.join('testing-1.key')
    args = parser.parse_args(['create',
                              '--comment', 'Spack testing key',
                              '--export', str(keypath),
                              'Spack testing 1',
                              'spack@googlegroups.com'])
    gpg.gpg(parser, args)
    keyfp = gpg_util.Gpg.signing_keys()[0]

    # List the keys.
    # TODO: Test the output here.
    args = parser.parse_args(['list', '--trusted'])
    gpg.gpg(parser, args)
    args = parser.parse_args(['list', '--signing'])
    gpg.gpg(parser, args)

    # Signing with the default (only) key.
    args = parser.parse_args(['sign', str(test_path)])
    gpg.gpg(parser, args)

    # Verify the file we just verified.
    args = parser.parse_args(['verify', str(test_path)])
    gpg.gpg(parser, args)

    # Export the key for future use.
    export_path = tmpdir.join('export.testing.key')
    args = parser.parse_args(['export', str(export_path)])
    gpg.gpg(parser, args)

    # Create a second key for use in the tests.
    args = parser.parse_args(['create',
                              '--comment', 'Spack testing key',
                              'Spack testing 2',
                              'spack@googlegroups.com'])
    gpg.gpg(parser, args)

    # List the keys.
    # TODO: Test the output here.
    args = parser.parse_args(['list', '--trusted'])
    gpg.gpg(parser, args)
    args = parser.parse_args(['list', '--signing'])
    gpg.gpg(parser, args)

    test_path = tmpdir.join('to-sign-2.txt')
    with open(str(test_path), 'w+') as fout:
        fout.write('Test content for signing.\n')

    # Signing with multiple signing keys is ambiguous.
    args = parser.parse_args(['sign', str(test_path)])
    with pytest.raises(RuntimeError) as exc_info:
        gpg.gpg(parser, args)
    assert exc_info.value.args[0] == \
        'multiple signing keys are available; please choose one'

    # Signing with a specified key.
    args = parser.parse_args(['sign', '--key', keyfp, str(test_path)])
    gpg.gpg(parser, args)

    # Untrusting signing keys needs a flag.
    args = parser.parse_args(['untrust', 'Spack testing 1'])
    with pytest.raises(ProcessError):
        gpg.gpg(parser, args)

    # Untrust the key we created.
    args = parser.parse_args(['untrust', '--signing', keyfp])
    gpg.gpg(parser, args)

    # Verification should now fail.
    args = parser.parse_args(['verify', str(test_path)])
    with pytest.raises(ProcessError):
        gpg.gpg(parser, args)

    # Trust the exported key.
    args = parser.parse_args(['trust', str(export_path)])
    gpg.gpg(parser, args)

    # Verification should now succeed again.
    args = parser.parse_args(['verify', str(test_path)])
    gpg.gpg(parser, args)

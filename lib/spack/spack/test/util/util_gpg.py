# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.util.gpg as gpg


def test_parse_gpg_output_case_one():
    # Two keys, fingerprint for primary keys, but not subkeys
    output = """sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
"""
    keys = gpg.parse_keys_output(output)

    assert len(keys) == 2
    assert keys[0] == 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    assert keys[1] == 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'


def test_parse_gpg_output_case_two():
    # One key, fingerprint for primary key as well as subkey
    output = """sec:-:2048:1:AAAAAAAAAA:AAAAAAAA:::-:::escaESCA:::+:::23::0:
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
uid:-::::AAAAAAAAA::AAAAAAAAA::Joe (Test) <j.s@s.com>::::::::::0:
ssb:-:2048:1:AAAAAAAAA::::::esa:::+:::23:
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
"""
    keys = gpg.parse_keys_output(output)

    assert len(keys) == 1
    assert keys[0] == 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


def test_parse_gpg_output_case_three():
    # Two keys, fingerprint for primary keys as well as subkeys
    output = """sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
sec::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA:AAAAAAAAAA:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:AAAAAAAAAA::::::::::
fpr:::::::::ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ:"""

    keys = gpg.parse_keys_output(output)

    assert len(keys) == 2
    assert keys[0] == 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    assert keys[1] == 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'

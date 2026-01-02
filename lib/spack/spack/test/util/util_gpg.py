# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import time

import pytest

import spack.util.gpg


@pytest.fixture()
def has_socket_dir():
    spack.util.gpg.init()
    return bool(spack.util.gpg.SOCKET_DIR)


def test_parse_gpg_output_case_one():
    now = int(time.time())
    # Two keys, fingerprint for primary keys, but not subkeys
    output = f"""sec::2048:1:AAAAAAAAAAAAAAAA:{now}:{now}:::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
uid:::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:{now}::::::::::
sec::2048:1:AAAAAAAAAAAAAAAA:{now}:{now}:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:{now}::::::::::
"""
    keys = spack.util.gpg._parse_gpg_output(output)

    assert len(keys) == 2
    assert keys[0].fpr == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    assert keys[1].fpr == "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"


def test_parse_gpg_output_case_two():
    now = int(time.time())
    # One key, fingerprint for primary key as well as subkey
    output = f"""sec:-:2048:1:AAAAAAAAAA:{now}:::-:::escaESCA:::+:::23::0:
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
uid:-::::{now}::AAAAAAAAA::Joe (Test) <j.s@s.com>::::::::::0:
ssb:-:2048:1:AAAAAAAAA:{now}:::::esa:::+:::23:
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
grp:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
"""
    keys = spack.util.gpg._parse_gpg_output(output)

    assert len(keys) == 1
    assert keys[0].fpr == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


def test_parse_gpg_output_case_three():
    now = int(time.time())
    # Two keys, fingerprint for primary keys as well as subkeys
    output = f"""sec::2048:1:AAAAAAAAAAAAAAAA:{now}:{now}:::::::::
fpr:::::::::WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW:
uid:::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:{now}::::::::::
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
sec::2048:1:AAAAAAAAAAAAAAAA:{now}:{now}:::::::::
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>:
ssb::2048:1:AAAAAAAAAAAAAAAA:{now}::::::::::
fpr:::::::::ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ:"""

    keys = spack.util.gpg._parse_gpg_output(output)

    assert len(keys) == 2
    assert keys[0].fpr == "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    assert keys[1].fpr == "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"


def test_really_long_gnupghome_dir(tmp_path: pathlib.Path, has_socket_dir):
    if not has_socket_dir:
        pytest.skip("This test requires /var/run/user/$(id -u)")

    N = 960
    tdir = str(tmp_path)
    while len(tdir) < N:
        tdir = os.path.join(tdir, "filler")

    tdir = tdir[:N].rstrip(os.sep)
    tdir += "0" * (N - len(tdir))

    with spack.util.gpg.gnupghome_override(tdir):
        spack.util.gpg.create(
            name="Spack testing 1", email="test@spack.io", comment="Spack testing key", expires="0"
        )
        spack.util.gpg.list(True, True)

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
    output = f"""sec:-:2048:1:AAAAAAAAAAAAAAAA:{now}:{now}::-:::CESces::::::23:{now}:0:
fpr:::::::::XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX:
uid:-::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>::::::::::0:
ssb:-:2048:1:AAAAAAAAAAAAAAAA:{now}:::-:::ces::::::23:
sec:-:2048:1:AAAAAAAAAAAAAAAA:{now}:{now}::-:::CESces::::::23::0:
fpr:::::::::YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY:
uid:-::::{now}::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA::Joe (Test) <j.s@s.com>::::::::::0:
ssb:-:2048:1:AAAAAAAAAAAAAAAA:{now}:::-:::ces::::::23:
"""
    keys = spack.util.gpg._parse_gpg_output(output)

    assert len(keys) == 2
    assert keys[0].fpr == "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    assert keys[1].fpr == "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

    assert f"{keys[0]:colons}" in output
    assert f"{keys[1]:colons}" in output


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
        spack.util.gpg.glist(True, True)


def test_gpg_capabilities_case_insensitvie():
    for e in spack.util.gpg.GpgKeyCapability:
        assert e == spack.util.gpg.GpgKeyCapability(e.value.lower())
        assert e == spack.util.gpg.GpgKeyCapability(e.value.upper())

    assert spack.util.gpg.GpgKeyCapability("q") == spack.util.gpg.GpgKeyCapability.UNKNOWN


def test_gpg_trust_case_insensitive():
    for e in spack.util.gpg.GpgKeyTrust:
        assert e == spack.util.gpg.GpgKeyTrust(e.value.lower())
        assert e == spack.util.gpg.GpgKeyTrust(e.value.upper())

    for alt_unknown in ("i", "o"):
        assert (
            spack.util.gpg.GpgKeyTrust(alt_unknown.lower()) == spack.util.gpg.GpgKeyTrust.UNKNOWN
        )
        assert (
            spack.util.gpg.GpgKeyTrust(alt_unknown.upper()) == spack.util.gpg.GpgKeyTrust.UNKNOWN
        )

    assert spack.util.gpg.GpgKeyTrust("v") == spack.util.gpg.GpgKeyTrust.ERROR


def test_gpg_trust_ownertrust():
    assert 0 == spack.util.gpg.GpgKeyTrust.UNKNOWN.ownertrust
    assert 1 == spack.util.gpg.GpgKeyTrust.EXPIRED.ownertrust
    assert 2 == spack.util.gpg.GpgKeyTrust.UNDEFINED.ownertrust
    assert 3 == spack.util.gpg.GpgKeyTrust.NEVER.ownertrust
    assert 4 == spack.util.gpg.GpgKeyTrust.MARGINAL.ownertrust
    assert 5 == spack.util.gpg.GpgKeyTrust.FULL.ownertrust
    assert 6 == spack.util.gpg.GpgKeyTrust.ULTIMATE.ownertrust
    assert 7 == spack.util.gpg.GpgKeyTrust.REVOKED.ownertrust
    assert 8 == spack.util.gpg.GpgKeyTrust.ERROR.ownertrust
    assert 8 == spack.util.gpg.GpgKeyTrust.KNOWN.ownertrust
    assert 8 == spack.util.gpg.GpgKeyTrust.SPECIAL.ownertrust

    assert spack.util.gpg.GpgKeyTrust(0) == spack.util.gpg.GpgKeyTrust.UNKNOWN
    assert spack.util.gpg.GpgKeyTrust(1) == spack.util.gpg.GpgKeyTrust.EXPIRED
    assert spack.util.gpg.GpgKeyTrust(2) == spack.util.gpg.GpgKeyTrust.UNDEFINED
    assert spack.util.gpg.GpgKeyTrust(3) == spack.util.gpg.GpgKeyTrust.NEVER
    assert spack.util.gpg.GpgKeyTrust(4) == spack.util.gpg.GpgKeyTrust.MARGINAL
    assert spack.util.gpg.GpgKeyTrust(5) == spack.util.gpg.GpgKeyTrust.FULL
    assert spack.util.gpg.GpgKeyTrust(6) == spack.util.gpg.GpgKeyTrust.ULTIMATE
    assert spack.util.gpg.GpgKeyTrust(7) == spack.util.gpg.GpgKeyTrust.REVOKED
    assert spack.util.gpg.GpgKeyTrust(8) == spack.util.gpg.GpgKeyTrust.ERROR

    assert spack.util.gpg.GpgKeyTrust(9) == spack.util.gpg.GpgKeyTrust.ERROR


def test_gpg_key_algorithm():
    with pytest.raises(
        ValueError, match="GpgKeyAlgorithm can only be constructed from another Enum or an `int`"
    ):
        spack.util.gpg.GpgKeyAlgorithm("need a number")

    assert spack.util.gpg.GpgKeyAlgorithm(40) == spack.util.gpg.GpgKeyAlgorithm.UNKNOWN
    assert spack.util.gpg.GpgKeyAlgorithm(300) == spack.util.gpg.GpgKeyAlgorithm.LIBGCRYPT

    for e in spack.util.gpg.GpgKeyAlgorithm:
        assert str(e) == f"{e}"
        assert "2048" in f"{e:2048}"


@pytest.mark.maybeslow
@pytest.mark.not_on_windows("does not run on windows")
def test_trust_secret_key_file(tmp_path: pathlib.Path, mock_gnupghome):
    """Verify that `spack gpg trust` can import secret keys from a keyfile."""
    # Create a signing key.
    spack.util.gpg.create(
        name="Spack CI test", email="ci@spack.io", comment="regression test key", expires="0"
    )
    signing = spack.util.gpg.signing_keys()
    assert len(signing) == 1, "expected exactly one signing key after create"
    original_fpr = signing[0].fpr

    # Export it to file.
    secret_keyfile = str(tmp_path / "secret.gpg")
    spack.util.gpg.export_keys(secret_keyfile, signing, secret=True)

    # Use gpg.untrust() to remove the key from the keyring.
    spack.util.gpg.untrust(True, original_fpr)
    assert spack.util.gpg.signing_keys() == [], "keyring should be empty after untrust"

    # Use gpg.trust() to re-import the key.
    spack.util.gpg.trust(secret_keyfile, yes_to_all=True)
    restored = spack.util.gpg.signing_keys()
    assert len(restored) == 1, "signing key should be restored after trusting secret key file"
    assert restored[0].fpr == original_fpr, "restored key fingerprint should match original"


def test_gpg_key_type():
    str_to_type = [
        ("pub", spack.util.gpg.GpgKeyType.PUBLIC),
        ("sub", spack.util.gpg.GpgKeyType.PUBLIC_SUBKEY),
        ("sec", spack.util.gpg.GpgKeyType.SECRET),
        ("ssb", spack.util.gpg.GpgKeyType.SECRET_SUBKEY),
        ("sec#", spack.util.gpg.GpgKeyType.SECRET_SUBKEY_ONLY),
        ("rvk", spack.util.gpg.GpgKeyType.REVOCATION),
    ]

    for s, t in str_to_type:
        assert s == str(t)
        assert spack.util.gpg.GpgKeyType(s) == t

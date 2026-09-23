# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.binary_distribution
import spack.util.filesystem as fs
import spack.util.gpg
from spack.main import SpackCommand
from spack.paths import mock_gpg_keys_path
from spack.util.executable import ProcessError

#: spack command used by tests below
gpg = SpackCommand("gpg")
bootstrap = SpackCommand("bootstrap")
mirror = SpackCommand("mirror")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


# test gpg command detection
@pytest.mark.parametrize(
    "cmd_name,version",
    [
        ("gpg", "undetectable"),  # undetectable version
        ("gpg", "gpg (GnuPG) 1.3.4"),  # insufficient version
        ("gpg", "gpg (GnuPG) 2.2.19"),  # sufficient version
        ("gpg2", "gpg (GnuPG) 2.2.19"),  # gpg2 command
    ],
)
def test_find_gpg(cmd_name, version, tmp_path: pathlib.Path, mock_gnupghome, monkeypatch):
    TEMPLATE = '#!/bin/sh\necho "{version}"\n'

    with fs.working_dir(str(tmp_path)):
        for fname in (cmd_name, "gpgconf"):
            with open(fname, "w", encoding="utf-8") as f:
                f.write(TEMPLATE.format(version=version))
            fs.set_executable(fname)

    monkeypatch.setenv("PATH", str(tmp_path))
    if version == "undetectable" or version.endswith("1.3.4"):
        with pytest.raises(spack.util.gpg.SpackGPGError):
            spack.util.gpg.init(force=True)
    else:
        spack.util.gpg.init(force=True)
        assert spack.util.gpg.GPG is not None


def test_no_gpg_in_path(tmp_path: pathlib.Path, mock_gnupghome, monkeypatch, mutable_config):
    monkeypatch.setenv("PATH", str(tmp_path))
    bootstrap("disable")
    with pytest.raises(RuntimeError):
        spack.util.gpg.init(force=True)


@pytest.mark.maybeslow
def test_gpg(tmp_path: pathlib.Path, mutable_config, mock_gnupghome):
    MOCK_KEY = "B27095DEEF1787C3C8C85917DCA0241840A5DAE2"

    # Import the default key.
    gpg("init", "-y", "--from", mock_gpg_keys_path)

    # List the keys.
    # TODO: Test the output here.
    out = gpg("list", "--trusted")
    assert out.count(MOCK_KEY) == 1

    out = gpg("list", "--signing")
    assert out.count(MOCK_KEY) == 1

    # Untrust the default key.
    gpg("untrust", "Spack testing")

    out = gpg("list", "--trusted")
    assert out.count(MOCK_KEY) == 0

    # Create a key for use in the tests.
    keypath = tmp_path / "testing-1.key"
    gpg(
        "create",
        "--comment",
        "Spack testing key",
        "--export",
        str(keypath),
        "Spack testing 1",
        "spack@googlegroups.com",
    )
    keyfp = spack.util.gpg.signing_keys()[0].fpr

    # List the keys.
    # TODO: Test the output here.
    out = gpg("list")
    assert out.count(MOCK_KEY) == 0
    assert out.count(keyfp) == 1

    out = gpg("list", "--trusted")
    assert out.count(MOCK_KEY) == 0
    assert out.count(keyfp) == 1

    out = gpg("list", "--signing")
    assert out.count(MOCK_KEY) == 0
    # Once for trusted, once for signing
    assert out.count(keyfp) == 2

    # Export the public key for future use (keyfp).
    export_path = tmp_path / "export.testing.key"
    gpg("export", str(export_path))

    # Ensure we exported the right content!
    with open(str(export_path), "r", encoding="utf-8") as fd:
        content = fd.read()
    assert "BEGIN PGP PUBLIC KEY BLOCK" in content

    # Export the private key
    private_export_path = tmp_path / "export-secret.testing.key"
    gpg("export", "--secret", str(private_export_path))

    # Ensure we exported the right content!
    with open(str(private_export_path), "r", encoding="utf-8") as fd:
        content = fd.read()
    assert "BEGIN PGP PRIVATE KEY BLOCK" in content

    # Create a second key for use in the tests.
    gpg("create", "--comment", "Spack testing key", "Spack testing 2", "spack@googlegroups.com")

    # List the keys.
    out = gpg("list", "--trusted")
    # Spack testing 1 and Spack testing 2
    assert out.count("pub ") == 2
    out = gpg("list", "--signing")
    assert out.count("sec ") == 2

    # Untrusting signing keys needs a flag.
    with pytest.raises(ProcessError):
        gpg("untrust", "Spack testing 1")

    # Untrust the key we created.
    gpg("untrust", "--signing", keyfp)

    out = gpg("list", "--signing")
    assert out.count("sec ") == 1
    assert out.count(keyfp) == 0

    # Trust the exported public key (keyfpr)
    # Trust the exported key.
    gpg("trust", "-y", str(export_path))
    out = gpg("list", "--signing")
    assert out.count("sec ") == 1
    assert out.count("pub ") == 2
    assert out.count(keyfp) == 1

    relative_keys_path = spack.binary_distribution.buildcache_relative_keys_path()

    # Publish the keys using a directory path
    test_path = tmp_path / "dir_cache"
    os.makedirs(f"{test_path}")
    gpg("publish", "--rebuild-index", "-d", str(test_path))
    assert os.path.exists(f"{test_path}/{relative_keys_path}/keys.manifest.json")

    # Publish the keys using a mirror url
    test_path = tmp_path / "url_cache"
    os.makedirs(f"{test_path}")
    test_url = test_path.as_uri()
    gpg("publish", "--rebuild-index", "--mirror-url", test_url)
    assert os.path.exists(f"{test_path}/{relative_keys_path}/keys.manifest.json")

    # Publish the keys using a mirror name
    test_path = tmp_path / "named_cache"
    os.makedirs(f"{test_path}")
    mirror_url = test_path.as_uri()
    mirror("add", "gpg", mirror_url)
    gpg("publish", "--rebuild-index", "-m", "gpg")
    assert os.path.exists(f"{test_path}/{relative_keys_path}/keys.manifest.json")

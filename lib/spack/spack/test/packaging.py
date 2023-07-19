# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks the binary packaging infrastructure
"""
import argparse
import os
import pathlib
import shutil
import sys
from collections import OrderedDict

import pytest

from llnl.util.symlink import symlink

import spack.binary_distribution as bindist
import spack.cmd.buildcache as buildcache
import spack.package_base
import spack.repo
import spack.store
import spack.util.gpg
import spack.util.url as url_util
from spack.fetch_strategy import FetchStrategyComposite, URLFetchStrategy
from spack.paths import mock_gpg_keys_path
from spack.relocate import (
    needs_binary_relocation,
    needs_text_relocation,
    relocate_links,
    relocate_text,
)
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


@pytest.mark.usefixtures("install_mockery", "mock_gnupghome")
def test_buildcache(mock_archive, tmp_path, monkeypatch, mutable_config):
    # Install a test package
    spec = Spec("trivial-install-test-package").concretized()
    fetcher = FetchStrategyComposite()
    fetcher.append(URLFetchStrategy(mock_archive.url))
    monkeypatch.setattr(spec.package, "fetcher", fetcher)
    spec.package.do_install()
    pkghash = "/" + str(spec.dag_hash(7))

    # Put some non-relocatable file in there
    dummy_txt = pathlib.Path(spec.prefix) / "dummy.txt"
    dummy_txt.write_text(spec.prefix)

    # Create an absolute symlink
    linkname = os.path.join(spec.prefix, "link_to_dummy.txt")
    symlink(dummy_txt, linkname)

    # Create the build cache and put it directly into the mirror
    mirror_path = str(tmp_path / "test-mirror")
    spack.mirror.create(mirror_path, specs=[])

    # register mirror with spack config
    mirrors = {"spack-mirror-test": url_util.path_to_file_url(mirror_path)}
    spack.config.set("mirrors", mirrors)

    with spack.stage.Stage(mirrors["spack-mirror-test"], name="build_cache", keep=True):
        parser = argparse.ArgumentParser()
        buildcache.setup_parser(parser)

        create_args = ["create", "-f", "--rebuild-index", mirror_path, pkghash]
        # Create a private key to sign package with if gpg2 available
        spack.util.gpg.create(
            name="test key 1",
            expires="0",
            email="spack@googlegroups.com",
            comment="Spack test key",
        )

        args = parser.parse_args(create_args)
        buildcache.buildcache(parser, args)
        # trigger overwrite warning
        buildcache.buildcache(parser, args)

        # Uninstall the package
        spec.package.do_uninstall(force=True)

        install_args = ["install", "-f", pkghash]
        args = parser.parse_args(install_args)
        # Test install
        buildcache.buildcache(parser, args)

        files = os.listdir(spec.prefix)

        assert "link_to_dummy.txt" in files
        assert "dummy.txt" in files

        # Validate the relocation information
        buildinfo = bindist.read_buildinfo_file(spec.prefix)
        assert buildinfo["relocate_textfiles"] == ["dummy.txt"]
        assert buildinfo["relocate_links"] == ["link_to_dummy.txt"]

        args = parser.parse_args(["keys"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["list", "trivial"])
        buildcache.buildcache(parser, args)

        # Copy a key to the mirror to have something to download
        shutil.copyfile(mock_gpg_keys_path + "/external.key", mirror_path + "/external.key")

        args = parser.parse_args(["keys"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["keys", "-f"])
        buildcache.buildcache(parser, args)

        args = parser.parse_args(["keys", "-i", "-t"])
        buildcache.buildcache(parser, args)


def test_relocate_text(tmp_path):
    """Tests that a text file containing the original directory of an installation, can be
    relocated to a target directory.
    """
    original_dir = "/home/spack/opt/spack"
    relocation_dir = "/opt/rh/devtoolset/"
    dummy_txt = tmp_path / "dummy.txt"
    dummy_txt.write_text(original_dir)

    relocate_text([str(dummy_txt)], {original_dir: relocation_dir})
    text = dummy_txt.read_text()

    assert relocation_dir in text
    assert original_dir not in text


def test_relocate_links(tmpdir):
    tmpdir.ensure("new_prefix_a", dir=True)

    own_prefix_path = str(tmpdir.join("prefix_a", "file"))
    dep_prefix_path = str(tmpdir.join("prefix_b", "file"))
    system_path = os.path.join(os.path.sep, "system", "path")

    # Old prefixes to new prefixes
    prefix_to_prefix = OrderedDict(
        [
            # map <tmpdir>/prefix_a -> <tmpdir>/new_prefix_a
            (str(tmpdir.join("prefix_a")), str(tmpdir.join("new_prefix_a"))),
            # map <tmpdir>/prefix_b -> <tmpdir>/new_prefix_b
            (str(tmpdir.join("prefix_b")), str(tmpdir.join("new_prefix_b"))),
            # map <tmpdir> -> /fallback/path -- this is just to see we respect order.
            (str(tmpdir), os.path.join(os.path.sep, "fallback", "path")),
        ]
    )

    with tmpdir.join("new_prefix_a").as_cwd():
        # To be relocated
        os.symlink(own_prefix_path, "to_self")
        os.symlink(dep_prefix_path, "to_dependency")

        # To be ignored
        os.symlink(system_path, "to_system")
        os.symlink("relative", "to_self_but_relative")

        relocate_links(["to_self", "to_dependency", "to_system"], prefix_to_prefix)

        # These two are relocated
        assert os.readlink("to_self") == str(tmpdir.join("new_prefix_a", "file"))
        assert os.readlink("to_dependency") == str(tmpdir.join("new_prefix_b", "file"))

        # These two are not.
        assert os.readlink("to_system") == system_path
        assert os.readlink("to_self_but_relative") == "relative"


def test_needs_relocation():
    assert needs_binary_relocation("application", "x-sharedlib")
    assert needs_binary_relocation("application", "x-executable")
    assert not needs_binary_relocation("application", "x-octet-stream")
    assert not needs_binary_relocation("text", "x-")
    assert needs_text_relocation("text", "x-")
    assert not needs_text_relocation("symbolic link to", "x-")
    assert needs_binary_relocation("application", "x-mach-binary")


@pytest.fixture()
def mock_download():
    """Mock a failing download strategy."""

    class FailedDownloadStrategy(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise spack.fetch_strategy.FailedDownloadError(
                "<non-existent URL>", "This FetchStrategy always fails"
            )

    fetcher = FetchStrategyComposite()
    fetcher.append(FailedDownloadStrategy())

    @property
    def fake_fn(self):
        return fetcher

    orig_fn = spack.package_base.PackageBase.fetcher
    spack.package_base.PackageBase.fetcher = fake_fn
    yield
    spack.package_base.PackageBase.fetcher = orig_fn


@pytest.mark.parametrize(
    "manual,instr", [(False, False), (False, True), (True, False), (True, True)]
)
@pytest.mark.disable_clean_stage_check
def test_manual_download(
    install_mockery, mock_download, default_mock_concretization, monkeypatch, manual, instr
):
    """
    Ensure expected fetcher fail message based on manual download and instr.
    """

    @property
    def _instr(pkg):
        return f"Download instructions for {pkg.spec.name}"

    spec = default_mock_concretization("a")
    spec.package.manual_download = manual
    if instr:
        monkeypatch.setattr(spack.package_base.PackageBase, "download_instr", _instr)

    expected = spec.package.download_instr if manual else "All fetchers failed"
    with pytest.raises(spack.util.web.FetchError, match=expected):
        spec.package.do_fetch()


@pytest.fixture()
def fetching_not_allowed(monkeypatch):
    class FetchingNotAllowed(spack.fetch_strategy.FetchStrategy):
        def mirror_id(self):
            return None

        def fetch(self):
            raise Exception("Sources are fetched but shouldn't have been")

    fetcher = FetchStrategyComposite()
    fetcher.append(FetchingNotAllowed())
    monkeypatch.setattr(spack.package_base.PackageBase, "fetcher", fetcher)


def test_fetch_without_code_is_noop(
    default_mock_concretization, install_mockery, fetching_not_allowed
):
    """do_fetch for packages without code should be a no-op"""
    pkg = default_mock_concretization("a").package
    pkg.has_code = False
    pkg.do_fetch()


def test_fetch_external_package_is_noop(
    default_mock_concretization, install_mockery, fetching_not_allowed
):
    """do_fetch for packages without code should be a no-op"""
    spec = default_mock_concretization("a")
    spec.external_path = "/some/where"
    assert spec.external
    spec.package.do_fetch()

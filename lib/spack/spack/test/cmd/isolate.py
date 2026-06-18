# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

import pytest

import spack.cmd.isolate
import spack.config
import spack.main
from spack.test.conftest import _create_mock_configuration_scopes

sp_isolate = spack.main.SpackCommand("isolate")
sp_config = spack.main.SpackCommand("config")


@pytest.fixture(scope="function")
def mutable_config_with_dir(tmp_path_factory: pytest.TempPathFactory, configuration_dir):
    """Like config, but tests can modify the configuration. This fixture also
    yields the configuration directory, unlike conf_test.mutable_config
    """
    mutable_dir = tmp_path_factory.mktemp("mutable_config") / "tmp"
    shutil.copytree(configuration_dir, mutable_dir)

    scopes = _create_mock_configuration_scopes(mutable_dir)
    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg, mutable_dir


@pytest.fixture(scope="function")
def mock_pre_isolate_config(mutable_config_with_dir, monkeypatch, tmp_path):
    _, cfg_dir = mutable_config_with_dir
    include_path = cfg_dir / "spack" / "include.yaml"
    isolate_path = cfg_dir / "isolate"
    preserved_include_path = cfg_dir / "spack" / ".isolate.include.yaml"
    # These paths usually live in spack/etc/spack
    monkeypatch.setattr(spack.cmd.isolate, "INCLUDE_PATH", str(include_path))
    monkeypatch.setattr(spack.cmd.isolate, "ISOLATE_SCOPE_PATH", str(isolate_path))
    monkeypatch.setattr(spack.cmd.isolate, "PRESERVED_INCLUDE_PATH", str(preserved_include_path))

    yield cfg_dir, tmp_path


def test_isolate_smoke_test(mock_pre_isolate_config):
    cfg_dir, iso_root = mock_pre_isolate_config
    isolated_path = iso_root / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    assert os.path.exists(spack.cmd.isolate.ISOLATE_SCOPE_PATH)
    assert os.path.exists(spack.cmd.isolate.PRESERVED_INCLUDE_PATH)
    assert isolated_path.exists()
    assert os.path.exists(os.path.join(spack.cmd.isolate.ISOLATE_SCOPE_PATH, "bootstrap.yaml"))
    assert os.path.exists(os.path.join(spack.cmd.isolate.ISOLATE_SCOPE_PATH, "config.yaml"))
    # we reload the config after isolation
    with spack.config.use_configuration(cfg_dir / "spack"):
        assert "isolate" in sp_config("scopes")


def test_isolate_added_config(mock_pre_isolate_config):
    cfg_dir, iso_root = mock_pre_isolate_config
    isolated_path = iso_root / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    with spack.config.use_configuration(cfg_dir / "spack"):
        sp_config("add", "config:build_jobs:42")
        assert (isolated_path / "config.yaml").exists()
        with open(isolated_path / "config.yaml", "r", encoding="utf-8") as f:
            text = f.read().strip()
        expected_text = """\
config:
  build_jobs: 42"""
        assert text == expected_text


def test_isolate_overwrite_same_dir(mock_pre_isolate_config):
    _, iso_root = mock_pre_isolate_config
    isolated_path1 = iso_root / "test-isolation1"
    sp_isolate("--path", str(isolated_path1))
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolated_path1))
    sp_isolate("--overwrite", "--path", str(isolated_path1))


def test_isolate_overwrite_different_dir(mock_pre_isolate_config):
    cfg_dir, iso_root = mock_pre_isolate_config
    isolated_path1 = iso_root / "test-isolation"
    isolated_path2 = iso_root / "test-isolation"
    sp_isolate("--path", str(isolated_path1))
    with pytest.raises(Exception):
        sp_isolate("--path", str(isolated_path1))
    sp_isolate("--overwrite", "--path", str(isolated_path2))
    with open(cfg_dir / "isolate" / "bootstrap.yaml", "r", encoding="utf-8") as f:
        text = f.read().strip()
    expected_text = f"""\
bootstrap:
  root: {isolated_path2 / "bootstrap"}"""
    assert text == expected_text


def test_isolate_undo(mock_pre_isolate_config):
    cfg_dir, iso_root = mock_pre_isolate_config
    isolated_path = iso_root / "test-isolation"
    sp_isolate("--path", str(isolated_path))
    sp_isolate("--undo")
    with spack.config.use_configuration(cfg_dir / "spack"):
        assert "isolate" not in sp_config("scopes")

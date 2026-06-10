import pytest
import shutil
from spack.test.conftest import _create_mock_configuration_scopes
import os
import textwrap
import spack.main
import spack.config
import spack.paths
import spack.cmd.isolate

sp_isolate = spack.main.SpackCommand("isolate")
sp_config = spack.main.SpackCommand("config")
@pytest.fixture(scope="function")
def mutable_config_with_dir(tmp_path_factory: pytest.TempPathFactory, configuration_dir):
    """Like config, but tests can modify the configuration."""
    mutable_dir = tmp_path_factory.mktemp("mutable_config") / "tmp"
    shutil.copytree(configuration_dir, mutable_dir)

    scopes = _create_mock_configuration_scopes(mutable_dir)
    with spack.config.use_configuration(*scopes) as cfg:
        yield cfg, mutable_dir

@pytest.fixture(scope="function")
def mock_pre_isolate_config(mutable_config_with_dir, monkeypatch):
    _, cfg_dir = mutable_config_with_dir
    include_path = cfg_dir / "spack" / "include.yaml"
    isolate_path = cfg_dir / "isolate"
    user_path = cfg_dir / "user"
    monkeypatch.setattr(spack.cmd.isolate, "INCLUDE_PATH", str(include_path))
    monkeypatch.setattr(spack.cmd.isolate, "ISOLATE_PATH", str(isolate_path))
    monkeypatch.setattr(spack.paths, "user_cache_path", user_path)
    monkeypatch.setattr(spack.paths, "user_config_path", user_path)
    yield cfg_dir


def test_isolate_smoke_test(mock_pre_isolate_config, tmp_path):
    cfg_dir = mock_pre_isolate_config
    isolate_scope_path = cfg_dir / "isolate"
    isolated_path = tmp_path / "test-isolation"
    sp_isolate(str(isolated_path))
    assert isolate_scope_path.exists()
    assert isolated_path.exists()
    assert (isolate_scope_path / "bootstrap.yaml").exists()
    assert (isolate_scope_path / "config.yaml").exists()
    # we reload the config after isolation
    with spack.config.use_configuration(cfg_dir / "spack"):
       assert "isolate" in sp_config("scopes")


def test_isolate_added_config(mock_pre_isolate_config, tmp_path):
    cfg_dir = mock_pre_isolate_config
    isolated_path = tmp_path / "test-isolation"
    sp_isolate(str(isolated_path))
    with spack.config.use_configuration(cfg_dir / "spack"):
        sp_config("add", "config:build_jobs:42")
        assert (isolated_path / "config.yaml").exists()
    

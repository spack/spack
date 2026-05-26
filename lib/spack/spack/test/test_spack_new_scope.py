# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test automatic creation and behavior of the spack-new config scope."""

import os

import pytest

import spack.config
import spack.paths


class MockPaths:
    """Simple mock object for spack.paths in tests."""

    def __init__(self, spack_root, etc_path, var_path, instance_id="test123"):
        self.prefix = str(spack_root)
        self.etc_path = str(etc_path)
        self.var_path = str(var_path)
        self.spack_instance_id = instance_id
        self.default_license_dir = str(etc_path / "licenses")


@pytest.fixture
def mock_spack_paths(tmp_path, monkeypatch):
    """Create a MockPaths object with temporary directories for testing.

    Returns a dict with:
        - paths: MockPaths object to pass to functions
        - spack_root: temporary spack root
        - home: temporary home directory
        - etc_path: $spack_root/etc/spack
        - var_path: $spack_root/var/spack
    """
    spack_root = tmp_path / "spack"
    home = tmp_path / "home"
    etc_path = spack_root / "etc" / "spack"
    var_path = spack_root / "var" / "spack"

    # Create basic structure
    etc_path.mkdir(parents=True)
    (etc_path / "defaults").mkdir()
    var_path.mkdir(parents=True)
    home.mkdir()

    # Mock home directory expansion
    def mock_expanduser(path):
        if path.startswith("~"):
            return str(home / path[2:])
        return path

    monkeypatch.setattr(os.path, "expanduser", mock_expanduser)

    # Create MockPaths object
    paths = MockPaths(spack_root, etc_path, var_path)

    return {
        "paths": paths,
        "spack_root": spack_root,
        "home": home,
        "etc_path": etc_path,
        "var_path": var_path,
    }


class TestSpackNewScopeCreation:
    """Test when and how the spack-new scope is created."""

    def test_created_for_fresh_install_writable(self, mock_spack_paths):
        """Test that spack-new is created for a fresh install when spack is writable."""
        m = mock_spack_paths

        # Fresh install: no ~/.spack, no old data in $spack
        # etc_path is writable by default in tmpdir

        # Call the initialization function with mock paths
        with spack.config.override_paths(m["paths"]):
            spack_new_path = spack.config._initialize_spack_new_scope()

        assert spack_new_path is not None
        assert (m["etc_path"] / "spack-new").exists()
        assert (m["etc_path"] / "spack-new" / "config.yaml").exists()
        assert (m["etc_path"] / "spack-new" / "modules.yaml").exists()

    def test_not_created_when_not_writable(self, mock_spack_paths, monkeypatch):
        """Test that spack-new is NOT created when $spack/etc is not writable."""
        m = mock_spack_paths

        # Mock os.access to return False for write check
        original_access = os.access

        def mock_access(path, mode):
            if str(path) == str(m["etc_path"]) and mode == os.W_OK:
                return False
            return original_access(path, mode)

        monkeypatch.setattr(os, "access", mock_access)

        with spack.config.override_paths(m["paths"]):
            spack_new_path = spack.config._initialize_spack_new_scope()

        assert spack_new_path is None
        assert not (m["etc_path"] / "spack-new").exists()

    def test_already_exists_returns_path(self, mock_spack_paths):
        """Test that if spack-new already exists, we just return its path."""
        m = mock_spack_paths

        # Pre-create spack-new
        spack_new_dir = m["etc_path"] / "spack-new"
        spack_new_dir.mkdir()
        (spack_new_dir / "config.yaml").write_text("config: {}\n")

        with spack.config.override_paths(m["paths"]):
            spack_new_path = spack.config._initialize_spack_new_scope()

        assert spack_new_path == str(spack_new_dir)


class TestSpackNewScopeContent:
    """Test the content of generated spack-new configs."""

    def test_xdg_paths_for_fresh_install(self, mock_spack_paths):
        """Test that fresh install gets XDG-compliant paths via full Configuration."""
        m = mock_spack_paths

        # Fresh install: no ~/.spack, no old data
        # Create the full Configuration the same way Spack does
        with spack.config.override_paths(m["paths"]):
            cfg = spack.config.create()

            # Check that user_cache_path is NOT in spack-new (determined by paths.py)
            # spack-new should not set user_cache_path so it can be explicitly configured
            user_cache_path_in_config = cfg.get("config:user_cache_path", default=None)
            assert user_cache_path_in_config is None

            # Derived paths use variable substitution
            reports_path = cfg.get("config:reports_path")
            assert reports_path == "$user_cache_path/reports"

            # Check that XDG paths use $xdg_data_home variable
            tcl_root = cfg.get("modules:default:roots:tcl")
            assert tcl_root == "$xdg_data_home/spack/modules"

            lmod_root = cfg.get("modules:default:roots:lmod")
            assert lmod_root == "$xdg_data_home/spack/lmod"

            # Check environments use $xdg_data_home
            environments_root = cfg.get("config:environments_root")
            assert environments_root == "$xdg_data_home/spack/environments"

            # Check source cache uses $xdg_data_home
            source_cache = cfg.get("config:source_cache")
            assert source_cache == "$xdg_data_home/spack/downloads"

            # Check install_tree uses $xdg_data_home
            install_tree_root = cfg.get("config:install_tree:root")
            assert install_tree_root == "$xdg_data_home/spack/installs"

            # Check misc cache uses variable substitution
            misc_cache = cfg.get("config:misc_cache")
            assert misc_cache == "$user_cache_path/test123/cache"

            # Verify that the spack-new scope was actually created
            assert (m["etc_path"] / "spack-new").exists()

    def test_old_style_paths_when_dotspack_exists(self, mock_spack_paths):
        """Test that ~/.spack existence triggers old-style paths."""
        m = mock_spack_paths

        # Create ~/.spack to simulate existing installation
        dotspack = m["home"] / ".spack"
        dotspack.mkdir()

        with spack.config.override_paths(m["paths"]):
            cfg = spack.config.create()

            # user_cache_path should NOT be set in spack-new config
            user_cache_path_in_config = cfg.get("config:user_cache_path", default=None)
            assert user_cache_path_in_config is None

            # Derived paths should use variable substitution
            reports_path = cfg.get("config:reports_path")
            assert reports_path == "$user_cache_path/reports"

            # Modules should still use old-style paths (same as defaults)
            tcl_root = cfg.get("modules:default:roots:tcl")
            assert tcl_root == "$spack/share/spack/modules"

            lmod_root = cfg.get("modules:default:roots:lmod")
            assert lmod_root == "$spack/share/spack/lmod"

            # Environments should use old-style path
            environments_root = cfg.get("config:environments_root")
            assert environments_root == "$spack/var/spack/environments"

    def test_spack_user_cache_path_env_var(self, mock_spack_paths, monkeypatch):
        """Test that SPACK_USER_CACHE_PATH env var overrides default."""
        m = mock_spack_paths

        # Set SPACK_USER_CACHE_PATH environment variable
        custom_cache = m["home"] / "custom" / "cache"
        monkeypatch.setenv("SPACK_USER_CACHE_PATH", str(custom_cache))

        with spack.config.override_paths(m["paths"]):
            cfg = spack.config.create()

            # SPACK_USER_CACHE_PATH doesn't write to config, so config shouldn't have it
            user_cache_path_in_config = cfg.get("config:user_cache_path", default=None)
            assert user_cache_path_in_config is None

            # Derived paths should use variable substitution
            reports_path = cfg.get("config:reports_path")
            assert reports_path == "$user_cache_path/reports"

    def test_old_style_paths_for_old_layout(self, mock_spack_paths):
        """Test old-style config when old data exists in $spack."""
        m = mock_spack_paths

        # Simulate old layout: create old install path with data
        old_install = m["spack_root"] / "opt" / "spack"
        old_install.mkdir(parents=True)
        (old_install / "some-package").mkdir()

        with spack.config.override_paths(m["paths"]):
            cfg = spack.config.create()

            # user_cache_path should NOT be set in spack-new config
            user_cache_path_in_config = cfg.get("config:user_cache_path", default=None)
            assert user_cache_path_in_config is None

            # Should point to old locations in $spack using variables
            # cfg.get() returns raw values; variable substitution happens in paths.py
            gpg_path = cfg.get("config:gpg_path")
            assert gpg_path == "$spack/opt/spack/gpg"

            install_tree_root = cfg.get("config:install_tree:root")
            assert install_tree_root == "$spack/opt/spack"

            source_cache = cfg.get("config:source_cache")
            assert source_cache == "$spack/var/spack/cache"

            # Modules should use old-style paths
            tcl_root = cfg.get("modules:default:roots:tcl")
            assert tcl_root == "$spack/share/spack/modules"

            lmod_root = cfg.get("modules:default:roots:lmod")
            assert lmod_root == "$spack/share/spack/lmod"

            # Environments should use old-style path
            environments_root = cfg.get("config:environments_root")
            assert environments_root == "$spack/var/spack/environments"


class TestOldLayoutDetection:
    """Test detection of old-style in-$spack layouts."""

    def test_detects_old_install_path(self, mock_spack_paths):
        """Test detection when opt/spack has installs."""
        m = mock_spack_paths

        # Create old install with some content (not just gpg dir)
        old_install = m["spack_root"] / "opt" / "spack"
        old_install.mkdir(parents=True)
        (old_install / "linux-ubuntu22.04-x86_64").mkdir(parents=True)

        with spack.config.override_paths(m["paths"]):
            assert spack.config._detect_old_spack_layout()

    def test_detects_old_environments(self, mock_spack_paths):
        """Test detection when var/spack/environments exists."""
        m = mock_spack_paths

        envs = m["var_path"] / "environments"
        envs.mkdir(parents=True)
        (envs / "myenv").mkdir()

        with spack.config.override_paths(m["paths"]):
            assert spack.config._detect_old_spack_layout()

    def test_detects_old_cache(self, mock_spack_paths):
        """Test detection when var/spack/cache has content."""
        m = mock_spack_paths

        cache = m["var_path"] / "cache"
        cache.mkdir(parents=True)
        (cache / "some-package.tar.gz").write_text("fake tarball")

        with spack.config.override_paths(m["paths"]):
            assert spack.config._detect_old_spack_layout()

    def test_no_detection_for_fresh_install(self, mock_spack_paths):
        """Test that fresh install is not detected as old layout."""
        m = mock_spack_paths
        # Fresh install with only directory structure, no data
        with spack.config.override_paths(m["paths"]):
            assert not spack.config._detect_old_spack_layout()

    def test_ignores_gpg_in_opt_spack(self, mock_spack_paths):
        """Test that lone gpg directory in opt/spack doesn't trigger detection."""
        m = mock_spack_paths

        # Create only gpg dir (should be ignored)
        old_install = m["spack_root"] / "opt" / "spack"
        old_install.mkdir(parents=True)
        (old_install / "gpg").mkdir()

        with spack.config.override_paths(m["paths"]):
            assert not spack.config._detect_old_spack_layout()

    def test_ignores_readme_in_gpg_keys(self, mock_spack_paths):
        """Test that README.md in var/spack/gpg doesn't trigger detection."""
        m = mock_spack_paths

        gpg_keys = m["var_path"] / "gpg"
        gpg_keys.mkdir(parents=True)
        (gpg_keys / "README.md").write_text("# GPG Keys")

        with spack.config.override_paths(m["paths"]):
            assert not spack.config._detect_old_spack_layout()


class CheckXdgVarInChildProc:
    """Callable that modifies XDG_DATA_HOME in child and verifies parent's frozen value is used."""

    def __init__(self, parent_xdg_data):
        self.parent_xdg_data = parent_xdg_data

    def __call__(self):
        import os

        import spack.util.path

        # Child process sets different XDG_DATA_HOME
        os.environ["XDG_DATA_HOME"] = "/different/child/data"

        # Verify that $xdg_data_home resolves to parent's value, not child's
        resolved = spack.util.path.substitute_config_variables("$xdg_data_home")
        assert resolved == self.parent_xdg_data, (
            f"Expected {self.parent_xdg_data}\nGot {resolved}"
        )


def test_child_proc_sanity_xdg_based_paths(tmp_path):
    """Test that child process uses parent's frozen XDG paths, not its own environment."""
    import spack.subprocess_context

    # Set parent's XDG_DATA_HOME
    parent_xdg_data = str(tmp_path / "parent-data")
    os.environ["XDG_DATA_HOME"] = parent_xdg_data

    try:
        spack_process = spack.subprocess_context.SpackTestProcess(
            CheckXdgVarInChildProc(parent_xdg_data)
        )
        p = spack_process.create()
        p.start()
        p.join()
        assert p.exitcode == 0
    finally:
        # Clean up env var
        os.environ.pop("XDG_DATA_HOME", None)

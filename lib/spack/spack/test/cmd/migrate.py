# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack
import spack.cmd.migrate
import spack.main
import spack.paths
from spack.paths import SpackPaths

migrate = spack.main.SpackCommand("migrate")


@pytest.fixture(autouse=True)
def clear_env_vars(working_env):
    """Clear XDG and SPACK location env vars."""
    for location in ["DATA", "STATE", "CACHE"]:
        os.environ.pop(f"XDG_{location}_HOME", None)
        os.environ.pop(f"SPACK_{location}_HOME", None)


@pytest.fixture
def set_home(working_env):
    """Fixture to set HOME environment variable for both Windows and Linux."""

    def _set_home(val):
        # Clear some env vars that can interfere w/ expanduser(~) on Windows
        os.environ.pop("USERPROFILE", None)
        os.environ.pop("HOMEDRIVE", None)
        os.environ["HOMEPATH"] = val

        # For expanduser on Linux
        os.environ["HOME"] = val

    yield _set_home


@pytest.fixture
def migrate_setup(tmp_path, set_home, monkeypatch, mutable_config):
    """Set up common test environment for migrate tests.

    Yields:
        tuple: (dotspack, created, new_config, paths)
    """
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()
    created = create_dotspack_files(dotspack)

    new_config = home / ".config" / "spack"

    # Create fresh SpackPaths object and patch the module
    paths = SpackPaths(_prefix=str(spack_root))
    monkeypatch.setattr(spack.paths, "locations", paths)

    yield (dotspack, created, new_config, paths)


def create_dotspack_files(base_path):
    """Create minimal test files under a base path to simulate ~/.spack structure.

    Args:
        base_path: Path-like object or string where files should be created

    Returns:
        dict: mapping of created file/dir paths to their expected content/structure
    """
    base = pathlib.Path(base_path)

    # Create config files with verifiable content
    config_yaml = base / "config.yaml"
    config_yaml.write_text("config:\n  build_jobs: 8\n")

    packages_yaml = base / "packages.yaml"
    packages_yaml.write_text("packages:\n  all:\n    compiler: [gcc]\n")

    # Return mapping of what we created
    return {"config_files": ["config.yaml", "packages.yaml"]}


def verify_files_copied(source_base, dest_base, created_files):
    """Verify that files from source_base have been copied to dest_base.

    Args:
        source_base: Path-like source directory
        dest_base: Path-like destination directory
        created_files: dict returned from create_dotspack_files

    Returns:
        bool: True if all expected files exist in dest_base with correct content
    """
    source = pathlib.Path(source_base)
    dest = pathlib.Path(dest_base)

    # Check if dest directory exists
    if not dest.exists():
        print(f"Destination directory does not exist: {dest}")
        return False

    # Check config files
    for config_file in created_files["config_files"]:
        source_file = source / config_file
        dest_file = dest / config_file

        if not dest_file.exists():
            print(f"Expected file does not exist: {dest_file}")
            if dest.exists():
                print(f"Files in {dest}: {list(dest.iterdir())}")
            else:
                print(f"{dest} does not exist")
            return False

        # Verify content matches
        if source_file.read_text() != dest_file.read_text():
            print(f"Content mismatch for {config_file}")
            return False

    return True


def test_migrate_basic(migrate_setup):
    """`spack migrate` with no additional arguments moves config files
    out of ~/.spack into ~/.config/spack, and does not delete any files
    in ~/.spack (e.g. if some spack instances are not getting updated to 1.2).
    """
    dotspack, created, new_config, paths = migrate_setup

    migrate()

    assert verify_files_copied(dotspack, new_config, created)
    assert dotspack.exists()
    for config_file in created["config_files"]:
        assert (dotspack / config_file).exists()


def test_migrate_with_clear(migrate_setup):
    """Test --clear: does everything `spack migrate` does, plus
    removes ~/.spack (moves it to ~/.spack.backup)."""
    dotspack, created, new_config, paths = migrate_setup

    backup_location = pathlib.Path(os.path.expanduser("~/.spack.backup"))

    migrate("--clear")

    assert verify_files_copied(backup_location, new_config, created)
    # --clear should remove old location (or rather, move it)
    assert not dotspack.exists()
    assert backup_location.exists()

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib

import pytest

import spack.cmd.migrate
import spack.main
import spack.paths
import spack.paths_base
from spack.paths import SpackPaths
from spack.paths_base import SpackPathsBase

migrate = spack.main.SpackCommand("migrate")


@pytest.fixture(autouse=True)
def clear_env_vars(working_env):
    spack.paths._unset_path_vars(os.environ)


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

    # Create package_repos directory with a test repo
    package_repos_dir = base / "package_repos"
    package_repos_dir.mkdir(parents=True, exist_ok=True)

    test_repo = package_repos_dir / "test_repo"
    test_repo.mkdir(parents=True, exist_ok=True)

    # Add a minimal repo.yaml to the test repo
    repo_yaml = test_repo / "repo.yaml"
    repo_yaml.write_text("repo:\n  namespace: test\n")

    # Add a packages directory
    packages_dir = test_repo / "packages"
    packages_dir.mkdir(parents=True, exist_ok=True)

    # Return mapping of what we created
    return {
        "config_files": ["config.yaml", "packages.yaml"],
        "package_repos": ["test_repo"],
        "test_repo_structure": {
            "repo.yaml": "repo:\n  namespace: test\n",
            "packages": {},  # directory
        },
    }


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


def verify_package_repos_copied(source_repos_base, dest_repos_base, created_files):
    """Verify that package repos have been copied correctly.

    Args:
        source_repos_base: Path-like source package_repos directory
        dest_repos_base: Path-like destination package_repos directory
        created_files: dict returned from create_dotspack_files

    Returns:
        bool: True if all expected repos exist in dest with correct structure
    """
    source_base = pathlib.Path(source_repos_base)
    dest_base = pathlib.Path(dest_repos_base)

    for repo_name in created_files["package_repos"]:
        source_repo = source_base / repo_name
        dest_repo = dest_base / repo_name

        if not dest_repo.exists():
            return False

        # Check for repo.yaml
        source_repo_yaml = source_repo / "repo.yaml"
        dest_repo_yaml = dest_repo / "repo.yaml"

        if not dest_repo_yaml.exists():
            return False

        if source_repo_yaml.read_text() != dest_repo_yaml.read_text():
            return False

        # Check for packages directory
        if not (dest_repo / "packages").is_dir():
            return False

    return True


def test_migrate_basic(tmp_path, set_home, monkeypatch, mutable_config):
    """Test basic migrate: copies files to new locations, preserves old location."""
    # Set up directories
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    # Set home BEFORE creating paths objects
    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()
    created = create_dotspack_files(dotspack)

    # Set expected new locations
    new_config = home / ".config" / "spack"
    new_state = home / ".local" / "state" / "spack"

    # Create fresh SpackPaths object and patch the module
    base_paths = SpackPathsBase(str(spack_root))
    paths = SpackPaths(base_paths)
    monkeypatch.setattr(spack.paths, "locations", paths)
    monkeypatch.setattr(spack.paths_base, "locations", base_paths)

    # Also need to patch the cmd.migrate module which has already imported these
    monkeypatch.setattr(spack.cmd.migrate, "paths", paths)
    monkeypatch.setattr(spack.cmd.migrate, "paths_base", base_paths)

    # Run migrate
    migrate()

    # Verify config files were copied
    assert verify_files_copied(dotspack, new_config, created)

    # Verify package repos were copied
    old_repos = dotspack / "package_repos"
    new_repos = new_state / "package_repos"
    assert verify_package_repos_copied(old_repos, new_repos, created)

    # Verify old location still exists (not deleted)
    assert dotspack.exists()
    for config_file in created["config_files"]:
        assert (dotspack / config_file).exists()


def test_migrate_with_clear(tmp_path, set_home, monkeypatch, mutable_config):
    """Test migrate --clear: copies files and removes ~/.spack."""
    # Set up directories
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    # Set home BEFORE creating paths objects
    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()
    created = create_dotspack_files(dotspack)

    # Set expected new locations
    new_config = home / ".config" / "spack"
    new_state = home / ".local" / "state" / "spack"

    # Create fresh SpackPaths object and patch the module
    base_paths = SpackPathsBase(str(spack_root))
    paths = SpackPaths(base_paths)
    monkeypatch.setattr(spack.paths, "locations", paths)
    monkeypatch.setattr(spack.paths_base, "locations", base_paths)

    # Also need to patch the cmd.migrate module which has already imported these
    monkeypatch.setattr(spack.cmd.migrate, "paths", paths)
    monkeypatch.setattr(spack.cmd.migrate, "paths_base", base_paths)

    # The backup location is now paths.dotspack_backup
    backup_location = pathlib.Path(paths.dotspack_backup)

    # Run migrate with --clear
    migrate("--clear")

    # Verify config files were copied
    assert verify_files_copied(backup_location, new_config, created)

    # Verify package repos were copied
    old_repos = backup_location / "package_repos"
    new_repos = new_state / "package_repos"
    assert verify_package_repos_copied(old_repos, new_repos, created)

    # Verify old location no longer exists
    assert not dotspack.exists()

    # Verify backup exists
    assert backup_location.exists()


def test_migrate_then_clear_replace(tmp_path, set_home, monkeypatch, mutable_config):
    """Test migrate, then migrate --clear --replace to clean up."""
    # Set up directories
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    # Set home BEFORE creating paths objects
    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()
    created = create_dotspack_files(dotspack)

    # Set expected new locations
    new_config = home / ".config" / "spack"
    new_state = home / ".local" / "state" / "spack"

    # Create fresh SpackPaths object and patch the module
    base_paths = SpackPathsBase(str(spack_root))
    paths = SpackPaths(base_paths)
    monkeypatch.setattr(spack.paths, "locations", paths)
    monkeypatch.setattr(spack.paths_base, "locations", base_paths)

    # Also need to patch the cmd.migrate module which has already imported these
    monkeypatch.setattr(spack.cmd.migrate, "paths", paths)
    monkeypatch.setattr(spack.cmd.migrate, "paths_base", base_paths)

    # Run migrate (without --clear)
    migrate()

    # Verify files were copied
    assert verify_files_copied(dotspack, new_config, created)
    old_repos = dotspack / "package_repos"
    new_repos = new_state / "package_repos"
    assert verify_package_repos_copied(old_repos, new_repos, created)

    # Verify old location still exists
    assert dotspack.exists()

    # Now run migrate --clear --replace (to remove existing files and clear ~/.spack)
    backup_location = pathlib.Path(paths.dotspack_backup)

    migrate("--clear", "--replace")

    # Verify old location is gone
    assert not dotspack.exists()

    # Verify backup exists with the original content
    assert backup_location.exists()
    for config_file in created["config_files"]:
        assert (backup_location / config_file).exists()


def test_migrate_then_clear_only(tmp_path, set_home, monkeypatch, mutable_config):
    """Test migrate, then migrate --clear-only to just remove ~/.spack."""
    # Set up directories
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    # Set home BEFORE creating paths objects
    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()
    created = create_dotspack_files(dotspack)

    # Set expected new locations
    new_config = home / ".config" / "spack"
    new_state = home / ".local" / "state" / "spack"

    # Create fresh SpackPaths object and patch the module
    base_paths = SpackPathsBase(str(spack_root))
    paths = SpackPaths(base_paths)
    monkeypatch.setattr(spack.paths, "locations", paths)
    monkeypatch.setattr(spack.paths_base, "locations", base_paths)

    # Also need to patch the cmd.migrate module which has already imported these
    monkeypatch.setattr(spack.cmd.migrate, "paths", paths)
    monkeypatch.setattr(spack.cmd.migrate, "paths_base", base_paths)

    # Run migrate (without --clear)
    migrate()

    # Verify files were copied
    assert verify_files_copied(dotspack, new_config, created)
    old_repos = dotspack / "package_repos"
    new_repos = new_state / "package_repos"
    assert verify_package_repos_copied(old_repos, new_repos, created)

    # Verify old location still exists
    assert dotspack.exists()

    # Now run migrate --clear-only (just move ~/.spack without re-migrating)
    backup_location = pathlib.Path(paths.dotspack_backup)

    migrate("--clear-only")

    # Verify old location is gone
    assert not dotspack.exists()

    # Verify backup exists with the original content
    assert backup_location.exists()
    for config_file in created["config_files"]:
        assert (backup_location / config_file).exists()

    # Verify new locations still have the files (weren't touched)
    assert verify_files_copied(backup_location, new_config, created)
    assert verify_package_repos_copied(backup_location / "package_repos", new_repos, created)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import pytest

import spack
import spack.cmd.migrate
import spack.main
import spack.paths
from spack.paths import SpackPaths

migrate = spack.main.SpackCommand("migrate")


@pytest.fixture
def migrate_setup(
    tmp_path, set_home, monkeypatch, clear_env_vars, modifies_spackpaths, mutable_config
):
    """Set up common test environment for migrate tests."""
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
    removes ~/.spack (moves it to $state_home/dotspack_backup)."""
    dotspack, created, new_config, paths = migrate_setup

    backup_loc = pathlib.Path(spack.cmd.migrate.backup_location())

    migrate("--clear")

    assert verify_files_copied(backup_loc, new_config, created)
    # --clear should remove old location (or rather, move it)
    assert not dotspack.exists()
    assert backup_loc.exists()


def test_migrate_restore(migrate_setup):
    """Test --restore: moves $state_home/dotspack_backup back to ~/.spack."""
    dotspack, created, new_config, paths = migrate_setup

    backup_loc = pathlib.Path(spack.cmd.migrate.backup_location())

    # First migrate with --clear to create the backup
    migrate("--clear")

    assert not dotspack.exists()
    assert backup_loc.exists()

    # Now restore
    migrate("--restore")

    # Should move backup back to original location
    assert dotspack.exists()
    assert not backup_loc.exists()

    # Verify original files are back
    for config_file in created["config_files"]:
        assert (dotspack / config_file).exists()


def test_migrate_with_relative_paths(
    tmp_path, set_home, monkeypatch, clear_env_vars, modifies_spackpaths, mutable_config
):
    """Test that relative paths in config files are absolutized (except in include sections)."""
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    set_home(str(home))

    # Create ~/.spack with test files
    dotspack = home / ".spack"
    dotspack.mkdir()

    # Create a subdirectory with a config file
    subdir = dotspack / "linux"
    subdir.mkdir()

    # Create a dummy file that paths can reference
    dummy_dir = dotspack / "my_packages"
    dummy_dir.mkdir()
    (dummy_dir / "dummy.py").write_text("# dummy")

    # Create config with relative paths
    config_yaml = dotspack / "config.yaml"
    config_yaml.write_text("""config:
  install_tree:
    root: my_packages
  source_cache: my_packages
""")

    # Create an include config with relative paths (should be kept relative)
    include_yaml = subdir / "packages.yaml"
    include_yaml.write_text("""include:
  - path: ../config.yaml
packages:
  all:
    compiler: [gcc]
""")

    new_config = home / ".config" / "spack"

    # Create fresh SpackPaths object and patch the module
    paths = SpackPaths(_prefix=str(spack_root))
    monkeypatch.setattr(spack.paths, "locations", paths)

    # Run migration
    migrate()

    # Check that files were migrated
    assert (new_config / "config.yaml").exists()
    assert (new_config / "linux" / "packages.yaml").exists()

    # Read the migrated config.yaml - relative paths should be absolutized
    import spack.util.spack_yaml as syaml

    with open(new_config / "config.yaml") as f:
        migrated_config = syaml.load(f)

    # The relative path 'my_packages' should now be absolute
    install_root = migrated_config["config"]["install_tree"]["root"]
    assert pathlib.Path(install_root).is_absolute()
    assert install_root == str(dotspack / "my_packages")

    # Read the migrated packages.yaml - include path should remain relative
    with open(new_config / "linux" / "packages.yaml") as f:
        migrated_include = syaml.load(f)

    # The include path should still be relative
    include_path = migrated_include["include"][0]["path"]
    assert not pathlib.Path(include_path).is_absolute()
    assert include_path == "../config.yaml"


def test_migrate_recursive_discovery(
    tmp_path, set_home, monkeypatch, clear_env_vars, modifies_spackpaths, mutable_config
):
    """Test that migrate finds config files recursively in subdirectories."""
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    set_home(str(home))

    # Create ~/.spack with nested structure
    dotspack = home / ".spack"
    dotspack.mkdir()

    # Create files at different levels
    (dotspack / "config.yaml").write_text("config:\n  build_jobs: 8\n")

    subdir1 = dotspack / "linux"
    subdir1.mkdir()
    (subdir1 / "packages.yaml").write_text("packages:\n  all:\n    compiler: [gcc]\n")

    subdir2 = subdir1 / "x86_64"
    subdir2.mkdir()
    (subdir2 / "compilers.yaml").write_text("compilers: []\n")

    new_config = home / ".config" / "spack"

    # Create fresh SpackPaths object and patch the module
    paths = SpackPaths(_prefix=str(spack_root))
    monkeypatch.setattr(spack.paths, "locations", paths)

    # Run migration
    migrate()

    # Check that all files were found and migrated, preserving directory structure
    assert (new_config / "config.yaml").exists()
    assert (new_config / "linux" / "packages.yaml").exists()
    assert (new_config / "linux" / "x86_64" / "compilers.yaml").exists()


def test_migrate_rewrites_absolute_include_paths(
    tmp_path, set_home, monkeypatch, clear_env_vars, modifies_spackpaths, mutable_config
):
    """Test that absolute include paths pointing to ~/.spack are rewritten to ~/.config/spack."""
    spack_root = tmp_path / "spack-root"
    spack_root.mkdir()
    home = tmp_path / "home"
    home.mkdir()

    set_home(str(home))

    # Create ~/.spack
    dotspack = home / ".spack"
    dotspack.mkdir()

    # Create a target config file
    subdir = dotspack / "linux"
    subdir.mkdir()
    (subdir / "packages.yaml").write_text("packages:\n  all:\n    compiler: [gcc]\n")

    # Create an include.yaml with absolute path pointing to ~/.spack
    absolute_include_path = str(subdir / "packages.yaml")
    include_yaml = dotspack / "include.yaml"
    include_yaml.write_text(f"""include:
  - path: {absolute_include_path}
""")

    new_config = home / ".config" / "spack"

    # Create fresh SpackPaths object and patch the module
    paths = SpackPaths(_prefix=str(spack_root))
    monkeypatch.setattr(spack.paths, "locations", paths)

    # Run migration
    migrate()

    # Check that files were migrated
    assert (new_config / "include.yaml").exists()
    assert (new_config / "linux" / "packages.yaml").exists()

    # Read the migrated include.yaml - absolute path should be rewritten
    import spack.util.spack_yaml as syaml

    with open(new_config / "include.yaml") as f:
        migrated_include = syaml.load(f)

    # The include path should now point to the new location
    rewritten_path = migrated_include["include"][0]["path"]
    assert rewritten_path == str(new_config / "linux" / "packages.yaml")
    # Should still be absolute
    assert pathlib.Path(rewritten_path).is_absolute()

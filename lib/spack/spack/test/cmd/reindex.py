# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import shutil

import spack.database
import spack.store
import spack.util.path
from spack.database import Database
from spack.enums import InstallRecordStatus
from spack.main import SpackCommand
from spack.store import Store

install = SpackCommand("install")
deprecate = SpackCommand("deprecate")
reindex = SpackCommand("reindex")


def test_reindex_basic(
    mock_packages, mock_archive, mock_fetch, temporary_store: Store, install_mockery
):
    install("--fake", "libelf@0.8.13")
    install("--fake", "libelf@0.8.12")
    all_installed = temporary_store.db.query()
    reindex()
    assert temporary_store.db.query() == all_installed


def _clear_db(store, tmp_path: pathlib.Path):
    empty_db = Database(str(tmp_path))
    with empty_db.write_transaction():
        pass
    shutil.rmtree(store.db.database_directory)
    shutil.copytree(empty_db.database_directory, store.db.database_directory)
    # force a re-read of the database
    assert len(store.db.query()) == 0


def test_reindex_db_deleted(
    mock_packages,
    mock_archive,
    mock_fetch,
    temporary_store: Store,
    install_mockery,
    tmp_path: pathlib.Path,
):
    install("--fake", "libelf@0.8.13")
    install("--fake", "libelf@0.8.12")
    all_installed = temporary_store.db.query()
    _clear_db(temporary_store, tmp_path)
    reindex()
    assert temporary_store.db.query() == all_installed


def test_reindex_with_deprecated_packages(
    mock_packages,
    mock_archive,
    mock_fetch,
    temporary_store: Store,
    install_mockery,
    tmp_path: pathlib.Path,
):
    install("--fake", "libelf@0.8.13")
    install("--fake", "libelf@0.8.12")

    deprecate("-y", "libelf@0.8.12", "libelf@0.8.13")

    db = temporary_store.db

    all_installed = db.query(installed=InstallRecordStatus.ANY)
    non_deprecated = db.query(installed=True)

    _clear_db(temporary_store, tmp_path)

    reindex()

    assert db.query(installed=InstallRecordStatus.ANY) == all_installed
    assert db.query(installed=True) == non_deprecated

    old_libelf = db.query_local_by_spec_hash(
        db.query_local("libelf@0.8.12", installed=InstallRecordStatus.ANY)[0].dag_hash()
    )
    new_libelf = db.query_local_by_spec_hash(
        db.query_local("libelf@0.8.13", installed=True)[0].dag_hash()
    )
    assert old_libelf is not None and new_libelf is not None
    assert old_libelf.deprecated_for == new_libelf.spec.dag_hash()
    assert new_libelf.deprecated_for is None
    assert new_libelf.ref_count == 1


def _padded_store(tmp_path: pathlib.Path, monkeypatch, *, pre_migration: bool) -> Store:
    """Create a padded/unpadded root pair and point spack.store.STORE at it.

    If `pre_migration` is True, the DB is placed at the padded root (old layout), as if
    created before the move to the unpadded root. Otherwise the DB ends up wherever a
    fresh Store puts it (the unpadded root).
    """
    unpadded = str(tmp_path / "opt" / "spack")
    padded = spack.util.path.add_padding(unpadded, len(unpadded) + 64)
    assert padded != unpadded

    store = Store(root=padded, unpadded_root=unpadded, projections={"all": "{name}/{version}"})

    if pre_migration:
        old_db_path = pathlib.Path(store.root) / spack.database._DB_DIRNAME
        old_db_path.mkdir(parents=True, exist_ok=True)
        store.metadata_root = store.root
        store.db = spack.database.Database(store.root, layout=store.layout)

    monkeypatch.setattr(spack.store, "STORE", store)
    return store


def test_reindex_migrates_db_from_padded_to_unpadded_root(
    mock_packages, mock_archive, mock_fetch, install_mockery, tmp_path: pathlib.Path, monkeypatch
):
    """Test that reindex migrates database from padded root to unpadded root."""
    store = _padded_store(tmp_path, monkeypatch, pre_migration=True)
    old_db_path = pathlib.Path(store.root) / spack.database._DB_DIRNAME
    new_db_path = pathlib.Path(store.unpadded_root) / spack.database._DB_DIRNAME

    install("--fake", "libelf@0.8.13")
    install("--fake", "libelf@0.8.12")
    all_installed = store.db.query()
    assert old_db_path.exists()
    assert not new_db_path.exists()

    reindex()

    assert not old_db_path.exists()
    assert new_db_path.exists()
    assert spack.store.STORE.db.query() == all_installed
    assert spack.store.STORE.metadata_root == spack.store.STORE.unpadded_root


def test_reindex_no_migration_when_already_migrated(
    mock_packages, mock_archive, mock_fetch, install_mockery, tmp_path: pathlib.Path, monkeypatch
):
    """Test that reindex doesn't migrate when DB already in new location."""
    store = _padded_store(tmp_path, monkeypatch, pre_migration=False)
    old_db_path = pathlib.Path(store.root) / spack.database._DB_DIRNAME
    new_db_path = pathlib.Path(store.unpadded_root) / spack.database._DB_DIRNAME

    install("--fake", "libelf@0.8.13")
    install("--fake", "libelf@0.8.12")
    all_installed = store.db.query()
    assert new_db_path.exists()
    assert not old_db_path.exists()

    reindex()

    assert new_db_path.exists()
    assert not old_db_path.exists()
    assert store.db.query() == all_installed
    assert store.metadata_root == store.unpadded_root


def test_reindex_migration_failure_restores_old_db(
    mock_packages, mock_archive, mock_fetch, install_mockery, tmp_path: pathlib.Path, monkeypatch
):
    """Test that a failed migration moves the old database back to the padded root."""
    store = _padded_store(tmp_path, monkeypatch, pre_migration=True)
    old_db_path = pathlib.Path(store.root) / spack.database._DB_DIRNAME

    install("--fake", "libelf@0.8.13")
    all_installed = store.db.query()

    def _fail_reindex(self):
        raise RuntimeError("reindex failed")

    monkeypatch.setattr(Store, "reindex", _fail_reindex)

    reindex(fail_on_error=False)
    assert isinstance(reindex.error, RuntimeError)
    assert str(reindex.error) == "reindex failed"

    old_db_temp = pathlib.Path(str(old_db_path) + ".old")
    assert old_db_path.exists()
    assert not old_db_temp.exists()
    assert (old_db_path / spack.database.INDEX_JSON_FILE).exists()

    restored = Store(
        root=store.root, unpadded_root=store.unpadded_root, projections=store.projections
    )
    assert restored.metadata_root == restored.root
    assert restored.db.query() == all_installed


def test_reindex_without_existing_index(
    mock_packages, mock_archive, mock_fetch, temporary_store: Store, install_mockery
):
    """Test that reindex works and skips the backup when there is no index file yet."""
    install("--fake", "libelf@0.8.13")
    all_installed = temporary_store.db.query()

    index_path = temporary_store.db._index_path
    index_path.unlink()

    output = reindex()

    assert "Created a backup copy" not in output
    assert "If you need to restore" not in output
    assert not pathlib.Path(f"{index_path}.bkp").exists()
    assert index_path.exists()
    assert temporary_store.db.query() == all_installed

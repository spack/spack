# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import shutil

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

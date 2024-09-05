# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import shutil

import spack.store
from spack.database import Database
from spack.main import SpackCommand

install = SpackCommand("install")
deprecate = SpackCommand("deprecate")
reindex = SpackCommand("reindex")


def test_reindex_basic(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.STORE.db.query()

    reindex()

    assert spack.store.STORE.db.query() == all_installed


def _clear_db(tmp_path):
    empty_db = Database(str(tmp_path))
    with empty_db.write_transaction():
        pass
    shutil.rmtree(spack.store.STORE.db.database_directory)
    shutil.copytree(empty_db.database_directory, spack.store.STORE.db.database_directory)
    # force a re-read of the database
    assert len(spack.store.STORE.db.query()) == 0


def test_reindex_db_deleted(mock_packages, mock_archive, mock_fetch, install_mockery, tmp_path):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.STORE.db.query()

    _clear_db(tmp_path)

    reindex()

    assert spack.store.STORE.db.query() == all_installed


def test_reindex_with_deprecated_packages(
    mock_packages, mock_archive, mock_fetch, install_mockery, tmp_path
):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    deprecate("-y", "libelf@0.8.12", "libelf@0.8.13")

    all_installed = spack.store.STORE.db.query(installed=any)
    non_deprecated = spack.store.STORE.db.query(installed=True)

    _clear_db(tmp_path)

    reindex()

    assert spack.store.STORE.db.query(installed=any) == all_installed
    assert spack.store.STORE.db.query(installed=True) == non_deprecated

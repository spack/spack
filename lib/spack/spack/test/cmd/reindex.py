# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import spack.store
from spack.main import SpackCommand

install = SpackCommand("install")
deprecate = SpackCommand("deprecate")
reindex = SpackCommand("reindex")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_reindex_basic(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.STORE.db.query()

    reindex()

    assert spack.store.STORE.db.query() == all_installed


def test_reindex_db_deleted(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.STORE.db.query()

    os.remove(spack.store.STORE.db._index_path)
    reindex()

    assert spack.store.STORE.db.query() == all_installed


def test_reindex_with_deprecated_packages(
    mock_packages, mock_archive, mock_fetch, install_mockery
):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    deprecate("-y", "libelf@0.8.12", "libelf@0.8.13")

    all_installed = spack.store.STORE.db.query(installed=any)
    non_deprecated = spack.store.STORE.db.query(installed=True)

    os.remove(spack.store.STORE.db._index_path)
    reindex()

    assert spack.store.STORE.db.query(installed=any) == all_installed
    assert spack.store.STORE.db.query(installed=True) == non_deprecated

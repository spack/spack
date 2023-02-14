# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import sys

import pytest

import spack.store
from spack.main import SpackCommand

install = SpackCommand("install")
deprecate = SpackCommand("deprecate")
reindex = SpackCommand("reindex")

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


def test_reindex_basic(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.db.query()

    reindex()

    assert spack.store.db.query() == all_installed


def test_reindex_db_deleted(mock_packages, mock_archive, mock_fetch, install_mockery):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    all_installed = spack.store.db.query()

    os.remove(spack.store.db._index_path)
    reindex()

    assert spack.store.db.query() == all_installed


def test_reindex_with_deprecated_packages(
    mock_packages, mock_archive, mock_fetch, install_mockery
):
    install("libelf@0.8.13")
    install("libelf@0.8.12")

    deprecate("-y", "libelf@0.8.12", "libelf@0.8.13")

    all_installed = spack.store.db.query(installed=any)
    non_deprecated = spack.store.db.query(installed=True)

    os.remove(spack.store.db._index_path)
    reindex()

    assert spack.store.db.query(installed=any) == all_installed
    assert spack.store.db.query(installed=True) == non_deprecated

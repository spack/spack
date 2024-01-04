# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil
from itertools import product

import pytest

import llnl.url
from llnl.util.filesystem import working_dir

from spack.paths import spack_root
from spack.util import compression as scomp
from spack.util.executable import CommandNotFoundError

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data", "compression")

ext_archive = {}
[
    ext_archive.update({ext: ".".join(["Foo", ext])})
    for ext in llnl.url.ALLOWED_ARCHIVE_TYPES
    if "TAR" not in ext
]
# Spack does not use Python native handling for tarballs or zip
# Don't test tarballs or zip in native test
native_archive_list = [key for key in ext_archive.keys() if "tar" not in key and "zip" not in key]


def support_stub():
    return False


@pytest.fixture
def compr_support_check(monkeypatch):
    monkeypatch.setattr(scomp, "is_lzma_supported", support_stub)
    monkeypatch.setattr(scomp, "is_gzip_supported", support_stub)
    monkeypatch.setattr(scomp, "is_bz2_supported", support_stub)


@pytest.fixture
def archive_file_and_extension(tmpdir_factory, request):
    """Copy example archive to temp directory into an extension-less file for test"""
    archive_file_stub = os.path.join(datadir, "Foo")
    extension, add_extension = request.param
    tmpdir = tmpdir_factory.mktemp("compression")
    tmp_archive_file = os.path.join(
        str(tmpdir), "Foo" + (("." + extension) if add_extension else "")
    )
    shutil.copy(archive_file_stub + "." + extension, tmp_archive_file)
    return (tmp_archive_file, extension)


@pytest.mark.parametrize(
    "archive_file_and_extension", product(native_archive_list, [True, False]), indirect=True
)
def test_native_unpacking(tmpdir_factory, archive_file_and_extension):
    archive_file, extension = archive_file_and_extension
    util = scomp.decompressor_for(archive_file, extension)
    tmpdir = tmpdir_factory.mktemp("comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        files = os.listdir(os.getcwd())
        assert len(files) == 1
        with open(files[0], "r") as f:
            contents = f.read()
        assert "TEST" in contents


@pytest.mark.not_on_windows("Only Python unpacking available on Windows")
@pytest.mark.parametrize(
    "archive_file_and_extension", [(ext, True) for ext in ext_archive.keys()], indirect=True
)
def test_system_unpacking(tmpdir_factory, archive_file_and_extension, compr_support_check):
    # actually run test
    archive_file, _ = archive_file_and_extension
    util = scomp.decompressor_for(archive_file)
    tmpdir = tmpdir_factory.mktemp("system_comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        files = os.listdir(os.getcwd())
        assert len(files) == 1
        with open(files[0], "r") as f:
            contents = f.read()
        assert "TEST" in contents


def test_unallowed_extension():
    # use a cxx file as python files included for the test
    # are picked up by the linter and break style checks
    bad_ext_archive = "Foo.cxx"
    with pytest.raises(CommandNotFoundError):
        scomp.decompressor_for(bad_ext_archive)

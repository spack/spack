# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

import pytest

from llnl.util.filesystem import working_dir

from spack.paths import spack_root
from spack.util import compression as scomp
from spack.util.executable import CommandNotFoundError

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data", "compression")

ext_archive = {}
[
    ext_archive.update({ext: ".".join(["Foo", ext])})
    for ext in scomp.ALLOWED_ARCHIVE_TYPES
    if "TAR" not in ext
]


def support_stub():
    return False


@pytest.fixture
def compr_support_check(monkeypatch):
    monkeypatch.setattr(scomp, "lzma_support", support_stub)
    monkeypatch.setattr(scomp, "tar_support", support_stub)
    monkeypatch.setattr(scomp, "gzip_support", support_stub)
    monkeypatch.setattr(scomp, "bz2_support", support_stub)


@pytest.fixture
def archive_file(tmpdir_factory, request):
    """Copy example archive to temp directory for test"""
    archive_file_stub = os.path.join(datadir, "Foo")
    extension = request.param
    tmpdir = tmpdir_factory.mktemp("compression")
    shutil.copy(archive_file_stub + "." + extension, str(tmpdir))
    return os.path.join(str(tmpdir), "Foo.%s" % extension)


@pytest.mark.parametrize("archive_file", ext_archive.keys(), indirect=True)
def test_native_unpacking(tmpdir_factory, archive_file):
    extension = scomp.extension(archive_file)
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


@pytest.mark.parametrize("archive_file", ext_archive.keys(), indirect=True)
def test_system_unpacking(tmpdir_factory, archive_file, compr_support_check):
    extension = scomp.extension(archive_file)
    # actually run test
    util = scomp.decompressor_for(archive_file, extension)
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
    bad_ext_archive = "Foo.py"
    with pytest.raises(CommandNotFoundError):
        scomp.decompressor_for(bad_ext_archive, "py")


@pytest.mark.parametrize("archive", ext_archive.values())
def test_get_extension(archive):
    ext = scomp.extension(archive)
    assert ext_archive[ext] == archive


def test_get_bad_extension():
    archive = "Foo.py"
    ext = scomp.extension(archive)
    assert ext is None


@pytest.mark.parametrize("path", ext_archive.values())
def test_allowed_archvie(path):
    assert scomp.allowed_archive(path)

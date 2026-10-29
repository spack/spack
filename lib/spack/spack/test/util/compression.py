# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import bz2
import gzip
import io
import lzma
import os
import pathlib
import shutil
import tarfile
from itertools import product

import pytest

import spack.util.url
from spack.paths import spack_root
from spack.util import compression
from spack.util.executable import CommandNotFoundError
from spack.util.filesystem import working_dir

datadir = os.path.join(spack_root, "lib", "spack", "spack", "test", "data", "compression")

ext_archive = {
    ext: f"Foo.{ext}" for ext in spack.util.url.ALLOWED_ARCHIVE_TYPES if "TAR" not in ext
}
# Spack does not use Python native handling for tarballs or zip
# Don't test tarballs or zip in native test
native_archive_list = [
    key for key in ext_archive.keys() if "tar" not in key and "zip" not in key and "whl" not in key
]


@pytest.fixture
def compr_support_check(monkeypatch):
    monkeypatch.setattr(compression, "LZMA_SUPPORTED", False)
    monkeypatch.setattr(compression, "GZIP_SUPPORTED", False)
    monkeypatch.setattr(compression, "BZ2_SUPPORTED", False)


@pytest.fixture
def archive_file_and_extension(tmp_path_factory: pytest.TempPathFactory, request):
    """Copy example archive to temp directory into an extension-less file for test"""
    archive_file_stub = os.path.join(datadir, "Foo")
    extension, add_extension = request.param
    tmpdir = tmp_path_factory.mktemp("compression")
    tmp_archive_file = os.path.join(
        str(tmpdir), "Foo" + (("." + extension) if add_extension else "")
    )
    shutil.copy(archive_file_stub + "." + extension, tmp_archive_file)
    return (tmp_archive_file, extension)


@pytest.mark.parametrize(
    "archive_file_and_extension", product(native_archive_list, [True, False]), indirect=True
)
def test_native_unpacking(tmp_path_factory: pytest.TempPathFactory, archive_file_and_extension):
    archive_file, extension = archive_file_and_extension
    util = compression.decompressor_for(archive_file, extension)
    tmpdir = tmp_path_factory.mktemp("comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        files = os.listdir(os.getcwd())
        assert len(files) == 1
        with open(files[0], "r", encoding="utf-8") as f:
            contents = f.read()
        assert "TEST" in contents


@pytest.mark.not_on_windows("Only Python unpacking available on Windows")
@pytest.mark.parametrize(
    "archive_file_and_extension",
    [(ext, True) for ext in ext_archive.keys() if "whl" not in ext],
    indirect=True,
)
def test_system_unpacking(
    tmp_path_factory: pytest.TempPathFactory, archive_file_and_extension, compr_support_check
):
    # actually run test
    archive_file, _ = archive_file_and_extension
    util = compression.decompressor_for(archive_file)
    tmpdir = tmp_path_factory.mktemp("system_comp_test")
    with working_dir(str(tmpdir)):
        assert not os.listdir(os.getcwd())
        util(archive_file)
        files = os.listdir(os.getcwd())
        assert len(files) == 1
        with open(files[0], "r", encoding="utf-8") as f:
            contents = f.read()
        assert "TEST" in contents


def test_unallowed_extension():
    # use a cxx file as python files included for the test
    # are picked up by the linter and break style checks
    bad_ext_archive = "Foo.cxx"
    with pytest.raises(CommandNotFoundError):
        compression.decompressor_for(bad_ext_archive)


@pytest.mark.parametrize("ext", ["gz", "bz2", "xz"])
def test_file_type_check_does_not_advance_stream(tmp_path: pathlib.Path, ext):
    # Create a tarball compressed with the given format
    path = str(tmp_path / "compressed_tarball")

    try:
        if ext == "gz":
            tar = tarfile.open(path, "w:gz")
        elif ext == "bz2":
            tar = tarfile.open(path, "w:bz2")
        elif ext == "xz":
            tar = tarfile.open(path, "w:xz")
        else:
            assert False, f"Unsupported extension: {ext}"
    except tarfile.CompressionError:
        pytest.skip(f"Cannot create tar.{ext} files")

    with tar:
        tar.addfile(tarfile.TarInfo("test.txt"), fileobj=io.BytesIO(b"test"))

    # Classify the file from its magic bytes, and check that the stream is not advanced
    with open(path, "rb") as f:
        computed_ext = compression.extension_from_magic_numbers_by_stream(f, decompress=False)
        assert computed_ext == ext
        assert f.tell() == 0
        computed_ext = compression.extension_from_magic_numbers_by_stream(f, decompress=True)
        assert computed_ext == f"tar.{ext}"
        assert f.tell() == 0


def _tar(*names: str) -> bytes:
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for name in names:
            info = tarfile.TarInfo(name)
            info.size = 2
            tar.addfile(info, io.BytesIO(b"a\n"))
    return out.getvalue()


@pytest.mark.parametrize("name", sorted(os.listdir(datadir)))
def test_validate_tarball_valid(tmp_path, name):
    """Valid tarballs pass, and other files are not checked."""
    shutil.copy(os.path.join(datadir, name), tmp_path)
    compression.validate_tarball(str(tmp_path / name))
    assert os.listdir(tmp_path) == [name]


@pytest.mark.parametrize(
    "ext,compress,error",
    [
        # A second archive after the first is extracted by some implementations, not others
        ("tar", lambda data: data + _tar("pkg/b"), "end-of-archive marker"),
        ("tar.gz", lambda data: gzip.compress(data + _tar("pkg/b")), "end-of-archive marker"),
        ("tar.bz2", lambda data: bz2.compress(data + _tar("pkg/b")), "end-of-archive marker"),
        ("tar.xz", lambda data: lzma.compress(data + _tar("pkg/b")), "end-of-archive marker"),
        ("tar.gz", lambda data: gzip.compress(data)[:-4], "truncated"),
    ],
)
def test_validate_tarball_invalid(tmp_path, ext, compress, error):
    path = tmp_path / f"pkg.{ext}"
    path.write_bytes(compress(_tar("pkg/a")))
    with pytest.raises(compression.InvalidTarballError, match=error):
        compression.validate_tarball(str(path))

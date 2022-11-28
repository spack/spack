# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import hashlib
import os
import os.path
import sys

import pytest

import spack.binary_distribution
import spack.main
import spack.spec
import spack.util.url

install = spack.main.SpackCommand("install")

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


def test_build_tarball_overwrite(install_mockery, mock_fetch, monkeypatch, tmpdir):

    with tmpdir.as_cwd():
        spec = spack.spec.Spec("trivial-install-test-package").concretized()
        install(str(spec))

        # Runs fine the first time, throws the second time
        out_url = spack.util.url.path_to_file_url(str(tmpdir))
        spack.binary_distribution._build_tarball(spec, out_url, unsigned=True)
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution._build_tarball(spec, out_url, unsigned=True)

        # Should work fine with force=True
        spack.binary_distribution._build_tarball(spec, out_url, force=True, unsigned=True)

        # Remove the tarball and try again.
        # This must *also* throw, because of the existing .spec.json file
        os.remove(
            os.path.join(
                spack.binary_distribution.build_cache_prefix("."),
                spack.binary_distribution.tarball_directory_name(spec),
                spack.binary_distribution.tarball_name(spec, ".spack"),
            )
        )

        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution._build_tarball(spec, out_url, unsigned=True)


def test_binary_cache_single(tmpdir):
    test_file = tmpdir.join("test.txt")
    test_url = "file://" + test_file.strpath
    cache_dir = tmpdir.join("cache").strpath

    def save(contents):
        with test_file.open("w") as f:
            f.write(contents)
        return spack.util.crypto.checksum(hashlib.sha256, test_file.strpath)

    with spack.config.override("config:local_binary_cache", cache_dir):
        lbc = spack.binary_distribution.local_binary_cache

        checksum = save("test data")

        # Local paths should never be cached unless force is given
        cached_path, fetched = lbc.get(test_url, "blah")
        assert cached_path is None and fetched is None

        # First call to get should cache the result, second should use the cached result
        cached_path, fetched = lbc.get(test_url, checksum, force=True)
        assert fetched
        assert cached_path[: len(cache_dir) + 1] == cache_dir + "/"

        cached_path2, fetched = lbc.get(test_url, checksum, force=True)
        assert cached_path2 == cached_path
        assert not fetched

        checksum = save("other test data")

        # If the URL didn't change but the hash did, we should re-fetch
        cached_path3, fetched = lbc.get(test_url, checksum, force=True)
        assert cached_path3 == cached_path
        assert fetched

        # If the checksum is outright wrong, we should get a NoChecksumException
        with pytest.raises(spack.binary_distribution.NoChecksumException):
            lbc.get(test_url, "00" * 16, force=True)

        # Destruction should not error
        lbc.destroy()


def test_binary_cache_multiple(tmpdir):
    data_dirs = (tmpdir.join("data0"), tmpdir.join("data1"))
    test_files = tuple(ddir.join("test.txt") for ddir in data_dirs)
    test_urls = tuple("file://" + fn.strpath for fn in test_files)
    cache_dirs = (tmpdir.join("cache0").strpath, tmpdir.join("cache1").strpath)

    for ddir in data_dirs:
        ddir.mkdir()

    def save(idx, contents):
        with test_files[idx].open("w") as f:
            f.write(contents)
        return spack.util.crypto.checksum(hashlib.sha256, test_files[idx].strpath)

    caches = [
        {"prefixes": ["file://" + data_dirs[0].strpath], "root": cache_dirs[0]},
        {"root": cache_dirs[1]},
    ]

    with spack.config.override("config:local_binary_cache", caches):
        lbc = spack.binary_distribution.local_binary_cache

        checksums = (save(0, "test data"), save(1, "other test data"))

        # Data should land in the appropriate root based on prefix matching
        cached_path, fetched = lbc.get(test_urls[0], checksums[0], force=True)
        assert fetched
        assert cached_path[: len(cache_dirs[0]) + 1] == cache_dirs[0] + "/"

        cached_path, fetched = lbc.get(test_urls[1], checksums[1], force=True)
        assert fetched
        assert cached_path[: len(cache_dirs[1]) + 1] == cache_dirs[1] + "/"

        # Destruction should not error
        lbc.destroy()


def test_binary_cache_fallthrough(tmpdir):
    data_dirs = (tmpdir.join("data0"), tmpdir.join("data1"))
    test_files = tuple(ddir.join("test.txt") for ddir in data_dirs)
    test_urls = tuple("file://" + fn.strpath for fn in test_files)
    cache_dirs = (tmpdir.join("cache0").strpath, tmpdir.join("cache1").strpath)

    for ddir in data_dirs:
        ddir.mkdir()

    def save(idx, contents):
        with test_files[idx].open("w") as f:
            f.write(contents)
        return spack.util.crypto.checksum(hashlib.sha256, test_files[idx].strpath)

    caches = [
        {"prefixes": ["file://" + data_dirs[0].strpath], "root": cache_dirs[0]},
    ]

    with spack.config.override("config:local_binary_cache", caches):
        lbc = spack.binary_distribution.local_binary_cache

        checksums = (save(0, "test data"), save(1, "other test data"))

        # URLs with a matching prefix should be cached
        cached_path, fetched = lbc.get(test_urls[0], checksums[0], force=True)
        assert fetched
        assert cached_path[: len(cache_dirs[0]) + 1] == cache_dirs[0] + "/"

        # URLs without should not be
        cached_path, fetched = lbc.get(test_urls[1], checksums[1], force=True)
        assert cached_path is None and fetched is None

        # Destruction should not error
        lbc.destroy()

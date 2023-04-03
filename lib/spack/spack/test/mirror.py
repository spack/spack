# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import sys

import pytest

from llnl.util.filesystem import resolve_link_target_relative_to_the_link

import spack.mirror
import spack.repo
import spack.util.executable
import spack.util.spack_json as sjson
import spack.util.url as url_util
from spack.spec import Spec
from spack.stage import Stage
from spack.util.executable import which
from spack.util.spack_yaml import SpackYAMLError

pytestmark = [
    pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows"),
    pytest.mark.usefixtures("mutable_config", "mutable_mock_repo"),
]

# paths in repos that shouldn't be in the mirror tarballs.
exclude = [".hg", ".git", ".svn"]


repos = {}


def set_up_package(name, repository, url_attr):
    """Set up a mock package to be mirrored.
    Each package needs us to:

    1. Set up a mock repo/archive to fetch from.
    2. Point the package's version args at that repo.
    """
    # Set up packages to point at mock repos.
    s = Spec(name).concretized()
    repos[name] = repository

    # change the fetch args of the first (only) version.
    assert len(s.package.versions) == 1

    v = next(iter(s.package.versions))
    s.package.versions[v][url_attr] = repository.url


def check_mirror():
    with Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")
        # register mirror with spack config
        mirrors = {"spack-mirror-test": url_util.path_to_file_url(mirror_root)}
        with spack.config.override("mirrors", mirrors):
            with spack.config.override("config:checksum", False):
                specs = [Spec(x).concretized() for x in repos]
                spack.mirror.create(mirror_root, specs)

            # Stage directory exists
            assert os.path.isdir(mirror_root)

            for spec in specs:
                fetcher = spec.package.fetcher[0]
                per_package_ref = os.path.join(spec.name, "-".join([spec.name, str(spec.version)]))
                mirror_paths = spack.mirror.mirror_archive_paths(fetcher, per_package_ref)
                expected_path = os.path.join(mirror_root, mirror_paths.storage_path)
                assert os.path.exists(expected_path)

            # Now try to fetch each package.
            for name, mock_repo in repos.items():
                spec = Spec(name).concretized()
                pkg = spec.package

                with spack.config.override("config:checksum", False):
                    with pkg.stage:
                        pkg.do_stage(mirror_only=True)

                        # Compare the original repo with the expanded archive
                        original_path = mock_repo.path
                        if "svn" in name:
                            # have to check out the svn repo to compare.
                            original_path = os.path.join(mock_repo.path, "checked_out")

                            svn = which("svn", required=True)
                            svn("checkout", mock_repo.url, original_path)

                        dcmp = filecmp.dircmp(original_path, pkg.stage.source_path)

                        # make sure there are no new files in the expanded
                        # tarball
                        assert not dcmp.right_only
                        # and that all original files are present.
                        assert all(left in exclude for left in dcmp.left_only)


def test_url_mirror(mock_archive):
    set_up_package("trivial-install-test-package", mock_archive, "url")
    check_mirror()
    repos.clear()


def test_git_mirror(git, mock_git_repository):
    set_up_package("git-test", mock_git_repository, "git")
    check_mirror()
    repos.clear()


def test_svn_mirror(mock_svn_repository):
    set_up_package("svn-test", mock_svn_repository, "svn")
    check_mirror()
    repos.clear()


def test_hg_mirror(mock_hg_repository):
    set_up_package("hg-test", mock_hg_repository, "hg")
    check_mirror()
    repos.clear()


def test_all_mirror(mock_git_repository, mock_svn_repository, mock_hg_repository, mock_archive):
    set_up_package("git-test", mock_git_repository, "git")
    set_up_package("svn-test", mock_svn_repository, "svn")
    set_up_package("hg-test", mock_hg_repository, "hg")
    set_up_package("trivial-install-test-package", mock_archive, "url")
    check_mirror()
    repos.clear()


@pytest.mark.parametrize(
    "mirror", [spack.mirror.Mirror("https://example.com/fetch", "https://example.com/push")]
)
def test_roundtrip_mirror(mirror):
    mirror_yaml = mirror.to_yaml()
    assert spack.mirror.Mirror.from_yaml(mirror_yaml) == mirror
    mirror_json = mirror.to_json()
    assert spack.mirror.Mirror.from_json(mirror_json) == mirror


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_mirror(invalid_yaml):
    with pytest.raises(SpackYAMLError) as e:
        spack.mirror.Mirror.from_yaml(invalid_yaml)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing YAML mirror:")
    assert invalid_yaml in exc_msg


@pytest.mark.parametrize("invalid_json, error_message", [("{13:", "Expecting property name")])
def test_invalid_json_mirror(invalid_json, error_message):
    with pytest.raises(sjson.SpackJSONError) as e:
        spack.mirror.Mirror.from_json(invalid_json)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing JSON mirror:")
    assert error_message in exc_msg


@pytest.mark.parametrize(
    "mirror_collection",
    [
        spack.mirror.MirrorCollection(
            mirrors={
                "example-mirror": spack.mirror.Mirror(
                    "https://example.com/fetch", "https://example.com/push"
                ).to_dict()
            }
        )
    ],
)
def test_roundtrip_mirror_collection(mirror_collection):
    mirror_collection_yaml = mirror_collection.to_yaml()
    assert spack.mirror.MirrorCollection.from_yaml(mirror_collection_yaml) == mirror_collection
    mirror_collection_json = mirror_collection.to_json()
    assert spack.mirror.MirrorCollection.from_json(mirror_collection_json) == mirror_collection


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_mirror_collection(invalid_yaml):
    with pytest.raises(SpackYAMLError) as e:
        spack.mirror.MirrorCollection.from_yaml(invalid_yaml)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing YAML mirror collection:")
    assert invalid_yaml in exc_msg


@pytest.mark.parametrize("invalid_json, error_message", [("{13:", "Expecting property name")])
def test_invalid_json_mirror_collection(invalid_json, error_message):
    with pytest.raises(sjson.SpackJSONError) as e:
        spack.mirror.MirrorCollection.from_json(invalid_json)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing JSON mirror collection:")
    assert error_message in exc_msg


def test_mirror_archive_paths_no_version(mock_packages, config, mock_archive):
    spec = Spec("trivial-install-test-package@nonexistingversion").concretized()
    fetcher = spack.fetch_strategy.URLFetchStrategy(mock_archive.url)
    spack.mirror.mirror_archive_paths(fetcher, "per-package-ref", spec)


def test_mirror_with_url_patches(mock_packages, config, monkeypatch):
    spec = Spec("patch-several-dependencies")
    spec.concretize()

    files_cached_in_mirror = set()

    def record_store(_class, fetcher, relative_dst, cosmetic_path=None):
        files_cached_in_mirror.add(os.path.basename(relative_dst))

    def successful_fetch(_class):
        with open(_class.stage.save_filename, "w"):
            pass

    def successful_expand(_class):
        expanded_path = os.path.join(_class.stage.path, spack.stage._source_path_subdir)
        os.mkdir(expanded_path)
        with open(os.path.join(expanded_path, "test.patch"), "w"):
            pass

    def successful_apply(*args, **kwargs):
        pass

    with Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")

        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "fetch", successful_fetch)
        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "expand", successful_expand)
        monkeypatch.setattr(spack.patch, "apply_patch", successful_apply)
        monkeypatch.setattr(spack.caches.MirrorCache, "store", record_store)

        with spack.config.override("config:checksum", False):
            spack.mirror.create(mirror_root, list(spec.traverse()))

        assert not (
            set(
                [
                    "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
                    "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd.gz",
                ]
            )
            - files_cached_in_mirror
        )


class MockFetcher(object):
    """Mock fetcher object which implements the necessary functionality for
    testing MirrorCache
    """

    @staticmethod
    def archive(dst):
        with open(dst, "w"):
            pass


@pytest.mark.regression("14067")
def test_mirror_cache_symlinks(tmpdir):
    """Confirm that the cosmetic symlink created in the mirror cache (which may
    be relative) targets the storage path correctly.
    """
    cosmetic_path = "zlib/zlib-1.2.11.tar.gz"
    global_path = "_source-cache/archive/c3/c3e5.tar.gz"
    cache = spack.caches.MirrorCache(str(tmpdir), False)
    reference = spack.mirror.MirrorReference(cosmetic_path, global_path)

    cache.store(MockFetcher(), reference.storage_path)
    cache.symlink(reference)

    link_target = resolve_link_target_relative_to_the_link(
        os.path.join(cache.root, reference.cosmetic_path)
    )
    assert os.path.exists(link_target)
    assert os.path.normpath(link_target) == os.path.join(cache.root, reference.storage_path)


@pytest.mark.regression("31627")
@pytest.mark.parametrize(
    "specs,expected_specs",
    [
        (["a"], ["a@1.0", "a@2.0"]),
        (["a", "brillig"], ["a@1.0", "a@2.0", "brillig@1.0.0", "brillig@2.0.0"]),
    ],
)
def test_get_all_versions(specs, expected_specs):
    specs = [Spec(s) for s in specs]
    output_list = spack.mirror.get_all_versions(specs)
    output_list = [str(x) for x in output_list]
    # Compare sets since order is not important
    assert set(output_list) == set(expected_specs)

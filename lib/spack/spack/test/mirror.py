# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import pathlib

import pytest

import spack.caches
import spack.cmd.mirror
import spack.concretize
import spack.config
import spack.fetch_strategy
import spack.mirrors.layout
import spack.mirrors.mirror
import spack.mirrors.utils
import spack.patch
import spack.stage
import spack.util.url as url_util
from spack.cmd.common.arguments import mirror_name_or_url
from spack.spec import Spec
from spack.util.executable import which
from spack.util.filesystem import resolve_link_target_relative_to_the_link, working_dir
from spack.util.spack_yaml import SpackYAMLError

pytestmark = [pytest.mark.usefixtures("mutable_config", "mutable_mock_repo")]

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
    s = spack.concretize.concretize_one(name)
    repos[name] = repository

    # change the fetch args of the first (only) version.
    assert len(s.package.versions) == 1

    v = next(iter(s.package.versions))
    s.package.versions[v][url_attr] = repository.url


def check_mirror():
    with spack.stage.Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")
        # register mirror with spack config
        mirrors = {"spack-mirror-test": url_util.path_to_file_url(mirror_root)}
        with spack.config.override("mirrors", mirrors):
            with spack.config.override("config:checksum", False):
                specs = [spack.concretize.concretize_one(x) for x in repos]
                spack.cmd.mirror.create(mirror_root, specs)

            # Stage directory exists
            assert os.path.isdir(mirror_root)

            for spec in specs:
                fetcher = spec.package.fetcher
                per_package_ref = os.path.join(spec.name, "-".join([spec.name, str(spec.version)]))
                mirror_layout = spack.mirrors.layout.default_mirror_layout(
                    fetcher, per_package_ref
                )
                expected_path = os.path.join(mirror_root, mirror_layout.path)
                assert os.path.exists(expected_path)

            # Now try to fetch each package.
            for name, mock_repo in repos.items():
                spec = spack.concretize.concretize_one(name)
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
    "mirror",
    [
        spack.mirrors.mirror.Mirror(
            {"fetch": "https://example.com/fetch", "push": "https://example.com/push"}
        )
    ],
)
def test_roundtrip_mirror(mirror: spack.mirrors.mirror.Mirror):
    mirror_yaml = mirror.to_yaml()
    assert spack.mirrors.mirror.Mirror.from_yaml(mirror_yaml) == mirror


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_mirror(invalid_yaml):
    with pytest.raises(SpackYAMLError, match="error parsing YAML") as e:
        spack.mirrors.mirror.Mirror.from_yaml(invalid_yaml)
    assert invalid_yaml in str(e.value)


def test_mirror_archive_paths_no_version(mock_packages, mock_archive):
    spec = spack.concretize.concretize_one(
        Spec("trivial-install-test-package@=nonexistingversion")
    )
    fetcher = spack.fetch_strategy.URLFetchStrategy(url=mock_archive.url)
    spack.mirrors.layout.default_mirror_layout(fetcher, "per-package-ref", spec)


def test_mirror_with_url_patches(mock_packages, monkeypatch):
    spec = spack.concretize.concretize_one("patch-several-dependencies")
    files_cached_in_mirror = set()

    def record_store(_class, fetcher, relative_dst, cosmetic_path=None):
        files_cached_in_mirror.add(os.path.basename(relative_dst))

    def successful_fetch(_class):
        with open(_class.stage.save_filename, "w", encoding="utf-8"):
            pass

    def successful_expand(_class):
        expanded_path = os.path.join(_class.stage.path, spack.stage._source_path_subdir)
        os.mkdir(expanded_path)
        with open(os.path.join(expanded_path, "test.patch"), "w", encoding="utf-8"):
            pass

    def successful_apply(*args, **kwargs):
        pass

    def successful_make_alias(*args, **kwargs):
        pass

    with spack.stage.Stage("spack-mirror-test") as stage:
        mirror_root = os.path.join(stage.path, "test-mirror")

        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "fetch", successful_fetch)
        monkeypatch.setattr(spack.fetch_strategy.URLFetchStrategy, "expand", successful_expand)
        monkeypatch.setattr(spack.patch, "apply_patch", successful_apply)
        monkeypatch.setattr(spack.caches.MirrorCache, "store", record_store)
        monkeypatch.setattr(
            spack.mirrors.layout.DefaultLayout, "make_alias", successful_make_alias
        )

        with spack.config.override("config:checksum", False):
            spack.cmd.mirror.create(mirror_root, list(spec.traverse()))

        assert {
            "abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234abcd1234",
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd.gz",
        }.issubset(files_cached_in_mirror)


class MockFetcher:
    """Mock fetcher object which implements the necessary functionality for
    testing MirrorCache
    """

    @staticmethod
    def archive(dst):
        with open(dst, "w", encoding="utf-8"):
            pass


def test_cache_store_atomic_on_failure(tmp_path: pathlib.Path):
    """A failed archive() must not leave a partial file at the final destination."""

    class FailingFetcher:
        cachable = True

        @staticmethod
        def archive(dst):
            with open(dst, "wb") as f:
                f.write(b"partial")
            raise RuntimeError("simulated failure mid-archive")

    for cache in [
        spack.caches.MirrorCache(root=str(tmp_path), skip_unstable_versions=False),
        spack.fetch_strategy.FsCache(str(tmp_path)),
    ]:
        with pytest.raises(RuntimeError, match="simulated failure"):
            cache.store(FailingFetcher(), "pkg/pkg-1.0.tar.gz")
        assert not (tmp_path / "pkg" / "pkg-1.0.tar.gz").exists()


@pytest.mark.regression("14067")
def test_mirror_layout_make_alias(tmp_path: pathlib.Path):
    """Confirm that the cosmetic symlink created in the mirror cache (which may
    be relative) targets the storage path correctly.
    """
    alias = os.path.join("zlib", "zlib-1.2.11.tar.gz")
    path = os.path.join("_source-cache", "archive", "c3", "c3e5.tar.gz")
    cache = spack.caches.MirrorCache(root=str(tmp_path), skip_unstable_versions=False)
    layout = spack.mirrors.layout.DefaultLayout(alias, path)

    cache.store(MockFetcher(), layout.path)
    layout.make_alias(cache.root)

    link_target = resolve_link_target_relative_to_the_link(os.path.join(cache.root, layout.alias))
    assert os.path.exists(link_target)
    assert os.path.normpath(link_target) == os.path.join(cache.root, layout.path)


@pytest.mark.regression("31627")
@pytest.mark.parametrize(
    "specs,expected_specs",
    [
        (["pkg-a"], ["pkg-a@=1.0", "pkg-a@=2.0"]),
        (["pkg-a", "brillig"], ["pkg-a@=1.0", "pkg-a@=2.0", "brillig@=1.0.0", "brillig@=2.0.0"]),
    ],
)
def test_get_all_versions(specs, expected_specs):
    specs = [Spec(s) for s in specs]
    output_list = spack.mirrors.utils.get_all_versions(specs)
    output_list = [str(x) for x in output_list]
    # Compare sets since order is not important
    assert set(output_list) == set(expected_specs)


def test_update_1():
    # No change
    m = spack.mirrors.mirror.Mirror("https://example.com")
    assert not m.update({"url": "https://example.com"})
    assert m.to_dict() == "https://example.com"


def test_update_2():
    # Change URL, shouldn't expand to {"url": ...} dict.
    m = spack.mirrors.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"})
    assert m.to_dict() == "https://example.org"
    assert m.fetch_url == "https://example.org"
    assert m.push_url == "https://example.org"


def test_update_3():
    # Change fetch url, ensure minimal config
    m = spack.mirrors.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"}, "fetch")
    assert m.to_dict() == {"url": "https://example.com", "fetch": "https://example.org"}
    assert m.fetch_url == "https://example.org"
    assert m.push_url == "https://example.com"


def test_update_4():
    # Change push url, ensure minimal config
    m = spack.mirrors.mirror.Mirror("https://example.com")
    assert m.update({"url": "https://example.org"}, "push")
    assert m.to_dict() == {"url": "https://example.com", "push": "https://example.org"}
    assert m.push_url == "https://example.org"
    assert m.fetch_url == "https://example.com"


@pytest.mark.parametrize("direction", ["fetch", "push"])
def test_update_connection_params(direction, monkeypatch):
    """Test whether new connection params expand the mirror config to a dict."""
    m = spack.mirrors.mirror.Mirror("https://example.com", "example")

    assert m.update(
        {
            "url": "http://example.org",
            "access_pair": ["username", "password"],
            "access_token": "token",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
        direction,
    )

    assert m.to_dict() == {
        "url": "https://example.com",
        direction: {
            "url": "http://example.org",
            "access_pair": ["username", "password"],
            "access_token": "token",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
    }
    assert m.get_access_pair(direction) == ("username", "password")
    assert m.get_access_token(direction) == "token"
    assert m.get_profile(direction) == "profile"
    assert m.get_endpoint_url(direction) == "https://example.com"

    # Expand environment variables
    os.environ["_SPACK_TEST_PAIR_USERNAME"] = "expanded_username"
    os.environ["_SPACK_TEST_PAIR_PASSWORD"] = "expanded_password"
    os.environ["_SPACK_TEST_TOKEN"] = "expanded_token"

    assert m.update(
        {
            "access_pair": {
                "id_variable": "_SPACK_TEST_PAIR_USERNAME",
                "secret_variable": "_SPACK_TEST_PAIR_PASSWORD",
            }
        },
        direction,
    )

    assert m.to_dict() == {
        "url": "https://example.com",
        direction: {
            "url": "http://example.org",
            "access_pair": {
                "id_variable": "_SPACK_TEST_PAIR_USERNAME",
                "secret_variable": "_SPACK_TEST_PAIR_PASSWORD",
            },
            "access_token": "token",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
    }

    assert m.get_access_pair(direction) == ("expanded_username", "expanded_password")

    assert m.update(
        {
            "access_pair": {"id": "username", "secret_variable": "_SPACK_TEST_PAIR_PASSWORD"},
            "access_token_variable": "_SPACK_TEST_TOKEN",
        },
        direction,
    )

    assert m.to_dict() == {
        "url": "https://example.com",
        direction: {
            "url": "http://example.org",
            "access_pair": {"id": "username", "secret_variable": "_SPACK_TEST_PAIR_PASSWORD"},
            "access_token_variable": "_SPACK_TEST_TOKEN",
            "profile": "profile",
            "endpoint_url": "https://example.com",
        },
    }

    assert m.get_access_pair(direction) == ("username", "expanded_password")
    assert m.get_access_token(direction) == "expanded_token"


def test_mirror_name_or_url_dir_parsing(tmp_path: pathlib.Path):
    curdir = tmp_path / "mirror"
    curdir.mkdir()

    with working_dir(curdir):
        assert mirror_name_or_url(".").fetch_url == curdir.as_uri()
        assert mirror_name_or_url("..").fetch_url == tmp_path.as_uri()


@pytest.mark.parametrize(
    "select,exclude,spec_str,expected",
    [
        # No filters: everything matches
        ([], [], "brillig", True),
        # Select only: matches if spec satisfies a select pattern
        (["brillig"], [], "brillig", True),
        (["brillig"], [], "canfail", False),
        # Exclude only: matches unless spec satisfies an exclude pattern
        ([], ["brillig"], "brillig", False),
        ([], ["brillig"], "canfail", True),
        # Both select and exclude
        (["brillig", "canfail"], ["canfail"], "brillig", True),
        (["brillig", "canfail"], ["canfail"], "canfail", False),
    ],
)
def test_spec_matches_filters(mock_packages, mutable_config, select, exclude, spec_str, expected):
    """Test the spec_matches_filters standalone function."""
    spec = spack.concretize.concretize_one(spec_str)
    assert spack.mirrors.mirror._spec_matches_filters(spec, select, exclude) is expected


def test_mirror_matches(mock_packages, mutable_config):
    """Test that Mirror.matches_binary() correctly applies select/exclude filters."""
    spec = spack.concretize.concretize_one("brillig")

    # No filters: everything matches
    m = spack.mirrors.mirror.Mirror({"url": "https://example.com"})
    assert m.matches_binary(spec, direction="fetch") is True

    # Exclude matches the spec
    m = spack.mirrors.mirror.Mirror({"url": "https://example.com", "exclude_binary": ["brillig"]})
    assert m.matches_binary(spec, direction="fetch") is False

    # Select does not include the spec
    m = spack.mirrors.mirror.Mirror({"url": "https://example.com", "include_binary": ["canfail"]})
    assert m.matches_binary(spec, direction="fetch") is False

    # Select includes the spec
    m = spack.mirrors.mirror.Mirror({"url": "https://example.com", "include_binary": ["brillig"]})
    assert m.matches_binary(spec, direction="fetch") is True

    # Exclude does not match the spec
    m = spack.mirrors.mirror.Mirror({"url": "https://example.com", "exclude_binary": ["canfail"]})
    assert m.matches_binary(spec, direction="fetch") is True

    # Select includes but exclude also matches: exclude wins
    m = spack.mirrors.mirror.Mirror(
        {
            "url": "https://example.com",
            "include_binary": ["brillig"],
            "exclude_binary": ["brillig"],
        }
    )
    assert m.matches_binary(spec, direction="fetch") is False

    # Direction-specific filter overrides global filters
    m = spack.mirrors.mirror.Mirror(
        {
            "url": "https://example.com",
            "include_binary": ["canfail"],
            "fetch": {"include_binary": ["brillig"]},
        }
    )
    assert m.matches_binary(spec, direction="fetch") is True
    assert m.matches_binary(spec, direction="push") is False

    # Direction-specific and mirror-level config compose
    m = spack.mirrors.mirror.Mirror(
        {
            "url": "https://example.com",
            "include_binary": ["brillig"],
            "fetch": {"exclude_binary": ["brillig"]},
        }
    )
    assert m.matches_binary(spec, direction="fetch") is False
    assert m.matches_binary(spec, direction="push") is True

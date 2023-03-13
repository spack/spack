# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import filecmp
import glob
import io
import os
import platform
import sys
import tarfile
import urllib.error
import urllib.request
import urllib.response

import py
import pytest

from llnl.util.filesystem import join_path, visit_directory_tree

import spack.binary_distribution as bindist
import spack.caches
import spack.config
import spack.fetch_strategy
import spack.hooks.sbang as sbang
import spack.main
import spack.mirror
import spack.repo
import spack.store
import spack.util.gpg
import spack.util.url as url_util
import spack.util.web as web_util
from spack.binary_distribution import get_buildfile_manifest
from spack.directory_layout import DirectoryLayout
from spack.paths import test_path
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")

mirror_cmd = spack.main.SpackCommand("mirror")
install_cmd = spack.main.SpackCommand("install")
uninstall_cmd = spack.main.SpackCommand("uninstall")
buildcache_cmd = spack.main.SpackCommand("buildcache")

legacy_mirror_dir = os.path.join(test_path, "data", "mirrors", "legacy_yaml")


@pytest.fixture(scope="function")
def cache_directory(tmpdir):
    fetch_cache_dir = tmpdir.ensure("fetch_cache", dir=True)
    fsc = spack.fetch_strategy.FsCache(str(fetch_cache_dir))
    spack.config.caches, old_cache_path = fsc, spack.caches.fetch_cache

    yield spack.config.caches

    fetch_cache_dir.remove()
    spack.config.caches = old_cache_path


@pytest.fixture(scope="module")
def mirror_dir(tmpdir_factory):
    dir = tmpdir_factory.mktemp("mirror")
    dir.ensure("build_cache", dir=True)
    yield str(dir)
    dir.join("build_cache").remove()


@pytest.fixture(scope="function")
def test_mirror(mirror_dir):
    mirror_url = url_util.path_to_file_url(mirror_dir)
    mirror_cmd("add", "--scope", "site", "test-mirror-func", mirror_url)
    yield mirror_dir
    mirror_cmd("rm", "--scope=site", "test-mirror-func")


@pytest.fixture(scope="module")
def config_directory(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("test_configs")
    # restore some sane defaults for packages and config
    config_path = py.path.local(spack.paths.etc_path)
    modules_yaml = config_path.join("defaults", "modules.yaml")
    os_modules_yaml = config_path.join(
        "defaults", "%s" % platform.system().lower(), "modules.yaml"
    )
    packages_yaml = config_path.join("defaults", "packages.yaml")
    config_yaml = config_path.join("defaults", "config.yaml")
    repos_yaml = config_path.join("defaults", "repos.yaml")
    tmpdir.ensure("site", dir=True)
    tmpdir.ensure("user", dir=True)
    tmpdir.ensure("site/%s" % platform.system().lower(), dir=True)
    modules_yaml.copy(tmpdir.join("site", "modules.yaml"))
    os_modules_yaml.copy(tmpdir.join("site/%s" % platform.system().lower(), "modules.yaml"))
    packages_yaml.copy(tmpdir.join("site", "packages.yaml"))
    config_yaml.copy(tmpdir.join("site", "config.yaml"))
    repos_yaml.copy(tmpdir.join("site", "repos.yaml"))
    yield tmpdir
    tmpdir.remove()


@pytest.fixture(scope="function")
def default_config(tmpdir, config_directory, monkeypatch, install_mockery_mutable_config):
    # This fixture depends on install_mockery_mutable_config to ensure
    # there is a clear order of initialization. The substitution of the
    # config scopes here is done on top of the substitution that comes with
    # install_mockery_mutable_config
    mutable_dir = tmpdir.mkdir("mutable_config").join("tmp")
    config_directory.copy(mutable_dir)

    cfg = spack.config.Configuration(
        *[
            spack.config.ConfigScope(name, str(mutable_dir))
            for name in ["site/%s" % platform.system().lower(), "site", "user"]
        ]
    )

    spack.config.config, old_config = cfg, spack.config.config
    spack.config.config.set("repos", [spack.paths.mock_packages_path])
    # This is essential, otherwise the cache will create weird side effects
    # that will compromise subsequent tests if compilers.yaml is modified
    monkeypatch.setattr(spack.compilers, "_cache_config_file", [])
    njobs = spack.config.get("config:build_jobs")
    if not njobs:
        spack.config.set("config:build_jobs", 4, scope="user")
    extensions = spack.config.get("config:template_dirs")
    if not extensions:
        spack.config.set(
            "config:template_dirs",
            [os.path.join(spack.paths.share_path, "templates")],
            scope="user",
        )

    mutable_dir.ensure("build_stage", dir=True)
    build_stage = spack.config.get("config:build_stage")
    if not build_stage:
        spack.config.set(
            "config:build_stage", [str(mutable_dir.join("build_stage"))], scope="user"
        )
    timeout = spack.config.get("config:connect_timeout")
    if not timeout:
        spack.config.set("config:connect_timeout", 10, scope="user")

    yield spack.config.config

    spack.config.config = old_config
    mutable_dir.remove()


@pytest.fixture(scope="function")
def install_dir_default_layout(tmpdir):
    """Hooks a fake install directory with a default layout"""
    scheme = os.path.join(
        "${architecture}", "${compiler.name}-${compiler.version}", "${name}-${version}-${hash}"
    )
    real_store, real_layout = spack.store.store, spack.store.layout
    opt_dir = tmpdir.join("opt")
    spack.store.store = spack.store.Store(str(opt_dir))
    spack.store.layout = DirectoryLayout(str(opt_dir), path_scheme=scheme)
    try:
        yield spack.store
    finally:
        spack.store.store = real_store
        spack.store.layout = real_layout


@pytest.fixture(scope="function")
def install_dir_non_default_layout(tmpdir):
    """Hooks a fake install directory with a non-default layout"""
    scheme = os.path.join(
        "${name}", "${version}", "${architecture}-${compiler.name}-${compiler.version}-${hash}"
    )
    real_store, real_layout = spack.store.store, spack.store.layout
    opt_dir = tmpdir.join("opt")
    spack.store.store = spack.store.Store(str(opt_dir))
    spack.store.layout = DirectoryLayout(str(opt_dir), path_scheme=scheme)
    try:
        yield spack.store
    finally:
        spack.store.store = real_store
        spack.store.layout = real_layout


args = ["strings", "file"]
if sys.platform == "darwin":
    args.extend(["/usr/bin/clang++", "install_name_tool"])
else:
    args.extend(["/usr/bin/g++", "patchelf"])


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.usefixtures(
    "default_config", "cache_directory", "install_dir_default_layout", "test_mirror"
)
def test_default_rpaths_create_install_default_layout(mirror_dir):
    """
    Test the creation and installation of buildcaches with default rpaths
    into the default directory layout scheme.
    """
    gspec, cspec = Spec("garply").concretized(), Spec("corge").concretized()
    sy_spec = Spec("symly").concretized()

    # Install 'corge' without using a cache
    install_cmd("--no-cache", cspec.name)
    install_cmd("--no-cache", sy_spec.name)

    # Create a buildache
    buildcache_cmd("create", "-au", "-d", mirror_dir, cspec.name, sy_spec.name)
    # Test force overwrite create buildcache (-f option)
    buildcache_cmd("create", "-auf", "-d", mirror_dir, cspec.name)

    # Create mirror index
    buildcache_cmd("update-index", "-d", mirror_dir)
    # List the buildcaches in the mirror
    buildcache_cmd("list", "-alv")

    # Uninstall the package and deps
    uninstall_cmd("-y", "--dependents", gspec.name)

    # Test installing from build caches
    buildcache_cmd("install", "-au", cspec.name, sy_spec.name)

    # This gives warning that spec is already installed
    buildcache_cmd("install", "-au", cspec.name)

    # Test overwrite install
    buildcache_cmd("install", "-afu", cspec.name)

    buildcache_cmd("keys", "-f")
    buildcache_cmd("list")

    buildcache_cmd("list", "-a")
    buildcache_cmd("list", "-l", "-v")


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.nomockstage
@pytest.mark.usefixtures(
    "default_config", "cache_directory", "install_dir_non_default_layout", "test_mirror"
)
def test_default_rpaths_install_nondefault_layout(mirror_dir):
    """
    Test the creation and installation of buildcaches with default rpaths
    into the non-default directory layout scheme.
    """
    cspec = Spec("corge").concretized()
    # This guy tests for symlink relocation
    sy_spec = Spec("symly").concretized()

    # Install some packages with dependent packages
    # test install in non-default install path scheme
    buildcache_cmd("install", "-au", cspec.name, sy_spec.name)

    # Test force install in non-default install path scheme
    buildcache_cmd("install", "-auf", cspec.name)


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.nomockstage
@pytest.mark.usefixtures("default_config", "cache_directory", "install_dir_default_layout")
def test_relative_rpaths_create_default_layout(mirror_dir):
    """
    Test the creation and installation of buildcaches with relative
    rpaths into the default directory layout scheme.
    """

    gspec, cspec = Spec("garply").concretized(), Spec("corge").concretized()

    # Install 'corge' without using a cache
    install_cmd("--no-cache", cspec.name)

    # Create build cache with relative rpaths
    buildcache_cmd("create", "-aur", "-d", mirror_dir, cspec.name)

    # Create mirror index
    buildcache_cmd("update-index", "-d", mirror_dir)

    # Uninstall the package and deps
    uninstall_cmd("-y", "--dependents", gspec.name)


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.nomockstage
@pytest.mark.usefixtures(
    "default_config", "cache_directory", "install_dir_default_layout", "test_mirror"
)
def test_relative_rpaths_install_default_layout(mirror_dir):
    """
    Test the creation and installation of buildcaches with relative
    rpaths into the default directory layout scheme.
    """
    gspec, cspec = Spec("garply").concretized(), Spec("corge").concretized()

    # Install buildcache created with relativized rpaths
    buildcache_cmd("install", "-auf", cspec.name)

    # This gives warning that spec is already installed
    buildcache_cmd("install", "-auf", cspec.name)

    # Uninstall the package and deps
    uninstall_cmd("-y", "--dependents", gspec.name)

    # Install build cache
    buildcache_cmd("install", "-auf", cspec.name)

    # Test overwrite install
    buildcache_cmd("install", "-auf", cspec.name)


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.nomockstage
@pytest.mark.usefixtures(
    "default_config", "cache_directory", "install_dir_non_default_layout", "test_mirror"
)
def test_relative_rpaths_install_nondefault(mirror_dir):
    """
    Test the installation of buildcaches with relativized rpaths
    into the non-default directory layout scheme.
    """
    cspec = Spec("corge").concretized()

    # Test install in non-default install path scheme and relative path
    buildcache_cmd("install", "-auf", cspec.name)


def test_push_and_fetch_keys(mock_gnupghome):
    testpath = str(mock_gnupghome)

    mirror = os.path.join(testpath, "mirror")
    mirrors = {"test-mirror": url_util.path_to_file_url(mirror)}
    mirrors = spack.mirror.MirrorCollection(mirrors)
    mirror = spack.mirror.Mirror(url_util.path_to_file_url(mirror))

    gpg_dir1 = os.path.join(testpath, "gpg1")
    gpg_dir2 = os.path.join(testpath, "gpg2")

    # dir 1: create a new key, record its fingerprint, and push it to a new
    #        mirror
    with spack.util.gpg.gnupghome_override(gpg_dir1):
        spack.util.gpg.create(name="test-key", email="fake@test.key", expires="0", comment=None)

        keys = spack.util.gpg.public_keys()
        assert len(keys) == 1
        fpr = keys[0]

        bindist.push_keys(mirror, keys=[fpr], regenerate_index=True)

    # dir 2: import the key from the mirror, and confirm that its fingerprint
    #        matches the one created above
    with spack.util.gpg.gnupghome_override(gpg_dir2):
        assert len(spack.util.gpg.public_keys()) == 0

        bindist.get_keys(mirrors=mirrors, install=True, trust=True, force=True)

        new_keys = spack.util.gpg.public_keys()
        assert len(new_keys) == 1
        assert new_keys[0] == fpr


@pytest.mark.requires_executables(*args)
@pytest.mark.maybeslow
@pytest.mark.nomockstage
@pytest.mark.usefixtures(
    "default_config", "cache_directory", "install_dir_non_default_layout", "test_mirror"
)
def test_built_spec_cache(mirror_dir):
    """Because the buildcache list command fetches the buildcache index
    and uses it to populate the binary_distribution built spec cache, when
    this test calls get_mirrors_for_spec, it is testing the popluation of
    that cache from a buildcache index."""
    buildcache_cmd("list", "-a", "-l")

    gspec, cspec = Spec("garply").concretized(), Spec("corge").concretized()

    for s in [gspec, cspec]:
        results = bindist.get_mirrors_for_spec(s)
        assert any([r["spec"] == s for r in results])


def fake_dag_hash(spec):
    # Generate an arbitrary hash that is intended to be different than
    # whatever a Spec reported before (to test actions that trigger when
    # the hash changes)
    return "tal4c7h4z0gqmixb1eqa92mjoybxn5l6"


@pytest.mark.usefixtures(
    "install_mockery_mutable_config", "mock_packages", "mock_fetch", "test_mirror"
)
def test_spec_needs_rebuild(monkeypatch, tmpdir):
    """Make sure needs_rebuild properly compares remote hash
    against locally computed one, avoiding unnecessary rebuilds"""

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join("mirror_dir")
    mirror_url = url_util.path_to_file_url(mirror_dir.strpath)

    s = Spec("libdwarf").concretized()

    # Install a package
    install_cmd(s.name)

    # Put installed package in the buildcache
    buildcache_cmd("create", "-u", "-a", "-d", mirror_dir.strpath, s.name)

    rebuild = bindist.needs_rebuild(s, mirror_url)

    assert not rebuild

    # Now monkey patch Spec to change the hash on the package
    monkeypatch.setattr(spack.spec.Spec, "dag_hash", fake_dag_hash)

    rebuild = bindist.needs_rebuild(s, mirror_url)

    assert rebuild


@pytest.mark.usefixtures("install_mockery_mutable_config", "mock_packages", "mock_fetch")
def test_generate_index_missing(monkeypatch, tmpdir, mutable_config):
    """Ensure spack buildcache index only reports available packages"""

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join("mirror_dir")
    mirror_url = url_util.path_to_file_url(mirror_dir.strpath)
    spack.config.set("mirrors", {"test": mirror_url})

    s = Spec("libdwarf").concretized()

    # Install a package
    install_cmd("--no-cache", s.name)

    # Create a buildcache and update index
    buildcache_cmd("create", "-uad", mirror_dir.strpath, s.name)
    buildcache_cmd("update-index", "-d", mirror_dir.strpath)

    # Check package and dependency in buildcache
    cache_list = buildcache_cmd("list", "--allarch")
    assert "libdwarf" in cache_list
    assert "libelf" in cache_list

    # Remove dependency from cache
    libelf_files = glob.glob(os.path.join(mirror_dir.join("build_cache").strpath, "*libelf*"))
    os.remove(*libelf_files)

    # Update index
    buildcache_cmd("update-index", "-d", mirror_dir.strpath)

    with spack.config.override("config:binary_index_ttl", 0):
        # Check dependency not in buildcache
        cache_list = buildcache_cmd("list", "--allarch")
        assert "libdwarf" in cache_list
        assert "libelf" not in cache_list


def test_generate_indices_key_error(monkeypatch, capfd):
    def mock_list_url(url, recursive=False):
        print("mocked list_url({0}, {1})".format(url, recursive))
        raise KeyError("Test KeyError handling")

    monkeypatch.setattr(web_util, "list_url", mock_list_url)

    test_url = "file:///fake/keys/dir"

    # Make sure generate_key_index handles the KeyError
    bindist.generate_key_index(test_url)

    err = capfd.readouterr()[1]
    assert "Warning: No keys at {0}".format(test_url) in err

    # Make sure generate_package_index handles the KeyError
    bindist.generate_package_index(test_url)

    err = capfd.readouterr()[1]
    assert "Warning: No packages at {0}".format(test_url) in err


def test_generate_indices_exception(monkeypatch, capfd):
    def mock_list_url(url, recursive=False):
        print("mocked list_url({0}, {1})".format(url, recursive))
        raise Exception("Test Exception handling")

    monkeypatch.setattr(web_util, "list_url", mock_list_url)

    test_url = "file:///fake/keys/dir"

    # Make sure generate_key_index handles the Exception
    bindist.generate_key_index(test_url)

    err = capfd.readouterr()[1]
    expect = "Encountered problem listing keys at {0}".format(test_url)
    assert expect in err

    # Make sure generate_package_index handles the Exception
    bindist.generate_package_index(test_url)

    err = capfd.readouterr()[1]
    expect = "Encountered problem listing packages at {0}".format(test_url)
    assert expect in err


@pytest.mark.usefixtures("mock_fetch", "install_mockery")
def test_update_sbang(tmpdir, test_mirror):
    """Test the creation and installation of buildcaches with default rpaths
    into the non-default directory layout scheme, triggering an update of the
    sbang.
    """
    scheme = os.path.join(
        "${name}", "${version}", "${architecture}-${compiler.name}-${compiler.version}-${hash}"
    )
    spec_str = "old-sbang"
    # Concretize a package with some old-fashioned sbang lines.
    old_spec = Spec(spec_str).concretized()
    old_spec_hash_str = "/{0}".format(old_spec.dag_hash())

    # Need a fake mirror with *function* scope.
    mirror_dir = test_mirror

    # Assume all commands will concretize old_spec the same way.
    install_cmd("--no-cache", old_spec.name)

    # Create a buildcache with the installed spec.
    buildcache_cmd("create", "-u", "-a", "-d", mirror_dir, old_spec_hash_str)

    # Need to force an update of the buildcache index
    buildcache_cmd("update-index", "-d", mirror_dir)

    # Uninstall the original package.
    uninstall_cmd("-y", old_spec_hash_str)

    # Switch the store to the new install tree locations
    newtree_dir = tmpdir.join("newtree")
    s = spack.store.Store(str(newtree_dir))
    s.layout = DirectoryLayout(str(newtree_dir), path_scheme=scheme)

    with spack.store.use_store(s):
        new_spec = Spec("old-sbang")
        new_spec.concretize()
        assert new_spec.dag_hash() == old_spec.dag_hash()

        # Install package from buildcache
        buildcache_cmd("install", "-a", "-u", "-f", new_spec.name)

        # Continue blowing away caches
        bindist.clear_spec_cache()
        spack.stage.purge()

        # test that the sbang was updated by the move
        sbang_style_1_expected = """{0}
#!/usr/bin/env python

{1}
""".format(
            sbang.sbang_shebang_line(), new_spec.prefix.bin
        )
        sbang_style_2_expected = """{0}
#!/usr/bin/env python

{1}
""".format(
            sbang.sbang_shebang_line(), new_spec.prefix.bin
        )

        installed_script_style_1_path = new_spec.prefix.bin.join("sbang-style-1.sh")
        assert sbang_style_1_expected == open(str(installed_script_style_1_path)).read()

        installed_script_style_2_path = new_spec.prefix.bin.join("sbang-style-2.sh")
        assert sbang_style_2_expected == open(str(installed_script_style_2_path)).read()

        uninstall_cmd("-y", "/%s" % new_spec.dag_hash())


def test_install_legacy_buildcache_layout(install_mockery_mutable_config):
    """Legacy buildcache layout involved a nested archive structure
    where the .spack file contained a repeated spec.json and another
    compressed archive file containing the install tree.  This test
    makes sure we can still read that layout."""
    legacy_layout_dir = os.path.join(test_path, "data", "mirrors", "legacy_layout")
    mirror_url = "file://{0}".format(legacy_layout_dir)
    filename = (
        "test-debian6-core2-gcc-4.5.0-archive-files-2.0-"
        "l3vdiqvbobmspwyb4q2b62fz6nitd4hk.spec.json"
    )
    spec_json_path = os.path.join(legacy_layout_dir, "build_cache", filename)
    mirror_cmd("add", "--scope", "site", "test-legacy-layout", mirror_url)
    output = install_cmd("--no-check-signature", "--cache-only", "-f", spec_json_path, output=str)
    mirror_cmd("rm", "--scope=site", "test-legacy-layout")
    expect_line = (
        "Extracting archive-files-2.0-" "l3vdiqvbobmspwyb4q2b62fz6nitd4hk from binary cache"
    )
    assert expect_line in output


def test_FetchCacheError_only_accepts_lists_of_errors():
    with pytest.raises(TypeError, match="list"):
        bindist.FetchCacheError("error")


def test_FetchCacheError_pretty_printing_multiple():
    e = bindist.FetchCacheError([RuntimeError("Oops!"), TypeError("Trouble!")])
    str_e = str(e)
    print("'" + str_e + "'")
    assert "Multiple errors" in str_e
    assert "Error 1: RuntimeError: Oops!" in str_e
    assert "Error 2: TypeError: Trouble!" in str_e
    assert str_e.rstrip() == str_e


def test_FetchCacheError_pretty_printing_single():
    e = bindist.FetchCacheError([RuntimeError("Oops!")])
    str_e = str(e)
    assert "Multiple errors" not in str_e
    assert "RuntimeError: Oops!" in str_e
    assert str_e.rstrip() == str_e


def test_build_manifest_visitor(tmpdir):
    dir = "directory"
    file = os.path.join("directory", "file")

    with tmpdir.as_cwd():
        # Create a file inside a directory
        os.mkdir(dir)
        with open(file, "wb") as f:
            f.write(b"example file")

        # Symlink the dir
        os.symlink(dir, "symlink_to_directory")

        # Symlink the file
        os.symlink(file, "symlink_to_file")

        # Hardlink the file
        os.link(file, "hardlink_of_file")

        # Hardlinked symlinks: seems like this is only a thing on Linux,
        # on Darwin the symlink *target* is hardlinked, on Linux the
        # symlink *itself* is hardlinked.
        if sys.platform.startswith("linux"):
            os.link("symlink_to_file", "hardlink_of_symlink_to_file")
            os.link("symlink_to_directory", "hardlink_of_symlink_to_directory")

    visitor = bindist.BuildManifestVisitor()
    visit_directory_tree(str(tmpdir), visitor)

    # We de-dupe hardlinks of files, so there should really be just one file
    assert len(visitor.files) == 1

    # We do not de-dupe symlinks, cause it's unclear how to update symlinks
    # in-place, preserving inodes.
    if sys.platform.startswith("linux"):
        assert len(visitor.symlinks) == 4  # includes hardlinks of symlinks.
    else:
        assert len(visitor.symlinks) == 2

    with tmpdir.as_cwd():
        assert not any(os.path.islink(f) or os.path.isdir(f) for f in visitor.files)
        assert all(os.path.islink(f) for f in visitor.symlinks)


def test_text_relocate_if_needed(install_mockery, mock_fetch, monkeypatch, capfd):
    spec = Spec("needs-text-relocation").concretized()
    install_cmd(str(spec))

    manifest = get_buildfile_manifest(spec)
    assert join_path("bin", "exe") in manifest["text_to_relocate"]
    assert join_path("bin", "otherexe") not in manifest["text_to_relocate"]
    assert join_path("bin", "secretexe") not in manifest["text_to_relocate"]


def test_etag_fetching_304():
    # Test conditional fetch with etags. If the remote hasn't modified the file
    # it returns 304, which is an HTTPError in urllib-land. That should be
    # handled as success, since it means the local cache is up-to-date.
    def response_304(request: urllib.request.Request):
        url = request.get_full_url()
        if url == "https://www.example.com/build_cache/index.json":
            assert request.get_header("If-none-match") == '"112a8bbc1b3f7f185621c1ee335f0502"'
            raise urllib.error.HTTPError(
                url, 304, "Not Modified", hdrs={}, fp=None  # type: ignore[arg-type]
            )
        assert False, "Should not fetch {}".format(url)

    fetcher = bindist.EtagIndexFetcher(
        url="https://www.example.com",
        etag="112a8bbc1b3f7f185621c1ee335f0502",
        urlopen=response_304,
    )

    result = fetcher.conditional_fetch()
    assert isinstance(result, bindist.FetchIndexResult)
    assert result.fresh


def test_etag_fetching_200():
    # Test conditional fetch with etags. The remote has modified the file.
    def response_200(request: urllib.request.Request):
        url = request.get_full_url()
        if url == "https://www.example.com/build_cache/index.json":
            assert request.get_header("If-none-match") == '"112a8bbc1b3f7f185621c1ee335f0502"'
            return urllib.response.addinfourl(
                io.BytesIO(b"Result"),
                headers={"Etag": '"59bcc3ad6775562f845953cf01624225"'},  # type: ignore[arg-type]
                url=url,
                code=200,
            )
        assert False, "Should not fetch {}".format(url)

    fetcher = bindist.EtagIndexFetcher(
        url="https://www.example.com",
        etag="112a8bbc1b3f7f185621c1ee335f0502",
        urlopen=response_200,
    )

    result = fetcher.conditional_fetch()
    assert isinstance(result, bindist.FetchIndexResult)
    assert not result.fresh
    assert result.etag == "59bcc3ad6775562f845953cf01624225"
    assert result.data == "Result"  # decoded utf-8.
    assert result.hash == bindist.compute_hash("Result")


def test_etag_fetching_404():
    # Test conditional fetch with etags. The remote has modified the file.
    def response_404(request: urllib.request.Request):
        raise urllib.error.HTTPError(
            request.get_full_url(),
            404,
            "Not found",
            hdrs={"Etag": '"59bcc3ad6775562f845953cf01624225"'},  # type: ignore[arg-type]
            fp=None,
        )

    fetcher = bindist.EtagIndexFetcher(
        url="https://www.example.com",
        etag="112a8bbc1b3f7f185621c1ee335f0502",
        urlopen=response_404,
    )

    with pytest.raises(bindist.FetchIndexError):
        fetcher.conditional_fetch()


def test_default_index_fetch_200():
    index_json = '{"Hello": "World"}'
    index_json_hash = bindist.compute_hash(index_json)

    def urlopen(request: urllib.request.Request):
        url = request.get_full_url()
        if url.endswith("index.json.hash"):
            return urllib.response.addinfourl(  # type: ignore[arg-type]
                io.BytesIO(index_json_hash.encode()),
                headers={},  # type: ignore[arg-type]
                url=url,
                code=200,
            )

        elif url.endswith("index.json"):
            return urllib.response.addinfourl(
                io.BytesIO(index_json.encode()),
                headers={"Etag": '"59bcc3ad6775562f845953cf01624225"'},  # type: ignore[arg-type]
                url=url,
                code=200,
            )

        assert False, "Unexpected request {}".format(url)

    fetcher = bindist.DefaultIndexFetcher(
        url="https://www.example.com", local_hash="outdated", urlopen=urlopen
    )

    result = fetcher.conditional_fetch()

    assert isinstance(result, bindist.FetchIndexResult)
    assert not result.fresh
    assert result.etag == "59bcc3ad6775562f845953cf01624225"
    assert result.data == index_json
    assert result.hash == index_json_hash


def test_default_index_dont_fetch_index_json_hash_if_no_local_hash():
    # When we don't have local hash, we should not be fetching the
    # remote index.json.hash file, but only index.json.
    index_json = '{"Hello": "World"}'
    index_json_hash = bindist.compute_hash(index_json)

    def urlopen(request: urllib.request.Request):
        url = request.get_full_url()
        if url.endswith("index.json"):
            return urllib.response.addinfourl(
                io.BytesIO(index_json.encode()),
                headers={"Etag": '"59bcc3ad6775562f845953cf01624225"'},  # type: ignore[arg-type]
                url=url,
                code=200,
            )

        assert False, "Unexpected request {}".format(url)

    fetcher = bindist.DefaultIndexFetcher(
        url="https://www.example.com", local_hash=None, urlopen=urlopen
    )

    result = fetcher.conditional_fetch()

    assert isinstance(result, bindist.FetchIndexResult)
    assert result.data == index_json
    assert result.hash == index_json_hash
    assert result.etag == "59bcc3ad6775562f845953cf01624225"
    assert not result.fresh


def test_default_index_not_modified():
    index_json = '{"Hello": "World"}'
    index_json_hash = bindist.compute_hash(index_json)

    def urlopen(request: urllib.request.Request):
        url = request.get_full_url()
        if url.endswith("index.json.hash"):
            return urllib.response.addinfourl(
                io.BytesIO(index_json_hash.encode()),
                headers={},  # type: ignore[arg-type]
                url=url,
                code=200,
            )

        # No request to index.json should be made.
        assert False, "Unexpected request {}".format(url)

    fetcher = bindist.DefaultIndexFetcher(
        url="https://www.example.com", local_hash=index_json_hash, urlopen=urlopen
    )

    assert fetcher.conditional_fetch().fresh


@pytest.mark.parametrize("index_json", [b"\xa9", b"!#%^"])
def test_default_index_invalid_hash_file(index_json):
    # Test invalid unicode / invalid hash type
    index_json_hash = bindist.compute_hash(index_json)

    def urlopen(request: urllib.request.Request):
        return urllib.response.addinfourl(
            io.BytesIO(),
            headers={},  # type: ignore[arg-type]
            url=request.get_full_url(),
            code=200,
        )

    fetcher = bindist.DefaultIndexFetcher(
        url="https://www.example.com", local_hash=index_json_hash, urlopen=urlopen
    )

    assert fetcher.get_remote_hash() is None


def test_default_index_json_404():
    # Test invalid unicode / invalid hash type
    index_json = '{"Hello": "World"}'
    index_json_hash = bindist.compute_hash(index_json)

    def urlopen(request: urllib.request.Request):
        url = request.get_full_url()
        if url.endswith("index.json.hash"):
            return urllib.response.addinfourl(
                io.BytesIO(index_json_hash.encode()),
                headers={},  # type: ignore[arg-type]
                url=url,
                code=200,
            )

        elif url.endswith("index.json"):
            raise urllib.error.HTTPError(
                url,
                code=404,
                msg="Not Found",
                hdrs={"Etag": '"59bcc3ad6775562f845953cf01624225"'},  # type: ignore[arg-type]
                fp=None,
            )

        assert False, "Unexpected fetch {}".format(url)

    fetcher = bindist.DefaultIndexFetcher(
        url="https://www.example.com", local_hash="invalid", urlopen=urlopen
    )

    with pytest.raises(bindist.FetchIndexError, match="Could not fetch index"):
        fetcher.conditional_fetch()


@pytest.mark.parametrize(
    "root,deps,expected",
    [
        (
            True,
            True,
            [
                "dttop",
                "dtbuild1",
                "dtbuild2",
                "dtlink2",
                "dtrun2",
                "dtlink1",
                "dtlink3",
                "dtlink4",
                "dtrun1",
                "dtlink5",
                "dtrun3",
                "dtbuild3",
            ],
        ),
        (
            False,
            True,
            [
                "dtbuild1",
                "dtbuild2",
                "dtlink2",
                "dtrun2",
                "dtlink1",
                "dtlink3",
                "dtlink4",
                "dtrun1",
                "dtlink5",
                "dtrun3",
                "dtbuild3",
            ],
        ),
        (True, False, ["dttop"]),
        (False, False, []),
    ],
)
def test_correct_specs_are_pushed(
    root, deps, expected, default_mock_concretization, tmpdir, temporary_store, monkeypatch
):
    # Concretize dttop and add it to the temporary database (without prefixes)
    spec = default_mock_concretization("dttop")
    temporary_store.db.add(spec, directory_layout=None)

    # Create a mirror push url
    push_url = spack.mirror.Mirror.from_local_path(str(tmpdir)).push_url

    packages_to_push = []

    def fake_build_tarball(node, push_url, **kwargs):
        assert push_url == push_url
        assert not kwargs
        assert isinstance(node, Spec)
        packages_to_push.append(node.name)

    monkeypatch.setattr(bindist, "_build_tarball", fake_build_tarball)

    bindist.push([spec], push_url, include_root=root, include_dependencies=deps)

    assert packages_to_push == expected


def test_reproducible_tarball_is_reproducible(tmpdir):
    p = tmpdir.mkdir("prefix")
    p.mkdir("bin")
    p.mkdir(".spack")

    app = p.join("bin", "app")

    tarball_1 = str(tmpdir.join("prefix-1.tar.gz"))
    tarball_2 = str(tmpdir.join("prefix-2.tar.gz"))

    with open(app, "w") as f:
        f.write("hello world")

    buildinfo = {"metadata": "yes please"}

    # Create a tarball with a certain mtime of bin/app
    os.utime(app, times=(0, 0))
    bindist._do_create_tarball(tarball_1, binaries_dir=p, pkg_dir="pkg", buildinfo=buildinfo)

    # Do it another time with different mtime of bin/app
    os.utime(app, times=(10, 10))
    bindist._do_create_tarball(tarball_2, binaries_dir=p, pkg_dir="pkg", buildinfo=buildinfo)

    # They should be bitwise identical:
    assert filecmp.cmp(tarball_1, tarball_2, shallow=False)

    # Sanity check for contents:
    with tarfile.open(tarball_1, mode="r") as f:
        for m in f.getmembers():
            assert m.uid == m.gid == m.mtime == 0
            assert m.uname == m.gname == ""

        assert set(f.getnames()) == {
            "pkg",
            "pkg/bin",
            "pkg/bin/app",
            "pkg/.spack",
            "pkg/.spack/binary_distribution",
        }


def test_tarball_normalized_permissions(tmpdir):
    p = tmpdir.mkdir("prefix")
    p.mkdir("bin")
    p.mkdir("share")
    p.mkdir(".spack")

    app = p.join("bin", "app")
    data = p.join("share", "file")
    tarball = str(tmpdir.join("prefix.tar.gz"))

    # Everyone can write & execute. This should turn into 0o755 when the tarball is
    # extracted (on a different system).
    with open(app, "w", opener=lambda path, flags: os.open(path, flags, 0o777)) as f:
        f.write("hello world")

    # User doesn't have execute permissions, but group/world have; this should also
    # turn into 0o644 (user read/write, group&world only read).
    with open(data, "w", opener=lambda path, flags: os.open(path, flags, 0o477)) as f:
        f.write("hello world")

    bindist._do_create_tarball(tarball, binaries_dir=p, pkg_dir="pkg", buildinfo={})

    with tarfile.open(tarball) as tar:
        path_to_member = {member.name: member for member in tar.getmembers()}

    # directories should have 0o755
    assert path_to_member["pkg"].mode == 0o755
    assert path_to_member["pkg/bin"].mode == 0o755
    assert path_to_member["pkg/.spack"].mode == 0o755

    # executable-by-user files should be 0o755
    assert path_to_member["pkg/bin/app"].mode == 0o755

    # not-executable-by-user files should be 0o644
    assert path_to_member["pkg/share/file"].mode == 0o644

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import json
import os
import pathlib
import shutil
from typing import List

import pytest

from llnl.util.filesystem import copy_tree, find

import spack.binary_distribution
import spack.buildcache_migrate as migrate
import spack.cmd.buildcache
import spack.concretize
import spack.environment as ev
import spack.error
import spack.main
import spack.mirrors.mirror
import spack.spec
import spack.util.url as url_util
from spack.installer import PackageInstaller
from spack.paths import test_path
from spack.url_buildcache import (
    BuildcacheComponent,
    URLBuildcacheEntry,
    URLBuildcacheEntryV2,
    check_mirror_for_layout,
    get_url_buildcache_class,
)

buildcache = spack.main.SpackCommand("buildcache")
install = spack.main.SpackCommand("install")
env = spack.main.SpackCommand("env")
add = spack.main.SpackCommand("add")
gpg = spack.main.SpackCommand("gpg")
mirror = spack.main.SpackCommand("mirror")
uninstall = spack.main.SpackCommand("uninstall")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    specs = database.query_local()
    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: specs)


@pytest.fixture()
def mock_get_specs_multiarch(database, monkeypatch):
    specs = [spec.copy() for spec in database.query_local()]

    # make one spec that is NOT the test architecture
    for spec in specs:
        if spec.name == "mpileaks":
            spec.architecture = spack.spec.ArchSpec("linux-rhel7-x86_64")
            break

    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: specs)


@pytest.mark.db
@pytest.mark.regression("13757")
def test_buildcache_list_duplicates(mock_get_specs, capsys):
    with capsys.disabled():
        output = buildcache("list", "mpileaks", "@2.3")

    assert output.count("mpileaks") == 3


@pytest.mark.db
@pytest.mark.regression("17827")
def test_buildcache_list_allarch(database, mock_get_specs_multiarch, capsys):
    with capsys.disabled():
        output = buildcache("list", "--allarch")

    assert output.count("mpileaks") == 3

    with capsys.disabled():
        output = buildcache("list")

    assert output.count("mpileaks") == 2


def tests_buildcache_create_env(
    install_mockery, mock_fetch, monkeypatch, tmpdir, mutable_mock_env_path
):
    """ "Ensure that buildcache create creates output files from env"""
    pkg = "trivial-install-test-package"

    env("create", "test")
    with ev.read("test"):
        add(pkg)
        install()

        buildcache("push", "--unsigned", str(tmpdir))

    spec = spack.concretize.concretize_one(pkg)

    mirror_url = f"file://{tmpdir.strpath}"

    cache_class = get_url_buildcache_class(
        layout_version=spack.binary_distribution.CURRENT_BUILD_CACHE_LAYOUT_VERSION
    )
    cache_entry = cache_class(mirror_url, spec, allow_unsigned=True)
    assert cache_entry.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])
    cache_entry.destroy()


def test_buildcache_create_fails_on_noargs(tmpdir):
    """Ensure that buildcache create fails when given no args or
    environment."""
    with pytest.raises(spack.main.SpackCommandError):
        buildcache("push", "--unsigned", str(tmpdir))


def test_buildcache_create_fail_on_perm_denied(install_mockery, mock_fetch, monkeypatch, tmpdir):
    """Ensure that buildcache create fails on permission denied error."""
    install("trivial-install-test-package")

    tmpdir.chmod(0)
    with pytest.raises(OSError) as error:
        buildcache("push", "--unsigned", str(tmpdir), "trivial-install-test-package")
    assert error.value.errno == errno.EACCES
    tmpdir.chmod(0o700)


def test_update_key_index(
    tmpdir,
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    mock_fetch,
    mock_stage,
    mock_gnupghome,
):
    """Test the update-index command with the --keys option"""
    working_dir = tmpdir.join("working_dir")

    mirror_dir = working_dir.join("mirror")
    mirror_url = "file://{0}".format(mirror_dir.strpath)

    mirror("add", "test-mirror", mirror_url)

    gpg("create", "Test Signing Key", "nobody@nowhere.com")

    s = spack.concretize.concretize_one("libdwarf")

    # Install a package
    install("--fake", s.name)

    # Put installed package in the buildcache, which, because we're signing
    # it, should result in the public key getting pushed to the buildcache
    # as well.
    buildcache("push", mirror_dir.strpath, s.name)

    # Now make sure that when we pass the "--keys" argument to update-index
    # it causes the index to get update.
    buildcache("update-index", "--keys", mirror_dir.strpath)

    key_dir_list = os.listdir(
        os.path.join(mirror_dir.strpath, spack.binary_distribution.buildcache_relative_keys_path())
    )

    uninstall("-y", s.name)
    mirror("rm", "test-mirror")

    assert "keys.manifest.json" in key_dir_list


def test_buildcache_autopush(tmp_path, install_mockery, mock_fetch):
    """Test buildcache with autopush"""
    mirror_dir = tmp_path / "mirror"
    mirror_autopush_dir = tmp_path / "mirror_autopush"

    mirror("add", "--unsigned", "mirror", mirror_dir.as_uri())
    mirror("add", "--autopush", "--unsigned", "mirror-autopush", mirror_autopush_dir.as_uri())

    s = spack.concretize.concretize_one("libdwarf")

    # Install and generate build cache index
    PackageInstaller([s.package], fake=True, explicit=True).install()

    assert s.name is not None
    manifest_file = URLBuildcacheEntry.get_manifest_filename(s)
    specs_dirs = os.path.join(
        *URLBuildcacheEntry.get_relative_path_components(BuildcacheComponent.SPEC), s.name
    )

    assert not (mirror_dir / specs_dirs / manifest_file).exists()
    assert (mirror_autopush_dir / specs_dirs / manifest_file).exists()


def test_buildcache_sync(
    mutable_mock_env_path, install_mockery, mock_packages, mock_fetch, mock_stage, tmpdir
):
    """
    Make sure buildcache sync works in an environment-aware manner, ignoring
    any specs that may be in the mirror but not in the environment.
    """
    working_dir = tmpdir.join("working_dir")

    src_mirror_dir = working_dir.join("src_mirror").strpath
    src_mirror_url = "file://{0}".format(src_mirror_dir)

    dest_mirror_dir = working_dir.join("dest_mirror").strpath
    dest_mirror_url = "file://{0}".format(dest_mirror_dir)

    in_env_pkg = "trivial-install-test-package"
    out_env_pkg = "libdwarf"

    def verify_mirror_contents():
        dest_list = os.listdir(
            os.path.join(
                dest_mirror_dir, spack.binary_distribution.buildcache_relative_specs_path()
            )
        )

        found_pkg = False

        for p in dest_list:
            assert out_env_pkg not in p
            if in_env_pkg in p:
                found_pkg = True

        assert found_pkg, f"Expected to find {in_env_pkg} in {dest_mirror_dir}"

    # Install a package and put it in the buildcache
    s = spack.concretize.concretize_one(out_env_pkg)
    install("--fake", s.name)
    buildcache("push", "-u", "-f", src_mirror_url, s.name)

    env("create", "test")
    with ev.read("test"):
        add(in_env_pkg)
        install()
        buildcache("push", "-u", "-f", src_mirror_url, in_env_pkg)

        # Now run the spack buildcache sync command with all the various options
        # for specifying mirrors

        # Use urls to specify mirrors
        buildcache("sync", src_mirror_url, dest_mirror_url)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        # Use local directory paths to specify fs locations
        buildcache("sync", src_mirror_dir, dest_mirror_dir)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        # Use mirror names to specify mirrors
        mirror("add", "src", src_mirror_url)
        mirror("add", "dest", dest_mirror_url)
        mirror("add", "ignored", "file:///dummy/io")

        buildcache("sync", "src", "dest")

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        cache_class = get_url_buildcache_class(
            layout_version=spack.binary_distribution.CURRENT_BUILD_CACHE_LAYOUT_VERSION
        )

        def manifest_insert(manifest, spec, dest_url):
            manifest[spec.dag_hash()] = {
                "src": cache_class.get_manifest_url(spec, src_mirror_url),
                "dest": cache_class.get_manifest_url(spec, dest_url),
            }

        manifest_file = os.path.join(tmpdir.strpath, "manifest_dest.json")
        with open(manifest_file, "w", encoding="utf-8") as fd:
            test_env = ev.active_environment()

            manifest = {}
            for spec in test_env.specs_by_hash.values():
                manifest_insert(manifest, spec, dest_mirror_url)
            json.dump(manifest, fd)

        buildcache("sync", "--manifest-glob", manifest_file)

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)

        manifest_file = os.path.join(tmpdir.strpath, "manifest_bad_dest.json")
        with open(manifest_file, "w", encoding="utf-8") as fd:
            manifest = {}
            for spec in test_env.specs_by_hash.values():
                manifest_insert(manifest, spec, url_util.join(dest_mirror_url, "invalid_path"))
            json.dump(manifest, fd)

        # Trigger the warning
        output = buildcache("sync", "--manifest-glob", manifest_file, "dest", "ignored")

        assert "Ignoring unused arguemnt: ignored" in output

        verify_mirror_contents()
        shutil.rmtree(dest_mirror_dir)


def test_buildcache_create_install(
    mutable_mock_env_path,
    install_mockery,
    mock_packages,
    mock_fetch,
    mock_stage,
    monkeypatch,
    tmpdir,
):
    """ "Ensure that buildcache create creates output files"""
    pkg = "trivial-install-test-package"
    install(pkg)

    buildcache("push", "--unsigned", str(tmpdir), pkg)

    mirror_url = f"file://{tmpdir.strpath}"

    spec = spack.concretize.concretize_one(pkg)
    cache_class = get_url_buildcache_class(
        layout_version=spack.binary_distribution.CURRENT_BUILD_CACHE_LAYOUT_VERSION
    )
    cache_entry = cache_class(mirror_url, spec, allow_unsigned=True)
    assert spec.name is not None
    manifest_path = os.path.join(
        str(tmpdir),
        *cache_class.get_relative_path_components(BuildcacheComponent.SPEC),
        spec.name,
        cache_class.get_manifest_filename(spec),
    )

    assert os.path.exists(manifest_path)
    cache_entry.read_manifest()
    spec_blob_record = cache_entry.get_blob_record(BuildcacheComponent.SPEC)
    tarball_blob_record = cache_entry.get_blob_record(BuildcacheComponent.TARBALL)

    spec_blob_path = os.path.join(
        tmpdir.strpath, *cache_class.get_blob_path_components(spec_blob_record)
    )
    assert os.path.exists(spec_blob_path)

    tarball_blob_path = os.path.join(
        tmpdir.strpath, *cache_class.get_blob_path_components(tarball_blob_record)
    )
    assert os.path.exists(tarball_blob_path)

    cache_entry.destroy()


@pytest.mark.parametrize(
    "things_to_install,expected",
    [
        (
            "",
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
            "dependencies",
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
        ("package", ["dttop"]),
    ],
)
def test_correct_specs_are_pushed(
    things_to_install, expected, tmpdir, monkeypatch, default_mock_concretization, temporary_store
):
    spec = default_mock_concretization("dttop")
    PackageInstaller([spec.package], explicit=True, fake=True).install()
    slash_hash = f"/{spec.dag_hash()}"

    class DontUpload(spack.binary_distribution.Uploader):
        def __init__(self):
            super().__init__(
                spack.mirrors.mirror.Mirror.from_local_path(str(tmpdir)), False, False
            )
            self.pushed = []

        def push(self, specs: List[spack.spec.Spec]):
            self.pushed.extend(s.name for s in specs)
            return [], []  # nothing skipped, nothing errored

    uploader = DontUpload()

    monkeypatch.setattr(
        spack.binary_distribution, "make_uploader", lambda *args, **kwargs: uploader
    )

    buildcache_create_args = ["create", "--unsigned"]

    if things_to_install != "":
        buildcache_create_args.extend(["--only", things_to_install])

    buildcache_create_args.extend([str(tmpdir), slash_hash])

    buildcache(*buildcache_create_args)

    # Order is not guaranteed, so we can't just compare lists
    assert set(uploader.pushed) == set(expected)

    # Ensure no duplicates
    assert len(set(uploader.pushed)) == len(uploader.pushed)


@pytest.mark.parametrize("signed", [True, False])
def test_push_and_install_with_mirror_marked_unsigned_does_not_require_extra_flags(
    tmp_path, mutable_database, mock_gnupghome, signed
):
    """Tests whether marking a mirror as unsigned makes it possible to push and install to/from
    it without requiring extra flags on the command line (and no signing keys configured)."""

    # Create a named mirror with signed set to True or False
    add_flag = "--signed" if signed else "--unsigned"
    mirror("add", add_flag, "my-mirror", str(tmp_path))
    spec = mutable_database.query_local("libelf", installed=True)[0]

    # Push
    if signed:
        # Need to pass "--unsigned" to override the mirror's default
        args = ["push", "--update-index", "--unsigned", "my-mirror", f"/{spec.dag_hash()}"]
    else:
        # No need to pass "--unsigned" if the mirror is unsigned
        args = ["push", "--update-index", "my-mirror", f"/{spec.dag_hash()}"]

    buildcache(*args)

    # Install
    if signed:
        # Need to pass "--no-check-signature" to avoid install errors
        kwargs = {"explicit": True, "cache_only": True, "unsigned": True}
    else:
        # No need to pass "--no-check-signature" if the mirror is unsigned
        kwargs = {"explicit": True, "cache_only": True}

    spec.package.do_uninstall(force=True)
    PackageInstaller([spec.package], **kwargs).install()


def test_skip_no_redistribute(mock_packages, config):
    specs = list(spack.concretize.concretize_one("no-redistribute-dependent").traverse())
    filtered = spack.cmd.buildcache._skip_no_redistribute_for_public(specs)
    assert not any(s.name == "no-redistribute" for s in filtered)
    assert any(s.name == "no-redistribute-dependent" for s in filtered)


def test_best_effort_vs_fail_fast_when_dep_not_installed(tmp_path, mutable_database):
    """When --fail-fast is passed, the push command should fail if it immediately finds an
    uninstalled dependency. Otherwise, failure to push one dependency shouldn't prevent the
    others from being pushed."""

    mirror("add", "--unsigned", "my-mirror", str(tmp_path))

    # Uninstall mpich so that its dependent mpileaks can't be pushed
    for s in mutable_database.query_local("mpich"):
        s.package.do_uninstall(force=True)

    with pytest.raises(spack.cmd.buildcache.PackagesAreNotInstalledError, match="mpich"):
        buildcache("push", "--update-index", "--fail-fast", "my-mirror", "mpileaks^mpich")

    # nothing should be pushed due to --fail-fast.
    assert not os.listdir(tmp_path)
    assert not spack.binary_distribution.update_cache_and_get_specs()

    with pytest.raises(spack.cmd.buildcache.PackageNotInstalledError):
        buildcache("push", "--update-index", "my-mirror", "mpileaks^mpich")

    specs = spack.binary_distribution.update_cache_and_get_specs()

    # everything but mpich should be pushed
    mpileaks = mutable_database.query_local("mpileaks^mpich")[0]
    assert set(specs) == {s for s in mpileaks.traverse() if s.name != "mpich"}


def test_push_without_build_deps(tmp_path, temporary_store, mock_packages, mutable_config):
    """Spack should not error when build deps are uninstalled and --without-build-dependenies is
    passed."""

    mirror("add", "--unsigned", "my-mirror", str(tmp_path))

    s = spack.concretize.concretize_one("dtrun3")
    PackageInstaller([s.package], explicit=True, fake=True).install()
    s["dtbuild3"].package.do_uninstall()

    # fails when build deps are required
    with pytest.raises(spack.error.SpackError, match="package not installed"):
        buildcache(
            "push", "--update-index", "--with-build-dependencies", "my-mirror", f"/{s.dag_hash()}"
        )

    # succeeds when build deps are not required
    buildcache(
        "push", "--update-index", "--without-build-dependencies", "my-mirror", f"/{s.dag_hash()}"
    )
    assert spack.binary_distribution.update_cache_and_get_specs() == [s]


@pytest.fixture(scope="function")
def v2_buildcache_layout(tmp_path):
    def _layout(signedness: str = "signed"):
        source_path = str(pathlib.Path(test_path) / "data" / "mirrors" / "v2_layout" / signedness)
        test_mirror_path = tmp_path / "mirror"
        copy_tree(source_path, test_mirror_path)
        return test_mirror_path

    return _layout


def test_check_mirror_for_layout(v2_buildcache_layout, mutable_config, capsys):
    """Check printed warning in the presence of v2 layout binary mirrors"""
    test_mirror_path = v2_buildcache_layout("unsigned")

    check_mirror_for_layout(spack.mirrors.mirror.Mirror.from_local_path(str(test_mirror_path)))
    err = str(capsys.readouterr()[1])
    assert all([word in err for word in ["Warning", "missing", "layout"]])


def test_url_buildcache_entry_v2_exists(
    capsys, v2_buildcache_layout, mock_packages, mutable_config
):
    """Test existence check for v2 buildcache entries"""
    test_mirror_path = v2_buildcache_layout("unsigned")
    mirror_url = f"file://{test_mirror_path}"
    mirror("add", "v2mirror", mirror_url)

    with capsys.disabled():
        output = buildcache("list", "-a", "-l")

    assert "Fetching an index from a v2 binary mirror layout" in output
    assert "is deprecated" in output

    v2_cache_class = URLBuildcacheEntryV2

    # If you don't give it a spec, it returns False
    build_cache = v2_cache_class(mirror_url)
    assert not build_cache.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])

    spec = spack.concretize.concretize_one("libdwarf")

    # In v2 we have to ask for both, because we need to have the spec to have the tarball
    build_cache = v2_cache_class(mirror_url, spec, allow_unsigned=True)
    assert not build_cache.exists([BuildcacheComponent.TARBALL])
    assert not build_cache.exists([BuildcacheComponent.SPEC])
    # But if we do ask for both, they should be there in this case
    assert build_cache.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])

    spec_path = build_cache._get_spec_url(spec, mirror_url, ext=".spec.json")[7:]
    tarball_path = build_cache._get_tarball_url(spec, mirror_url)[7:]

    os.remove(tarball_path)
    build_cache = v2_cache_class(mirror_url, spec, allow_unsigned=True)
    assert not build_cache.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])

    os.remove(spec_path)
    build_cache = v2_cache_class(mirror_url, spec, allow_unsigned=True)
    assert not build_cache.exists([BuildcacheComponent.SPEC, BuildcacheComponent.TARBALL])


@pytest.mark.parametrize("signing", ["unsigned", "signed"])
def test_install_v2_layout(
    signing,
    capsys,
    v2_buildcache_layout,
    mock_packages,
    mutable_config,
    mutable_mock_env_path,
    install_mockery,
    mock_gnupghome,
    monkeypatch,
):
    """Ensure we can still install from signed and unsigned v2 buildcache"""
    test_mirror_path = v2_buildcache_layout(signing)
    mirror("add", "my-mirror", str(test_mirror_path))

    # Trust original signing key (no-op if this is the unsigned pass)
    buildcache("keys", "--install", "--trust")

    with capsys.disabled():
        output = install("--fake", "--no-check-signature", "libdwarf")

    assert "Extracting libelf" in output
    assert "libelf: Successfully installed" in output
    assert "Extracting libdwarf" in output
    assert "libdwarf: Successfully installed" in output
    assert "Installing a spec from a v2 binary mirror layout" in output
    assert "is deprecated" in output


def test_basic_migrate_unsigned(capsys, v2_buildcache_layout, mutable_config):
    """Make sure first unsigned migration results in usable buildcache,
    leaving the previous layout in place. Also test that a subsequent one
    doesn't need to migrate anything, and that using --delete-existing
    removes the previous layout"""

    test_mirror_path = v2_buildcache_layout("unsigned")
    mirror("add", "my-mirror", str(test_mirror_path))

    with capsys.disabled():
        output = buildcache("migrate", "--unsigned", "my-mirror")

    # The output indicates both specs were migrated
    assert output.count("Successfully migrated") == 6

    build_cache_path = str(test_mirror_path / "build_cache")

    # Without "--delete-existing" and "--yes-to-all", migration leaves the
    # previous layout in place
    assert os.path.exists(build_cache_path)
    assert os.path.isdir(build_cache_path)

    # Now list the specs available under the new layout
    with capsys.disabled():
        output = buildcache("list", "--allarch")

    assert "libdwarf" in output and "libelf" in output

    with capsys.disabled():
        output = buildcache(
            "migrate", "--unsigned", "--delete-existing", "--yes-to-all", "my-mirror"
        )

    # A second migration of the same mirror indicates neither spec
    # needs to be migrated
    assert output.count("No need to migrate") == 6

    # When we provide "--delete-existing" and "--yes-to-all", migration
    # removes the old layout
    assert not os.path.exists(build_cache_path)


def test_basic_migrate_signed(
    capsys, v2_buildcache_layout, monkeypatch, mock_gnupghome, mutable_config
):
    """Test a signed migration requires a signing key, requires the public
    key originally used to sign the pkgs, fails and prints reasonable messages
    if those requirements are unmet, and eventually succeeds when they are met."""
    test_mirror_path = v2_buildcache_layout("signed")
    mirror("add", "my-mirror", str(test_mirror_path))

    with pytest.raises(migrate.MigrationException) as error:
        buildcache("migrate", "my-mirror")

    # Without a signing key spack fails and explains why
    assert error.value.message == "Signed migration requires exactly one secret key in keychain"

    # Create a signing key and trust the key used to sign the pkgs originally
    gpg("create", "New Test Signing Key", "noone@nowhere.org")

    with capsys.disabled():
        output = buildcache("migrate", "my-mirror")

    # Without trusting the original signing key, spack fails with an explanation
    assert "Failed to verify signature of libelf" in output
    assert "Failed to verify signature of libdwarf" in output
    assert "did you mean to perform an unsigned migration" in output

    # Trust original signing key (since it's in the original layout location,
    # this is where the monkeypatched attribute is used)
    with capsys.disabled():
        output = buildcache("keys", "--install", "--trust")

    with capsys.disabled():
        output = buildcache("migrate", "my-mirror")

    # Once we have the proper keys, migration should succeed
    assert "Successfully migrated libelf" in output
    assert "Successfully migrated libelf" in output

    # Now list the specs available under the new layout
    with capsys.disabled():
        output = buildcache("list", "--allarch")

    assert "libdwarf" in output and "libelf" in output


def test_unsigned_migrate_of_signed_mirror(capsys, v2_buildcache_layout, mutable_config):
    """Test spack can do an unsigned migration of a signed buildcache by
    ignoring signatures and skipping re-signing."""

    test_mirror_path = v2_buildcache_layout("signed")
    mirror("add", "my-mirror", str(test_mirror_path))

    with capsys.disabled():
        output = buildcache(
            "migrate", "--unsigned", "--delete-existing", "--yes-to-all", "my-mirror"
        )

    # Now list the specs available under the new layout
    with capsys.disabled():
        output = buildcache("list", "--allarch")

    assert "libdwarf" in output and "libelf" in output

    # We should find two spec manifest files, one for each spec
    file_list = find(test_mirror_path, "*.spec.manifest.json")
    assert len(file_list) == 6
    assert any(["libdwarf" in file for file in file_list])
    assert any(["libelf" in file for file in file_list])

    # The two spec manifest files should be unsigned
    for file_path in file_list:
        with open(file_path, "r", encoding="utf-8") as fd:
            assert json.load(fd)


def test_migrate_requires_index(capsys, v2_buildcache_layout, mutable_config):
    """Test spack fails with a reasonable error message when mirror does
    not have an index"""

    test_mirror_path = v2_buildcache_layout("unsigned")
    v2_index_path = test_mirror_path / "build_cache" / "index.json"
    v2_index_hash_path = test_mirror_path / "build_cache" / "index.json.hash"
    os.remove(str(v2_index_path))
    os.remove(str(v2_index_hash_path))

    mirror("add", "my-mirror", str(test_mirror_path))

    with pytest.raises(migrate.MigrationException) as error:
        buildcache("migrate", "--unsigned", "my-mirror")

    # If the buildcache has no index, spack fails and explains why
    assert error.value.message == "Buildcache migration requires a buildcache index"

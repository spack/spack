# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import os
import shutil

import pytest

import spack.binary_distribution
import spack.cmd.buildcache
import spack.environment as ev
import spack.main
import spack.spec
import spack.util.url
from spack.spec import Spec

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


def test_buildcache_preview_just_runs():
    # TODO: remove in Spack 0.21
    buildcache("preview", "mpileaks")


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


def tests_buildcache_create(install_mockery, mock_fetch, monkeypatch, tmpdir):
    """ "Ensure that buildcache create creates output files"""
    pkg = "trivial-install-test-package"
    install(pkg)

    buildcache("push", "--unsigned", str(tmpdir), pkg)

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


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

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


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

    s = Spec("libdwarf").concretized()

    # Install a package
    install(s.name)

    # Put installed package in the buildcache, which, because we're signing
    # it, should result in the public key getting pushed to the buildcache
    # as well.
    buildcache("push", mirror_dir.strpath, s.name)

    # Now make sure that when we pass the "--keys" argument to update-index
    # it causes the index to get update.
    buildcache("update-index", "--keys", mirror_dir.strpath)

    key_dir_list = os.listdir(os.path.join(mirror_dir.strpath, "build_cache", "_pgp"))

    uninstall("-y", s.name)
    mirror("rm", "test-mirror")

    assert "index.json" in key_dir_list


def test_buildcache_sync(
    mutable_mock_env_path,
    install_mockery_mutable_config,
    mock_packages,
    mock_fetch,
    mock_stage,
    tmpdir,
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
        dest_list = os.listdir(os.path.join(dest_mirror_dir, "build_cache"))

        found_pkg = False

        for p in dest_list:
            assert out_env_pkg not in p
            if in_env_pkg in p:
                found_pkg = True

        if not found_pkg:
            print("Expected to find {0} in {1}".format(in_env_pkg, dest_mirror_dir))
            assert False

    # Install a package and put it in the buildcache
    s = Spec(out_env_pkg).concretized()
    install(s.name)
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

        buildcache("sync", "src", "dest")

        verify_mirror_contents()


def test_buildcache_create_install(
    mutable_mock_env_path,
    install_mockery_mutable_config,
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

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, ".spack")
    tarball = spack.binary_distribution.tarball_name(spec, ".spec.json")
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball_path))
    assert os.path.exists(os.path.join(str(tmpdir), "build_cache", tarball))


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
    # Concretize dttop and add it to the temporary database (without prefixes)
    spec = default_mock_concretization("dttop")
    temporary_store.db.add(spec, directory_layout=None)
    slash_hash = "/{0}".format(spec.dag_hash())

    packages_to_push = []

    def fake_push(node, push_url, options):
        assert isinstance(node, Spec)
        packages_to_push.append(node.name)

    monkeypatch.setattr(spack.binary_distribution, "push_or_raise", fake_push)

    buildcache_create_args = ["create", "--unsigned"]

    if things_to_install != "":
        buildcache_create_args.extend(["--only", things_to_install])

    buildcache_create_args.extend([str(tmpdir), slash_hash])

    buildcache(*buildcache_create_args)

    # Order is not guaranteed, so we can't just compare lists
    assert set(packages_to_push) == set(expected)

    # Ensure no duplicates
    assert len(set(packages_to_push)) == len(packages_to_push)

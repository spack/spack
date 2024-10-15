# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
""" Test ABI-based splicing of dependencies """

import os

import pytest

import spack.config
import spack.package_base
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
from spack.installer import PackageInstaller
from spack.spec import Spec


@pytest.fixture
def abi_splice_repo(mutable_config):
    repo = os.path.join(spack.paths.repos_path, "abi_splice.test")
    with spack.repo.use_repositories(repo) as mock_repo:
        yield mock_repo


def _mock_has_runtime_dependencies(_x):
    return True


def test_simple_reuse(mutable_database, abi_splice_repo, mutable_config, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    foo = Spec("foo@1.0.0+compat").concretized()
    PackageInstaller([foo.package], fake=True, explicit=True).install()
    spack.config.set("packages", {"foo": {"buildable": False}})
    Spec("foo").concretized()
    foo.package.do_uninstall()
    assert True


def test_simple_dep_reuse(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    foo = Spec("foo@1.0.0+compat").concretized()
    PackageInstaller([foo.package], fake=True, explicit=True).install()
    bar = Spec("bar@1").concretized()
    assert foo in bar.dependencies()
    foo.package.do_uninstall()


def test_splice_installed_hash(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    new_bar = Spec("bar@1.0.2+compat").concretized()
    PackageInstaller([old_baz.package], fake=True, explicit=True).install()
    PackageInstaller([new_bar.package], fake=True, explicit=True).install()
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    goal_spec.concretized()
    old_baz.package.do_uninstall()
    new_bar.package.do_uninstall()
    assert True


def test_splice_build_dep(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    old_baz = Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat").concretized()
    PackageInstaller([old_baz.package], fake=True, explicit=True).install()
    baz_config = {"baz": {"buildable": False}}
    spack.config.set("packages", baz_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.0+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    goal_spec.concretized()
    old_baz.package.do_uninstall()
    assert True


def test_mpi_splices(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    mpileaks_openmpi = Spec("mpileaks ^openmpi").concretized()
    mpileaks_mpich = Spec("mpileaks ^mpich").concretized()
    PackageInstaller([mpileaks_openmpi.package], fake=True, explicit=True).install()
    PackageInstaller([mpileaks_mpich.package], fake=True, explicit=True).install()
    mpileaks_config = {"mpileaks": {"buildable": False}}
    spack.config.set("packages", mpileaks_config)
    openmpi_goal_spec = Spec("mpileaks ^xmpi abi=openmpi")
    mpich_goal_spec = Spec("mpileaks ^xmpi abi=mpich")
    with pytest.raises(Exception):
        openmpi_goal_spec.concretized()
    with pytest.raises(Exception):
        mpich_goal_spec.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    openmpi_goal_spec.concretized()
    mpich_goal_spec.concretized()
    mpileaks_openmpi.package.do_uninstall()
    mpileaks_mpich.package.do_uninstall()
    assert True


def test_double_splice(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        Spec("baz@1 ^bar@1.0.0+compat ^foo@1.0.0+compat"),
        Spec("bar@1.0.2+compat ^foo@1.0.1+compat"),
        Spec("foo@1.0.2+compat"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    freeze_builds_config = {
        "baz": {"buildable": False},
        "bar": {"buildable": False},
        "foo": {"buildable": False},
    }
    spack.config.set("packages", freeze_builds_config)
    goal_spec = Spec("baz@1 ^bar@1.0.2+compat ^foo@1.0.2+compat")
    with pytest.raises(Exception):
        goal_spec.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    goal_spec.concretized()
    for s in cache:
        s.package.do_uninstall()


def test_manyvariant_star_matching_variant_splice(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        # can_splice("manyvariants@1.0.0", when="@1.0.1", match_variants="*")
        Spec("depends-on-manyvariants ^manyvariants@1.0.0+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.0~a~b c=v3 d=v3"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    goal_specs = [
        Spec("depends-on-manyvariants ^manyvariants@1.0.1+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.1~a~b c=v3 d=v3"),
    ]
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    spack.config.set("packages", freeze_build_config)
    for goal in goal_specs:
        with pytest.raises(Exception):
            goal.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    for goal in goal_specs:
        goal.concretized()

    for s in cache:
        s.package.do_uninstall()
    assert True


def test_manyvariant_limited_matching(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [
        # can_splice("manyvariants@2.0.0+a~b", when="@2.0.1~a+b", match_variants=["c", "d"])
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.0+a~b c=v3 d=v2"),
        # can_splice("manyvariants@2.0.0 c=v1 d=v1", when="@2.0.1+a+b")
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.0~a~b c=v1 d=v1"),
    ]
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    goal_specs = [
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1~a+b c=v3 d=v2"),
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1+a+b c=v3 d=v3"),
    ]
    freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
    spack.config.set("packages", freeze_build_config)
    for s in goal_specs:
        with pytest.raises(Exception):
            s.concretized()
    spack.config.set("concretizer:splice", {"automatic": True})
    for s in goal_specs:
        s.concretized()
    for s in cache:
        s.package.do_uninstall()

    assert True


def test_external_splice_same_name(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [Spec("bar@1.0.0 ^foo@1.0.0+compat"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.1+compat")]
    packages_yaml = {
        "foo": {"externals": [{"spec": "foo@1.0.2+compat", "prefix": "/usr"}], "buildable": True},
        "bar": {"buildable": True},
    }
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    spack.config.set("packages", packages_yaml)
    goal_specs = [Spec("bar@1.0.0 ^foo@1.0.2"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.2")]
    spack.config.set("concretizer:splice", {"automatic": True})
    for s in goal_specs:
        s.concretized()


def test_external_splice_mpi(mutable_database, abi_splice_repo, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )
    cache = [Spec("bar@1.0.0 ^foo@1.0.0+compat"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.1+compat")]
    packages_yaml = {
        "foo": {"externals": [{"spec": "foo@1.0.2+compat", "prefix": "/usr"}], "buildable": True},
        "bar": {"buildable": True},
    }
    for s in cache:
        s.concretize()
        PackageInstaller([s.package], fake=True, explicit=True).install()
    spack.config.set("packages", packages_yaml)
    goal_specs = [Spec("bar@1.0.0 ^foo@1.0.2"), Spec("baz@1.0 ^bar@1.0.1 ^foo@1.0.2")]
    spack.config.set("concretizer:splice", {"automatic": True})
    for s in goal_specs:
        s.concretized()

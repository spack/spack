# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
""" Test ABI-based splicing of dependencies """

from typing import List

import pytest

import spack.config
import spack.package_base
import spack.paths
import spack.repo
import spack.solver.asp
import spack.spec
from spack.installer import PackageInstaller
from spack.spec import Spec


class CacheManager:
    def __init__(self, specs: List[str]) -> None:
        self.req_specs = specs
        self.concr_specs: List[Spec]
        self.concr_specs = []

    def __enter__(self):
        self.concr_specs = [Spec(s).concretized() for s in self.req_specs]
        for s in self.concr_specs:
            PackageInstaller([s.package], fake=True, explicit=True).install()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for s in self.concr_specs:
            s.package.do_uninstall()


# MacOS and Windows only work if you pass this function pointer rather than a
# closure
def _mock_has_runtime_dependencies(_x):
    return True


def _make_specs_non_buildable(specs: List[str]):
    output_config = {}
    for spec in specs:
        output_config[spec] = {"buildable": False}
    return output_config


@pytest.fixture
def splicing_setup(mutable_database, mock_packages, monkeypatch):
    spack.config.set("concretizer:reuse", True)
    monkeypatch.setattr(
        spack.solver.asp, "_has_runtime_dependencies", _mock_has_runtime_dependencies
    )


def _enable_splicing():
    spack.config.set("concretizer:splice", {"automatic": True})


def test_simple_reuse(splicing_setup):
    with CacheManager(["splice-z@1.0.0+compat"]):
        spack.config.set("packages", _make_specs_non_buildable(["splice-z"]))
        Spec("splice-z").concretized()
    assert True


def test_simple_dep_reuse(splicing_setup):
    with CacheManager(["splice-z@1.0.0+compat"]):
        spack.config.set("packages", _make_specs_non_buildable(["splice-z"]))
        Spec("splice-h@1").concretized()
    assert True


def test_splice_installed_hash(splicing_setup):
    cache = [
        "splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0",
        "splice-h@1.0.2+compat ^splice-z@1.0.0",
    ]
    with CacheManager(cache):
        packages_config = _make_specs_non_buildable(["splice-t", "splice-h"])
        spack.config.set("packages", packages_config)
        goal_spec = Spec("splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.0")
        with pytest.raises(Exception):
            goal_spec.concretized()
        _enable_splicing()
        goal_spec.concretized()
    assert True


def test_splice_build_splice_node(splicing_setup):
    with CacheManager(["splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0+compat"]):
        spack.config.set("packages", _make_specs_non_buildable(["splice-t"]))
        goal_spec = Spec("splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.0+compat")
        with pytest.raises(Exception):
            goal_spec.concretized()
        _enable_splicing()
        goal_spec.concretized()
    assert True


def test_double_splice(splicing_setup):
    cache = [
        "splice-t@1 ^splice-h@1.0.0+compat ^splice-z@1.0.0+compat",
        "splice-h@1.0.2+compat ^splice-z@1.0.1+compat",
        "splice-z@1.0.2+compat",
    ]
    with CacheManager(cache):
        freeze_builds_config = _make_specs_non_buildable(["splice-t", "splice-h", "splice-z"])
        spack.config.set("packages", freeze_builds_config)
        goal_spec = Spec("splice-t@1 ^splice-h@1.0.2+compat ^splice-z@1.0.2+compat")
        with pytest.raises(Exception):
            goal_spec.concretized()
        _enable_splicing()
        goal_spec.concretized()


# The next two tests are mirrors of one another
def test_virtual_multi_splices_in(splicing_setup):
    cache = [
        "depends-on-virtual-with-abi ^virtual-abi-1",
        "depends-on-virtual-with-abi ^virtual-abi-2",
    ]
    goal_specs = [
        "depends-on-virtual-with-abi ^virtual-abi-multi abi=one",
        "depends-on-virtual-with-abi ^virtual-abi-multi abi=two",
    ]
    with CacheManager(cache):
        spack.config.set("packages", _make_specs_non_buildable(["depends-on-virtual-with-abi"]))
        with pytest.raises(Exception):
            for gs in goal_specs:
                Spec(gs).concretized()
        _enable_splicing()
        for gs in goal_specs:
            Spec(gs).concretized()


def test_virtual_multi_can_be_spliced(splicing_setup):
    cache = [
        "depends-on-virtual-with-abi ^virtual-abi-multi abi=one",
        "depends-on-virtual-with-abi ^virtual-abi-multi abi=two",
    ]
    goal_specs = [
        "depends-on-virtual-with-abi ^virtual-abi-1",
        "depends-on-virtual-with-abi ^virtual-abi-2",
    ]
    with CacheManager(cache):
        spack.config.set("packages", _make_specs_non_buildable(["depends-on-virtual-with-abi"]))
        with pytest.raises(Exception):
            for gs in goal_specs:
                Spec(gs).concretized()
        _enable_splicing()
        for gs in goal_specs:
            Spec(gs).concretized()


def test_manyvariant_star_matching_variant_splice(splicing_setup):
    cache = [
        # can_splice("manyvariants@1.0.0", when="@1.0.1", match_variants="*")
        "depends-on-manyvariants ^manyvariants@1.0.0+a+b c=v1 d=v2",
        "depends-on-manyvariants ^manyvariants@1.0.0~a~b c=v3 d=v3",
    ]
    goal_specs = [
        Spec("depends-on-manyvariants ^manyvariants@1.0.1+a+b c=v1 d=v2"),
        Spec("depends-on-manyvariants ^manyvariants@1.0.1~a~b c=v3 d=v3"),
    ]
    with CacheManager(cache):
        freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
        spack.config.set("packages", freeze_build_config)
        for goal in goal_specs:
            with pytest.raises(Exception):
                goal.concretized()
        _enable_splicing()
        for goal in goal_specs:
            goal.concretized()

    assert True


def test_manyvariant_limited_matching(splicing_setup):
    cache = [
        # can_splice("manyvariants@2.0.0+a~b", when="@2.0.1~a+b", match_variants=["c", "d"])
        "depends-on-manyvariants@2.0 ^manyvariants@2.0.0+a~b c=v3 d=v2",
        # can_splice("manyvariants@2.0.0 c=v1 d=v1", when="@2.0.1+a+b")
        "depends-on-manyvariants@2.0 ^manyvariants@2.0.0~a~b c=v1 d=v1",
    ]
    goal_specs = [
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1~a+b c=v3 d=v2"),
        Spec("depends-on-manyvariants@2.0 ^manyvariants@2.0.1+a+b c=v3 d=v3"),
    ]
    with CacheManager(cache):
        freeze_build_config = {"depends-on-manyvariants": {"buildable": False}}
        spack.config.set("packages", freeze_build_config)
        for s in goal_specs:
            with pytest.raises(Exception):
                s.concretized()
        _enable_splicing()
        for s in goal_specs:
            s.concretized()
    assert True


def test_external_splice_same_name(splicing_setup):
    cache = [
        "splice-h@1.0.0 ^splice-z@1.0.0+compat",
        "splice-t@1.0 ^splice-h@1.0.1 ^splice-z@1.0.1+compat",
    ]
    packages_yaml = {
        "splice-z": {"externals": [{"spec": "splice-z@1.0.2+compat", "prefix": "/usr"}]}
    }
    goal_specs = [
        Spec("splice-h@1.0.0 ^splice-z@1.0.2"),
        Spec("splice-t@1.0 ^splice-h@1.0.1 ^splice-z@1.0.2"),
    ]
    with CacheManager(cache):
        spack.config.set("packages", packages_yaml)
        _enable_splicing()
        for s in goal_specs:
            s.concretized()
    assert True

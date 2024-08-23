# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import sys

import pytest

import spack.rewiring
import spack.store
from spack.installer import PackageInstaller
from spack.spec import Spec
from spack.test.relocate import text_in_bin

args = ["file"]
if sys.platform == "darwin":
    args.extend(["/usr/bin/clang++", "install_name_tool"])
else:
    args.extend(["g++", "patchelf"])


@pytest.mark.requires_executables(*args)
@pytest.mark.parametrize("transitive", [True, False])
def test_rewire_db(mock_fetch, install_mockery, transitive):
    """Tests basic rewiring without binary executables."""
    spec = Spec("splice-t^splice-h~foo").concretized()
    dep = Spec("splice-h+foo").concretized()
    PackageInstaller([spec.package, dep.package], explicit=True).install()
    spliced_spec = spec.splice(dep, transitive=transitive)
    assert spec.dag_hash() != spliced_spec.dag_hash()

    spack.rewiring.rewire(spliced_spec)

    # check that the prefix exists
    assert os.path.exists(spliced_spec.prefix)

    # test that it made it into the database
    rec = spack.store.STORE.db.get_record(spliced_spec)
    installed_in_db = rec.installed if rec else False
    assert installed_in_db

    # check the file in the prefix has the correct paths
    for node in spliced_spec.traverse(root=True):
        text_file_path = os.path.join(node.prefix, node.name)
        with open(text_file_path, "r") as f:
            text = f.read()
            for modded_spec in node.traverse(root=True, deptype=("link", "run")):
                assert modded_spec.prefix in text


@pytest.mark.requires_executables(*args)
@pytest.mark.parametrize("transitive", [True, False])
def test_rewire_bin(mock_fetch, install_mockery, transitive):
    """Tests basic rewiring with binary executables."""
    spec = Spec("quux").concretized()
    dep = Spec("garply cflags=-g").concretized()
    PackageInstaller([spec.package, dep.package], explicit=True).install()
    spliced_spec = spec.splice(dep, transitive=transitive)

    assert spec.dag_hash() != spliced_spec.dag_hash()

    spack.rewiring.rewire(spliced_spec)

    # check that the prefix exists
    assert os.path.exists(spliced_spec.prefix)

    # test that it made it into the database
    rec = spack.store.STORE.db.get_record(spliced_spec)
    installed_in_db = rec.installed if rec else False
    assert installed_in_db

    # check the file in the prefix has the correct paths
    bin_names = {"garply": "garplinator", "corge": "corgegator", "quux": "quuxifier"}
    for node in spliced_spec.traverse(root=True):
        for dep in node.traverse(root=True):
            bin_file_path = os.path.join(dep.prefix.bin, bin_names[dep.name])
            assert text_in_bin(dep.prefix, bin_file_path)


@pytest.mark.requires_executables(*args)
def test_rewire_writes_new_metadata(mock_fetch, install_mockery):
    """Tests that new metadata was written during a rewire.
    Accuracy of metadata is left to other tests."""
    spec = Spec("quux").concretized()
    dep = Spec("garply cflags=-g").concretized()
    PackageInstaller([spec.package, dep.package], explicit=True).install()
    spliced_spec = spec.splice(dep, transitive=True)
    spack.rewiring.rewire(spliced_spec)

    # test install manifests
    for node in spliced_spec.traverse(root=True):
        spack.store.STORE.layout.ensure_installed(node)
        manifest_file_path = os.path.join(
            node.prefix,
            spack.store.STORE.layout.metadata_dir,
            spack.store.STORE.layout.manifest_file_name,
        )
        assert os.path.exists(manifest_file_path)
        orig_node = spec[node.name]
        if node == orig_node:
            continue
        orig_manifest_file_path = os.path.join(
            orig_node.prefix,
            spack.store.STORE.layout.metadata_dir,
            spack.store.STORE.layout.manifest_file_name,
        )
        assert os.path.exists(orig_manifest_file_path)
        assert not filecmp.cmp(orig_manifest_file_path, manifest_file_path, shallow=False)
        specfile_path = os.path.join(
            node.prefix,
            spack.store.STORE.layout.metadata_dir,
            spack.store.STORE.layout.spec_file_name,
        )
        assert os.path.exists(specfile_path)
        orig_specfile_path = os.path.join(
            orig_node.prefix,
            spack.store.STORE.layout.metadata_dir,
            spack.store.STORE.layout.spec_file_name,
        )
        assert os.path.exists(orig_specfile_path)
        assert not filecmp.cmp(orig_specfile_path, specfile_path, shallow=False)


@pytest.mark.requires_executables(*args)
@pytest.mark.parametrize("transitive", [True, False])
def test_uninstall_rewired_spec(mock_fetch, install_mockery, transitive):
    """Test that rewired packages can be uninstalled as normal."""
    spec = Spec("quux").concretized()
    dep = Spec("garply cflags=-g").concretized()
    PackageInstaller([spec.package, dep.package], explicit=True).install()
    spliced_spec = spec.splice(dep, transitive=transitive)
    spack.rewiring.rewire(spliced_spec)
    spliced_spec.package.do_uninstall()
    assert len(spack.store.STORE.db.query(spliced_spec)) == 0
    assert not os.path.exists(spliced_spec.prefix)


@pytest.mark.requires_executables(*args)
def test_rewire_not_installed_fails(mock_fetch, install_mockery):
    """Tests error when an attempt is made to rewire a package that was not
    previously installed."""
    spec = Spec("quux").concretized()
    dep = Spec("garply cflags=-g").concretized()
    spliced_spec = spec.splice(dep, False)
    with pytest.raises(
        spack.rewiring.PackageNotInstalledError,
        match="failed due to missing install of build spec",
    ):
        spack.rewiring.rewire(spliced_spec)


@pytest.mark.parametrize("transitive", [True, False])
def test_rewire_virtual(mock_fetch, install_mockery, transitive):
    """Check installed package can successfully splice an alternate virtual implementation"""
    dep = "splice-a"
    alt_dep = "splice-h"

    spec = Spec(f"splice-vt^{dep}").concretized()
    spec.package.do_install()

    alt_spec = Spec(alt_dep).concretized()
    alt_spec.package.do_install()

    spliced_spec = spec.splice(alt_spec, transitive)
    spack.rewiring.rewire(spliced_spec)

    # Confirm the original spec still has the original virtual implementation.
    assert spec.satisfies(f"^{dep}")

    # Confirm the spliced spec uses the new virtual implementation.
    assert spliced_spec.satisfies(f"^{alt_dep}")

    # Confirm expected provenance.
    #
    # Expanded dependencies for the spec with dependency and alternate show
    # significant re-use with the spec, original dependency, and spliced
    # dependency.
    #
    #   with dependency     with alternate dependency
    #   ---------------     -------------------------
    #   splice-vt       =>  splice-vt'
    #     glibc               glibc
    #     splice-a      =>    splice-h
    #       glibc               glibc
    #       splice-z            splice-z
    #     splice-z            splice-z
    #
    # The spliced spec will have the provenance of the spec. The provenance
    # of dependency specs will only be updated if they are intransitively
    # sliced.

    assert spec._build_spec is None
    assert spliced_spec._build_spec == spec, "Expected spec for provenance"

    # Confirm no provenance updates were made to unchanged specs/dependencies
    # and to changed dependencies when intransitive.
    fmt = "{0}: Expected no provenance updates to the {1} spec"

    def confirm_unchanged(spec_tuple):
        for s, _type in spec_tuple:
            assert s._build_spec is None, fmt.format(s.name, _type)

    specs = [(spec, "original spec")]
    specs.extend([(d, "original dependency") for d in spec.dependencies()])
    confirm_unchanged(specs)

    specs = []
    for d in spliced_spec.dependencies():
        if not transitive and d.satisfies(alt_dep):
            assert d._build_spec is not None, f"{d.name}: Expected provenance update (to self)"
            continue
        specs.append((d, "spliced dependency"))
    confirm_unchanged(specs)

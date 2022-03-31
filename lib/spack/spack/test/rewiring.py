# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os
import sys

import pytest

import spack.rewiring
import spack.store
from spack.spec import Spec
from spack.test.relocate import text_in_bin


@pytest.mark.parametrize('transitive', [True, False])
def test_rewire(mock_fetch, install_mockery, transitive):
    spec = Spec('splice-t^splice-h~foo').concretized()
    dep = Spec('splice-h+foo').concretized()
    spec.package.do_install()
    dep.package.do_install()
    spliced_spec = spec.splice(dep, transitive=transitive)
    assert spec.dag_hash() != spliced_spec.dag_hash()

    spack.rewiring.rewire(spliced_spec)

    # check that the prefix exists
    assert os.path.exists(spliced_spec.prefix)

    # test that it made it into the database
    rec = spack.store.db.get_record(spliced_spec)
    installed_in_db = rec.installed if rec else False
    assert installed_in_db

    # check the file in the prefix has the correct paths
    for node in spliced_spec.traverse(root=True):
        text_file_path = os.path.join(node.prefix, node.name)
        with open(text_file_path, 'r') as f:
            text = f.read()
            for modded_spec in node.traverse(root=True):
                assert modded_spec.prefix in text


args = ['strings', 'file']
if sys.platform == 'darwin':
    args.extend(['/usr/bin/clang++', 'install_name_tool'])
else:
    args.extend(['/usr/bin/g++', 'patchelf'])


@pytest.mark.requires_executables(*args)
@pytest.mark.parametrize('transitive', [True, False])
def test_rewire_bin(mock_fetch, install_mockery, transitive):
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install()
    dep.package.do_install()
    spliced_spec = spec.splice(dep, transitive=transitive)
    assert spec.dag_hash() != spliced_spec.dag_hash()

    spack.rewiring.rewire(spliced_spec)

    # check that the prefix exists
    assert os.path.exists(spliced_spec.prefix)

    # test that it made it into the database
    rec = spack.store.db.get_record(spliced_spec)
    installed_in_db = rec.installed if rec else False
    assert installed_in_db

    # check the file in the prefix has the correct paths
    bin_names = {'garply': 'garplinator',
                 'corge': 'corgegator',
                 'quux': 'quuxifier'}
    for node in spliced_spec.traverse(root=True):
        for dep in node.traverse(root=True):
            bin_file_path = os.path.join(dep.prefix.bin, bin_names[dep.name])
            assert text_in_bin(dep.prefix, bin_file_path)


@pytest.mark.requires_executables(*args)
def test_rewire_writes_new_metadata(mock_fetch, install_mockery):
    # check for spec.json and install_manifest.json and that they are new
    # for a simple case.
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install()
    dep.package.do_install()
    spliced_spec = spec.splice(dep, transitive=True)
    spack.rewiring.rewire(spliced_spec)

    # test install manifests
    for node in spliced_spec.traverse(root=True):
        spack.store.layout.ensure_installed(node)
        manifest_file_path = os.path.join(node.prefix,
                                          spack.store.layout.metadata_dir,
                                          spack.store.layout.manifest_file_name)
        assert os.path.exists(manifest_file_path)
        orig_node = spec[node.name]
        orig_manifest_file_path = os.path.join(orig_node.prefix,
                                               spack.store.layout.metadata_dir,
                                               spack.store.layout.manifest_file_name)
        assert os.path.exists(orig_manifest_file_path)
        assert not filecmp.cmp(orig_manifest_file_path, manifest_file_path,
                               shallow=False)
        specfile_path = os.path.join(node.prefix,
                                     spack.store.layout.metadata_dir,
                                     spack.store.layout.spec_file_name)
        assert os.path.exists(specfile_path)
        orig_specfile_path = os.path.join(orig_node.prefix,
                                          spack.store.layout.metadata_dir,
                                          spack.store.layout.spec_file_name)
        assert os.path.exists(orig_specfile_path)
        assert not filecmp.cmp(orig_specfile_path, specfile_path,
                               shallow=False)


@pytest.mark.requires_executables(*args)
@pytest.mark.parametrize('transitive', [True, False])
def test_uninstall_rewired_spec(mock_fetch, install_mockery, transitive):
    # Test that rewired packages can be uninstalled as normal.
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install()
    dep.package.do_install()
    spliced_spec = spec.splice(dep, transitive=transitive)
    spack.rewiring.rewire(spliced_spec)
    spliced_spec.package.do_uninstall()
    assert len(spack.store.db.query(spliced_spec)) == 0
    assert not os.path.exists(spliced_spec.prefix)


@pytest.mark.requires_executables(*args)
def test_rewire_not_installed_fails(mock_fetch, install_mockery):
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spliced_spec = spec.splice(dep, False)
    with pytest.raises(spack.rewiring.PackageNotInstalledError,
                       match="failed due to missing install of build spec"):
        spack.rewiring.rewire(spliced_spec)

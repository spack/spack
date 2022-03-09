# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import os

import pytest

import spack.rewiring
import spack.store
from spack.spec import Spec
from spack.test.relocate import text_in_bin


@pytest.mark.parametrize('transitive', [True, False])
def test_rewire(mock_fetch, install_mockery, transitive):
    spec = Spec('splice-t^splice-h~foo').concretized()
    dep = Spec('splice-h+foo').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
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


@pytest.mark.parametrize('transitive', [True, False])
def test_rewire_bin(mock_fetch, install_mockery, transitive):
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
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


def test_rewire_writes_new_metadata(mock_fetch, install_mockery):
    # check for spec.json and install_manifest.json and that they are new
    # for a simple case.
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
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

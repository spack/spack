# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    assert spec is not spliced_spec
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
        text = ''
        with open(text_file_path, 'r') as f:
            text = f.read()
        for modded_spec in node.traverse(root=True):
            assert modded_spec.prefix in text
        # test install manifest
        assert spack.store.layout.check_installed(node)
        manifest_file_path = os.path.join(node.prefix,
                                          spack.store.layout.metadata_dir,
                                          spack.store.layout.manifest_file_name)
        assert os.path.exists(manifest_file_path)
        # monkeypatch the modulefile_generation hook to an accumulator


@pytest.mark.parametrize('transitive', [True, False])
def test_rewire_bin(mock_fetch, install_mockery, transitive):
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
    spliced_spec = spec.splice(dep, transitive=transitive)
    assert spec is not spliced_spec
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
        # test install manifest
        assert spack.store.layout.check_installed(node)
        manifest_file_path = os.path.join(node.prefix,
                                          spack.store.layout.metadata_dir,
                                          spack.store.layout.manifest_file_name)
        assert os.path.exists(manifest_file_path)

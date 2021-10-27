# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from glob import glob

import spack.rewiring
from spack.spec import Spec
from spack.test.relocate import text_in_bin


def test_rewire(mock_fetch, install_mockery):
    spec = Spec('splice-t^splice-h~foo').concretized()
    dep = Spec('splice-h+foo').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
    spliced_spec = spec.splice(dep, transitive=False)
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
        # monkeypatch the modulefile_generation hook to an accumulator and make
        # sure that it’s called with all of the arguments you would expect


def test_rewire_bin(mock_fetch, install_mockery):
    spec = Spec('quux').concretized()
    dep = Spec('garply cflags=-g').concretized()
    spec.package.do_install(force=True)
    dep.package.do_install(force=True)
    spliced_spec = spec.splice(dep, transitive=False)
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
        if 'garply' in node.name:
            bin_name = 'garplinator'
        elif 'corge' in node.name:
            bin_name = 'corgegator'
        elif 'quux' in node.name:
            bin_name = 'quuxifier'
        bin_file_path = os.path.join(node.prefix.bin, bin_name)
        for fname in glob(bin_file_path):
            with open(fname, 'rb') as f:
                f.seek(0)
            assert text_in_bin(node.prefix, fname)
        # test install manifest
        assert spack.store.layout.check_installed(node)
        manifest_file_path = os.path.join(node.prefix,
                                          spack.store.layout.metadata_dir,
                                          spack.store.layout.manifest_file_name)
        assert os.path.exists(manifest_file_path)
        # monkeypatch the modulefile_generation hook to an accumulator and make
        # sure that it’s called with all of the arguments you would expect

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack verify` command"""
import os
import sys

import pytest

import llnl.util.filesystem as fs

import spack.spec
import spack.store
import spack.util.spack_json as sjson
import spack.verify
from spack.main import SpackCommand

verify = SpackCommand('verify')
install = SpackCommand('install')

pytestmark = pytest.mark.skipif(sys.platform == "win32",
                                reason="does not run on windows")


def test_single_file_verify_cmd(tmpdir):
    # Test the verify command interface to verifying a single file.
    filedir = str(tmpdir).joinpath( 'a', 'b', 'c', 'd')
    filepath = filedir.joinpath( 'file')
    metadir = str(tmpdir).joinpath( spack.store.layout.metadata_dir)

    fs.mkdirp(filedir)
    fs.mkdirp(metadir)

    with open(filepath, 'w') as f:
        f.write("I'm a file")

    data = spack.verify.create_manifest_entry(filepath)

    manifest_file = metadir.joinpath(
                                 spack.store.layout.manifest_file_name)

    with open(manifest_file, 'w') as f:
        sjson.dump({filepath: data}, f)

    results = verify('-f', filepath, fail_on_error=False)
    print(results)
    assert not results

    os.utime(filepath, (0, 0))
    with open(filepath, 'w') as f:
        f.write("I changed.")

    results = verify('-f', filepath, fail_on_error=False)

    expected = ['hash']
    mtime = filepath.stat().st_mtime
    if mtime != data['time']:
        expected.append('mtime')

    assert results
    assert filepath in results
    assert all(x in results for x in expected)

    results = verify('-fj', filepath, fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    errors = res.pop(filepath)
    assert sorted(errors) == sorted(expected)


def test_single_spec_verify_cmd(tmpdir, mock_packages, mock_archive,
                                mock_fetch, config, install_mockery):
    # Test the verify command interface to verify a single spec
    install('libelf')
    s = spack.spec.Spec('libelf').concretized()
    prefix = s.prefix
    hash = s.dag_hash()

    results = verify('/%s' % hash, fail_on_error=False)
    assert not results

    new_file = prefix.joinpath( 'new_file_for_verify_test')
    with open(new_file, 'w') as f:
        f.write('New file')

    results = verify('/%s' % hash, fail_on_error=False)
    assert new_file in results
    assert 'added' in results

    results = verify('-j', '/%s' % hash, fail_on_error=False)
    res = sjson.load(results)
    assert len(res) == 1
    assert res[new_file] == ['added']

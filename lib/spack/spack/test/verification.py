# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack.verify` module"""
import os
import llnl.util.filesystem as fs
import spack.verify
import spack.spec

def test_link_manifest(tmpdir):
    file = str(tmpdir.join('file'))
    open(file, 'a').close()
    link = str(tmpdir.join('link'))
    os.symlink(file, link)

    data = spack.verify.create_manifest_entry(link)
    assert data['type'] == 'link'
    assert data['dest'] == file
    assert all(x in data for x in ('mode', 'owner', 'group'))

    results = spack.verify.check_entry(link, data)
    assert not results

    data['type'] = 'garbage'
    results = spack.verify.check_entry(link, data)

    results = spack.verify.check_entry(link, data)
    assert results
    assert link in results.errors
    assert results.errors[link] == ['type']

    data['type'] = 'link'

    file2 = str(tmpdir.join('file2'))
    open(file2, 'a').close()
    os.remove(link)
    os.symlink(file2, link)

    results = spack.verify.check_entry(link, data)
    assert results
    assert link in results.errors
    assert results.errors[link] == ['link']


def test_dir_manifest(tmpdir):
    dirent = str(tmpdir.join('dir'))
    fs.mkdirp(dirent)

    data = spack.verify.create_manifest_entry(dirent)
    assert data['type'] == 'dir'
    assert all(x in data for x in ('mode', 'owner', 'group'))

    results = spack.verify.check_entry(dirent, data)
    assert not results

    data['type'] = 'garbage'

    results = spack.verify.check_entry(dirent, data)
    assert results
    assert dirent in results.errors
    assert results.errors[dirent] == ['type']


def test_file_manifest(tmpdir):
    file = str(tmpdir.join('dir'))
    with open(file, 'w') as f:
        f.write('This is a file')

    data = spack.verify.create_manifest_entry(file)
    assert data['type'] == 'file'
    assert data['size'] == 14
    assert all(x in data for x in ('mode', 'owner', 'group'))

    results = spack.verify.check_entry(file, data)
    assert not results

    data['type'] = 'garbage'

    results = spack.verify.check_entry(file, data)
    assert results
    assert file in results.errors
    assert results.errors[file] == ['type']

    data['type'] = 'file'

    with open(file, 'w') as f:
        f.write('The file has changed')

    results = spack.verify.check_entry(file, data)
    assert results
    assert file in results.errors
    assert all(x in results.errors[file] for x in ('size', 'hash', 'mtime'))
    assert len(results.errors[file]) == 3


def test_check_chmod_manifest(tmpdir):
    file = str(tmpdir.join('dir'))
    with open(file, 'w') as f:
        f.write('This is a file')

    data = spack.verify.create_manifest_entry(file)

    os.chmod(file, data['mode'] - 1)

    results = spack.verify.check_entry(file, data)
    assert results
    assert file in results.errors
    assert results.errors[file] == ['mode']


def test_check_prefix_manifest(tmpdir, monkeypatch):
    prefix_path = tmpdir.join('prefix')
    prefix = str(prefix_path)

    spec = spack.spec.Spec('libelf')
    spec._mark_concrete()
    monkeypatch.setattr(spack.spec.Spec, 'prefix', prefix)

    results = spack.verify.check_spec_manifest(spec)
    assert results
    assert prefix in results.errors
    assert results.errors[prefix] == ['manifest missing']

    metadata_dir = str(prefix_path.join('.spack'))
    bin_dir = str(prefix_path.join('bin'))
    other_dir = str(prefix_path.join('other'))

    for d in (metadata_dir, bin_dir, other_dir):
        fs.mkdirp(d)

    file = os.path.join(other_dir, 'file')
    with open(file, 'w') as f:
        f.write("I'm a little file short and stout")

    link = os.path.join(bin_dir, 'run')
    os.symlink(file, link)

    spack.verify.write_manifest(spec)
    results = spack.verify.check_spec_manifest(spec)
    assert not results

    os.remove(link)
    malware = os.path.join(metadata_dir, 'hiddenmalware')
    with open(malware, 'w') as f:
        f.write("Foul evil deeds")

    results = spack.verify.check_spec_manifest(spec)
    assert results
    assert all(x in results.errors for x in (malware, link))
    assert len(results.errors) == 2

    assert results.errors[link] == ['deleted']
    assert results.errors[malware] == ['added']

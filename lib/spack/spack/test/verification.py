# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for the `spack.verify` module"""
import os
import json
import sys
import time
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

    expected = ['size', 'hash']
    mtime = os.stat(file).st_mtime
    if mtime != data['time']:
        expected.append('mtime')

    assert results
    assert file in results.errors
    assert sorted(results.errors[file]) == sorted(expected)


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


def test_single_file_verification(tmpdir):
    filedir = os.path.join(str(tmpdir), 'a', 'b', 'c', 'd')
    filepath = os.path.join(filedir, 'file')
    metadir = os.path.join(str(tmpdir), spack.store.layout.metadata_dir)

    fs.mkdirp(filedir)
    fs.mkdirp(metadir)

    with open(filepath, 'w') as f:
        f.write("I'm a file")

    data = spack.verify.create_manifest_entry(filepath)

    manifest_file = os.path.join(metadir,
                                 spack.store.layout.manifest_file_name)

    with open(manifest_file, 'wb') as f:
        js = json.dumps({filepath: data})
        if sys.version_info[0] >= 3:
            js = js.encode()
        f.write(js)

    results = spack.verify.check_file_manifest(filepath)
    assert not results

    time.sleep(1)
    with open(filepath, 'w') as f:
        f.write("I changed.")

    results = spack.verify.check_file_manifest(filepath)

    expected = ['hash']
    mtime = os.stat(filepath).st_mtime
    if mtime != data['time']:
        expected.append('mtime')

    assert results
    assert filepath in results.errors
    assert sorted(results.errors[filepath]) == sorted(expected)

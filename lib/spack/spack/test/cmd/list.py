# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

list = SpackCommand('list')


def test_list(capsys):
    output = list(out=capsys)
    assert 'cloverleaf3d' in output
    assert 'hdf5' in output


def test_list_filter(capsys):
    output = list('py-*', out=capsys)
    assert 'py-numpy' in output
    assert 'perl-file-copy-recursive' not in output

    output = list('py-', out=capsys)
    assert 'py-numpy' in output
    assert 'perl-file-copy-recursive' in output


@pytest.mark.maybeslow
def test_list_search_description(capsys):
    output = list('--search-description', 'xml', out=capsys)
    assert 'expat' in output


def test_list_tags(capsys):
    output = list('--tag', 'proxy-app', out=capsys)
    assert 'cloverleaf3d' in output
    assert 'hdf5' not in output

    output = list('--tag', 'hpc', out=capsys)
    assert 'nek5000' in output
    assert 'mfem' in output

    output = list('--tag', 'HPC', out=capsys)
    assert 'nek5000' in output
    assert 'mfem' in output


def test_list_format_name_only(capsys):
    output = list('--format', 'name_only', out=capsys)
    assert 'cloverleaf3d' in output
    assert 'hdf5' in output


@pytest.mark.maybeslow
def test_list_format_version_json(capsys):
    output = list('--format', 'version_json', out=capsys)
    assert '  {"name": "cloverleaf3d",' in output
    assert '  {"name": "hdf5",' in output
    import json
    json.loads(output)


@pytest.mark.maybeslow
def test_list_format_html(capsys):
    output = list('--format', 'html', out=capsys)
    assert '<div class="section" id="cloverleaf3d">' in output
    assert '<h1>cloverleaf3d' in output

    assert '<div class="section" id="hdf5">' in output
    assert '<h1>hdf5' in output


def test_list_update(tmpdir):
    update_file = tmpdir.join('output')

    # not yet created when list is run
    list('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read()

    # created but older than any package
    with update_file.open('w') as f:
        f.write('empty\n')
    update_file.setmtime(0)
    list('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() != 'empty\n'

    # newer than any packages
    with update_file.open('w') as f:
        f.write('empty\n')
    list('--update', str(update_file))
    assert update_file.exists()
    with update_file.open() as f:
        assert f.read() == 'empty\n'

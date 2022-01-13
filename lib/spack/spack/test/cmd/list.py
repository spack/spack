# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand

list = SpackCommand('list')


def test_list():
    output = list()
    assert 'cloverleaf3d' in output
    assert 'hdf5' in output


def test_list_filter(mock_packages):
    output = list('py-*')
    assert 'py-extension1' in output
    assert 'py-extension2' in output
    assert 'py-extension3' in output
    assert 'python' not in output
    assert 'mpich' not in output

    output = list('py')
    assert 'py-extension1' in output
    assert 'py-extension2' in output
    assert 'py-extension3' in output
    assert 'python' in output
    assert 'mpich' not in output


def test_list_search_description(mock_packages):
    output = list('--search-description', 'one build dependency')
    assert 'depb' in output


def test_list_format_name_only(mock_packages):
    output = list('--format', 'name_only')
    assert 'zmpi' in output
    assert 'hdf5' in output


def test_list_format_version_json(mock_packages):
    output = list('--format', 'version_json')
    assert '{"name": "zmpi",' in output
    assert '{"name": "dyninst",' in output
    import json
    json.loads(output)


def test_list_format_html(mock_packages):
    output = list('--format', 'html')
    assert '<div class="section" id="zmpi">' in output
    assert '<h1>zmpi' in output

    assert '<div class="section" id="hdf5">' in output
    assert '<h1>hdf5' in output


def test_list_update(tmpdir, mock_packages):
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

# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

list = SpackCommand('list')


def test_list():
    output = list()
    assert 'cloverleaf3d' in output
    assert 'hdf5' in output


def test_list_filter():
    output = list('py-*')
    assert 'py-numpy' in output
    assert 'perl-file-copy-recursive' not in output

    output = list('py-')
    assert 'py-numpy' in output
    assert 'perl-file-copy-recursive' in output


@pytest.mark.maybeslow
def test_list_search_description():
    output = list('--search-description', 'xml')
    assert 'expat' in output


def test_list_tags():
    output = list('--tags', 'proxy-app')
    assert 'cloverleaf3d' in output
    assert 'hdf5' not in output


def test_list_format_name_only():
    output = list('--format', 'name_only')
    assert 'cloverleaf3d' in output
    assert 'hdf5' in output


@pytest.mark.maybeslow
def test_list_format_rst():
    output = list('--format', 'rst')
    assert '.. _cloverleaf3d:' in output
    assert '.. _hdf5:' in output


@pytest.mark.maybeslow
def test_list_format_html():
    output = list('--format', 'html')
    assert '<div class="section" id="cloverleaf3d">' in output
    assert '<h1>cloverleaf3d' in output

    assert '<div class="section" id="hdf5">' in output
    assert '<h1>hdf5' in output

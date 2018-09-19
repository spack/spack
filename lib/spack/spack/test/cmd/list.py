##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
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

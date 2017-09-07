##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import argparse

import pytest
import spack.cmd.list


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.list.setup_parser(prs)
    return prs


@pytest.fixture()
def pkg_names():
    pkg_names = []
    return pkg_names


@pytest.fixture()
def mock_name_only(monkeypatch, pkg_names):

    def name_only(x):
        pkg_names.extend(x)

    monkeypatch.setattr(spack.cmd.list, 'name_only', name_only)
    monkeypatch.setitem(spack.cmd.list.formatters, 'name_only', name_only)


@pytest.mark.usefixtures('mock_name_only')
class TestListCommand(object):

    def test_list_without_filters(self, parser, pkg_names):

        args = parser.parse_args([])
        spack.cmd.list.list(parser, args)

        assert pkg_names
        assert 'cloverleaf3d' in pkg_names
        assert 'hdf5' in pkg_names

    def test_list_with_filters(self, parser, pkg_names):
        args = parser.parse_args(['--tags', 'proxy-app'])
        spack.cmd.list.list(parser, args)

        assert pkg_names
        assert 'cloverleaf3d' in pkg_names
        assert 'hdf5' not in pkg_names
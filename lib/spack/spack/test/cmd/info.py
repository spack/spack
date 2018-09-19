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
import argparse

import pytest
import spack.cmd.info

from spack.main import SpackCommand

info = SpackCommand('info')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.info.setup_parser(prs)
    return prs


@pytest.fixture()
def info_lines():
    lines = []
    return lines


@pytest.fixture()
def mock_print(monkeypatch, info_lines):

    def _print(*args):
        info_lines.extend(args)

    monkeypatch.setattr(spack.cmd.info.color, 'cprint', _print, raising=False)


@pytest.mark.parametrize('pkg', [
    'openmpi',
    'trilinos',
    'boost',
    'python',
    'dealii'
])
def test_it_just_runs(pkg):
    info(pkg)


@pytest.mark.parametrize('pkg_query', [
    'hdf5',
    'cloverleaf3d',
    'trilinos'
])
@pytest.mark.usefixtures('mock_print')
def test_info_fields(pkg_query, parser, info_lines):

    expected_fields = (
        'Description:',
        'Homepage:',
        'Safe versions:',
        'Variants:',
        'Installation Phases:',
        'Virtual Packages:',
        'Tags:'
    )

    args = parser.parse_args([pkg_query])
    spack.cmd.info.info(parser, args)

    for text in expected_fields:
        match = [x for x in info_lines if text in x]
        assert match

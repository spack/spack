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
import spack.cmd.find
from spack.util.pattern import Bunch


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.find.setup_parser(prs)
    return prs


@pytest.fixture()
def specs():
    s = []
    return s


@pytest.fixture()
def mock_display(monkeypatch, specs):
    """Monkeypatches the display function to return its first argument"""

    def display(x, *args, **kwargs):
        specs.extend(x)

    monkeypatch.setattr(spack.cmd.find, 'display_specs', display)


def test_query_arguments():
    query_arguments = spack.cmd.find.query_arguments

    # Default arguments
    args = Bunch(
        only_missing=False,
        missing=False,
        unknown=False,
        explicit=False,
        implicit=False,
        start_date="2018-02-23",
        end_date=None
    )

    q_args = query_arguments(args)
    assert 'installed' in q_args
    assert 'known' in q_args
    assert 'explicit' in q_args
    assert q_args['installed'] is True
    assert q_args['known'] is any
    assert q_args['explicit'] is any
    assert 'start_date' in q_args
    assert 'end_date' not in q_args

    # Check that explicit works correctly
    args.explicit = True
    q_args = query_arguments(args)
    assert q_args['explicit'] is True

    args.explicit = False
    args.implicit = True
    q_args = query_arguments(args)
    assert q_args['explicit'] is False


@pytest.mark.db
@pytest.mark.usefixtures('database', 'mock_display')
def test_tag1(parser, specs):

    args = parser.parse_args(['--tags', 'tag1'])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 2
    assert 'mpich' in [x.name for x in specs]
    assert 'mpich2' in [x.name for x in specs]


@pytest.mark.db
@pytest.mark.usefixtures('database', 'mock_display')
def test_tag2(parser, specs):
    args = parser.parse_args(['--tags', 'tag2'])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 1
    assert 'mpich' in [x.name for x in specs]


@pytest.mark.db
@pytest.mark.usefixtures('database', 'mock_display')
def test_tag2_tag3(parser, specs):
    args = parser.parse_args(['--tags', 'tag2', '--tags', 'tag3'])
    spack.cmd.find.find(parser, args)

    assert len(specs) == 0

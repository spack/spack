# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

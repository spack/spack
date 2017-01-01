##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os.path

import pytest
import spack.cmd.module as module
import spack.modules as modules


def _get_module_files(args):
    return [modules.module_types[args.module_type](spec).file_name
            for spec in args.specs()]


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    parser = argparse.ArgumentParser()
    module.setup_parser(parser)
    return parser


@pytest.fixture(
    params=[
        ['rm', 'doesnotexist'],  # Try to remove a non existing module [tcl]
        ['find', 'mpileaks'],  # Try to find a module with multiple matches
        ['find', 'doesnotexist'],  # Try to find a module with no matches
    ]
)
def failure_args(request):
    """A list of arguments that will cause a failure"""
    return request.param


# TODO : test the --delete-tree option
# TODO : this requires having a separate directory for test modules
# TODO : add tests for loads and find to check the prompt format


def test_exit_with_failure(database, parser, failure_args):
    args = parser.parse_args(failure_args)
    with pytest.raises(SystemExit):
        module.module(parser, args)


def test_remove_and_add_tcl(database, parser):
    # Remove existing modules [tcl]
    args = parser.parse_args(['rm', '-y', 'mpileaks'])
    module_files = _get_module_files(args)
    for item in module_files:
        assert os.path.exists(item)
    module.module(parser, args)
    for item in module_files:
        assert not os.path.exists(item)

    # Add them back [tcl]
    args = parser.parse_args(['refresh', '-y', 'mpileaks'])
    module.module(parser, args)
    for item in module_files:
        assert os.path.exists(item)


def test_find(database, parser):
    # Try to find a module
    args = parser.parse_args(['find', 'libelf'])
    module.module(parser, args)


def test_remove_and_add_dotkit(database, parser):
    # Remove existing modules [dotkit]
    args = parser.parse_args(['rm', '-y', '-m', 'dotkit', 'mpileaks'])
    module_files = _get_module_files(args)
    for item in module_files:
        assert os.path.exists(item)
    module.module(parser, args)
    for item in module_files:
        assert not os.path.exists(item)

    # Add them back [dotkit]
    args = parser.parse_args(['refresh', '-y', '-m', 'dotkit', 'mpileaks'])
    module.module(parser, args)
    for item in module_files:
        assert os.path.exists(item)

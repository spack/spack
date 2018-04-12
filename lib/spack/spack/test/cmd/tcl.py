##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
import os.path

import pytest

import spack.cmd.tcl
import spack.main
import spack.modules

tcl = spack.main.SpackCommand('tcl')


def _get_module_files(args):
    specs = args.specs()
    writer_cls = spack.modules.module_types['tcl']
    return [writer_cls(spec).layout.filename for spec in specs]


@pytest.fixture(
    params=[
        ['rm', 'doesnotexist'],  # Try to remove a non existing module
        ['find', 'mpileaks'],  # Try to find a module with multiple matches
        ['find', 'doesnotexist'],  # Try to find a module with no matches
    ]
)
def failure_args(request):
    """A list of arguments that will cause a failure"""
    return request.param


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    parser = argparse.ArgumentParser()
    spack.cmd.tcl.setup_parser(parser)
    return parser

# TODO : test the --delete-tree option
# TODO : this requires having a separate directory for test modules
# TODO : add tests for loads and find to check the prompt format


def test_exit_with_failure(database, failure_args):
    with pytest.raises(spack.main.SpackCommandError):
        tcl(*failure_args)


def test_remove_and_add_tcl(database, parser):
    """Tests adding and removing a tcl module file."""

    rm_cli_args = ['rm', '-y', 'mpileaks']
    module_files = _get_module_files(parser.parse_args(rm_cli_args))
    for item in module_files:
        assert os.path.exists(item)

    tcl(*rm_cli_args)
    for item in module_files:
        assert not os.path.exists(item)

    tcl('refresh', '-y', 'mpileaks')
    for item in module_files:
        assert os.path.exists(item)


@pytest.mark.parametrize('cli_args', [
    ['libelf'],
    ['--full-path', 'libelf']
])
def test_find(database, cli_args):
    """Tests 'spack tcl find' under a few common scenarios."""
    tcl(*(['find'] + cli_args))

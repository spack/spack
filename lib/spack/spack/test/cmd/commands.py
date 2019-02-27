# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from llnl.util.argparsewriter import ArgparseWriter

import spack.cmd
import spack.main
from spack.main import SpackCommand

commands = SpackCommand('commands')

parser = spack.main.make_argument_parser()
spack.main.add_all_commands(parser)


def test_commands_by_name():
    """Test default output of spack commands."""
    out = commands()
    assert out.strip().split('\n') == sorted(spack.cmd.all_commands())


def test_subcommands():
    """Test subcommand traversal."""
    out = commands('--format=subcommands')
    assert 'spack mirror create' in out
    assert 'spack buildcache list' in out
    assert 'spack repo add' in out
    assert 'spack pkg diff' in out
    assert 'spack url parse' in out
    assert 'spack view symlink' in out

    class Subcommands(ArgparseWriter):
        def begin_command(self, prog):
            assert prog in out

    Subcommands().write(parser)


def test_rst():
    """Do some simple sanity checks of the rst writer."""
    out = commands('--format=rst')

    class Subcommands(ArgparseWriter):
        def begin_command(self, prog):
            assert prog in out
            assert re.sub(r' ', '-', prog) in out
    Subcommands().write(parser)

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

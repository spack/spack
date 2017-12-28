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
from spack.main import SpackCommand


help_cmd = SpackCommand('help')


def test_help():
    """Sanity check the help command to make sure it works."""

    out = help_cmd()
    assert 'These are common spack commands:' in out


def test_help_all():
    """Test the spack help --all flag"""

    out = help_cmd('--all')
    assert 'Complete list of spack commands:' in out


def test_help_spec():
    """Test the spack help --spec flag"""

    out = help_cmd('--spec')
    assert 'spec expression syntax:' in out


def test_help_subcommand():
    """Test the spack help subcommand argument"""

    out = help_cmd('help')
    assert 'get help on spack and its commands' in out

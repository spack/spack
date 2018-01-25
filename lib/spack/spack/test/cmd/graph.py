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
from spack.main import SpackCommand, SpackCommandError

import pytest


graph = SpackCommand('graph')


@pytest.mark.db
@pytest.mark.usefixtures('builtin_mock', 'database')
class TestGraphCommand(object):
    def test_graph_ascii(self):
        """Tests spack graph --ascii"""

        graph('--ascii', 'dt-diamond')

    def test_graph_dot(self):
        """Tests spack graph --dot"""

        graph('--dot', 'dt-diamond')

    def test_graph_normalize(self):
        """Tests spack graph --normalize"""

        graph('--normalize', 'dt-diamond')

    def test_graph_static(self):
        """Tests spack graph --static"""

        graph('--static', 'dt-diamond')

    def test_graph_installed(self):
        """Tests spack graph --installed"""

        graph('--installed')

        with pytest.raises(SpackCommandError):
            graph('--installed', 'dt-diamond')

    def test_graph_deptype(self):
        """Tests spack graph --deptype"""

        graph('--deptype', 'all', 'dt-diamond')


def test_graph_no_specs():
    """Tests spack graph with no arguments"""

    with pytest.raises(SpackCommandError):
        graph()

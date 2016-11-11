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
import spack.test.mock_database
import spack.store
from spack.cmd.uninstall import uninstall


class MockArgs(object):

    def __init__(self, packages, all=False, force=False, dependents=False):
        self.packages = packages
        self.all = all
        self.force = force
        self.dependents = dependents
        self.yes_to_all = True


class TestUninstall(spack.test.mock_database.MockDatabase):

    def test_uninstall(self):
        parser = None
        # Multiple matches
        args = MockArgs(['mpileaks'])
        self.assertRaises(SystemExit, uninstall, parser, args)
        # Installed dependents
        args = MockArgs(['libelf'])
        self.assertRaises(SystemExit, uninstall, parser, args)
        # Recursive uninstall
        args = MockArgs(['callpath'], all=True, dependents=True)
        uninstall(parser, args)

        all_specs = spack.store.layout.all_specs()
        self.assertEqual(len(all_specs), 7)
        # query specs with multiple configurations
        mpileaks_specs = [s for s in all_specs if s.satisfies('mpileaks')]
        callpath_specs = [s for s in all_specs if s.satisfies('callpath')]
        mpi_specs = [s for s in all_specs if s.satisfies('mpi')]

        self.assertEqual(len(mpileaks_specs), 0)
        self.assertEqual(len(callpath_specs), 0)
        self.assertEqual(len(mpi_specs),      3)

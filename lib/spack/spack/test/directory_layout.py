##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""\
This test verifies that the Spack directory layout works properly.
"""
import unittest
import tempfile
import shutil
import os
from contextlib import closing

from llnl.util.filesystem import *

import spack
from spack.spec import Spec
from spack.packages import PackageDB
from spack.directory_layout import SpecHashDirectoryLayout

class DirectoryLayoutTest(unittest.TestCase):
    """Tests that a directory layout works correctly and produces a
       consistent install path."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.layout = SpecHashDirectoryLayout(self.tmpdir)


    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        self.layout = None


    def test_read_and_write_spec(self):
        """This goes through each package in spack and creates a directory for
           it.  It then ensures that the spec for the directory's
           installed package can be read back in consistently, and
           finally that the directory can be removed by the directory
           layout.
        """
        for pkg in spack.db.all_packages():
            spec = pkg.spec

            # If a spec fails to concretize, just skip it.  If it is a
            # real error, it will be caught by concretization tests.
            try:
                spec.concretize()
            except:
                continue

            self.layout.make_path_for_spec(spec)

            install_dir = self.layout.path_for_spec(spec)
            spec_path = self.layout.spec_file_path(spec)

            # Ensure directory has been created in right place.
            self.assertTrue(os.path.isdir(install_dir))
            self.assertTrue(install_dir.startswith(self.tmpdir))

            # Ensure spec file exists when directory is created
            self.assertTrue(os.path.isfile(spec_path))
            self.assertTrue(spec_path.startswith(install_dir))

            # Make sure spec file can be read back in to get the original spec
            spec_from_file = self.layout.read_spec(spec_path)
            self.assertEqual(spec, spec_from_file)
            self.assertTrue(spec.eq_dag, spec_from_file)
            self.assertTrue(spec_from_file.concrete)

            # Ensure that specs that come out "normal" are really normal.
            with closing(open(spec_path)) as spec_file:
                read_separately = Spec(spec_file.read())

                read_separately.normalize()
                self.assertEqual(read_separately, spec_from_file)

                read_separately.concretize()
                self.assertEqual(read_separately, spec_from_file)

            # Make sure the dep hash of the read-in spec is the same
            self.assertEqual(spec.dep_hash(), spec_from_file.dep_hash())

            # Ensure directories are properly removed
            self.layout.remove_path_for_spec(spec)
            self.assertFalse(os.path.isdir(install_dir))
            self.assertFalse(os.path.exists(install_dir))


    def test_handle_unknown_package(self):
        """This test ensures that spack can at least do *some*
           operations with packages that are installed but that it
           does not know about.  This is actually not such an uncommon
           scenario with spack; it can happen when you switch from a
           git branch where you're working on a new package.

           This test ensures that the directory layout stores enough
           information about installed packages' specs to uninstall
           or query them again if the package goes away.
        """
        mock_db = PackageDB(spack.mock_packages_path)

        not_in_mock = set(spack.db.all_package_names()).difference(
            set(mock_db.all_package_names()))

        # Create all the packages that are not in mock.
        installed_specs = {}
        for pkg_name in not_in_mock:
            spec = spack.db.get(pkg_name).spec

            # If a spec fails to concretize, just skip it.  If it is a
            # real error, it will be caught by concretization tests.
            try:
                spec.concretize()
            except:
                continue

            self.layout.make_path_for_spec(spec)
            installed_specs[spec] = self.layout.path_for_spec(spec)

        tmp = spack.db
        spack.db = mock_db

        # Now check that even without the package files, we know
        # enough to read a spec from the spec file.
        for spec, path in installed_specs.items():
            spec_from_file = self.layout.read_spec(join_path(path, '.spec'))

            # To satisfy these conditions, directory layouts need to
            # read in concrete specs from their install dirs somehow.
            self.assertEqual(path, self.layout.path_for_spec(spec_from_file))
            self.assertEqual(spec, spec_from_file)
            self.assertEqual(spec.dep_hash(), spec_from_file.dep_hash())

        spack.db = tmp

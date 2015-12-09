##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
import os
import unittest
import shutil
import tempfile

from llnl.util.filesystem import *

import spack
from spack.stage import Stage
from spack.fetch_strategy import URLFetchStrategy
from spack.directory_layout import YamlDirectoryLayout
from spack.util.executable import which
from spack.test.mock_packages_test import *
from spack.test.mock_repo import MockArchive


class InstallTest(MockPackagesTest):
    """Tests install and uninstall on a trivial package."""

    def setUp(self):
        super(InstallTest, self).setUp()

        # create a simple installable package directory and tarball
        self.repo = MockArchive()

        # We use a fake package, so skip the checksum.
        spack.do_checksum = False

        # Use a fake install directory to avoid conflicts bt/w
        # installed pkgs and mock packages.
        self.tmpdir = tempfile.mkdtemp()
        self.orig_layout = spack.install_layout
        spack.install_layout = YamlDirectoryLayout(self.tmpdir)


    def tearDown(self):
        super(InstallTest, self).tearDown()

        if self.repo.stage is not None:
            self.repo.stage.destroy()

        # Turn checksumming back on
        spack.do_checksum = True

        # restore spack's layout.
        spack.install_layout = self.orig_layout
        shutil.rmtree(self.tmpdir, ignore_errors=True)


    def test_install_and_uninstall(self):
        # Get a basic concrete spec for the trivial install package.
        spec = Spec('trivial_install_test_package')
        spec.concretize()
        self.assertTrue(spec.concrete)

        # Get the package
        pkg = spack.db.get(spec)

        # Fake the URL for the package so it downloads from a file.
        pkg.fetcher = URLFetchStrategy(self.repo.url)

        try:
            pkg.do_install()
            pkg.do_uninstall()
        except Exception, e:
            pkg.remove_prefix()
            raise

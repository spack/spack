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
import shutil
import tempfile

import spack
import spack.store
from llnl.util.filesystem import *
from spack.directory_layout import YamlDirectoryLayout
from spack.database import Database
from spack.fetch_strategy import URLFetchStrategy, FetchStrategyComposite
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
        self.orig_layout = spack.store.layout
        self.orig_db = spack.store.db

        spack.store.layout = YamlDirectoryLayout(self.tmpdir)
        spack.store.db     = Database(self.tmpdir)

    def tearDown(self):
        super(InstallTest, self).tearDown()
        self.repo.destroy()

        # Turn checksumming back on
        spack.do_checksum = True

        # restore spack's layout.
        spack.store.layout = self.orig_layout
        spack.store.db     = self.orig_db
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def fake_fetchify(self, pkg):
        """Fake the URL for a package so it downloads from a file."""
        fetcher = FetchStrategyComposite()
        fetcher.append(URLFetchStrategy(self.repo.url))
        pkg.fetcher = fetcher

    def test_install_and_uninstall(self):
        # Get a basic concrete spec for the trivial install package.
        spec = Spec('trivial_install_test_package')
        spec.concretize()
        self.assertTrue(spec.concrete)

        # Get the package
        pkg = spack.repo.get(spec)

        self.fake_fetchify(pkg)

        try:
            pkg.do_install()
            pkg.do_uninstall()
        except Exception:
            pkg.remove_prefix()
            raise

    def test_store(self):
        spec = Spec('cmake-client').concretized()

        for s in spec.traverse():
            self.fake_fetchify(s.package)

        pkg = spec.package
        try:
            pkg.do_install()
        except Exception:
            pkg.remove_prefix()
            raise

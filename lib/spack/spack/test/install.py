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
import os
import unittest
import shutil
import tempfile
from contextlib import closing

from llnl.util.filesystem import *

import spack
from spack.stage import Stage
from spack.fetch_strategy import URLFetchStrategy
from spack.directory_layout import SpecHashDirectoryLayout
from spack.util.executable import which
from spack.test.mock_packages_test import *


dir_name = 'trivial-1.0'
archive_name = 'trivial-1.0.tar.gz'
install_test_package = 'trivial_install_test_package'

class InstallTest(MockPackagesTest):
    """Tests install and uninstall on a trivial package."""

    def setUp(self):
        super(InstallTest, self).setUp()

        self.stage = Stage('not_a_real_url')
        archive_dir = join_path(self.stage.path, dir_name)
        dummy_configure = join_path(archive_dir, 'configure')

        mkdirp(archive_dir)
        with closing(open(dummy_configure, 'w')) as configure:
            configure.write(
                "#!/bin/sh\n"
                "prefix=$(echo $1 | sed 's/--prefix=//')\n"
                "cat > Makefile <<EOF\n"
                "all:\n"
                "\techo Building...\n\n"
                "install:\n"
                "\tmkdir -p $prefix\n"
                "\ttouch $prefix/dummy_file\n"
                "EOF\n")
        os.chmod(dummy_configure, 0755)

        with working_dir(self.stage.path):
            tar = which('tar')
            tar('-czf', archive_name, dir_name)

        # We use a fake package, so skip the checksum.
        spack.do_checksum = False

        # Use a fake install directory to avoid conflicts bt/w
        # installed pkgs and mock packages.
        self.tmpdir = tempfile.mkdtemp()
        self.orig_layout = spack.install_layout
        spack.install_layout = SpecHashDirectoryLayout(self.tmpdir)


    def tearDown(self):
        super(InstallTest, self).tearDown()

        if self.stage is not None:
            self.stage.destroy()

        # Turn checksumming back on
        spack.do_checksum = True

        # restore spack's layout.
        spack.install_layout = self.orig_layout
        shutil.rmtree(self.tmpdir, ignore_errors=True)


    def test_install_and_uninstall(self):
        # Get a basic concrete spec for the trivial install package.
        spec = Spec(install_test_package)
        spec.concretize()
        self.assertTrue(spec.concrete)

        # Get the package
        print
        print "======== GETTING PACKAGE ========"
        pkg = spack.db.get(spec)

        print "======== GOT PACKAGE ========"
        print

        # Fake the URL for the package so it downloads from a file.
        archive_path = join_path(self.stage.path, archive_name)
        pkg.fetcher = URLFetchStrategy('file://' + archive_path)

        try:
            pkg.do_install()
            pkg.do_uninstall()
        except Exception, e:
            pkg.remove_prefix()
            raise

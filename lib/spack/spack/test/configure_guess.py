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
import os
import shutil
import tempfile
import unittest

from llnl.util.filesystem import *
from spack.cmd.create import ConfigureGuesser
from spack.stage import Stage
from spack.test.mock_packages_test import *
from spack.util.executable import which


class InstallTest(unittest.TestCase):
    """Tests the configure guesser in spack create"""

    def setUp(self):
        self.tar = which('tar')
        self.tmpdir = tempfile.mkdtemp()
        self.orig_dir = os.getcwd()
        os.chdir(self.tmpdir)
        self.stage = None


    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        os.chdir(self.orig_dir)


    def check_archive(self, filename, system):
        mkdirp('archive')
        touch(join_path('archive', filename))
        self.tar('czf', 'archive.tar.gz', 'archive')

        url = 'file://' + join_path(os.getcwd(), 'archive.tar.gz')
        print url
        with Stage(url) as stage:
            stage.fetch()

            guesser = ConfigureGuesser()
            guesser(stage)
            self.assertEqual(system, guesser.build_system)


    def test_python(self):
        self.check_archive('setup.py', 'python')


    def test_autotools(self):
        self.check_archive('configure', 'autotools')


    def test_cmake(self):
        self.check_archive('CMakeLists.txt', 'cmake')


    def test_unknown(self):
        self.check_archive('foobar', 'unknown')



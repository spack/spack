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
"""Tests Spack's ability to substitute a different version into a URL."""

import os
import unittest
from spack.url import substitute_version


class UrlSubstitutionTest(unittest.TestCase):

    def check(self, base, version, new_url):
        self.assertEqual(substitute_version(base, version), new_url)

    def test_same_version(self):
        # Ensures that substituting the same version results in the same URL
        self.check(
            'http://www.mr511.de/software/libelf-0.8.13.tar.gz', '0.8.13',
            'http://www.mr511.de/software/libelf-0.8.13.tar.gz')

    def test_different_version(self):
        # Test a completely different version syntax
        self.check(
            'http://www.prevanders.net/libdwarf-20130729.tar.gz', '8.12',
            'http://www.prevanders.net/libdwarf-8.12.tar.gz')

    def test_double_version(self):
        # Test a URL where the version appears twice
        # It should get substituted both times
        self.check(
            'https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz', '2.1.3',
            'https://github.com/hpc/mpileaks/releases/download/v2.1.3/mpileaks-2.1.3.tar.gz')

    def test_partial_version_prefix(self):
        # Test now with a partial prefix earlier in the URL
        # This is hard to figure out so Spack only substitutes
        # the last instance of the version
        self.check(
            'https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.0.tar.bz2', '2.2.0',
            'https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.2.0.tar.bz2')
        self.check(
            'https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.1.0.tar.bz2', '2.2',
            'https://www.open-mpi.org/software/ompi/v2.1/downloads/openmpi-2.2.tar.bz2')

    def test_no_separator(self):
        # No separator between the name and version of the package
        self.check(
            'file://{0}/turbolinux702.tar.gz'.format(os.getcwd()), '703',
            'file://{0}/turbolinux703.tar.gz'.format(os.getcwd()))

    def test_github_raw(self):
        self.check(
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true', '2.0.7',
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true')
        self.check(
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true', '4.7',
            'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v4.7.tgz?raw=true')

    def test_regex(self):
        # Package name contains regex characters
        self.check(
            'http://math.lbl.gov/voro++/download/dir/voro++-0.4.6.tar.gz', '1.2.3',
            'http://math.lbl.gov/voro++/download/dir/voro++-1.2.3.tar.gz')

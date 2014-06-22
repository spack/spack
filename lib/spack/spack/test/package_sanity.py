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
This test does sanity checks on Spack's builtin package database.
"""
import unittest

import spack
import spack.url as url

class PackageSanityTest(unittest.TestCase):

    def test_get_all_packages(self):
        """Get all packages once and make sure that works."""
        for name in spack.db.all_package_names():
            spack.db.get(name)


    def test_url_versions(self):
        """Ensure that url_for_version does the right thing for at least the
           default version of each package.
        """
        for pkg in spack.db.all_packages():
            v = url.parse_version(pkg.url)
            self.assertEqual(pkg.url, pkg.url_for_version(v))

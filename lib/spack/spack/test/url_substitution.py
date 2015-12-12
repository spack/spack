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
"""\
This test does sanity checks on substituting new versions into URLs
"""
import unittest

import spack
import spack.url as url
from spack.packages import PackageDB


class PackageSanityTest(unittest.TestCase):
    def test_hypre_url_substitution(self):
        base = "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-2.9.0b.tar.gz"

        self.assertEqual(url.substitute_version(base, '2.9.0b'), base)
        self.assertEqual(
            url.substitute_version(base, '2.8.0b'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-2.8.0b.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '2.7.0b'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-2.7.0b.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '2.6.0b'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-2.6.0b.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '1.14.0b'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-1.14.0b.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '1.13.0b'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-1.13.0b.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '2.0.0'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-2.0.0.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '1.6.0'),
            "https://computation-rnd.llnl.gov/linear_solvers/download/hypre-1.6.0.tar.gz")


    def test_otf2_url_substitution(self):
        base = "http://www.vi-hps.org/upload/packages/otf2/otf2-1.4.tar.gz"

        self.assertEqual(url.substitute_version(base, '1.4'), base)

        self.assertEqual(
            url.substitute_version(base, '1.3.1'),
            "http://www.vi-hps.org/upload/packages/otf2/otf2-1.3.1.tar.gz")
        self.assertEqual(
            url.substitute_version(base, '1.2.1'),
            "http://www.vi-hps.org/upload/packages/otf2/otf2-1.2.1.tar.gz")

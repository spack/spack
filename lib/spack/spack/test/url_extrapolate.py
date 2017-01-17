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
"""Tests ability of spack to extrapolate URL versions from
existing versions.
"""
import unittest

import spack.url as url


class UrlExtrapolateTest(unittest.TestCase):

    def check_url(self, base, version, new_url):
        self.assertEqual(url.substitute_version(base, version), new_url)

    def test_libelf_version(self):
        base = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"
        self.check_url(base, '0.8.13', base)
        self.check_url(
            base, '0.8.12', "http://www.mr511.de/software/libelf-0.8.12.tar.gz")
        self.check_url(
            base, '0.3.1',  "http://www.mr511.de/software/libelf-0.3.1.tar.gz")
        self.check_url(
            base, '1.3.1b', "http://www.mr511.de/software/libelf-1.3.1b.tar.gz")

    def test_libdwarf_version(self):
        base = "http://www.prevanders.net/libdwarf-20130729.tar.gz"
        self.check_url(base, '20130729', base)
        self.check_url(
            base, '8.12', "http://www.prevanders.net/libdwarf-8.12.tar.gz")

    def test_dyninst_version(self):
        # Dyninst has a version twice in the URL.
        base = "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1.2/DyninstAPI-8.1.2.tgz"
        self.check_url(base, '8.1.2', base)
        self.check_url(base, '8.2',
                       "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.2/DyninstAPI-8.2.tgz")
        self.check_url(base, '8.3.1',
                       "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.3.1/DyninstAPI-8.3.1.tgz")

    def test_partial_version_prefix(self):
        # Test now with a partial prefix earlier in the URL -- this is
        # hard to figure out so Spack only substitutes the last
        # instance of the version.
        base = "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1/DyninstAPI-8.1.2.tgz"
        self.check_url(base, '8.1.2', base)
        self.check_url(base, '8.1.4',
                       "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1/DyninstAPI-8.1.4.tgz")
        self.check_url(base, '8.2',
                       "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1/DyninstAPI-8.2.tgz")
        self.check_url(base, '8.3.1',
                       "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1/DyninstAPI-8.3.1.tgz")

    def test_scalasca_partial_version(self):
        # Note that this probably doesn't actually work, but sites are
        # inconsistent about their directory structure, so it's not
        # clear what is right.  This test is for consistency and to
        # document behavior.  If you figure out a good way to handle
        # this case, fix the tests too.
        self.check_url('http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz', '8.3.1',
                       'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-8.3.1.tar.gz')
        self.check_url('http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-4.3-TP1.tar.gz', '8.3.1',
                       'http://apps.fz-juelich.de/scalasca/releases/cube/4.3/dist/cube-8.3.1.tar.gz')

    def test_mpileaks_version(self):
        self.check_url('https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz', '2.1.3',
                       'https://github.com/hpc/mpileaks/releases/download/v2.1.3/mpileaks-2.1.3.tar.gz')

    def test_gcc(self):
        self.check_url('http://open-source-box.org/gcc/gcc-4.9.2/gcc-4.9.2.tar.bz2', '4.7',
                       'http://open-source-box.org/gcc/gcc-4.7/gcc-4.7.tar.bz2')
        self.check_url('http://open-source-box.org/gcc/gcc-4.4.7/gcc-4.4.7.tar.bz2', '4.4.7',
                       'http://open-source-box.org/gcc/gcc-4.4.7/gcc-4.4.7.tar.bz2')

    def test_github_raw(self):
        self.check_url('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true', '2.0.7',
                       'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true')
        self.check_url('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true', '4.7',
                       'https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v4.7.tgz?raw=true')

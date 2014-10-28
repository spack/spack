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
Tests ability of spack to extrapolate URL versions from existing versions.
"""
import spack
import spack.url as url
from spack.spec import Spec
from spack.version import ver
from spack.test.mock_packages_test import *


class UrlExtrapolateTest(MockPackagesTest):

    def test_known_version(self):
        d = spack.db.get('dyninst')

        self.assertEqual(
            d.url_for_version('8.2'), 'http://www.paradyn.org/release8.2/DyninstAPI-8.2.tgz')
        self.assertEqual(
            d.url_for_version('8.1.2'), 'http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz')
        self.assertEqual(
            d.url_for_version('8.1.1'), 'http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz')


    def test_extrapolate_version(self):
        d = spack.db.get('dyninst')

        # Nearest URL for 8.1.1.5 is 8.1.1, and the URL there is
        # release8.1/DyninstAPI-8.1.1.tgz.  Only the last part matches
        # the version, so only extrapolate the last part.  Obviously
        # dyninst has ambiguous URL versions, but we want to make sure
        # extrapolation works in a well-defined way.
        self.assertEqual(
            d.url_for_version('8.1.1.5'), 'http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.5.tgz')

        # 8.2 matches both the release8.2 component and the DyninstAPI-8.2 component.
        # Extrapolation should replace both with the new version.
        # TODO: figure out a consistent policy for this.
        # self.assertEqual(
        #     d.url_for_version('8.2.3'), 'http://www.paradyn.org/release8.2.3/DyninstAPI-8.2.3.tgz')


    def test_with_package(self):
        d = spack.db.get('dyninst@8.2')
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.2/DyninstAPI-8.2.tgz')

        d = spack.db.get('dyninst@8.1.2')
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz')

        d = spack.db.get('dyninst@8.1.1')
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz')


    def test_concrete_package(self):
        s = Spec('dyninst@8.2')
        s.concretize()
        d = spack.db.get(s)
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.2/DyninstAPI-8.2.tgz')

        s = Spec('dyninst@8.1.2')
        s.concretize()
        d = spack.db.get(s)
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.1.2/DyninstAPI-8.1.2.tgz')

        s = Spec('dyninst@8.1.1')
        s.concretize()
        d = spack.db.get(s)
        self.assertEqual(d.fetcher.url, 'http://www.paradyn.org/release8.1/DyninstAPI-8.1.1.tgz')

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
"""Tests for web.py."""
import os

import spack.paths
from spack.util.web import spider, find_versions_of_archive
from spack.version import ver


web_data_path = os.path.join(spack.paths.test_path, 'data', 'web')

root = 'file://' + web_data_path + '/index.html'
root_tarball = 'file://' + web_data_path + '/foo-0.0.0.tar.gz'

page_1 = 'file://' + os.path.join(web_data_path, '1.html')
page_2 = 'file://' + os.path.join(web_data_path, '2.html')
page_3 = 'file://' + os.path.join(web_data_path, '3.html')
page_4 = 'file://' + os.path.join(web_data_path, '4.html')


def test_spider_0():
    pages, links = spider(root, depth=0)

    assert root in pages
    assert page_1 not in pages
    assert page_2 not in pages
    assert page_3 not in pages
    assert page_4 not in pages

    assert "This is the root page." in pages[root]

    assert root not in links
    assert page_1 in links
    assert page_2 not in links
    assert page_3 not in links
    assert page_4 not in links


def test_spider_1():
    pages, links = spider(root, depth=1)

    assert root in pages
    assert page_1 in pages
    assert page_2 not in pages
    assert page_3 not in pages
    assert page_4 not in pages

    assert "This is the root page." in pages[root]
    assert "This is page 1." in pages[page_1]

    assert root not in links
    assert page_1 in links
    assert page_2 in links
    assert page_3 not in links
    assert page_4 not in links


def test_spider_2():
    pages, links = spider(root, depth=2)

    assert root in pages
    assert page_1 in pages
    assert page_2 in pages
    assert page_3 not in pages
    assert page_4 not in pages

    assert "This is the root page." in pages[root]
    assert "This is page 1." in pages[page_1]
    assert "This is page 2." in pages[page_2]

    assert root not in links
    assert page_1 in links
    assert page_1 in links
    assert page_2 in links
    assert page_3 in links
    assert page_4 in links


def test_spider_3():
    pages, links = spider(root, depth=3)

    assert root in pages
    assert page_1 in pages
    assert page_2 in pages
    assert page_3 in pages
    assert page_4 in pages

    assert "This is the root page." in pages[root]
    assert "This is page 1." in pages[page_1]
    assert "This is page 2." in pages[page_2]
    assert "This is page 3." in pages[page_3]
    assert "This is page 4." in pages[page_4]

    assert root in links  # circular link on page 3
    assert page_1 in links
    assert page_1 in links
    assert page_2 in links
    assert page_3 in links
    assert page_4 in links


def test_find_versions_of_archive_0():
    versions = find_versions_of_archive(root_tarball, root, list_depth=0)
    assert ver('0.0.0') in versions


def test_find_versions_of_archive_1():
    versions = find_versions_of_archive(root_tarball, root, list_depth=1)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions


def test_find_versions_of_archive_2():
    versions = find_versions_of_archive(root_tarball, root, list_depth=2)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions


def test_find_exotic_versions_of_archive_2():
    versions = find_versions_of_archive(root_tarball, root, list_depth=2)
    # up for grabs to make this better.
    assert ver('2.0.0b2') in versions


def test_find_versions_of_archive_3():
    versions = find_versions_of_archive(root_tarball, root, list_depth=3)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions
    assert ver('3.0') in versions
    assert ver('4.5') in versions


def test_find_exotic_versions_of_archive_3():
    versions = find_versions_of_archive(root_tarball, root, list_depth=3)
    assert ver('2.0.0b2') in versions
    assert ver('3.0a1') in versions
    assert ver('4.5-rc5') in versions

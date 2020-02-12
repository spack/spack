# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Tests for web.py."""
import os
import pytest

from ordereddict_backport import OrderedDict

import spack.paths
import spack.util.web as web_util
from spack.version import ver


web_data_path = os.path.join(spack.paths.test_path, 'data', 'web')

root = 'file://' + web_data_path + '/index.html'
root_tarball = 'file://' + web_data_path + '/foo-0.0.0.tar.gz'

page_1 = 'file://' + os.path.join(web_data_path, '1.html')
page_2 = 'file://' + os.path.join(web_data_path, '2.html')
page_3 = 'file://' + os.path.join(web_data_path, '3.html')
page_4 = 'file://' + os.path.join(web_data_path, '4.html')


def test_spider_0():
    pages, links = web_util.spider(root, depth=0)

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
    pages, links = web_util.spider(root, depth=1)

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
    pages, links = web_util.spider(root, depth=2)

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
    pages, links = web_util.spider(root, depth=3)

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
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=0)
    assert ver('0.0.0') in versions


def test_find_versions_of_archive_1():
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=1)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions


def test_find_versions_of_archive_2():
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=2)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions


def test_find_exotic_versions_of_archive_2():
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=2)
    # up for grabs to make this better.
    assert ver('2.0.0b2') in versions


def test_find_versions_of_archive_3():
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=3)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions
    assert ver('3.0') in versions
    assert ver('4.5') in versions


def test_find_exotic_versions_of_archive_3():
    versions = web_util.find_versions_of_archive(
        root_tarball, root, list_depth=3)
    assert ver('2.0.0b2') in versions
    assert ver('3.0a1') in versions
    assert ver('4.5-rc5') in versions


def test_get_header():
    headers = {
        'Content-type': 'text/plain'
    }

    # looking up headers should just work like a plain dict
    # lookup when there is an entry with the right key
    assert(web_util.get_header(headers, 'Content-type') == 'text/plain')

    # looking up headers should still work if there is a fuzzy match
    assert(web_util.get_header(headers, 'contentType') == 'text/plain')

    # ...unless there is an exact match for the "fuzzy" spelling.
    headers['contentType'] = 'text/html'
    assert(web_util.get_header(headers, 'contentType') == 'text/html')

    # If lookup has to fallback to fuzzy matching and there are more than one
    # fuzzy match, the result depends on the internal ordering of the given
    # mapping
    headers = OrderedDict()
    headers['Content-type'] = 'text/plain'
    headers['contentType'] = 'text/html'

    assert(web_util.get_header(headers, 'CONTENT_TYPE') == 'text/plain')
    del headers['Content-type']
    assert(web_util.get_header(headers, 'CONTENT_TYPE') == 'text/html')

    # Same as above, but different ordering
    headers = OrderedDict()
    headers['contentType'] = 'text/html'
    headers['Content-type'] = 'text/plain'

    assert(web_util.get_header(headers, 'CONTENT_TYPE') == 'text/html')
    del headers['contentType']
    assert(web_util.get_header(headers, 'CONTENT_TYPE') == 'text/plain')

    # If there isn't even a fuzzy match, raise KeyError
    with pytest.raises(KeyError):
        web_util.get_header(headers, 'ContentLength')

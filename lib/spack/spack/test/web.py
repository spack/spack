# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import ordereddict_backport
import pytest
import spack.paths
import spack.util.web
from spack.version import ver


def _create_url(relative_url):
    web_data_path = os.path.join(spack.paths.test_path, 'data', 'web')
    return 'file://' + os.path.join(web_data_path, relative_url)


root = _create_url('index.html')
root_tarball = _create_url('foo-0.0.0.tar.gz')
page_1 = _create_url('1.html')
page_2 = _create_url('2.html')
page_3 = _create_url('3.html')
page_4 = _create_url('4.html')


@pytest.mark.parametrize(
    'depth,expected_found,expected_not_found,expected_text', [
        (0,
         {'pages': [root], 'links': [page_1]},
         {'pages': [page_1, page_2, page_3, page_4],
          'links': [root, page_2, page_3, page_4]},
         {root: "This is the root page."}),
        (1,
         {'pages': [root, page_1], 'links': [page_1, page_2]},
         {'pages': [page_2, page_3, page_4],
          'links': [root, page_3, page_4]},
         {root: "This is the root page.",
          page_1: "This is page 1."}),
        (2,
         {'pages': [root, page_1, page_2],
          'links': [page_1, page_2, page_3, page_4]},
         {'pages': [page_3, page_4], 'links': [root]},
         {root: "This is the root page.",
          page_1: "This is page 1.",
          page_2: "This is page 2."}),
        (3,
         {'pages': [root, page_1, page_2, page_3, page_4],
          'links': [root, page_1, page_2, page_3, page_4]},
         {'pages': [], 'links': []},
         {root: "This is the root page.",
          page_1: "This is page 1.",
          page_2: "This is page 2.",
          page_3: "This is page 3.",
          page_4: "This is page 4."}),
    ])
def test_spider(depth, expected_found, expected_not_found, expected_text):
    pages, links = spack.util.web.spider(root, depth=depth)

    for page in expected_found['pages']:
        assert page in pages

    for page in expected_not_found['pages']:
        assert page not in pages

    for link in expected_found['links']:
        assert link in links

    for link in expected_not_found['links']:
        assert link not in links

    for page, text in expected_text.items():
        assert text in pages[page]


def test_spider_no_response(monkeypatch):
    # Mock the absence of a response
    monkeypatch.setattr(
        spack.util.web, 'read_from_url', lambda x, y: (None, None, None)
    )
    pages, links = spack.util.web.spider(root, depth=0)
    assert not pages and not links


def test_find_versions_of_archive_0():
    versions = spack.util.web.find_versions_of_archive(
        root_tarball, root, list_depth=0)
    assert ver('0.0.0') in versions


def test_find_versions_of_archive_1():
    versions = spack.util.web.find_versions_of_archive(
        root_tarball, root, list_depth=1)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions


def test_find_versions_of_archive_2():
    versions = spack.util.web.find_versions_of_archive(
        root_tarball, root, list_depth=2)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions


def test_find_exotic_versions_of_archive_2():
    versions = spack.util.web.find_versions_of_archive(
        root_tarball, root, list_depth=2)
    # up for grabs to make this better.
    assert ver('2.0.0b2') in versions


def test_find_versions_of_archive_3():
    versions = spack.util.web.find_versions_of_archive(
        root_tarball, root, list_depth=3)
    assert ver('0.0.0') in versions
    assert ver('1.0.0') in versions
    assert ver('2.0.0') in versions
    assert ver('3.0') in versions
    assert ver('4.5') in versions


def test_find_exotic_versions_of_archive_3():
    versions = spack.util.web.find_versions_of_archive(
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
    assert(spack.util.web.get_header(headers, 'Content-type') == 'text/plain')

    # looking up headers should still work if there is a fuzzy match
    assert(spack.util.web.get_header(headers, 'contentType') == 'text/plain')

    # ...unless there is an exact match for the "fuzzy" spelling.
    headers['contentType'] = 'text/html'
    assert(spack.util.web.get_header(headers, 'contentType') == 'text/html')

    # If lookup has to fallback to fuzzy matching and there are more than one
    # fuzzy match, the result depends on the internal ordering of the given
    # mapping
    headers = ordereddict_backport.OrderedDict()
    headers['Content-type'] = 'text/plain'
    headers['contentType'] = 'text/html'

    assert(spack.util.web.get_header(headers, 'CONTENT_TYPE') == 'text/plain')
    del headers['Content-type']
    assert(spack.util.web.get_header(headers, 'CONTENT_TYPE') == 'text/html')

    # Same as above, but different ordering
    headers = ordereddict_backport.OrderedDict()
    headers['contentType'] = 'text/html'
    headers['Content-type'] = 'text/plain'

    assert(spack.util.web.get_header(headers, 'CONTENT_TYPE') == 'text/html')
    del headers['contentType']
    assert(spack.util.web.get_header(headers, 'CONTENT_TYPE') == 'text/plain')

    # If there isn't even a fuzzy match, raise KeyError
    with pytest.raises(KeyError):
        spack.util.web.get_header(headers, 'ContentLength')

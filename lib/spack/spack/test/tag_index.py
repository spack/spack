# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Tests for tag index cache files."""

import pytest
from six import StringIO

import spack.repo
import spack.tag_index

# Alternate representation
tags_json = \
    """
    {
      "tags": {
        "no-version": [
          "noversion",
          "noversion-bundle"
        ],
        "no-source": [
          "nosource"
        ]
      }
    }
    """

more_tags_json = \
    """
    {
      "tags": {
        "merge": [
          "check"
        ]
      }
    }
    """


def test_tag_copy(mock_packages):
    index = spack.tag_index.TagIndex.from_json(StringIO(tags_json))
    new_index = index.copy()

    assert index.tags == new_index.tags


def test_tag_index_round_trip(mock_packages):
    # Assumes at least two packages -- mpich and mpich2 -- have tags
    mock_index = spack.repo.path.tag_index
    assert mock_index.tags

    ostream = StringIO()
    mock_index.to_json(ostream)

    istream = StringIO(ostream.getvalue())
    new_index = spack.tag_index.TagIndex.from_json(istream)

    assert mock_index == new_index


def test_tag_equal():
    first_index = spack.tag_index.TagIndex.from_json(StringIO(tags_json))
    second_index = spack.tag_index.TagIndex.from_json(StringIO(tags_json))

    assert first_index == second_index


def test_tag_merge():
    first_index = spack.tag_index.TagIndex.from_json(StringIO(tags_json))
    second_index = spack.tag_index.TagIndex.from_json(StringIO(more_tags_json))

    assert first_index != second_index

    tags1 = list(first_index.tags.keys())
    tags2 = list(second_index.tags.keys())
    all_tags = sorted(list(set(tags1 + tags2)))

    first_index.merge(second_index)
    tag_keys = sorted(first_index.tags.keys())
    assert tag_keys == all_tags

    # Merge again to make sure the index does not retain duplicates
    first_index.merge(second_index)
    tag_keys = sorted(first_index.tags.keys())
    assert tag_keys == all_tags


def test_tag_not_dict():
    list_json = "[]"
    with pytest.raises(spack.tag_index.TagIndexError) as e:
        spack.tag_index.TagIndex.from_json(StringIO(list_json))
        assert "not a dict" in str(e)


def test_tag_no_tags():
    pkg_json = "{\"packages\": []}"
    with pytest.raises(spack.tag_index.TagIndexError) as e:
        spack.tag_index.TagIndex.from_json(StringIO(pkg_json))
        assert "does not start with" in str(e)


def test_tag_update_package(mock_packages):
    mock_index = spack.repo.path.tag_index

    index = spack.tag_index.TagIndex()
    for name in spack.repo.all_package_names():
        index.update_package(name)

    assert mock_index.tags == index.tags
    assert mock_index == index

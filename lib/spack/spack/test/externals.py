# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

import pytest

from spack.vendor.archspec.cpu import TARGETS

import spack.archspec
import spack.repo
from spack.externals import ExternalDict, ExternalSpecsParser

pytestmark = pytest.mark.usefixtures("config", "mock_packages")


@pytest.mark.parametrize(
    "externals_dict,expected_length,expected_queries",
    [
        # Empty dictionary case
        ([], 0, {"gmake": 0}),
        # Single spec case
        (
            [{"spec": "gmake@1.0", "prefix": "/path/to/gmake"}],
            1,
            {"gmake": 1, "gmake@1.0": 1, "gmake@2.0": 0},
        ),
        # Multiple specs case
        (
            [
                {"spec": "gmake@1.0", "prefix": "/path/to/gmake1"},
                {"spec": "gmake@2.0", "prefix": "/path/to/gmake2"},
                {"spec": "gcc@1.0", "prefix": "/path/to/gcc"},
            ],
            3,
            {"gmake": 2, "gmake@2": 1, "gcc": 1, "baz": 0},
        ),
        # Case with modules and extra attributes
        (
            [
                {
                    "spec": "gmake@1.0",
                    "prefix": "/path/to/gmake",
                    "modules": ["module1", "module2"],
                    "extra_attributes": {"attr1": "value1"},
                }
            ],
            1,
            {"gmake": 1},
        ),
    ],
)
def test_basic_parsing(externals_dict, expected_length, expected_queries):
    """Tests parsing external specs, in some basic cases"""
    parser = ExternalSpecsParser(externals_dict)

    assert len(parser.all_specs()) == expected_length
    for node in parser.all_specs():
        assert node.concrete

    for query, expected in expected_queries.items():
        assert len(parser.query(query)) == expected


@pytest.mark.parametrize(
    "externals_dict,expected_triplet",
    [([{"spec": "gmake@1.0", "prefix": "/path/to/gmake1"}], ("test", "debian6", "aarch64"))],
)
def test_external_specs_architecture_completion(
    externals_dict: List[ExternalDict], expected_triplet, monkeypatch
):
    """Tests the completion of external specs architectures when using the default behavior"""
    monkeypatch.setattr(spack.archspec, "HOST_TARGET_FAMILY", TARGETS["aarch64"])
    parser = ExternalSpecsParser(externals_dict)

    expected_platform, expected_os, expected_target = expected_triplet

    for node in parser.all_specs():
        assert node.architecture is not None
        assert node.architecture.platform == expected_platform
        assert node.architecture.os == expected_os
        assert node.target == expected_target


def test_external_specs_parser_with_missing_packages():
    """Tests the parsing of external specs when some packages are missing"""
    externals_dict: List[ExternalDict] = [
        {"spec": "gmake@1.0", "prefix": "/path/to/gmake1"},
        {"spec": "gmake@2.0", "prefix": "/path/to/gmake2"},
        {"spec": "gcc@1.0", "prefix": "/path/to/gcc"},
        # This package does not exist in the builtin_mock repository
        {"spec": "baz@1.0", "prefix": "/path/to/baz"},
    ]

    external_specs = ExternalSpecsParser(externals_dict, allow_nonexisting=True).all_specs()
    assert len(external_specs) == 3
    assert len([x for x in external_specs if x.satisfies("gmake")]) == 2
    assert len([x for x in external_specs if x.satisfies("gcc")]) == 1

    with pytest.raises(spack.repo.UnknownPackageError, match="Package 'baz' not found"):
        ExternalSpecsParser(externals_dict, allow_nonexisting=False)

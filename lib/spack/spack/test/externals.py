# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

import pytest

from spack.vendor.archspec.cpu import TARGETS

import spack.archspec
import spack.repo
from spack.externals import (
    DuplicateExternalError,
    ExternalDict,
    ExternalSpecsParser,
    complete_architecture,
    complete_variants_and_architecture,
)

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
    assert len(parser.specs_by_external_id) == expected_length
    for node in parser.all_specs():
        assert node.concrete

    for query, expected in expected_queries.items():
        assert len(parser.query(query)) == expected


@pytest.mark.parametrize(
    "externals_dict,expected_triplet",
    [
        ([{"spec": "gmake@1.0", "prefix": "/path/to/gmake1"}], ("test", "debian6", "aarch64")),
        (
            [{"spec": "gmake@1.0 target=icelake", "prefix": "/path/to/gmake1"}],
            ("test", "debian6", "icelake"),
        ),
        (
            [{"spec": "gmake@1.0 platform=linux target=icelake", "prefix": "/path/to/gmake1"}],
            ("linux", "debian6", "icelake"),
        ),
        (
            [{"spec": "gmake@1.0 os=rhel8", "prefix": "/path/to/gmake1"}],
            ("test", "rhel8", "aarch64"),
        ),
    ],
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


def test_externals_with_duplicate_id():
    """Tests the parsing of external specs when some specs have the same id"""
    externals_dict: List[ExternalDict] = [
        {"spec": "gmake@1.0", "prefix": "/path/to/gmake1", "id": "gmake"},
        {"spec": "gmake@2.0", "prefix": "/path/to/gmake2", "id": "gmake"},
        {"spec": "gcc@1.0", "prefix": "/path/to/gcc", "id": "gcc"},
    ]

    with pytest.raises(DuplicateExternalError, match=" Fix your packages.yaml configuration"):
        ExternalSpecsParser(externals_dict)


@pytest.mark.parametrize(
    "externals_dicts,expected_satisfies",
    [
        # o ascent@0.9.2
        # o adios2@2.7.1
        # o bzip2@1.0.8
        (
            [
                {
                    "spec": "ascent@0.9.2+adios2+shared",
                    "prefix": "/user/path",
                    "id": "ascent",
                    "dependencies": [{"id": "adios2", "deptypes": ["build", "link"]}],
                },
                {
                    "spec": "adios2@2.7.1+shared",
                    "prefix": "/user/path",
                    "id": "adios2",
                    "dependencies": [{"id": "bzip2", "deptypes": ["build", "link"]}],
                },
                {"spec": "bzip2@1.0.8+shared", "prefix": "/user/path", "id": "bzip2"},
            ],
            {
                "ascent": ["%[deptypes=build,link] adios2@2.7.1"],
                "adios2": ["%[deptypes=build,link] bzip2@1.0.8"],
            },
        ),
        # o ascent@0.9.2
        # |\
        # | o adios2@2.7.1
        # |/
        # o bzip2@1.0.8
        (
            [
                {
                    "spec": "ascent@0.9.2+adios2+shared",
                    "prefix": "/user/path",
                    "id": "ascent",
                    "dependencies": [
                        {"id": "adios2", "deptypes": "link"},
                        {"id": "bzip2", "deptypes": "run"},
                    ],
                },
                {
                    "spec": "adios2@2.7.1+shared",
                    "prefix": "/user/path",
                    "id": "adios2",
                    "dependencies": [{"id": "bzip2", "deptypes": ["build", "link"]}],
                },
                {"spec": "bzip2@1.0.8+shared", "prefix": "/user/path", "id": "bzip2"},
            ],
            {
                "ascent": ["%[deptypes=link] adios2@2.7.1", "%[deptypes=run] bzip2@1.0.8"],
                "adios2": ["%[deptypes=build,link] bzip2@1.0.8"],
            },
        ),
        # Old type specification for
        # o mpileaks@2.2
        # o gcc@15.0.1
        (
            [
                [
                    {"spec": "mpileaks@2.2 %gcc", "prefix": "/user/path"},
                    {"spec": "gcc@14.2.1 languages=c,c++", "prefix": "/user/path"},
                    {"spec": "gcc@15.0.1 languages=c,c++", "prefix": "/user/path"},
                ],
                {"mpileaks": ["%[deptypes=build] gcc@15"]},
            ]
        ),
        # Old type specification for
        # o mpileaks@2.2
        # o gcc@14.2.1 <- selected because of the architecture of gcc@15
        (
            [
                [
                    {"spec": "mpileaks@2.2 %gcc", "prefix": "/user/path"},
                    {"spec": "gcc@14.2.1 languages=c,c++", "prefix": "/user/path"},
                    {"spec": "gcc@15.0.1 os=CNL languages=c,c++", "prefix": "/user/path"},
                ],
                {"mpileaks": ["%[deptypes=build] gcc@14"]},
            ]
        ),
    ],
)
def test_externals_with_dependencies(externals_dicts: List[ExternalDict], expected_satisfies):
    """Tests constructing externals with dependencies"""
    parser = ExternalSpecsParser(externals_dicts)

    for query_spec, expected_list in expected_satisfies.items():
        result = parser.query(query_spec)
        assert len(result) == 1
        for expected in expected_list:
            assert result[0].satisfies(expected)


@pytest.mark.parametrize(
    "externals_dicts,expected_length,not_expected",
    [
        ([{"spec": "mpileaks", "prefix": "/user/path", "id": "mpileaks"}], 0, ["mpileaks"]),
        ([{"spec": "mpileaks@2:", "prefix": "/user/path", "id": "mpileaks"}], 0, ["mpileaks"]),
    ],
)
def test_externals_without_concrete_version(
    externals_dicts: List[ExternalDict], expected_length, not_expected
):
    """Tests parsing externals, when some dicts are malformed and don't have a concrete version"""
    parser = ExternalSpecsParser(externals_dicts)
    result = parser.all_specs()

    assert len(result) == expected_length
    for c in not_expected:
        assert all(not s.satisfies(c) for s in result)


@pytest.mark.parametrize(
    "externals_dict,completion_fn,expected,not_expected",
    [
        (
            [{"spec": "mpileaks@2.3", "prefix": "/user/path"}],
            complete_architecture,
            {"mpileaks": ["platform=test"]},
            {"mpileaks": ["debug=*", "opt=*", "shared=*", "static=*"]},
        ),
        (
            [{"spec": "mpileaks@2.3", "prefix": "/user/path"}],
            complete_variants_and_architecture,
            {"mpileaks": ["platform=test", "~debug", "~opt", "+shared", "+static"]},
            {"mpileaks": ["+debug", "+opt", "~shared", "~static"]},
        ),
    ],
)
def test_external_node_completion(
    externals_dict: List[ExternalDict], completion_fn, expected, not_expected
):
    """Tests the completion of external specs with different node completion"""
    parser = ExternalSpecsParser(externals_dict, complete_node=completion_fn)

    for query_spec, expected_list in expected.items():
        result = parser.query(query_spec)
        assert len(result) == 1
        for expected in expected_list:
            assert result[0].satisfies(expected)

    for query_spec, expected_list in not_expected.items():
        result = parser.query(query_spec)
        assert len(result) == 1
        for expected in expected_list:
            assert not result[0].satisfies(expected)

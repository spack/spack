# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools

import pytest

import spack.concretize
from spack.environment.list import SpecListParser
from spack.installer import PackageInstaller
from spack.spec import Spec

DEFAULT_EXPANSION = [
    "mpileaks",
    "zmpi@1.0",
    "mpich@3.0",
    {"matrix": [["hypre"], ["%gcc@4.5.0", "%clang@3.3"]]},
    "libelf",
]

DEFAULT_CONSTRAINTS = [
    [Spec("mpileaks")],
    [Spec("zmpi@1.0")],
    [Spec("mpich@3.0")],
    [Spec("hypre"), Spec("%gcc@4.5.0")],
    [Spec("hypre"), Spec("%clang@3.3")],
    [Spec("libelf")],
]

DEFAULT_SPECS = [
    Spec("mpileaks"),
    Spec("zmpi@1.0"),
    Spec("mpich@3.0"),
    Spec("hypre%gcc@4.5.0"),
    Spec("hypre%clang@3.3"),
    Spec("libelf"),
]


@pytest.fixture()
def parser_and_speclist():
    """Default configuration of parser and user spec list for tests"""
    parser = SpecListParser()
    parser.parse_definitions(
        data=[
            {"gccs": ["%gcc@4.5.0"]},
            {"clangs": ["%clang@3.3"]},
            {"mpis": ["zmpi@1.0", "mpich@3.0"]},
        ]
    )
    result = parser.parse_user_specs(
        name="specs",
        yaml_list=["mpileaks", "$mpis", {"matrix": [["hypre"], ["$gccs", "$clangs"]]}, "libelf"],
    )
    return parser, result


class TestSpecList:
    @pytest.mark.regression("28749")
    @pytest.mark.parametrize(
        "specs,expected",
        [
            # Constraints are ordered randomly
            (
                [
                    {
                        "matrix": [
                            ["^zmpi"],
                            ["%gcc@4.5.0"],
                            ["hypre", "libelf"],
                            ["~shared"],
                            ["cflags=-O3", 'cflags="-g -O0"'],
                            ["^foo"],
                        ]
                    }
                ],
                [
                    "hypre cflags=-O3 ~shared %gcc@4.5.0 ^foo ^zmpi",
                    'hypre cflags="-g -O0" ~shared %gcc@4.5.0 ^foo ^zmpi',
                    "libelf cflags=-O3 ~shared %gcc@4.5.0 ^foo ^zmpi",
                    'libelf cflags="-g -O0" ~shared %gcc@4.5.0 ^foo ^zmpi',
                ],
            ),
            # A constraint affects both the root and a dependency
            (
                [{"matrix": [["gromacs"], ["%gcc"], ["+plumed ^plumed%gcc"]]}],
                ["gromacs+plumed%gcc ^plumed%gcc"],
            ),
        ],
    )
    def test_spec_list_constraint_ordering(self, specs, expected):
        result = SpecListParser().parse_user_specs(name="specs", yaml_list=specs)
        assert result.specs == [Spec(x) for x in expected]

    def test_mock_spec_list(self, parser_and_speclist):
        """Tests expected properties on the default mock spec list"""
        parser, mock_list = parser_and_speclist
        assert mock_list.specs_as_yaml_list == DEFAULT_EXPANSION
        assert mock_list.specs_as_constraints == DEFAULT_CONSTRAINTS
        assert mock_list.specs == DEFAULT_SPECS

    def test_spec_list_add(self, parser_and_speclist):
        parser, mock_list = parser_and_speclist
        mock_list.add("libdwarf")

        assert mock_list.specs_as_yaml_list == DEFAULT_EXPANSION + ["libdwarf"]
        assert mock_list.specs_as_constraints == DEFAULT_CONSTRAINTS + [[Spec("libdwarf")]]
        assert mock_list.specs == DEFAULT_SPECS + [Spec("libdwarf")]

    def test_spec_list_remove(self, parser_and_speclist):
        parser, mock_list = parser_and_speclist
        mock_list.remove("libelf")

        assert mock_list.specs_as_yaml_list + ["libelf"] == DEFAULT_EXPANSION
        assert mock_list.specs_as_constraints + [[Spec("libelf")]] == DEFAULT_CONSTRAINTS
        assert mock_list.specs + [Spec("libelf")] == DEFAULT_SPECS

    def test_spec_list_extension(self, parser_and_speclist):
        parser, mock_list = parser_and_speclist
        other_list = parser.parse_user_specs(
            name="specs", yaml_list=[{"matrix": [["callpath"], ["%intel@18"]]}]
        )
        mock_list.extend(other_list)

        assert mock_list.specs_as_yaml_list == (DEFAULT_EXPANSION + other_list.specs_as_yaml_list)
        assert mock_list.specs == DEFAULT_SPECS + other_list.specs

    def test_spec_list_nested_matrices(self, parser_and_speclist):
        parser, _ = parser_and_speclist

        inner_matrix = [{"matrix": [["zlib", "libelf"], ["%gcc", "%intel"]]}]
        outer_addition = ["+shared", "~shared"]
        outer_matrix = [{"matrix": [inner_matrix, outer_addition]}]
        result = parser.parse_user_specs(name="specs", yaml_list=outer_matrix)

        expected_components = itertools.product(
            ["zlib", "libelf"], ["%gcc", "%intel"], ["+shared", "~shared"]
        )
        expected = [Spec(" ".join(combo)) for combo in expected_components]
        assert set(result.specs) == set(expected)

    @pytest.mark.regression("16897")
    def test_spec_list_recursion_specs_as_constraints(self):
        input = ["mpileaks", "$mpis", {"matrix": [["hypre"], ["$%gccs", "$%clangs"]]}, "libelf"]

        definitions = [
            {"gccs": ["gcc@4.5.0"]},
            {"clangs": ["clang@3.3"]},
            {"mpis": ["zmpi@1.0", "mpich@3.0"]},
        ]

        parser = SpecListParser()
        parser.parse_definitions(data=definitions)
        result = parser.parse_user_specs(name="specs", yaml_list=input)

        assert result.specs_as_yaml_list == DEFAULT_EXPANSION
        assert result.specs_as_constraints == DEFAULT_CONSTRAINTS
        assert result.specs == DEFAULT_SPECS

    @pytest.mark.regression("16841")
    def test_spec_list_matrix_exclude(self, mock_packages):
        parser = SpecListParser()
        result = parser.parse_user_specs(
            name="specs",
            yaml_list=[
                {
                    "matrix": [["multivalue-variant"], ["foo=bar", "foo=baz"]],
                    "exclude": ["foo=bar"],
                }
            ],
        )
        assert len(result.specs) == 1

    def test_spec_list_exclude_with_abstract_hashes(self, mock_packages, install_mockery):
        # Put mpich in the database so it can be referred to by hash.
        mpich_1 = spack.concretize.concretize_one("mpich+debug")
        mpich_2 = spack.concretize.concretize_one("mpich~debug")
        PackageInstaller([mpich_1.package, mpich_2.package], explicit=True, fake=True).install()

        # Create matrix and exclude +debug, which excludes the first mpich after its abstract hash
        # is resolved.
        parser = SpecListParser()
        result = parser.parse_user_specs(
            name="specs",
            yaml_list=[
                {
                    "matrix": [
                        ["mpileaks"],
                        ["^callpath"],
                        [f"^mpich/{mpich_1.dag_hash(5)}", f"^mpich/{mpich_2.dag_hash(5)}"],
                    ],
                    "exclude": ["^mpich+debug"],
                }
            ],
        )

        # Ensure that only mpich~debug is selected, and that the assembled spec remains abstract.
        assert len(result.specs) == 1
        assert result.specs[0] == Spec(f"mpileaks ^callpath ^mpich/{mpich_2.dag_hash(5)}")

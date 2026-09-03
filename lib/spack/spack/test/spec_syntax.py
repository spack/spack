# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import pathlib
import re
import sys

import pytest

import spack.binary_distribution
import spack.cmd
import spack.concretize
import spack.error
import spack.hash_lookup
import spack.platforms.test
import spack.repo
import spack.solver.asp
import spack.spec
import spack.util.filesystem as fs
from spack.externals import (
    ExternalSpecsParser,
    complete_variants_and_architecture,
    extract_dicts_from_configuration,
)
from spack.spec_parser import (
    UNIX_FILENAME,
    WINDOWS_FILENAME,
    SpecParser,
    SpecParsingError,
    SpecTokenizationError,
    expand_toolchains,
    parse_one_or_raise,
)

SKIP_ON_WINDOWS = pytest.mark.skipif(sys.platform == "win32", reason="Unix style path on Windows")

SKIP_ON_UNIX = pytest.mark.skipif(sys.platform != "win32", reason="Windows style path on Unix")


def Token(kind, value, **kwargs):
    return (kind, value, dict(kwargs))


def simple_package_name(name):
    """A simple package name in canonical form"""
    return name, [Token("UNQUALIFIED_PACKAGE_NAME", value=name)], name


def dependency_with_version(text):
    root, rest = text.split("^")
    dependency, version = rest.split("@")
    return (
        text,
        [
            Token("UNQUALIFIED_PACKAGE_NAME", value=root.strip()),
            Token("DEPENDENCY", value="^"),
            Token("UNQUALIFIED_PACKAGE_NAME", value=dependency.strip()),
            Token("VERSION", value=f"@{version}"),
        ],
        text,
    )


@pytest.fixture()
def specfile_for(config, mock_packages):
    def _specfile_for(spec_str, filename):
        s = spack.concretize.concretize_one(spec_str)
        is_json = str(filename).endswith(".json")
        is_yaml = str(filename).endswith(".yaml")
        if not is_json and not is_yaml:
            raise ValueError("wrong extension used for specfile")

        with filename.open("w") as f:
            if is_json:
                f.write(s.to_json())
            else:
                f.write(s.to_yaml())
        return s

    return _specfile_for


@pytest.mark.parametrize(
    "spec_str,tokens,expected_roundtrip",
    [
        # Package names
        simple_package_name("mvapich"),
        simple_package_name("mvapich_foo"),
        simple_package_name("_mvapich_foo"),
        simple_package_name("3dtk"),
        simple_package_name("ns-3-dev"),
        # Single token anonymous specs
        ("@2.7", [Token("VERSION", value="@2.7")], "@2.7"),
        ("@2.7:", [Token("VERSION", value="@2.7:")], "@2.7:"),
        ("@:2.7", [Token("VERSION", value="@:2.7")], "@:2.7"),
        ("+foo", [Token("BOOL_VARIANT", value="+foo")], "+foo"),
        ("~foo", [Token("BOOL_VARIANT", value="~foo")], "~foo"),
        ("-foo", [Token("BOOL_VARIANT", value="-foo")], "~foo"),
        ("platform=test", [Token("KEY_VALUE_PAIR", value="platform=test")], "platform=test"),
        # Multiple tokens anonymous specs
        (
            "%intel",
            [Token("DEPENDENCY", value="%"), Token("UNQUALIFIED_PACKAGE_NAME", "intel")],
            "%intel",
        ),
        (
            "languages=go @4.2:",
            [Token("KEY_VALUE_PAIR", value="languages=go"), Token("VERSION", value="@4.2:")],
            "@4.2: languages=go",
        ),
        (
            "@4.2:     languages=go",
            [Token("VERSION", value="@4.2:"), Token("KEY_VALUE_PAIR", value="languages=go")],
            "@4.2: languages=go",
        ),
        (
            "^zlib",
            [Token("DEPENDENCY", value="^"), Token("UNQUALIFIED_PACKAGE_NAME", value="zlib")],
            "^zlib",
        ),
        # Specs with simple dependencies
        (
            "openmpi ^hwloc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="hwloc"),
            ],
            "openmpi ^hwloc",
        ),
        (
            "openmpi ^hwloc ^libunwind",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="hwloc"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="libunwind"),
            ],
            "openmpi ^hwloc ^libunwind",
        ),
        (
            "openmpi      ^hwloc^libunwind",
            [  # White spaces are tested
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="hwloc"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="libunwind"),
            ],
            "openmpi ^hwloc ^libunwind",
        ),
        # Version after compiler
        (
            "foo @2.0 %bar@1.0",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="foo"),
                Token("VERSION", value="@2.0"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="bar"),
                Token("VERSION", value="@1.0"),
            ],
            "foo@2.0 %bar@1.0",
        ),
        # Single dependency with version
        dependency_with_version("openmpi ^hwloc@1.2e6"),
        dependency_with_version("openmpi ^hwloc@1.2e6:"),
        dependency_with_version("openmpi ^hwloc@:1.4b7-rc3"),
        dependency_with_version("openmpi ^hwloc@1.2e6:1.4b7-rc3"),
        # Complex specs with multiple constraints
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6+debug~qt_4 %intel@12.1 ^stackwalker@8.1_1e",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich_foo"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("VERSION", value="@1.2:1.4,1.6"),
                Token("BOOL_VARIANT", value="+debug"),
                Token("BOOL_VARIANT", value="~qt_4"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
                Token("VERSION", value="@12.1"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="stackwalker"),
                Token("VERSION", value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6+debug~qt_4 %intel@12.1 ^stackwalker@8.1_1e",
        ),
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6~qt_4 debug=2 %intel@12.1 ^stackwalker@8.1_1e",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich_foo"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("VERSION", value="@1.2:1.4,1.6"),
                Token("BOOL_VARIANT", value="~qt_4"),
                Token("KEY_VALUE_PAIR", value="debug=2"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
                Token("VERSION", value="@12.1"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="stackwalker"),
                Token("VERSION", value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6~qt_4 debug=2 %intel@12.1 ^stackwalker@8.1_1e",
        ),
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6 cppflags=-O3 +debug~qt_4 %intel@12.1 "
            "^stackwalker@8.1_1e",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich_foo"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("VERSION", value="@1.2:1.4,1.6"),
                Token("KEY_VALUE_PAIR", value="cppflags=-O3"),
                Token("BOOL_VARIANT", value="+debug"),
                Token("BOOL_VARIANT", value="~qt_4"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
                Token("VERSION", value="@12.1"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="stackwalker"),
                Token("VERSION", value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6 cppflags=-O3 +debug~qt_4 %intel@12.1"
            " ^stackwalker@8.1_1e",
        ),
        # Specs containing YAML or JSON in the package name
        (
            "yaml-cpp@0.1.8%intel@12.1 ^boost@3.1.4",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="yaml-cpp"),
                Token("VERSION", value="@0.1.8"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
                Token("VERSION", value="@12.1"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="boost"),
                Token("VERSION", value="@3.1.4"),
            ],
            "yaml-cpp@0.1.8 %intel@12.1 ^boost@3.1.4",
        ),
        (
            r"builtin.yaml-cpp%gcc",
            [
                Token("FULLY_QUALIFIED_PACKAGE_NAME", value="builtin.yaml-cpp"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
            ],
            "builtin.yaml-cpp %gcc",
        ),
        (
            r"testrepo.yaml-cpp%gcc",
            [
                Token("FULLY_QUALIFIED_PACKAGE_NAME", value="testrepo.yaml-cpp"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
            ],
            "testrepo.yaml-cpp %gcc",
        ),
        (
            r"builtin.yaml-cpp@0.1.8%gcc@7.2.0 ^boost@3.1.4",
            [
                Token("FULLY_QUALIFIED_PACKAGE_NAME", value="builtin.yaml-cpp"),
                Token("VERSION", value="@0.1.8"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@7.2.0"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="boost"),
                Token("VERSION", value="@3.1.4"),
            ],
            "builtin.yaml-cpp@0.1.8 %gcc@7.2.0 ^boost@3.1.4",
        ),
        (
            r"builtin.yaml-cpp ^testrepo.boost ^zlib",
            [
                Token("FULLY_QUALIFIED_PACKAGE_NAME", value="builtin.yaml-cpp"),
                Token("DEPENDENCY", value="^"),
                Token("FULLY_QUALIFIED_PACKAGE_NAME", value="testrepo.boost"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
            ],
            "builtin.yaml-cpp ^testrepo.boost ^zlib",
        ),
        # Canonicalization of the string representation
        (
            r"mvapich ^stackwalker ^_openmpi",  # Dependencies are reordered
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="stackwalker"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
            ],
            "mvapich ^_openmpi ^stackwalker",
        ),
        (
            r"y~f+e~d+c~b+a",  # Variants are reordered
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("BOOL_VARIANT", value="~f"),
                Token("BOOL_VARIANT", value="+e"),
                Token("BOOL_VARIANT", value="~d"),
                Token("BOOL_VARIANT", value="+c"),
                Token("BOOL_VARIANT", value="~b"),
                Token("BOOL_VARIANT", value="+a"),
            ],
            "y+a~b+c~d+e~f",
        ),
        # Things that evaluate to Spec()
        # TODO: consider making these format to "*" instead of ""
        ("@:", [Token("VERSION", value="@:")], r""),
        ("*", [Token("UNQUALIFIED_PACKAGE_NAME", value="*")], r""),
        # anonymous dependencies with variants
        (
            "^* foo=bar",
            [
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("KEY_VALUE_PAIR", value="foo=bar"),
            ],
            "^* foo=bar",
        ),
        (
            "%* foo=bar",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("KEY_VALUE_PAIR", value="foo=bar"),
            ],
            "%* foo=bar",
        ),
        (
            "^*+foo",
            [
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("BOOL_VARIANT", value="+foo"),
            ],
            "^+foo",
        ),
        (
            "^*~foo",
            [
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("BOOL_VARIANT", value="~foo"),
            ],
            "^~foo",
        ),
        (
            "%*+foo",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("BOOL_VARIANT", value="+foo"),
            ],
            "%+foo",
        ),
        (
            "%*~foo",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="*"),
                Token("BOOL_VARIANT", value="~foo"),
            ],
            "%~foo",
        ),
        # version range and list
        ("@1.6,1.2:1.4", [Token("VERSION", value="@1.6,1.2:1.4")], r"@1.2:1.4,1.6"),
        (
            r"os=fe",  # Various translations associated with the architecture
            [Token("KEY_VALUE_PAIR", value="os=fe")],
            "platform=test os=debian6",
        ),
        (
            r"os=default_os",
            [Token("KEY_VALUE_PAIR", value="os=default_os")],
            "platform=test os=debian6",
        ),
        (
            r"target=be",
            [Token("KEY_VALUE_PAIR", value="target=be")],
            f"platform=test target={spack.platforms.test.Test.default}",
        ),
        (
            r"target=default_target",
            [Token("KEY_VALUE_PAIR", value="target=default_target")],
            f"platform=test target={spack.platforms.test.Test.default}",
        ),
        (r"platform=linux", [Token("KEY_VALUE_PAIR", value="platform=linux")], r"platform=linux"),
        # Version hash pair
        (
            rf"develop-branch-version@{'abc12' * 8}=develop",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="develop-branch-version"),
                Token(
                    "VERSION",
                    value=f"@{'abc12' * 8}=develop",
                    git_version=f"{'abc12' * 8}=develop",
                ),
            ],
            rf"develop-branch-version@{'abc12' * 8}=develop",
        ),
        # Redundant specs
        (
            r"x ^y@foo ^y@foo",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="x"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("VERSION", value="@foo"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("VERSION", value="@foo"),
            ],
            r"x ^y@foo",
        ),
        (
            r"x ^y@foo ^y+bar",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="x"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("VERSION", value="@foo"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("BOOL_VARIANT", value="+bar"),
            ],
            r"x ^y+bar ^y@foo",
        ),
        (
            r"x ^y@foo +bar ^y@foo",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="x"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("VERSION", value="@foo"),
                Token("BOOL_VARIANT", value="+bar"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="y"),
                Token("VERSION", value="@foo"),
            ],
            r"x ^y@foo+bar",
        ),
        # Ambiguous variant specification
        (
            r"_openmpi +debug-qt_4",  # Parse as a single bool variant
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("BOOL_VARIANT", value="+debug-qt_4"),
            ],
            r"_openmpi+debug-qt_4",
        ),
        (
            r"_openmpi +debug -qt_4",  # Parse as two variants
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("BOOL_VARIANT", value="+debug"),
                Token("BOOL_VARIANT", value="-qt_4"),
            ],
            r"_openmpi+debug~qt_4",
        ),
        (
            r"_openmpi +debug~qt_4",  # Parse as two variants
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="_openmpi"),
                Token("BOOL_VARIANT", value="+debug"),
                Token("BOOL_VARIANT", value="~qt_4"),
            ],
            r"_openmpi+debug~qt_4",
        ),
        # Key value pairs with ":" and "," in the value
        (
            r"target=:broadwell,icelake",
            [Token("KEY_VALUE_PAIR", value="target=:broadwell,icelake")],
            r"target=:broadwell,icelake",
        ),
        # Hash pair version followed by a variant
        (
            f"develop-branch-version@git.{'a' * 40}=develop+var1+var2",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="develop-branch-version"),
                Token(
                    "VERSION",
                    value=f"@git.{'a' * 40}=develop",
                    git_version=f"git.{'a' * 40}=develop",
                ),
                Token("BOOL_VARIANT", value="+var1", bv_prefix="+", bv_name="var1"),
                Token("BOOL_VARIANT", value="+var2", bv_prefix="+", bv_name="var2"),
            ],
            f"develop-branch-version@git.{'a' * 40}=develop+var1+var2",
        ),
        # Compiler with version ranges
        (
            "%gcc@10.2.1:",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@10.2.1:"),
            ],
            "%gcc@10.2.1:",
        ),
        (
            "%gcc@:10.2.1",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@:10.2.1"),
            ],
            "%gcc@:10.2.1",
        ),
        (
            "%gcc@10.2.1:12.1.0",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@10.2.1:12.1.0"),
            ],
            "%gcc@10.2.1:12.1.0",
        ),
        (
            "%gcc@10.1.0,12.2.1:",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@10.1.0,12.2.1:"),
            ],
            "%gcc@10.1.0,12.2.1:",
        ),
        (
            "%gcc@:8.4.3,10.2.1:12.1.0",
            [
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@:8.4.3,10.2.1:12.1.0"),
            ],
            "%gcc@:8.4.3,10.2.1:12.1.0",
        ),
        # Special key value arguments
        ("dev_path=*", [Token("KEY_VALUE_PAIR", value="dev_path=*")], "dev_path='*'"),
        ("dev_path=none", [Token("KEY_VALUE_PAIR", value="dev_path=none")], "dev_path=none"),
        (
            "dev_path=../relpath/work",
            [Token("KEY_VALUE_PAIR", value="dev_path=../relpath/work")],
            "dev_path=../relpath/work",
        ),
        (
            "dev_path=/abspath/work",
            [Token("KEY_VALUE_PAIR", value="dev_path=/abspath/work")],
            "dev_path=/abspath/work",
        ),
        # One liner for flags like 'a=b=c' that are injected
        ("cflags=a=b=c", [Token("KEY_VALUE_PAIR", value="cflags=a=b=c")], "cflags='a=b=c'"),
        ("cflags=a=b=c", [Token("KEY_VALUE_PAIR", value="cflags=a=b=c")], "cflags='a=b=c'"),
        ("cflags=a=b=c+~", [Token("KEY_VALUE_PAIR", value="cflags=a=b=c+~")], "cflags='a=b=c+~'"),
        (
            "cflags=-Wl,a,b,c",
            [Token("KEY_VALUE_PAIR", value="cflags=-Wl,a,b,c")],
            "cflags=-Wl,a,b,c",
        ),
        # Multi quoted
        (
            'cflags=="-O3 -g"',
            [
                Token(
                    "KEY_VALUE_PAIR",
                    value='cflags=="-O3 -g"',
                    kv_name="cflags",
                    kv_sep="==",
                    kv_value='"-O3 -g"',
                )
            ],
            "cflags=='-O3 -g'",
        ),
        # Whitespace is allowed in version lists
        ("@1.2:1.4 , 1.6 ", [Token("VERSION", value="@1.2:1.4 , 1.6")], "@1.2:1.4,1.6"),
        # But not in ranges. `a@1:` and `b` are separate specs, not a single `a@1:b`.
        (
            "a@1: b",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="a"),
                Token("VERSION", value="@1:"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="b"),
            ],
            "a@1:",
        ),
        (
            "+ debug % intel @ 12.1:12.6",
            [
                Token("BOOL_VARIANT", value="+ debug"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
                Token("VERSION", value="@ 12.1:12.6"),
            ],
            "+debug %intel@12.1:12.6",
        ),
        (
            "@ 12.1:12.6 + debug - qt_4",
            [
                Token("VERSION", value="@ 12.1:12.6"),
                Token("BOOL_VARIANT", value="+ debug"),
                Token("BOOL_VARIANT", value="- qt_4"),
            ],
            "@12.1:12.6+debug~qt_4",
        ),
        (
            "@10.4.0:10,11.3.0:target=aarch64:",
            [
                Token("VERSION", value="@10.4.0:10,11.3.0:"),
                Token("KEY_VALUE_PAIR", value="target=aarch64:"),
            ],
            "@10.4.0:10,11.3.0: target=aarch64:",
        ),
        (
            "@:0.4 % nvhpc",
            [
                Token("VERSION", value="@:0.4"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="nvhpc"),
            ],
            "@:0.4 %nvhpc",
        ),
        (
            "^[virtuals=mpi] openmpi",
            [
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="virtuals=mpi"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
            ],
            "^mpi=openmpi",
        ),
        (
            "^mpi=openmpi",
            [
                Token(
                    "DEPENDENCY",
                    value="^mpi=openmpi",
                    edge_virtuals="mpi",
                    edge_substitute="openmpi",
                )
            ],
            "^mpi=openmpi",
        ),
        # Neither edge is direct, and the virtuals they declare are different, so the two share
        # no role and stay parallel, like the plain ^y@foo ^y+bar case above.
        (
            "^[virtuals=mpi] openmpi+foo ^[virtuals=lapack] openmpi+bar",
            [
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="virtuals=mpi"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
                Token("BOOL_VARIANT", value="+foo"),
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="virtuals=lapack"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="openmpi"),
                Token("BOOL_VARIANT", value="+bar"),
            ],
            "^lapack=openmpi+bar ^mpi=openmpi+foo",
        ),
        (
            "^lapack,mpi=openmpi+foo+bar",
            [
                Token(
                    "DEPENDENCY",
                    value="^lapack,mpi=openmpi",
                    edge_virtuals="lapack,mpi",
                    edge_substitute="openmpi",
                ),
                Token("BOOL_VARIANT", value="+foo", bv_prefix="+", bv_name="foo"),
                Token("BOOL_VARIANT", value="+bar", bv_prefix="+", bv_name="bar"),
            ],
            "^lapack,mpi=openmpi+bar+foo",
        ),
        (
            "^[deptypes=link,build] zlib",
            [
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="deptypes=link,build"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
            ],
            "^[deptypes=build,link] zlib",
        ),
        # Indirect edges to one name are never one node on deptypes alone; a shared virtual, or
        # being direct, is what fuses them. When neither depflag is a superset of the other, the
        # edges stay parallel.
        (
            "^[deptypes=link] zlib ^[deptypes=build] zlib",
            [
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="deptypes=link"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="deptypes=build"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
            ],
            "^[deptypes=link] zlib ^[deptypes=build] zlib",
        ),
        # [build,link] already satisfies [link], so the second edge is redundant and is discarded.
        (
            "^[deptypes=build,link] zlib ^[deptypes=link] zlib",
            [
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="deptypes=build,link"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
                Token("DEPENDENCY", value="^["),
                Token("KEY_VALUE_PAIR", value="deptypes=link"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
            ],
            "^[deptypes=build,link] zlib",
        ),
        # A bare duplicate ^pkg-b is redundant, on either side of the % edge.
        (
            "pkg-a ^pkg-b %pkg-c ^pkg-b",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-a"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-c"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
            ],
            "pkg-a ^pkg-b %pkg-c",
        ),
        # A ^ dependency is merged only once its trailing % edges are parsed: the % edge
        # survives on the merged node.
        (
            "pkg-a ^pkg-b ^pkg-b %pkg-c",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-a"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-c"),
            ],
            "pkg-a ^pkg-b %pkg-c",
        ),
        (
            "pkg-a ^pkg-b ^pkg-b@1 %pkg-c",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-a"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("VERSION", value="@1"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-c"),
            ],
            "pkg-a ^pkg-b@1 %pkg-c",
        ),
        # With the % sub-dag included, neither ^pkg-b edge satisfies the other, so they
        # stay parallel.
        (
            "pkg-a ^pkg-b@1 ^pkg-b %pkg-c",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-a"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("VERSION", value="@1"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-b"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="pkg-c"),
            ],
            "pkg-a ^pkg-b %pkg-c ^pkg-b@1",
        ),
        (
            "git-test@git.foo/bar",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "git-test"),
                Token("VERSION", "@git.foo/bar", git_version="git.foo/bar"),
            ],
            "git-test@git.foo/bar",
        ),
        # Variant propagation
        (
            "zlib ++foo",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("BOOL_VARIANT", "++foo", bv_prefix="++", bv_name="foo"),
            ],
            "zlib++foo",
        ),
        (
            "zlib ~~foo",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("BOOL_VARIANT", "~~foo", bv_prefix="~~", bv_name="foo"),
            ],
            "zlib~~foo",
        ),
        (
            "zlib foo==bar",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("KEY_VALUE_PAIR", "foo==bar", kv_name="foo", kv_sep="==", kv_value="bar"),
            ],
            "zlib foo==bar",
        ),
        # Compilers specifying virtuals
        (
            "zlib %[virtuals=c] gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("DEPENDENCY", value="%["),
                Token("KEY_VALUE_PAIR", value="virtuals=c"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
            ],
            "zlib %c=gcc",
        ),
        (
            "zlib %c=gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("DEPENDENCY", value="%c=gcc", edge_virtuals="c", edge_substitute="gcc"),
            ],
            "zlib %c=gcc",
        ),
        (
            "zlib %[virtuals=c,cxx] gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("DEPENDENCY", value="%["),
                Token("KEY_VALUE_PAIR", value="virtuals=c,cxx"),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
            ],
            "zlib %c,cxx=gcc",
        ),
        (
            "zlib %c,cxx=gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token(
                    "DEPENDENCY", value="%c,cxx=gcc", edge_virtuals="c,cxx", edge_substitute="gcc"
                ),
            ],
            "zlib %c,cxx=gcc",
        ),
        (
            "zlib %[virtuals=c,cxx] gcc@14.1",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("DEPENDENCY", value="%[", edge_bracket="["),
                Token(
                    "KEY_VALUE_PAIR",
                    value="virtuals=c,cxx",
                    kv_name="virtuals",
                    kv_sep="=",
                    kv_value="c,cxx",
                ),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@14.1", version_list="14.1"),
            ],
            "zlib %c,cxx=gcc@14.1",
        ),
        (
            "zlib %c,cxx=gcc@14.1",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token(
                    "DEPENDENCY", value="%c,cxx=gcc", edge_virtuals="c,cxx", edge_substitute="gcc"
                ),
                Token("VERSION", value="@14.1", version_list="14.1"),
            ],
            "zlib %c,cxx=gcc@14.1",
        ),
        (
            "zlib %[virtuals=fortran] gcc@14.1 %[virtuals=c,cxx] clang",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token("DEPENDENCY", value="%[", edge_bracket="["),
                Token(
                    "KEY_VALUE_PAIR",
                    value="virtuals=fortran",
                    kv_name="virtuals",
                    kv_sep="=",
                    kv_value="fortran",
                ),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("VERSION", value="@14.1", version_list="14.1"),
                Token("DEPENDENCY", value="%[", edge_bracket="["),
                Token(
                    "KEY_VALUE_PAIR",
                    value="virtuals=c,cxx",
                    kv_name="virtuals",
                    kv_sep="=",
                    kv_value="c,cxx",
                ),
                Token("END_EDGE_PROPERTIES", value="]"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="clang"),
            ],
            "zlib %fortran=gcc@14.1 %c,cxx=clang",
        ),
        (
            "zlib %fortran=gcc@14.1 %c,cxx=clang",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "zlib"),
                Token(
                    "DEPENDENCY",
                    value="%fortran=gcc",
                    edge_virtuals="fortran",
                    edge_substitute="gcc",
                ),
                Token("VERSION", value="@14.1", version_list="14.1"),
                Token(
                    "DEPENDENCY",
                    value="%c,cxx=clang",
                    edge_virtuals="c,cxx",
                    edge_substitute="clang",
                ),
            ],
            "zlib %fortran=gcc@14.1 %c,cxx=clang",
        ),
        # test := and :== syntax for key value pairs
        (
            "gcc languages:=c,c++",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
                Token("KEY_VALUE_PAIR", "languages:=c,c++"),
            ],
            "gcc languages:='c,c++'",
        ),
        (
            "gcc languages:==c,c++",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
                Token(
                    "KEY_VALUE_PAIR",
                    "languages:==c,c++",
                    kv_name="languages",
                    kv_sep=":==",
                    kv_value="c,c++",
                ),
            ],
            "gcc languages:=='c,c++'",
        ),
        # test <variants> etc. after %
        (
            "mvapich %gcc languages:=c,c++ target=x86_64",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "mvapich"),
                Token("DEPENDENCY", "%"),
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
                Token("KEY_VALUE_PAIR", "languages:=c,c++"),
                Token("KEY_VALUE_PAIR", "target=x86_64"),
            ],
            "mvapich %gcc languages:='c,c++' target=x86_64",
        ),
        # Test conditional dependencies
        (
            "foo ^[when='%c' virtuals=c] gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "^["),
                Token("KEY_VALUE_PAIR", "when='%c'"),
                Token("KEY_VALUE_PAIR", "virtuals=c"),
                Token("END_EDGE_PROPERTIES", "]"),
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
            ],
            "foo ^[when=%c] c=gcc",
        ),
        (
            "foo ^[when='%c' virtuals=c]gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "^["),
                Token("KEY_VALUE_PAIR", "when='%c'"),
                Token("KEY_VALUE_PAIR", "virtuals=c"),
                Token("END_EDGE_PROPERTIES", "]"),
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
            ],
            "foo ^[when=%c] c=gcc",
        ),
        (
            "foo ^[when=%c] c=gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "^[", edge_bracket="["),
                Token("KEY_VALUE_PAIR", "when=%c", kv_name="when", kv_sep="=", kv_value="%c"),
                Token(
                    "END_EDGE_PROPERTIES",
                    "] c=gcc",
                    end_edge_virtuals="c",
                    end_edge_substitute="gcc",
                ),
            ],
            "foo ^[when=%c] c=gcc",
        ),
        # Test dependency propagation
        (
            "foo %%gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "%%"),
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
            ],
            "foo %%gcc",
        ),
        (
            "foo %%c,cxx=gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "%%c,cxx=gcc", edge_virtuals="c,cxx", edge_substitute="gcc"),
            ],
            "foo %%c,cxx=gcc",
        ),
        (
            "foo %%[when=%c] c=gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "%%[", edge_bracket="["),
                Token("KEY_VALUE_PAIR", "when=%c", kv_name="when", kv_sep="=", kv_value="%c"),
                Token(
                    "END_EDGE_PROPERTIES",
                    "] c=gcc",
                    end_edge_virtuals="c",
                    end_edge_substitute="gcc",
                ),
            ],
            "foo %%[when=%c] c=gcc",
        ),
        (
            "foo %%[when='%c' virtuals=c] gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", "foo"),
                Token("DEPENDENCY", "%%["),
                Token("KEY_VALUE_PAIR", "when='%c'"),
                Token("KEY_VALUE_PAIR", "virtuals=c"),
                Token("END_EDGE_PROPERTIES", "]"),
                Token("UNQUALIFIED_PACKAGE_NAME", "gcc"),
            ],
            "foo %%[when=%c] c=gcc",
        ),
        # whitespace between edge properties and a virtual assignment
        (
            "foo ^[when=%c]   c,cxx=builtin.gcc@14+bar",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="foo"),
                Token("DEPENDENCY", value="^[", edge_bracket="["),
                Token("KEY_VALUE_PAIR", "when=%c", kv_name="when", kv_sep="=", kv_value="%c"),
                Token(
                    "END_EDGE_PROPERTIES",
                    "]   c,cxx=builtin.gcc",
                    end_edge_virtuals="c,cxx",
                    end_edge_substitute="builtin.gcc",
                ),
                Token("VERSION", value="@14", version_list="14"),
                Token("BOOL_VARIANT", value="+bar", bv_prefix="+", bv_name="bar"),
            ],
            "foo ^[when=%c] c,cxx=builtin.gcc@14+bar",
        ),
    ],
)
def test_parse_single_spec(spec_str, tokens, expected_roundtrip, mock_git_test_package):
    parser = SpecParser(spec_str)
    has_detailed_tokens = any(t[2] for t in tokens)
    assert tokens == parser.tokens(with_subgroups=has_detailed_tokens)
    assert expected_roundtrip == str(parser.next_spec())


@pytest.mark.parametrize(
    "text,tokens,expected_specs",
    [
        (
            "mvapich emacs",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
            ],
            ["mvapich", "emacs"],
        ),
        (
            "mvapich cppflags='-O3 -fPIC' emacs",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("KEY_VALUE_PAIR", value="cppflags='-O3 -fPIC'"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
            ],
            ["mvapich cppflags='-O3 -fPIC'", "emacs"],
        ),
        (
            "mvapich cppflags=-O3 emacs",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("KEY_VALUE_PAIR", value="cppflags=-O3"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
            ],
            ["mvapich cppflags=-O3", "emacs"],
        ),
        (
            "mvapich emacs @1.1.1 cflags=-O3 %intel",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
                Token("VERSION", value="@1.1.1"),
                Token("KEY_VALUE_PAIR", value="cflags=-O3"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
            ],
            ["mvapich", "emacs @1.1.1 cflags=-O3 %intel"],
        ),
        (
            'mvapich cflags="-O3 -fPIC" emacs^ncurses%intel',
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("KEY_VALUE_PAIR", value='cflags="-O3 -fPIC"'),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="ncurses"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="intel"),
            ],
            ['mvapich cflags="-O3 -fPIC"', "emacs ^ncurses%intel"],
        ),
        (
            "mvapich %gcc languages=c,c++ emacs ^ncurses%gcc languages:=c",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="mvapich"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("KEY_VALUE_PAIR", value="languages=c,c++"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="emacs"),
                Token("DEPENDENCY", value="^"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="ncurses"),
                Token("DEPENDENCY", value="%"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
                Token("KEY_VALUE_PAIR", value="languages:=c"),
            ],
            ["mvapich %gcc languages=c,c++", "emacs ^ncurses%gcc languages:=c"],
        ),
        (
            "zlib %c=gcc gcc",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="zlib"),
                Token("DEPENDENCY", value="%c=gcc"),
                Token("UNQUALIFIED_PACKAGE_NAME", value="gcc"),
            ],
            ["zlib %c=gcc", "gcc"],
        ),
    ],
)
def test_parse_multiple_specs(text, tokens, expected_specs):
    total_parser = SpecParser(text)
    assert total_parser.tokens() == tokens

    for single_spec_text in expected_specs:
        single_spec_parser = SpecParser(single_spec_text)
        assert str(total_parser.next_spec()) == str(single_spec_parser.next_spec())


@pytest.mark.parametrize(
    "args,expected",
    [
        # Test that CLI-quoted flags/variant values are preserved
        (["zlib", "cflags=-O3 -g", "+bar", "baz"], "zlib cflags='-O3 -g' +bar baz"),
        # Test that CLI-quoted propagated flags/variant values are preserved
        (["zlib", "cflags==-O3 -g", "+bar", "baz"], "zlib cflags=='-O3 -g' +bar baz"),
        # An entire string passed on the CLI with embedded quotes also works
        (["zlib cflags='-O3 -g' +bar baz"], "zlib cflags='-O3 -g' +bar baz"),
        # Entire string *without* quoted flags splits -O3/-g (-g interpreted as a variant)
        (["zlib cflags=-O3 -g +bar baz"], "zlib cflags=-O3 +bar~g baz"),
        # If the entirety of "-O3 -g +bar baz" is quoted on the CLI, it's all taken as flags
        (["zlib", "cflags=-O3 -g +bar baz"], "zlib cflags='-O3 -g +bar baz'"),
        # If the string doesn't start with key=, it needs internal quotes for flags
        (["zlib", " cflags=-O3 -g +bar baz"], "zlib cflags=-O3 +bar~g baz"),
        # Internal quotes for quoted CLI args are considered part of *one* arg
        (["zlib", 'cflags="-O3 -g" +bar baz'], """zlib cflags='"-O3 -g" +bar baz'"""),
        # Use double quotes if internal single quotes are present
        (["zlib", "cflags='-O3 -g' +bar baz"], '''zlib cflags="'-O3 -g' +bar baz"'''),
        # There is no escaping: a value cannot contain both kinds of quotes
        (["zlib", '''cflags='-O3 -g' "+bar baz"'''], spack.error.SpecSyntaxError),
        # and a backslash is a character like any other: the compiler gets the define as typed
        (["zlib", r"cflags=-DCHAR=\'x\'"], r'''zlib cflags="-DCHAR=\'x\'"'''),
        # Ensure that empty strings are handled correctly on CLI
        (["zlib", "ldflags=", "+pic"], "zlib+pic"),
        # These flags are assumed to be quoted by the shell, but the space doesn't matter because
        # flags are space-separated.
        (["zlib", "ldflags= +pic"], "zlib ldflags='+pic'"),
        (["ldflags= +pic"], "ldflags='+pic'"),
        # If the name is not a flag name, the space is preserved verbatim, because variant values
        # are comma-separated.
        (["zlib", "foo= +pic"], "zlib foo=' +pic'"),
        (["foo= +pic"], "foo=' +pic'"),
        # You can ensure no quotes are added parse_specs() by starting your string with space,
        # but you still need to quote empty strings properly.
        ([" ldflags= +pic"], SpecTokenizationError),
        ([" ldflags=", "+pic"], SpecTokenizationError),
        ([" ldflags='' +pic"], "+pic"),
        ([" ldflags=''", "+pic"], "+pic"),
        # Ensure that empty strings are handled properly in quoted strings
        (["zlib ldflags='' +pic"], "zlib+pic"),
        # Ensure that $ORIGIN is handled correctly
        (["zlib", "ldflags=-Wl,-rpath=$ORIGIN/_libs"], "zlib ldflags='-Wl,-rpath=$ORIGIN/_libs'"),
        # A closing bracket ends the edge attribute list, it is never part of the value
        (["mpileaks", "%[", "when=@1.0]", "gcc"], "mpileaks %[when=@1.0] gcc"),
        # a value that parses as it is stays unquoted: c=gcc@14 is a virtual assignment
        (["mpileaks", "%[when=+x]", "c=gcc@14"], "mpileaks %[when=+x] c=gcc@14"),
        # Ensure that passing escaped quotes on the CLI raises a tokenization error
        (["zlib", '"-g', '-O2"'], SpecTokenizationError),
    ],
)
def test_cli_spec_roundtrip(args, expected):
    if isinstance(expected, type) and issubclass(expected, BaseException):
        with pytest.raises(expected):
            spack.cmd.parse_specs(args)
        return

    specs = spack.cmd.parse_specs(args)
    output_string = " ".join(str(spec) for spec in specs)
    assert expected == output_string


@pytest.mark.parametrize(
    ["spec_str", "toolchain", "expected_roundtrip"],
    [
        (
            "foo%my_toolchain",
            {"my_toolchain": "%[when='%c' virtuals=c]gcc"},
            ["foo %[when=%c] c=gcc"],
        ),
        ("foo%my_toolchain", {"my_toolchain": "%[when=%c] c=gcc"}, ["foo %[when=%c] c=gcc"]),
        (
            "foo%my_toolchain",
            {"my_toolchain": "+bar cflags=baz %[when='%c' virtuals=c]gcc"},
            ["foo cflags=baz +bar %[when=%c] c=gcc"],
        ),
        (
            "foo%my_toolchain",
            {"my_toolchain": "+bar cflags=baz %[when=%c]c=gcc"},
            ["foo cflags=baz +bar %[when=%c] c=gcc"],
        ),
        (
            "foo%my_toolchain2",
            {"my_toolchain2": "%[when='%c' virtuals=c]gcc %[when='+mpi' virtuals=mpi]mpich"},
            ["foo %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain2",
            {"my_toolchain2": "%[when=%c] c=gcc %[when=+mpi] mpi=mpich"},
            ["foo %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain bar%my_toolchain2",
            {
                "my_toolchain": "%[when='%c' virtuals=c]gcc",
                "my_toolchain2": "%[when='%c' virtuals=c]gcc %[when='+mpi' virtuals=mpi]mpich",
            },
            ["foo %[when=%c] c=gcc", "bar %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain bar%my_toolchain2",
            {
                "my_toolchain": "%[when=%c] c=gcc",
                "my_toolchain2": "%[when=%c] c=gcc %[when=+mpi]mpi=mpich",
            },
            ["foo %[when=%c] c=gcc", "bar %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain2",
            {
                "my_toolchain2": [
                    {"spec": "%[virtuals=c]gcc", "when": "%c"},
                    {"spec": "%[virtuals=mpi]mpich", "when": "+mpi"},
                ]
            },
            ["foo %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain2",
            {
                "my_toolchain2": [
                    {"spec": "%c=gcc", "when": "%c"},
                    {"spec": "%mpi=mpich", "when": "+mpi"},
                ]
            },
            ["foo %[when=%c] c=gcc %[when=+mpi] mpi=mpich"],
        ),
        (
            "foo%my_toolchain2",
            {"my_toolchain2": [{"spec": "%[virtuals=c]gcc %[virtuals=mpi]mpich", "when": "%c"}]},
            ["foo %[when=%c] c=gcc %[when=%c] mpi=mpich"],
        ),
        (
            "foo%my_toolchain2",
            {"my_toolchain2": [{"spec": "%c=gcc %mpi=mpich", "when": "%c"}]},
            ["foo %[when=%c] c=gcc %[when=%c] mpi=mpich"],
        ),
        # Test that we don't get caching wrong in the parser
        (
            "foo %gcc-mpich ^bar%gcc-mpich",
            {
                "gcc-mpich": [
                    {"spec": "%[virtuals=c] gcc", "when": "%c"},
                    {"spec": "%[virtuals=mpi] mpich", "when": "%mpi"},
                ]
            },
            [
                "foo %[when=%c] c=gcc %[when=%mpi] mpi=mpich "
                "^bar %[when=%c] c=gcc %[when=%mpi] mpi=mpich"
            ],
        ),
        (
            "foo %gcc-mpich ^bar%gcc-mpich",
            {
                "gcc-mpich": [
                    {"spec": "%c=gcc", "when": "%c"},
                    {"spec": "%mpi=mpich", "when": "%mpi"},
                ]
            },
            [
                "foo %[when=%c] c=gcc %[when=%mpi] mpi=mpich "
                "^bar %[when=%c] c=gcc %[when=%mpi] mpi=mpich"
            ],
        ),
    ],
)
def test_parse_toolchain(spec_str, toolchain, expected_roundtrip, mutable_config, mock_packages):
    """Tests that toolchains are expanded correctly"""
    parser = SpecParser(spec_str)
    for expected in expected_roundtrip:
        result = parser.next_spec()
        expand_toolchains(result, toolchain)
        assert expected == str(result)


@pytest.mark.parametrize(
    "text,expected_in_error",
    [
        ("x@@1.2", r"x@@1.2\n ^"),
        ("y ^x@@1.2", r"y ^x@@1.2\n    ^"),
        ("x@1.2::", r"x@1.2::\n      ^"),
        ("x::", r"x::\n ^^"),
        ("cflags=''-Wl,a,b,c''", r"cflags=''-Wl,a,b,c''\n            ^ ^ ^ ^^"),
        ("@1.2:   develop   = foo", r"@1.2:   develop   = foo\n                  ^"),
        ("@1.2:develop   = foo", r"@1.2:develop   = foo\n               ^"),
    ],
)
def test_error_reporting(text, expected_in_error):
    parser = SpecParser(text)
    with pytest.raises(SpecTokenizationError) as exc:
        parser.tokens()

    assert expected_in_error in str(exc), parser.tokens()


@pytest.mark.parametrize(
    "text,tokens",
    [
        ("/abcde", [Token("DAG_HASH", value="/abcde")]),
        (
            "foo/abcde",
            [Token("UNQUALIFIED_PACKAGE_NAME", value="foo"), Token("DAG_HASH", value="/abcde")],
        ),
        (
            "foo@1.2.3 /abcde",
            [
                Token("UNQUALIFIED_PACKAGE_NAME", value="foo"),
                Token("VERSION", value="@1.2.3"),
                Token("DAG_HASH", value="/abcde"),
            ],
        ),
    ],
)
def test_spec_by_hash_tokens(text, tokens):
    parser = SpecParser(text)
    assert parser.tokens() == tokens


@pytest.mark.db
def test_spec_by_hash(database, monkeypatch, config):
    mpileaks = database.query_one("mpileaks ^zmpi")
    b = spack.concretize.concretize_one("pkg-b")
    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: [b])

    hash_str = f"/{mpileaks.dag_hash()}"
    parsed_spec = SpecParser(hash_str).next_spec()
    spack.hash_lookup.replace_hash(parsed_spec)
    assert parsed_spec == mpileaks

    short_hash_str = f"/{mpileaks.dag_hash()[:5]}"
    parsed_spec = SpecParser(short_hash_str).next_spec()
    spack.hash_lookup.replace_hash(parsed_spec)
    assert parsed_spec == mpileaks

    name_version_and_hash = f"{mpileaks.name}@{mpileaks.version} /{mpileaks.dag_hash()[:5]}"
    parsed_spec = SpecParser(name_version_and_hash).next_spec()
    spack.hash_lookup.replace_hash(parsed_spec)
    assert parsed_spec == mpileaks

    b_hash = f"/{b.dag_hash()}"
    parsed_spec = SpecParser(b_hash).next_spec()
    spack.hash_lookup.replace_hash(parsed_spec)
    assert parsed_spec == b


@pytest.mark.db
def test_dep_spec_by_hash(database, config):
    mpileaks_zmpi = database.query_one("mpileaks ^zmpi")
    zmpi = database.query_one("zmpi")
    fake = database.query_one("fake")

    assert "fake" in mpileaks_zmpi
    assert "zmpi" in mpileaks_zmpi

    mpileaks_hash_fake = SpecParser(f"mpileaks ^/{fake.dag_hash()} ^zmpi").next_spec()
    spack.hash_lookup.replace_hash(mpileaks_hash_fake)
    assert "fake" in mpileaks_hash_fake
    assert mpileaks_hash_fake["fake"] == fake
    assert "zmpi" in mpileaks_hash_fake
    assert mpileaks_hash_fake["zmpi"] == spack.spec.Spec("zmpi")

    mpileaks_hash_zmpi = SpecParser(f"mpileaks ^ /{zmpi.dag_hash()}").next_spec()
    spack.hash_lookup.replace_hash(mpileaks_hash_zmpi)
    assert "zmpi" in mpileaks_hash_zmpi
    assert mpileaks_hash_zmpi["zmpi"] == zmpi

    mpileaks_hash_fake_and_zmpi = SpecParser(
        f"mpileaks ^/{fake.dag_hash()[:4]} ^ /{zmpi.dag_hash()[:5]}"
    ).next_spec()
    spack.hash_lookup.replace_hash(mpileaks_hash_fake_and_zmpi)
    assert "zmpi" in mpileaks_hash_fake_and_zmpi
    assert mpileaks_hash_fake_and_zmpi["zmpi"] == zmpi

    assert "fake" in mpileaks_hash_fake_and_zmpi
    assert mpileaks_hash_fake_and_zmpi["fake"] == fake


@pytest.mark.db
def test_multiple_specs_with_hash(database, config):
    mpileaks_zmpi = database.query_one("mpileaks ^zmpi")
    callpath_mpich2 = database.query_one("callpath ^mpich2")

    # name + hash + separate hash
    specs = SpecParser(
        f"mpileaks /{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()}"
    ).all_specs()
    assert len(specs) == 2

    # 2 separate hashes
    specs = SpecParser(f"/{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()}").all_specs()
    assert len(specs) == 2

    # 2 separate hashes + name
    specs = SpecParser(
        f"/{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()} callpath"
    ).all_specs()
    assert len(specs) == 3

    # hash + 2 names
    specs = SpecParser(f"/{mpileaks_zmpi.dag_hash()} callpath callpath").all_specs()
    assert len(specs) == 3

    # hash + name + hash
    specs = SpecParser(
        f"/{mpileaks_zmpi.dag_hash()} callpath /{callpath_mpich2.dag_hash()}"
    ).all_specs()
    assert len(specs) == 2


@pytest.mark.db
def test_ambiguous_hash(mutable_database):
    """Test that abstract hash ambiguity is delayed until concretization.
    In the past this ambiguity error would happen during parse time."""

    # This is a very sketchy as manually setting hashes easily breaks invariants
    x1 = spack.concretize.concretize_one("pkg-a")
    x2 = x1.copy()
    x1._hash = "xxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    x2._hash = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    assert x1 != x2  # doesn't hold when only the dag hash is modified.

    mutable_database.add(x1)
    mutable_database.add(x2)

    # ambiguity in first hash character
    s1 = SpecParser("/xxx").next_spec()
    with pytest.raises(spack.spec.AmbiguousHashError):
        spack.hash_lookup.lookup_hash(s1)

    # ambiguity in first hash character AND spec name
    s2 = SpecParser("pkg-a/xxx").next_spec()
    with pytest.raises(spack.spec.AmbiguousHashError):
        spack.hash_lookup.lookup_hash(s2)


@pytest.mark.db
def test_invalid_hash(database, config):
    zmpi = database.query_one("zmpi")
    mpich = database.query_one("mpich")

    # name + incompatible hash
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"zmpi /{mpich.dag_hash()}").next_spec()
        spack.hash_lookup.replace_hash(parsed_spec)
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"mpich /{zmpi.dag_hash()}").next_spec()
        spack.hash_lookup.replace_hash(parsed_spec)

    # name + dep + incompatible hash
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"mpileaks ^zmpi /{mpich.dag_hash()}").next_spec()
        spack.hash_lookup.replace_hash(parsed_spec)


def test_invalid_hash_dep(database, config):
    mpich = database.query_one("mpich")
    hash = mpich.dag_hash()
    with pytest.raises(spack.spec.InvalidHashError):
        s = spack.spec.Spec(f"callpath ^zlib/{hash}")
        spack.hash_lookup.replace_hash(s)


@pytest.mark.db
def test_nonexistent_hash(database, config):
    """Ensure we get errors for non existent hashes."""
    specs = database.query()

    # This hash shouldn't be in the test DB.  What are the odds :)
    no_such_hash = "aaaaaaaaaaaaaaa"
    hashes = [s._hash for s in specs]
    assert no_such_hash not in [h[: len(no_such_hash)] for h in hashes]

    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"/{no_such_hash}").next_spec()
        spack.hash_lookup.replace_hash(parsed_spec)


@pytest.mark.parametrize(
    "spec1,spec2,constraint",
    [
        ("zlib", "hdf5", None),
        ("zlib+shared", "zlib~shared", "+shared"),
        ("hdf5+mpi^zmpi", "hdf5~mpi", "^zmpi"),
        ("hdf5+mpi^mpich+debug", "hdf5+mpi^mpich~debug", "^mpich+debug"),
    ],
)
def test_disambiguate_hash_by_spec(spec1, spec2, constraint, mock_packages, monkeypatch, config):
    spec1_concrete = spack.concretize.concretize_one(spec1)
    spec2_concrete = spack.concretize.concretize_one(spec2)

    spec1_concrete._hash = "spec1"
    spec2_concrete._hash = "spec2"

    monkeypatch.setattr(
        spack.binary_distribution,
        "update_cache_and_get_specs",
        lambda: [spec1_concrete, spec2_concrete],
    )

    # Ordering is tricky -- for constraints we want after, for names we want before
    if not constraint:
        spec = spack.spec.Spec(spec1 + "/spec")
    else:
        spec = spack.spec.Spec("/spec" + constraint)

    assert spack.hash_lookup.lookup_hash(spec) == spec1_concrete


@pytest.mark.parametrize(
    "text,match_string",
    [
        # Duplicate variants
        ("x@1.2+debug+debug", "variant"),
        ("x ^y@1.2+debug debug=true", "variant"),
        ("x ^y@1.2 debug=false debug=true", "variant"),
        ("x ^y@1.2 debug=false ~debug", "variant"),
        # Multiple versions
        ("x@1.2@2.3", "version"),
        ("x@1.2:2.3@1.4", "version"),
        ("x@1.2@2.3:2.4", "version"),
        ("x@1.2@2.3,2.4", "version"),
        ("x@1.2 +foo~bar @2.3", "version"),
        ("x@1.2%y@1.2@2.3:2.4", "version"),
        # Duplicate Architectures
        ("x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64", "two architectures"),
        ("x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le", "two architectures"),
        ("x arch=linux-rhel7-ppc64le arch=linux-rhel7-x86_64", "two architectures"),
        ("y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64", "two architectures"),
        ("y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le", "two architectures"),
        ("x os=redhat6 os=debian6", "'os'"),
        ("x os=debian6 os=redhat6", "'os'"),
        ("x target=core2 target=x86_64", "'target'"),
        ("x target=x86_64 target=core2", "'target'"),
        ("x platform=test platform=test", "'platform'"),
        # TODO: these two seem wrong: need to change how arch is initialized (should fail on os)
        ("x os=debian6 platform=test target=default_target os=redhat6", "two architectures"),
        ("x target=default_target platform=test os=redhat6 os=debian6", "'platform'"),
        # Dependencies
        ("^[@foo] zlib", "edge attributes"),
        # TODO: Remove this as soon as use variants are added and we can parse custom attributes
        ("^[foo=bar] zlib", "edge attributes"),
        # Propagating reserved names generates a parse error
        ("x namespace==foo.bar.baz", "Propagation"),
        ("x arch==linux-rhel9-x86_64", "Propagation"),
        ("x architecture==linux-rhel9-x86_64", "Propagation"),
        ("x os==rhel9", "Propagation"),
        ("x operating_system==rhel9", "Propagation"),
        ("x target==x86_64", "Propagation"),
        ("x dev_path==/foo/bar/baz", "Propagation"),
        ("x patches==abcde12345,12345abcde", "Propagation"),
        # a when= condition is a spec, which extends up to the closing bracket
        ("foo ^[when=] bar", "expected a spec after when="),
        ("foo ^[when=", "expected a spec after when="),
        ("foo ^[when=bar baz] qux", "unexpected token in edge attributes"),
        ("foo ^[when=bar ^baz", "unexpected token in edge attributes"),
        # a quoted condition is a single spec: neither two specs nor none
        ("foo ^[when='bar baz'] qux", "expected a single spec as the when= condition"),
        ("foo ^[when=''] qux", "expected a single spec as the when= condition"),
        # the parts of an architecture and the namespace print unquoted, so they must be values
        # that parse without quotes, and a namespace a dotted identifier
        ("x os='a b'", "invalid value"),
        ("x target='x?y'", "invalid value"),
        ("x platform=''", "invalid value"),
        ("x os=''", "invalid value"),
        ("x arch='a b'", "invalid value"),
        ("x namespace=a+b", "invalid value"),
        ("x namespace=','", "invalid value"),
        ("x namespace=''", "invalid value"),
        # they have a string value like arch, so the bool variant form is an error rather than
        # silently dropped
        ("x ~os", "must have a string value"),
        ("x ~platform", "must have a string value"),
        ("x ~target", "must have a string value"),
        ("x ~namespace", "must have a string value"),
        ("x +os", "must have a string value"),
        # = marks an exact version, which cannot be a bound of a range: a syntax error of the
        # spec, not a ValueError from the version list
        ("x @=1:2", "Bad characters in version string"),
        ("x @1:=2", "Bad characters in version string"),
        # a virtual assignment must directly follow a dependency sigil or edge properties
        ("c,cxx=gcc", "virtual assignment"),
        ("zlib c,cxx=gcc", "virtual assignment"),
        ("zlib %[c=gcc]", "edge attributes"),
        # regression: an unconsumed token used to make the parser loop forever
        ("zlib ]", "unexpected token"),
    ],
)
def test_error_conditions(text, match_string):
    with pytest.raises(SpecParsingError, match=match_string):
        SpecParser(text).all_specs()


@pytest.mark.parametrize(
    "text,exc_cls",
    [
        # Specfile related errors
        pytest.param(
            "/bogus/path/libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_WINDOWS
        ),
        pytest.param(
            "../../libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_WINDOWS
        ),
        pytest.param("./libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_WINDOWS),
        pytest.param(
            "libfoo ^/bogus/path/libdwarf.yaml",
            spack.error.NoSuchSpecFileError,
            marks=SKIP_ON_WINDOWS,
        ),
        pytest.param(
            "libfoo ^../../libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_WINDOWS
        ),
        pytest.param(
            "libfoo ^./libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_WINDOWS
        ),
        pytest.param(
            "/bogus/path/libdwarf.yamlfoobar",
            spack.error.NoSuchSpecFileError,
            marks=SKIP_ON_WINDOWS,
        ),
        pytest.param(
            "libdwarf^/bogus/path/libelf.yamlfoobar ^/path/to/bogus.yaml",
            spack.error.NoSuchSpecFileError,
            marks=SKIP_ON_WINDOWS,
        ),
        pytest.param(
            "c:\\bogus\\path\\libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_UNIX
        ),
        pytest.param("..\\..\\libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_UNIX),
        pytest.param(".\\libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_UNIX),
        pytest.param(
            "libfoo ^c:\\bogus\\path\\libdwarf.yaml",
            spack.error.NoSuchSpecFileError,
            marks=SKIP_ON_UNIX,
        ),
        pytest.param(
            "libfoo ^..\\..\\libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_UNIX
        ),
        pytest.param(
            "libfoo ^.\\libdwarf.yaml", spack.error.NoSuchSpecFileError, marks=SKIP_ON_UNIX
        ),
        pytest.param(
            "c:\\bogus\\path\\libdwarf.yamlfoobar",
            spack.error.SpecFilenameError,
            marks=SKIP_ON_UNIX,
        ),
        pytest.param(
            "libdwarf^c:\\bogus\\path\\libelf.yamlfoobar ^c:\\path\\to\\bogus.yaml",
            spack.error.SpecFilenameError,
            marks=SKIP_ON_UNIX,
        ),
    ],
)
def test_specfile_error_conditions_windows(text, exc_cls):
    with pytest.raises(exc_cls):
        SpecParser(text).all_specs()


@pytest.mark.parametrize(
    "filename,regex",
    [
        (r"c:\abs\windows\\path.yaml", WINDOWS_FILENAME),
        (r".\\relative\\dot\\win\\path.yaml", WINDOWS_FILENAME),
        (r"relative\\windows\\path.yaml", WINDOWS_FILENAME),
        ("/absolute/path/to/file.yaml", UNIX_FILENAME),
        ("relative/path/to/file.yaml", UNIX_FILENAME),
        ("./dot/rel/to/file.yaml", UNIX_FILENAME),
    ],
)
def test_specfile_parsing(filename, regex):
    match = re.match(regex, filename)
    assert match
    assert match.end() == len(filename)


def test_parse_specfile_simple(specfile_for, tmp_path: pathlib.Path):
    specfile = tmp_path / "libdwarf.json"
    s = specfile_for("libdwarf", specfile)

    spec = SpecParser(str(specfile)).next_spec()
    assert spec == s

    # Check we can mix literal and spec-file in text
    specs = SpecParser(f"mvapich_foo {str(specfile)}").all_specs()
    assert len(specs) == 2


@pytest.mark.parametrize("filename", ["libelf.yaml", "libelf.json"])
def test_parse_filename_missing_slash_as_spec(specfile_for, tmp_path: pathlib.Path, filename):
    """Ensure that libelf(.yaml|.json) parses as a spec, NOT a file."""
    specfile = tmp_path / filename
    specfile_for(filename.split(".")[0], specfile)

    # Move to where the specfile is located so that libelf.yaml is there
    with fs.working_dir(str(tmp_path)):
        specs = SpecParser("libelf.yaml").all_specs()
    assert len(specs) == 1

    spec = specs[0]
    assert spec.name == "yaml"
    assert spec.namespace == "libelf"
    assert spec.fullname == "libelf.yaml"

    # Check that if we concretize this spec, we get a good error
    # message that mentions we might've meant a file.
    with pytest.raises(spack.repo.UnknownEntityError) as exc_info:
        spack.concretize.concretize_one(spec)
    assert exc_info.value.long_message
    assert (
        "Did you mean to specify a filename with './libelf.yaml'?" in exc_info.value.long_message
    )

    # make sure that only happens when the spec ends in yaml
    with pytest.raises(spack.solver.asp.UnsatisfiableSpecError) as exc_info:
        spack.concretize.concretize_one("builtin_mock.doesnotexist")
    assert not exc_info.value.long_message or (
        "Did you mean to specify a filename with" not in exc_info.value.long_message
    )


def test_parse_specfile_dependency(config, mock_packages, tmp_path: pathlib.Path):
    """Ensure we can use a specfile as a dependency"""
    s = spack.concretize.concretize_one("libdwarf")

    specfile = tmp_path / "libelf.json"
    with open(specfile, "w", encoding="utf-8") as f:
        f.write(s["libelf"].to_json())

    # Make sure we can use yaml path as dependency, e.g.:
    #     "spack spec libdwarf ^ /path/to/libelf.json"
    spec = SpecParser(f"libdwarf ^ {str(specfile)}").next_spec()
    assert spec and spec["libelf"] == s["libelf"]

    with fs.working_dir(str(tmp_path)):
        # Make sure this also works: "spack spec ./libelf.yaml"
        spec = SpecParser(f"libdwarf^.{os.path.sep}{specfile.name}").next_spec()
        assert spec and spec["libelf"] == s["libelf"]

        # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
        spec = SpecParser(
            f"libdwarf^..{os.path.sep}{specfile.parent.name}{os.path.sep}{specfile.name}"
        ).next_spec()
        assert spec and spec["libelf"] == s["libelf"]


def test_parse_specfile_relative_paths(specfile_for, tmp_path: pathlib.Path):
    specfile = tmp_path / "libdwarf.json"
    s = specfile_for("libdwarf", specfile)

    basename = specfile.name
    parent_dir = specfile.parent

    with fs.working_dir(str(parent_dir)):
        # Make sure this also works: "spack spec ./libelf.yaml"
        spec = SpecParser(f".{os.path.sep}{basename}").next_spec()
        assert spec == s

        # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
        spec = SpecParser(f"..{os.path.sep}{parent_dir.name}{os.path.sep}{basename}").next_spec()
        assert spec == s

        # Should also handle mixed clispecs and relative paths, e.g.:
        #     "spack spec mvapich_foo ../<cur-dir>/libelf.yaml"
        specs = SpecParser(
            f"mvapich_foo ..{os.path.sep}{parent_dir.name}{os.path.sep}{basename}"
        ).all_specs()
        assert len(specs) == 2
        assert specs[1] == s


def test_parse_specfile_relative_subdir_path(specfile_for, tmp_path: pathlib.Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    specfile = subdir / "libdwarf.json"
    s = specfile_for("libdwarf", specfile)

    with fs.working_dir(str(tmp_path)):
        spec = SpecParser(f"subdir{os.path.sep}{specfile.name}").next_spec()
        assert spec == s


@pytest.mark.regression("20310")
def test_compare_abstract_specs():
    """Spec comparisons must be valid for abstract specs.

    Check that the spec cmp_key appropriately handles comparing specs for
    which some attributes are None in exactly one of two specs
    """
    # Add fields in order they appear in `Spec._cmp_node`
    constraints = [
        "foo",
        "foo.foo",
        "foo.foo@foo",
        "foo.foo@foo+foo",
        "foo.foo@foo+foo arch=foo-foo-foo",
        "foo.foo@foo+foo arch=foo-foo-foo %foo",
        "foo.foo@foo+foo arch=foo-foo-foo cflags=foo %foo",
    ]
    specs = [SpecParser(s).next_spec() for s in constraints]

    for a, b in itertools.product(specs, repeat=2):
        # Check that we can compare without raising an error
        assert a <= b or b < a


@pytest.mark.parametrize(
    "lhs_str,rhs_str,expected",
    [
        # Git shasum vs generic develop
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            "develop-branch-version@develop",
            (True, True, False),
        ),
        # Two different shasums
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            f"develop-branch-version@git.{'b' * 40}=develop",
            (False, False, False),
        ),
        # Git shasum vs. git tag
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            "develop-branch-version@git.0.2.15=develop",
            (False, False, False),
        ),
        # Git tag vs. generic develop
        (
            "develop-branch-version@git.0.2.15=develop",
            "develop-branch-version@develop",
            (True, True, False),
        ),
    ],
)
def test_git_ref_spec_equivalences(mock_packages, lhs_str, rhs_str, expected):
    lhs = SpecParser(lhs_str).next_spec()
    rhs = SpecParser(rhs_str).next_spec()
    intersect, lhs_sat_rhs, rhs_sat_lhs = expected

    assert lhs.intersects(rhs) is intersect
    assert rhs.intersects(lhs) is intersect
    assert lhs.satisfies(rhs) is lhs_sat_rhs
    assert rhs.satisfies(lhs) is rhs_sat_lhs


@pytest.mark.regression("32471")
@pytest.mark.parametrize("spec_str", ["target=x86_64", "os=redhat6", "target=x86_64:"])
def test_platform_is_none_if_not_present(spec_str):
    s = SpecParser(spec_str).next_spec()
    assert s.architecture.platform is None, s


def test_parse_one_or_raise_error_message():
    with pytest.raises(ValueError) as exc:
        parse_one_or_raise("  x y   z")

    msg = """\
expected a single spec, but got more:
  x y   z
    ^\
"""

    assert str(exc.value) == msg

    with pytest.raises(ValueError, match="expected a single spec, but got none"):
        parse_one_or_raise("    ")


@pytest.mark.parametrize(
    "input_args,expected",
    [
        # mpileaks %[virtuals=c deptypes=build] gcc
        (
            ["mpileaks", "%[virtuals=c", "deptypes=build]", "gcc"],
            ["mpileaks %[virtuals=c deptypes=build] gcc"],
        ),
        # mpileaks %[ virtuals=c deptypes=build] gcc
        (
            ["mpileaks", "%[", "virtuals=c", "deptypes=build]", "gcc"],
            ["mpileaks %[virtuals=c deptypes=build] gcc"],
        ),
        # mpileaks %[ virtuals=c deptypes=build ] gcc
        (
            ["mpileaks", "%[", "virtuals=c", "deptypes=build", "]", "gcc"],
            ["mpileaks %[virtuals=c deptypes=build] gcc"],
        ),
    ],
)
def test_parse_multiple_edge_attributes(input_args, expected):
    """Tests that we can parse correctly multiple edge attributes within square brackets,
    from the command line.

    The input are strings as they would be parsed from argparse.REMAINDER
    """
    s, *_ = spack.cmd.parse_specs(input_args)
    for c in expected:
        assert s.satisfies(c)


def test_when_edge_attribute_keeps_commas():
    """A when value is one spec string, where a comma is part of the syntax, unlike the
    comma-separated deptypes and virtuals lists."""
    edge = spack.spec.Spec("foo ^[when='@1,2'] bar").edges_to_dependencies(name="bar")[0]
    assert edge.when == spack.spec.Spec("@1,2")


@pytest.mark.parametrize(
    "spec_str,expected",
    [
        # square brackets are not valid characters in an unquoted value
        ("a=']'", "a=']'"),
        ("a='['", "a='['"),
        # an anonymous dependency is named * only where its options could be read as a name
        ("foo ^", "foo ^*"),
        ("pkg-a %*+foo ^*@1.0", "pkg-a %+foo ^@1.0"),
        ("^cflags=-O2", "^* cflags=-O2"),
        # a virtual assignment is one token, the node options follow
        ("zlib % c=gcc", "zlib %c=gcc"),
        ("^mpi=intel-parallel-studio+mkl", "^mpi=intel-parallel-studio+mkl"),
        ("%c=builtin.gcc@14", "%c=builtin.gcc@14"),
        # virtuals of an anonymous spec stay in the edge attributes, there is no name to
        # substitute them with
        ("%[virtuals=c] *", "%[virtuals=c] *"),
        ("%[deptypes=build virtuals=c] *", "%[deptypes=build virtuals=c] *"),
        ("^[virtuals=c,cxx] *", "^[virtuals=c,cxx] *"),
        ("%[virtuals=c] *@4.0 foo=bar", "%[virtuals=c] @4.0 foo=bar"),
        # a star is a package name, so name=* is a variant value, not a substitute
        ("^dev_path=*", "^* dev_path='*'"),
        # a when= value is a spec, which extends to the closing bracket and is printed unquoted
        ("%[when=a=*]", "%[when=a='*'] *"),
        ("""x %[when="a=']'"] gcc""", "x %[when=a=']'] gcc"),
        ("foo ^[when=bar virtuals=c] baz", "foo ^[when=bar virtuals=c] baz"),
        ("foo when=bar", "foo when=bar"),
        # a quoted when= is a value like any other, so it can precede other edge attributes
        ("foo ^[when='+x' virtuals=c] bar", "foo ^[when=+x] c=bar"),
        ('foo ^[when="+x" virtuals=c] bar', "foo ^[when=+x] c=bar"),
        ("foo ^[when='+x']c=bar", "foo ^[when=+x] c=bar"),
        # repeated edge attributes combine: conditions are constrained, like virtuals accumulate
        ("x ^[when='+a' when='+b'] y", "x ^[when=+a+b] y"),
        ("%[when='@1,2' virtuals=c] *", "%[virtuals=c when=@1:2] *"),
        ("%[virtuals=c when=@1,2] *", "%[virtuals=c when=@1:2] *"),
        ("%[deptypes=build virtuals=c when=@1,2] *", "%[deptypes=build virtuals=c when=@1:2] *"),
        ("x %[when=%c=gcc] y", "x %[when=%c=gcc] y"),
        # a version bound is never truncated at a "." to make room for a key=value pair
        ("@:a.a=''", "a.a=''"),
        ("@1.2:2.0=x", "@1.2: 2.0=x"),
        # there is no escaping in quoted values: a backslash is a character like any other, and a
        # value that contains one kind of quote is quoted with the other
        (r"a='x\' b='y'", r"a='x\' b=y"),
        (r"""a="it's\"""", r"""a="it's\""""),
        # nor is there json-style escaping of non-ASCII or control characters on output
        ('a="café\'s"', 'a="café\'s"'),
        ('a="x\'\ty"', 'a="x\'\ty"'),
        # a key=value pair after a sigil is a virtual assignment only if the whole value is a
        # package name, otherwise it is a variant of an anonymous dependency
        ("^foo=bar:baz", "^* foo='bar:baz'"),
        ("^foo=bar,baz", "^* foo=bar,baz"),
        ("^foo=bar=baz", "^* foo='bar=baz'"),
        ("%x=y~", "%* x='y~'"),
    ],
)
def test_spec_str_round_trips(spec_str, expected):
    """The string of a spec must be parseable, and parse back to the same spec."""
    spec = spack.spec.Spec(spec_str)
    assert str(spec) == expected
    assert spack.spec.Spec(str(spec)) == spec


@pytest.mark.regression("52375")
def test_external_spec_hash_can_be_looked_up(config, mock_packages):
    """Tests that the hash of an external can be successfully looked up."""
    packages_yaml = config.deepcopy_as_builtin("packages")
    externals_dict = extract_dicts_from_configuration(packages_yaml)
    parser = ExternalSpecsParser(externals_dict, complete_node=complete_variants_and_architecture)
    abstract_hashes = [f"{x.name}/{x.dag_hash()[:5]}" for x in parser.all_specs()]

    assert all(spack.hash_lookup.lookup_hash(spack.spec.Spec(x)) for x in abstract_hashes)

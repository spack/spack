# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

from spack.main import SpackCommand, SpackCommandError

pytestmark = [pytest.mark.usefixtures("mock_packages")]

info = SpackCommand("info")


def test_deprecated_option_warns():
    info("--variants-by-name", "vtk-m")
    assert "--variants-by-name is deprecated" in info.output


# no specs, more than one spec
@pytest.mark.parametrize("args", [[], ["vtk-m", "zmpi"]])
def test_info_failures(args):
    with pytest.raises(SpackCommandError):
        info(*args)


def test_info_noversion():
    """Check that a mock package with no versions outputs None."""
    output = info("noversion")

    assert "Preferred\n    None" not in output
    assert "Safe\n    None" not in output
    assert "Deprecated\n    None" not in output


@pytest.mark.parametrize(
    "pkg_query,expected", [("zlib", "False"), ("find-externals1", "True (version)")]
)
def test_is_externally_detectable(pkg_query, expected):
    output = info("--detectable", pkg_query)
    assert f"Externally Detectable:\n    {expected}" in output


@pytest.mark.parametrize(
    "pkg_query", ["vtk-m", "gcc"]  # This should ensure --test's c_names processing loop covered
)
@pytest.mark.parametrize("extra_args", [[], ["--by-name"]])
def test_info_fields(pkg_query, extra_args):
    expected_fields = (
        "Description:",
        "Homepage:",
        "Externally Detectable:",
        "Safe versions:",
        "Variants:",
        "Installation Phases:",
        "Virtual Packages:",
        "Tags:",
        "Licenses:",
    )

    output = info("--all", *extra_args, pkg_query)
    assert all(field in output for field in expected_fields)


@pytest.mark.parametrize(
    "args,in_output,not_in_output",
    [
        # no variants
        (["package-base-extendee"], [r"Variants:\n\s*None"], []),
        # test that long lines wrap around
        (
            ["long-boost-dependency+longdep"],
            [
                r"boost\+atomic\+chrono\+date_time\+filesystem\+graph\+iostreams\+locale\n"
                r"\s*build, link"
            ],
            [],
        ),
        (
            ["long-boost-dependency~longdep"],
            [],
            [
                r"boost\+atomic\+chrono\+date_time\+filesystem\+graph\+iostreams\+locale\n"
                r"\s*build, link"
            ],
        ),
        # conditional licenses change output
        (["licenses-1 +foo"], ["MIT"], ["Apache-2.0"]),
        (["licenses-1 ~foo"], ["Apache-2.0"], ["MIT"]),
        # filtering bowtie versions
        (["bowtie"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (["bowtie@1.2:"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (["bowtie@1.3:"], ["1.4.0", "1.3.0"], ["1.2.2", "1.2.0"]),
        (["bowtie@1.2"], ["1.2.2", "1.2.0"], ["1.3.0"]),  # 1.4.0 still shown as preferred
        # many dependencies with suggestion to filter
        (
            ["many-conditional-deps"],
            ["consider this for a simpler view:\n  spack info many-conditional-deps~cuda~rocm"],
            [],
        ),
        (
            ["many-conditional-deps ~cuda"],
            ["consider this for a simpler view:\n  spack info many-conditional-deps~cuda~rocm"],
            [],
        ),
        (
            ["many-conditional-deps ~rocm"],
            ["consider this for a simpler view:\n  spack info many-conditional-deps~cuda~rocm"],
            [],
        ),
        (["many-conditional-deps ~cuda ~rocm"], [], ["consider this for a simpler view:"]),
        # Ensure spack info knows that build_system is a single value variant
        (
            ["dual-cmake-autotools"],
            [r"when\s*build_system=cmake", r"when\s*build_system=autotools"],
            [],
        ),
        (
            ["dual-cmake-autotools build_system=cmake"],
            [r"when\s*build_system=cmake"],
            [r"when\s*build_system=autotools"],
        ),
        # Ensure that gemerator=make implies build_system=cmake and therefore no autotools
        (
            ["dual-cmake-autotools generator=make"],
            [r"when\s*build_system=cmake"],
            [r"when\s*build_system=autotools"],
        ),
        (
            ["optional-dep-test"],
            [
                r"when \^pkg-g",
                r"when \%intel",
                r"when \%intel\@64\.1",
                r"when \%clang@34\:40",
                r"when \^pkg\-f",
            ],
            [],
        ),
    ],
)
@pytest.mark.parametrize("by_name", [True, False])
def test_info_output(by_name, args, in_output, not_in_output, monkeypatch):
    monkeypatch.setenv("COLUMNS", "80")
    by_name_arg = ["--by-name"] if by_name else ["--by-when"]
    output = info(*(by_name_arg + args))

    for io in in_output:
        assert re.search(io, output)
    for nio in not_in_output:
        assert not re.search(nio, output)

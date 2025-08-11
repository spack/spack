# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

from spack.main import SpackCommand

pytestmark = [pytest.mark.usefixtures("mock_packages")]

info = SpackCommand("info")


@pytest.mark.parametrize("extra_args", [[], ["--variants-by-name"]])
def test_it_just_runs(extra_args):
    info(*extra_args, "vtk-m")


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
    "by_name,args,in_output,not_in_output",
    [
        (True, ["licenses-1 +foo"], ["MIT"], ["Apache-2.0"]),
        (True, ["licenses-1 ~foo"], ["Apache-2.0"], ["MIT"]),
        (True, ["bowtie"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (True, ["bowtie@1.2:"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (True, ["bowtie@1.3:"], ["1.4.0", "1.3.0"], ["1.2.2", "1.2.0"]),
        (True, ["bowtie@1.2"], ["1.2.2", "1.2.0"], ["1.3.0"]),  # 1.4.0 still shown as preferred
        (False, ["licenses-1 +foo"], ["MIT"], ["Apache-2.0"]),
        (False, ["licenses-1 ~foo"], ["Apache-2.0"], ["MIT"]),
        (False, ["bowtie"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (False, ["bowtie@1.2:"], ["1.4.0", "1.3.0", "1.2.2", "1.2.0"], []),
        (False, ["bowtie@1.3:"], ["1.4.0", "1.3.0"], ["1.2.2", "1.2.0"]),
        (False, ["bowtie@1.2"], ["1.2.2", "1.2.0"], ["1.3.0"]),  # 1.4.0 still shown as preferred
    ],
)
def test_filtered_info(by_name, args, in_output, not_in_output):
    by_name_arg = ["--by-name"] if by_name else []
    output = info(*(by_name_arg + args))
    assert all(io in output for io in in_output)
    assert all(nio not in output for nio in not_in_output)

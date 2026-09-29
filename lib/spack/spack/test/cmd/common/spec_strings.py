# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import spack.cmd.common.spec_strings


def test_spec_strings(tmp_path: pathlib.Path):
    (tmp_path / "example.py").write_text(
        """\
def func(x):
    print("dont fix %s me" % x, 3)
    return x.satisfies("+foo %gcc +bar") and x.satisfies("%gcc +baz")
"""
    )
    (tmp_path / "example.json").write_text(
        """\
{
    "spec": [
        "+foo %gcc +bar~nope   ^dep %clang +yup @3.2 target=x86_64 /abcdef ^another   %gcc   ",
        "%gcc +baz"
    ],
    "%gcc x=y": 2
}
"""
    )
    (tmp_path / "example.yaml").write_text(
        """\
spec:
  - "+foo   %gcc +bar"
  - "%gcc +baz"
  - "this is fine %clang"
"%gcc x=y": 2
"""
    )

    issues = set()

    def collect_issues(path: str, line: int, col: int, old: str, new: str):
        issues.add((path, line, col, old, new))

    # check for issues with custom handler
    spack.cmd.common.spec_strings._check_spec_strings(
        [
            str(tmp_path / "nonexistent.py"),
            str(tmp_path / "example.py"),
            str(tmp_path / "example.json"),
            str(tmp_path / "example.yaml"),
        ],
        handler=collect_issues,
    )

    assert issues == {
        (
            str(tmp_path / "example.json"),
            3,
            9,
            "+foo %gcc +bar~nope   ^dep %clang +yup @3.2 target=x86_64 /abcdef ^another   %gcc   ",
            "+foo +bar~nope %gcc   ^dep +yup @3.2 target=x86_64 /abcdef %clang ^another   %gcc   ",
        ),
        (str(tmp_path / "example.json"), 4, 9, "%gcc +baz", "+baz %gcc"),
        (str(tmp_path / "example.json"), 6, 5, "%gcc x=y", "x=y %gcc"),
        (str(tmp_path / "example.py"), 3, 23, "+foo %gcc +bar", "+foo +bar %gcc"),
        (str(tmp_path / "example.py"), 3, 57, "%gcc +baz", "+baz %gcc"),
        (str(tmp_path / "example.yaml"), 2, 5, "+foo   %gcc +bar", "+foo +bar   %gcc"),
        (str(tmp_path / "example.yaml"), 3, 5, "%gcc +baz", "+baz %gcc"),
        (str(tmp_path / "example.yaml"), 5, 1, "%gcc x=y", "x=y %gcc"),
    }

    # fix the issues in the files
    spack.cmd.common.spec_strings._check_spec_strings(
        [
            str(tmp_path / "nonexistent.py"),
            str(tmp_path / "example.py"),
            str(tmp_path / "example.json"),
            str(tmp_path / "example.yaml"),
        ],
        handler=spack.cmd.common.spec_strings._spec_str_fix_handler,
    )

    assert (
        (tmp_path / "example.json").read_text()
        == """\
{
    "spec": [
        "+foo +bar~nope %gcc   ^dep +yup @3.2 target=x86_64 /abcdef %clang ^another   %gcc   ",
        "+baz %gcc"
    ],
    "x=y %gcc": 2
}
"""
    )
    assert (
        (tmp_path / "example.py").read_text()
        == """\
def func(x):
    print("dont fix %s me" % x, 3)
    return x.satisfies("+foo +bar %gcc") and x.satisfies("+baz %gcc")
"""
    )
    assert (
        (tmp_path / "example.yaml").read_text()
        == """\
spec:
  - "+foo +bar   %gcc"
  - "+baz %gcc"
  - "this is fine %clang"
"x=y %gcc": 2
"""
    )

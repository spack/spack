# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
from contextlib import contextmanager

import pytest

import spack.config
import spack.error
import spack.repo
import spack.util.file_cache
import spack.util.spack_yaml as syaml
from spack.concretize import concretize_one
from spack.main import SpackCommand

solve = SpackCommand("solve")


def update_packages_config(conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set("packages", conf["packages"], scope="concretize")


_pkgx1 = (
    "x1",
    """\
class X1(Package):
    version("1.2")
    version("1.1")

    depends_on("x2")
    depends_on("x3")
""",
)


_pkgx2 = (
    "x2",
    """\
class X2(Package):
    version("2.1")
    version("2.0")

    depends_on("x4@4.1")
""",
)


_pkgx3 = (
    "x3",
    """\
class X3(Package):
    version("3.5")
    version("3.4")

    depends_on("x4@4.0")
""",
)


_pkgx4 = (
    "x4",
    """\
class X4(Package):
    version("4.1")
    version("4.0")
""",
)


_pkgy1 = (
    "y1",
    """\
class Y1(Package):
    version("1.2")
    version("1.1")

    depends_on("y2+v1")
    depends_on("y3")
""",
)


_pkgy2 = (
    "y2",
    """\
class Y2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    depends_on("y4@4.1", when="+v1")
    depends_on("y4")
""",
)


_pkgy3 = (
    "y3",
    """\
class Y3(Package):
    version("3.5")
    version("3.4")

    depends_on("y4@4.0")
""",
)


_pkgy4 = (
    "y4",
    """\
class Y4(Package):
    version("4.1")
    version("4.0")
""",
)


_pkgz1 = (
    "z1",
    """\
class Z1(Package):
    version("1.2")
    version("1.1")

    variant("v1", default=True)

    depends_on("z2")

    depends_on("z3")
    depends_on("z3+v2", when="~v1")

    conflicts("+v1", when="@:1.1")
""",
)


_pkgz2 = (
    "z2",
    """\
class Z2(Package):
    version("3.1")
    version("3.0")

    depends_on("z3@:2.0")
""",
)


_pkgz3 = (
    "z3",
    """\
class Z3(Package):
    version("2.1")
    version("2.0")

    variant("v2", default=True, when="@2.1:")
""",
)


# Cluster of packages that includes requirements - goal is to "chain"
# the requirements like other constraints.
_pkgw4 = (
    "w4",
    """\
class W4(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    depends_on("w2")
    depends_on("w2@:2.0", when="@:2.0")

    # test_errmsg_requirements_1 stresses these constraints by asking
    # for "w4@:2.0 ^w3@2.1". On develop, the error message was never
    # good; in this PR, the error message "used to be" good and is now
    # not so good (see W3 definition for more details: this does not
    # seem to be an issue with requirements)
    depends_on("w3")
    depends_on("w3+v1", when="@2.0") # EX1
    # depends_on("w3~v1", when="@2.0") # EX2
""",
)


_pkgw3 = (
    "w3",
    """\
class W3(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    # conflicts("+v1", when="@2.1")
    # This requirement is equivalent to prior conflict. If you swap
    # it in, the error message is still not good (so that points to
    # an issue with error messages that is not related to requirements)
    requires("~v1", when="@2.1") # EX1
    # requires("+v1", when="@2.1") # EX2

    depends_on("w1")
""",
)


_pkgw2 = (
    "w2",
    """\
class W2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    depends_on("w1")
""",
)


_pkgw1 = (
    "w1",
    """\
class W1(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)
""",
)


# Like the W* packages, but encodes the config requirements constraints
# into the packages to see if that improves the error from
# test_errmsg_requirements_2
_pkgt4 = (
    "t4",
    """\
class T4(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    # test_errmsg_requirements_3 stresses these constraints and
    # generates a bad error message: "t4@:2.0 ^t2+v1"
    depends_on("t2")
    depends_on("t2@:2.0", when="@:2.0")

    depends_on("t3")
    depends_on("t3~v1", when="@2.0")
""",
)


_pkgt3 = (
    "t3",
    """\
class T3(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    requires("+v1", when="@2.1")

    depends_on("t1")
""",
)


_pkgt2 = (
    "t2",
    """\
class T2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    # It used to be that swapping `require` for `conflicts` would
    # improve the error message.
    requires("~v1", when="@:2.0")
    # conflicts("+v1", when="@:2.0")

    depends_on("t1")
""",
)


_pkgt1 = (
    "t1",
    """\
class T1(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)
""",
)


all_pkgs = [
    _pkgx1,
    _pkgx2,
    _pkgx3,
    _pkgx4,
    _pkgy1,
    _pkgy2,
    _pkgy3,
    _pkgy4,
    _pkgz1,
    _pkgz2,
    _pkgz3,
    _pkgw1,
    _pkgw2,
    _pkgw3,
    _pkgw4,
    _pkgt1,
    _pkgt2,
    _pkgt3,
    _pkgt4,
]


def _add_import(pkg_def):
    return (
        """\
from spack.package import *
from spack.package import Package
"""
        + pkg_def
    )


all_pkgs = list((x, _add_import(y)) for (x, y) in all_pkgs)


_repo_name_id = 0


def create_test_repo(tmp_path, pkg_name_content_tuples):
    global _repo_name_id

    repo_name = f"testrepo{str(_repo_name_id)}"
    repo_path = tmp_path / "spack_repo" / repo_name
    os.makedirs(repo_path)
    with open(repo_path / "__init__.py", "w", encoding="utf-8"):
        pass
    repo_yaml = os.path.join(repo_path, "repo.yaml")
    with open(str(repo_yaml), "w", encoding="utf-8") as f:
        f.write(
            f"""\
repo:
  namespace: {repo_name}
  api: v2.1
"""
        )

    _repo_name_id += 1

    packages_dir = repo_path / "packages"
    os.mkdir(packages_dir)
    with open(packages_dir / "__init__.py", "w", encoding="utf-8"):
        pass
    for pkg_name, pkg_str in pkg_name_content_tuples:
        pkg_dir = packages_dir / pkg_name
        os.mkdir(pkg_dir)
        pkg_file = pkg_dir / "package.py"
        with open(str(pkg_file), "w", encoding="utf-8") as f:
            f.write(pkg_str)

    repo_cache = spack.util.file_cache.FileCache(str(tmp_path / "cache"))
    return spack.repo.Repo(str(repo_path), cache=repo_cache)


@pytest.fixture
def _create_test_repo(tmp_path, mutable_config):
    yield create_test_repo(tmp_path, all_pkgs)


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


@contextmanager
def expect_failure_and_print():
    got_an_error_as_expected = False
    try:
        yield
    except spack.error.UnsatisfiableSpecError as e:
        print(str(e))
        got_an_error_as_expected = True
    if not got_an_error_as_expected:
        raise ValueError("A failure was supposed to occur in this context manager")


# Error message is good
def test_diamond_with_pkg_conflict1(concretize_scope, test_repo):
    concretize_one("x2")
    concretize_one("x3")
    concretize_one("x4")

    with expect_failure_and_print():
        concretize_one("x1")


# Error message is good (has some redundancy though)
def test_diamond_with_pkg_conflict2(concretize_scope, test_repo):
    with expect_failure_and_print():
        concretize_one("y1")


# This error message is not so great
def test_version_range_null(concretize_scope, test_repo):
    with expect_failure_and_print():
        concretize_one("x2@3:4")


# This error message is hard to follow: neither z2 or z3
# are mentioned, so if this hierarchy had 10 other "OK"
# packages, a user would be conducting a tedious manual
# search
def test_null_variant_for_requested_version(concretize_scope, test_repo):
    concretize_one("z1")
    # output = solve("--show=asp", "z1@1.1")
    # with open(, "w") as f:
    #    f.write(output)
    with expect_failure_and_print():
        concretize_one("z1@1.1")


# Error message for requirement introduced in the package
# definition seems OK: requirements generate `condition`s, which
# should be traceable as condition causes in error_messages.lp
def test_errmsg_requirements_1(concretize_scope, test_repo):
    # output = solve("--show=asp", "w4@:2.0 ^w3@2.1")
    # with open("/Users/scheibel1/Desktop/spack/spack/err-msg-asp/good-w.txt", "w") as f:
    #    f.write(output)
    with expect_failure_and_print():
        concretize_one("w4@:2.0 ^w3@2.1")


# This error message is short. Would it be good if I encoded
# it in the package.py?
def test_errmsg_requirements_2(concretize_scope, test_repo):
    conf_str = """\
packages:
  w2:
    require:
    - spec: "~v1"
      when: "@2.0"
"""
    update_packages_config(conf_str)

    # output = solve("--show=asp", "w4@2.0 ^w2+v1")
    # with open("/Users/scheibel1/Desktop/spack/spack/err-msg-asp/bad-w.txt", "w") as f:
    #    f.write(output)
    with expect_failure_and_print():
        concretize_one("w4@2.0 ^w2+v1")


# Short error message: this reencodes test_errmsg_requirements_2
# in terms of package `requires`, the error message is improved
def test_errmsg_requirements_3(concretize_scope, test_repo):
    with expect_failure_and_print():
        concretize_one("t4@:2.0 ^t2+v1")


# Simulates a user error: package is specified as external with a version,
# but a different version was required. Currently the error message is
# improved WRT develop
def test_errmsg_requirements_4(concretize_scope, test_repo):
    conf_str = """\
packages:
  t1:
    buildable: false
    externals:
    - spec: "t1@2.1"
      prefix: /a/path/that/doesnt/need/to/exist/
    require:
    - spec: "t1@2.0"
"""
    update_packages_config(conf_str)

    with expect_failure_and_print():
        concretize_one("t1")

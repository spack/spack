# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pathlib

import pytest

import spack.build_systems.generic
import spack.config
import spack.error
import spack.package_base
import spack.repo
import spack.util.spack_yaml as syaml
import spack.version
from spack.solver.asp import InternalConcretizerError, UnsatisfiableSpecError
from spack.spec import Spec
from spack.test.conftest import create_test_repo
from spack.util.url import path_to_file_url

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


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(
        tmpdir,
        [_pkgx1, _pkgx2, _pkgx3, _pkgx4,
         _pkgy1, _pkgy2, _pkgy3, _pkgy4,
         _pkgz1, _pkgz2, _pkgz3,
        ]
    )


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


# Error message is good
def test_diamond_with_pkg_conflict1(concretize_scope, test_repo):
    x2 = Spec("x2").concretized()
    x3 = Spec("x3").concretized()
    x4 = Spec("x4").concretized()

    Spec("x1").concretized()


# Error message is good (has some redundancy though)
def test_diamond_with_pkg_conflict2(concretize_scope, test_repo):
    Spec("y1").concretized()


# This error message is not so great
def test_version_range_null(concretize_scope, test_repo):
    Spec("x2@3:4").concretized()


# This error message is hard to follow: neither z2 or z3
# are mentioned, so if this hierarchy had 10 other "OK"
# packages, a user would be conducting a tedious manual
# search
def test_null_variant_for_requested_version(concretize_scope, test_repo):
    Spec("z1").concretized()
    Spec("z1@1.1").concretized()
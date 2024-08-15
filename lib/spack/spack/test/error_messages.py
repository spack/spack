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


_pkgw = (
    "w",
    """\
class W(Package):
    version("1.2")
    version("1.1")

    depends_on("x")
    depends_on("y")
""",
)


_pkgx = (
    "x",
    """\
class X(Package):
    version("2.1")
    version("2.0")

    depends_on("z@4.1")
""",
)


_pkgy = (
    "y",
    """\
class Y(Package):
    version("3.5")
    version("3.4")

    depends_on("z@4.0")
""",
)


_pkgz = (
    "z",
    """\
class Z(Package):
    version("4.1")
    version("4.0")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(tmpdir, [_pkgw, _pkgx, _pkgy, _pkgz])


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


def test_diamond_with_pkg_conflict(concretize_scope, test_repo):
    x = Spec("x").concretized()
    y = Spec("y").concretized()
    z = Spec("z").concretized()

    w = Spec("w").concretized()
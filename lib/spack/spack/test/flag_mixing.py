# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.build_systems.generic
import spack.config
import spack.error
import spack.package_base
import spack.repo
import spack.util.spack_yaml as syaml
import spack.version
from spack.main import SpackCommand
from spack.spec import Spec
from spack.test.conftest import create_test_repo

pytestmark = [
    pytest.mark.only_clingo("Original concretizer does not support configuration requirements")
]


solve = SpackCommand("solve")


_pkgx = (
    "x",
    """\
class X(Package):
    version("1.1")
    version("1.0")

    variant("activatemultiflag", default=False)
    depends_on('y cflags="-d1"', when="~activatemultiflag")
    depends_on('y cflags="-d1 -d2"', when="+activatemultiflag")
""",
)


_pkgy = (
    "y",
    """\
class Y(Package):
    version("2.1")
    version("2.0")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(tmpdir, [_pkgx, _pkgy])


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


def update_concretize_scope(conf_str, section):
    conf = syaml.load_config(conf_str)
    spack.config.set(section, conf[section], scope="concretize")


def test_order1(concretize_scope, test_repo):
    conf_str = """\
compilers::
- compiler:
    spec: gcc@12-fake
    paths:
      cc: /usr/bin/fake-gcc
      cxx: /usr/bin/fake-g++
      f77: null
      fc: null
    flags:
      cflags: "-Walllllllllllllllllllllllllll"
    operating_system: debian6
    modules: []
"""
    update_concretize_scope(conf_str, "compilers")

    Spec("y %gcc@12-fake").concretized()


def test_mix_spec_and_requirements(concretize_scope, test_repo):
    conf_str = """\
packages:
  y:
    require: cflags="-c"
"""
    update_concretize_scope(conf_str, "packages")

    s1 = Spec('y cflags="-a"').concretized()
    assert s1.satisfies('cflags="-a -c"')


def test_mix_spec_and_dependent(concretize_scope, test_repo):
    s1 = Spec('x ^y cflags="-a"').concretized()
    assert s1["y"].satisfies('cflags="-a -d1"')


def test_mix_spec_and_compiler_cfg(concretize_scope, test_repo):
    conf_str = """\
compilers::
- compiler:
    spec: gcc@12-fake
    paths:
      cc: /usr/bin/fake-gcc
      cxx: /usr/bin/fake-g++
      f77: null
      fc: null
    flags:
      cflags: "-Wall"
    operating_system: debian6
    modules: []
"""
    update_concretize_scope(conf_str, "compilers")

    s1 = Spec('y %gcc@12-fake cflags="-O2"').concretized()
    assert s1.satisfies('cflags="-Wall -O2"')


def test_flag_order_and_grouping(concretize_scope, test_repo):
    """Flags should be grouped on a per-source basis, the order
    should match the original order they were listed in for the
    source.
    """
    conf_str = """\
packages:
  y:
    require: cflags="-c"
"""
    update_concretize_scope(conf_str, "packages")

    s2 = Spec('y cflags="-a -b"').concretized()
    assert s2.satisfies('cflags="-a -b -c"')
    assert s2.compiler_flags["cflags"] == ["-c", "-a", "-b"]

    conf_str = """\
packages:
  y:
    require: cflags="-x5 -x6"
"""
    update_concretize_scope(conf_str, "packages")

    s3 = Spec('y cflags="-x7 -x4"').concretized()
    assert s3.satisfies('cflags="-x4 -x5 -x6 -x7"')
    assert s3.compiler_flags["cflags"] == ["-x5", "-x6", "-x7", "-x4"]

    conf_str = """\
compilers::
- compiler:
    spec: gcc@12-fake
    paths:
      cc: /usr/bin/fake-gcc
      cxx: /usr/bin/fake-g++
      f77: null
      fc: null
    flags:
      cflags: "-x3 -x8"
    operating_system: debian6
    modules: []
"""
    update_concretize_scope(conf_str, "compilers")

    s4 = Spec('y cflags="-x7 -x4"').concretized()
    assert s4.satisfies('cflags="-x3 -x4 -x5 -x6 -x7 -x8"')
    assert s4.compiler_flags["cflags"] == ["-x3", "-x8", "-x5", "-x6", "-x7", "-x4"]

    s5 = Spec('x+activatemultiflag ^y cflags="-x7 -x4"').concretized()
    assert s5["y"].satisfies('cflags="-x3 -x4 -x5 -x6 -x7 -x8 -d1 -d2"')
    assert s5["y"].compiler_flags["cflags"] == [
        "-x3",
        "-x8",
        "-d1",
        "-d2",
        "-x5",
        "-x6",
        "-x7",
        "-x4",
    ]

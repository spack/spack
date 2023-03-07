# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

import spack.build_systems.generic
import spack.config
import spack.repo
import spack.util.spack_yaml as syaml
from spack.solver.asp import UnsatisfiableSpecError
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="Windows uses old concretizer")


def update_packages_config(conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set("packages", conf["packages"], scope="concretize")


_pkgx = (
    "x",
    """\
class X(Package):
    version('1.1')
    version('1.0')
    version('0.9')

    variant('shared', default=True,
            description='Build shared libraries')

    depends_on('y')
""",
)


_pkgy = (
    "y",
    """\
class Y(Package):
    version('2.5')
    version('2.4')
    version('2.3', deprecated=True)

    variant('shared', default=True,
            description='Build shared libraries')
""",
)


_pkgv = (
    "v",
    """\
class V(Package):
    version('2.1')
    version('2.0')
""",
)


@pytest.fixture
def create_test_repo(tmpdir, mutable_config):
    repo_path = str(tmpdir)
    repo_yaml = tmpdir.join("repo.yaml")
    with open(str(repo_yaml), "w") as f:
        f.write(
            """\
repo:
  namespace: testcfgrequirements
"""
        )

    packages_dir = tmpdir.join("packages")
    for pkg_name, pkg_str in [_pkgx, _pkgy, _pkgv]:
        pkg_dir = packages_dir.ensure(pkg_name, dir=True)
        pkg_file = pkg_dir.join("package.py")
        with open(str(pkg_file), "w") as f:
            f.write(pkg_str)

    yield spack.repo.Repo(repo_path)


@pytest.fixture
def test_repo(create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(create_test_repo) as mock_repo_path:
        yield mock_repo_path


class MakeStage(object):
    def __init__(self, stage):
        self.stage = stage

    def __call__(self, *args, **kwargs):
        return self.stage


@pytest.fixture
def fake_installs(monkeypatch, tmpdir):
    stage_path = str(tmpdir.ensure("fake-stage", dir=True))
    universal_unused_stage = spack.stage.DIYStage(stage_path)
    monkeypatch.setattr(
        spack.build_systems.generic.Package, "_make_stage", MakeStage(universal_unused_stage)
    )


def test_requirement_isnt_optional(concretize_scope, test_repo):
    """If a user spec requests something that directly conflicts
    with a requirement, make sure we get an error.
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    with pytest.raises(UnsatisfiableSpecError):
        Spec("x@1.1").concretize()


def test_requirement_is_successfully_applied(concretize_scope, test_repo):
    """If a simple requirement can be satisfied, make sure the
    concretization succeeds and the requirement spec is applied.
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    s1 = Spec("x").concretized()
    # Without any requirements/preferences, the later version is preferred
    assert s1.satisfies("@1.1")

    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    s2 = Spec("x").concretized()
    # The requirement forces choosing the eariler version
    assert s2.satisfies("@1.0")


def test_multiple_packages_requirements_are_respected(concretize_scope, test_repo):
    """Apply requirements to two packages; make sure the concretization
    succeeds and both requirements are respected.
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  x:
    require: "@1.0"
  y:
    require: "@2.4"
"""
    update_packages_config(conf_str)
    spec = Spec("x").concretized()
    assert spec["x"].satisfies("@1.0")
    assert spec["y"].satisfies("@2.4")


def test_oneof(concretize_scope, test_repo):
    """'one_of' allows forcing the concretizer to satisfy one of
    the specs in the group (but not all have to be satisfied).
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4", "~shared"]
"""
    update_packages_config(conf_str)
    spec = Spec("x").concretized()
    # The concretizer only has to satisfy one of @2.4/~shared, and @2.4
    # comes first so it is prioritized
    assert spec["y"].satisfies("@2.4+shared")


def test_one_package_multiple_oneof_groups(concretize_scope, test_repo):
    """One package has two 'one_of' groups; check that both are
    applied.
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4%gcc", "@2.5%clang"]
    - one_of: ["@2.5~shared", "@2.4+shared"]
"""
    update_packages_config(conf_str)

    s1 = Spec("y@2.5").concretized()
    assert s1.satisfies("%clang~shared")

    s2 = Spec("y@2.4").concretized()
    assert s2.satisfies("%gcc+shared")


def test_requirements_for_package_that_is_not_needed(concretize_scope, test_repo):
    """Specify requirements for specs that are not concretized or
    a dependency of a concretized spec (in other words, none of
    the requirements are used for the requested spec).
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    # Note that the exact contents aren't important since this isn't
    # intended to be used, but the important thing is that a number of
    # packages have requirements applied
    conf_str = """\
packages:
  x:
    require: "@1.0"
  y:
    require:
    - one_of: ["@2.4%gcc", "@2.5%clang"]
    - one_of: ["@2.5~shared", "@2.4+shared"]
"""
    update_packages_config(conf_str)

    s1 = Spec("v").concretized()
    assert s1.satisfies("@2.1")


def test_oneof_ordering(concretize_scope, test_repo):
    """Ensure that earlier elements of 'one_of' have higher priority.
    This priority should override default priority (e.g. choosing
    later versions).
    """
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4", "@2.5"]
"""
    update_packages_config(conf_str)

    s1 = Spec("y").concretized()
    assert s1.satisfies("@2.4")

    s2 = Spec("y@2.5").concretized()
    assert s2.satisfies("@2.5")


def test_reuse_oneof(concretize_scope, create_test_repo, mutable_database, fake_installs):
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.5", "%gcc"]
"""

    with spack.repo.use_repositories(create_test_repo):
        s1 = Spec("y@2.5%gcc").concretized()
        s1.package.do_install(fake=True, explicit=True)

        update_packages_config(conf_str)

        with spack.config.override("concretizer:reuse", True):
            s2 = Spec("y").concretized()
            assert not s2.satisfies("@2.5 %gcc")


def test_requirements_are_higher_priority_than_deprecation(concretize_scope, test_repo):
    """Test that users can override a deprecated version with a requirement."""
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    # @2.3 is a deprecated versions. Ensure that any_of picks both constraints,
    # since they are possible
    conf_str = """\
packages:
  y:
    require:
    - any_of: ["@2.3", "%gcc"]
"""
    update_packages_config(conf_str)

    s1 = Spec("y").concretized()
    assert s1.satisfies("@2.3")
    assert s1.satisfies("%gcc")


@pytest.mark.parametrize("spec_str,requirement_str", [("x", "%gcc"), ("x", "%clang")])
def test_default_requirements_with_all(spec_str, requirement_str, concretize_scope, test_repo):
    """Test that default requirements are applied to all packages."""
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")

    conf_str = """\
packages:
  all:
    require: "{}"
""".format(
        requirement_str
    )
    update_packages_config(conf_str)

    spec = Spec(spec_str).concretized()
    for s in spec.traverse():
        assert s.satisfies(requirement_str)


@pytest.mark.parametrize(
    "requirements,expectations",
    [
        (("%gcc", "%clang"), ("%gcc", "%clang")),
        (("%gcc ~shared", "@1.0"), ("%gcc ~shared", "@1.0 +shared")),
    ],
)
def test_default_and_package_specific_requirements(
    concretize_scope, requirements, expectations, test_repo
):
    """Test that specific package requirements override default package requirements."""
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")
    generic_req, specific_req = requirements
    generic_exp, specific_exp = expectations
    conf_str = """\
packages:
  all:
    require: "{}"
  x:
    require: "{}"
""".format(
        generic_req, specific_req
    )
    update_packages_config(conf_str)

    spec = Spec("x").concretized()
    assert spec.satisfies(specific_exp)
    for s in spec.traverse(root=False):
        assert s.satisfies(generic_exp)


@pytest.mark.parametrize("mpi_requirement", ["mpich", "mpich2", "zmpi"])
def test_requirements_on_virtual(mpi_requirement, concretize_scope, mock_packages):
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")
    conf_str = """\
packages:
  mpi:
    require: "{}"
""".format(
        mpi_requirement
    )
    update_packages_config(conf_str)

    spec = Spec("callpath").concretized()
    assert "mpi" in spec
    assert mpi_requirement in spec


@pytest.mark.parametrize(
    "mpi_requirement,specific_requirement",
    [("mpich", "@3.0.3"), ("mpich2", "%clang"), ("zmpi", "%gcc")],
)
def test_requirements_on_virtual_and_on_package(
    mpi_requirement, specific_requirement, concretize_scope, mock_packages
):
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")
    conf_str = """\
packages:
  mpi:
    require: "{0}"
  {0}:
    require: "{1}"
""".format(
        mpi_requirement, specific_requirement
    )
    update_packages_config(conf_str)

    spec = Spec("callpath").concretized()
    assert "mpi" in spec
    assert mpi_requirement in spec
    assert spec["mpi"].satisfies(specific_requirement)


def test_incompatible_virtual_requirements_raise(concretize_scope, mock_packages):
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")
    conf_str = """\
    packages:
      mpi:
        require: "mpich"
    """
    update_packages_config(conf_str)

    spec = Spec("callpath ^zmpi")
    with pytest.raises(UnsatisfiableSpecError):
        spec.concretize()


def test_non_existing_variants_under_all(concretize_scope, mock_packages):
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Original concretizer does not support configuration" " requirements")
    conf_str = """\
    packages:
      all:
        require:
        - any_of: ["~foo", "@:"]
    """
    update_packages_config(conf_str)

    spec = Spec("callpath ^zmpi").concretized()
    assert "~foo" not in spec

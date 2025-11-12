# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from abc import ABC, abstractmethod
from collections import namedtuple

import pytest

import spack.concretize
import spack.dependency
import spack.directives
import spack.repo
import spack.spec
import spack.version


def test_false_directives_do_not_exist(mock_packages):
    """Ensure directives that evaluate to False at import time are added to
    dicts on packages.
    """
    cls = spack.repo.PATH.get_pkg_class("when-directives-false")
    assert not cls.dependencies
    assert not cls.resources
    assert not cls.patches


def test_true_directives_exist(mock_packages):
    """Ensure directives that evaluate to True at import time are added to
    dicts on packages.
    """
    cls = spack.repo.PATH.get_pkg_class("when-directives-true")

    assert cls.dependencies
    assert "extendee" in cls.dependencies[spack.spec.Spec()]
    assert "pkg-b" in cls.dependencies[spack.spec.Spec()]

    assert cls.resources
    assert spack.spec.Spec() in cls.resources

    assert cls.patches
    assert spack.spec.Spec() in cls.patches


def test_constraints_from_context(mock_packages):
    pkg_cls = spack.repo.PATH.get_pkg_class("with-constraint-met")

    assert pkg_cls.dependencies
    assert "pkg-b" in pkg_cls.dependencies[spack.spec.Spec("@1.0")]

    assert pkg_cls.conflicts
    assert (spack.spec.Spec("%gcc"), None) in pkg_cls.conflicts[spack.spec.Spec("+foo@1.0")]


@pytest.mark.regression("26656")
def test_constraints_from_context_are_merged(mock_packages):
    pkg_cls = spack.repo.PATH.get_pkg_class("with-constraint-met")

    assert pkg_cls.dependencies
    assert "pkg-c" in pkg_cls.dependencies[spack.spec.Spec("@0.14:15 ^pkg-b@3.8:4.0")]


@pytest.mark.regression("27754")
def test_extends_spec(config, mock_packages):
    extender = spack.concretize.concretize_one("extends-spec")
    extendee = spack.concretize.concretize_one("extendee")

    assert extender.dependencies
    assert extender.package.extends(extendee)


@pytest.mark.regression("48024")
def test_conditionally_extends_transitive_dep(config, mock_packages):
    spec = spack.concretize.concretize_one("conditionally-extends-transitive-dep")

    assert not spec.package.extendee_spec


@pytest.mark.regression("48025")
def test_conditionally_extends_direct_dep(config, mock_packages):
    spec = spack.concretize.concretize_one("conditionally-extends-direct-dep")

    assert not spec.package.extendee_spec


@pytest.mark.regression("34368")
def test_error_on_anonymous_dependency(config, mock_packages):
    pkg = spack.repo.PATH.get_pkg_class("pkg-a")
    with pytest.raises(spack.directives.DependencyError):
        spack.directives._depends_on(pkg, spack.spec.Spec("@4.5"))


@pytest.mark.regression("34879")
@pytest.mark.parametrize(
    "package_name,expected_maintainers",
    [
        ("maintainers-1", ["user1", "user2"]),
        # Extends PythonPackage
        ("py-extension1", ["user1", "user2"]),
        # Extends maintainers-1
        ("maintainers-3", ["user0", "user1", "user2", "user3"]),
    ],
)
def test_maintainer_directive(config, mock_packages, package_name, expected_maintainers):
    pkg_cls = spack.repo.PATH.get_pkg_class(package_name)
    assert pkg_cls.maintainers == expected_maintainers


@pytest.mark.parametrize(
    "package_name,expected_licenses", [("licenses-1", [("MIT", "+foo"), ("Apache-2.0", "~foo")])]
)
def test_license_directive(config, mock_packages, package_name, expected_licenses):
    pkg_cls = spack.repo.PATH.get_pkg_class(package_name)
    for license in expected_licenses:
        assert spack.spec.Spec(license[1]) in pkg_cls.licenses
        assert license[0] == pkg_cls.licenses[spack.spec.Spec(license[1])]


def test_duplicate_exact_range_license():
    package = namedtuple("package", ["licenses", "name"])
    package.licenses = {spack.spec.Spec("+foo"): "Apache-2.0"}
    package.name = "test_package"

    msg = (
        r"test_package is specified as being licensed as MIT when \+foo, but it is also "
        r"specified as being licensed under Apache-2.0 when \+foo, which conflict."
    )

    with pytest.raises(spack.directives.OverlappingLicenseError, match=msg):
        spack.directives._execute_license(package, "MIT", "+foo")


def test_overlapping_duplicate_licenses():
    package = namedtuple("package", ["licenses", "name"])
    package.licenses = {spack.spec.Spec("+foo"): "Apache-2.0"}
    package.name = "test_package"

    msg = (
        r"test_package is specified as being licensed as MIT when \+bar, but it is also "
        r"specified as being licensed under Apache-2.0 when \+foo, which conflict."
    )

    with pytest.raises(spack.directives.OverlappingLicenseError, match=msg):
        spack.directives._execute_license(package, "MIT", "+bar")


def test_version_type_validation():
    # A version should be a string or an int, not a float, because it leads to subtle issues
    # such as 3.10 being interpreted as 3.1.

    package = namedtuple("package", ["name"])

    msg = r"python: declared version '.+' in package should be a string or int\."

    # Pass a float
    with pytest.raises(spack.version.VersionError, match=msg):
        spack.directives._execute_version(package(name="python"), 3.10)

    # Try passing a bogus type; it's just that we want a nice error message
    with pytest.raises(spack.version.VersionError, match=msg):
        spack.directives._execute_version(package(name="python"), {})


@pytest.mark.parametrize(
    "spec_str,distribute_src,distribute_bin",
    [
        ("redistribute-x@1.1~foo", False, False),
        ("redistribute-x@1.2+foo", False, False),
        ("redistribute-x@1.2~foo", False, True),
        ("redistribute-x@1.0~foo", False, True),
        ("redistribute-x@1.3+foo", True, True),
        ("redistribute-y@2.0", False, False),
        ("redistribute-y@2.1+bar", False, False),
    ],
)
def test_redistribute_directive(mock_packages, spec_str, distribute_src, distribute_bin):
    spec = spack.spec.Spec(spec_str)
    assert spack.repo.PATH.get_pkg_class(spec.fullname).redistribute_source(spec) == distribute_src
    concretized_spec = spack.concretize.concretize_one(spec)
    assert concretized_spec.package.redistribute_binary == distribute_bin


def test_redistribute_override_when():
    """Allow a user to call `redistribute` twice to separately disable
    source and binary distribution for the same when spec.

    The second call should not undo the effect of the first.
    """

    class MockPackage:
        name = "mock"
        disable_redistribute = {}

    cls = MockPackage
    spack.directives._execute_redistribute(cls, source=False, binary=None, when="@1.0")
    spec_key = spack.directives._make_when_spec("@1.0")
    assert not cls.disable_redistribute[spec_key].binary
    assert cls.disable_redistribute[spec_key].source
    spack.directives._execute_redistribute(cls, source=None, binary=False, when="@1.0")
    assert cls.disable_redistribute[spec_key].binary
    assert cls.disable_redistribute[spec_key].source


@pytest.mark.regression("51248")
def test_direct_dependencies_from_when_context_are_retained(mock_packages):
    """Tests that direct dependencies from the "when" context manager don't lose the "direct"
    attribute when turned into directives on the package class.
    """
    pkg_cls = spack.repo.PATH.get_pkg_class("with-constraint-met")
    # Direct dependency in a "when" single context manager
    assert spack.spec.Spec("%pkg-b") in pkg_cls.dependencies
    # Direct dependency in a "when" nested context manager
    assert spack.spec.Spec("@2 %c=gcc %pkg-c %pkg-b@:4.0") in pkg_cls.dependencies
    # Nested ^foo followed by %foo
    assert spack.spec.Spec("%pkg-c") in pkg_cls.dependencies
    # Nested ^foo followed by ^foo %gcc
    assert spack.spec.Spec("^pkg-c %gcc") in pkg_cls.dependencies


class FakePkg:
    def __init__(self, name, directive_dict):
        self.name = name
        setattr(self, name, directive_dict)


class FakeDependency(spack.dependency.Dependency):
    def __init__(self, pkg, spec):
        self.pkg = pkg
        self.spec = spec.copy()
        self.patches = {}
        self.depflag = 0

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()


class MockDirectiveBase(ABC):
    directive_name = ""

    def __init__(self, data):
        directive_dict = {
            spack.spec.Spec(when): self.create_directives(spec_names)
            for when, spec_names in data.items()
        }
        self.pkg = FakePkg(self.directive_name, directive_dict)

    def compare(self, data):
        expected = {
            spack.spec.Spec(when): self.create_directives(spec_names)
            for when, spec_names in data.items()
        }
        assert getattr(self.pkg, self.directive_name) == expected

    @abstractmethod
    def create_directives(self, spec_names):
        pass

    @property
    def removal_class(self):
        return spack.directives.DropDirectiveBase

    def remove(self, spec, when):
        self.removal_class(spec, when).remove()(self.pkg)


class MockConflicts(MockDirectiveBase):
    directive_name = "conflicts"

    def create_directives(self, spec_names):
        return [(spack.spec.Spec(spec_name), None) for spec_name in spec_names]

    @property
    def removal_class(self):
        return spack.directives.DropConflicts


class MockDependencies(MockDirectiveBase):
    directive_name = "dependencies"

    def create_directives(self, spec_names):
        pkg = FakePkg(self.directive_name, {})
        return {
            spec_name: FakeDependency(pkg, spack.spec.Spec(spec_name)) for spec_name in spec_names
        }

    @property
    def removal_class(self):
        return spack.directives.DropDependsOn


class MockRequirements(MockDirectiveBase):
    directive_name = "requirements"

    def create_directives(self, spec_names):
        return [((spack.spec.Spec(spec_name),), "one_of", None) for spec_name in spec_names]

    @property
    def removal_class(self):
        return spack.directives.DropRequire


@pytest.fixture(params=[MockConflicts, MockDependencies, MockRequirements])
def mock_directive_class(request):
    """Fixture to provide parameterized mock directive classes."""
    return request.param


def test_remove_no_directives(mock_directive_class):
    mock = mock_directive_class({"@1.0": ["pkg1"]})
    mock.remove("pkg2", "@1.0")
    mock.compare({"@1.0": ["pkg1"]})


def test_remove_one_directive(mock_directive_class):
    mock = mock_directive_class({"@1.0": ["pkg1"]})
    mock.remove("pkg1", "@1.0")
    mock.compare({})


def test_remove_intersecting_directive(mock_directive_class):
    mock = mock_directive_class({"@3:": ["pkg1"]})
    mock.remove("pkg1", "@5:")
    mock.compare({"@3:4": ["pkg1"]})


def test_remove_entire_intersecting_directive(mock_directive_class):
    mock = mock_directive_class({"@3:": ["pkg1"]})
    mock.remove("pkg1", "@2:")
    mock.compare({})


def test_remove_modify_skip_directives(mock_directive_class):
    mock = mock_directive_class({"@1:": ["pkg1", "pkg2", "pkg3"], "@3": ["pkg4"]})
    mock.remove("pkg1", "@1:")  # Remove
    mock.remove("pkg2", "@3:")  # Modify
    # pkg3 is skipped in the nested else statement
    mock.remove("pkg4", "@2")  # Skipped in the outer else statement
    mock.compare({"@1:2": ["pkg2"], "@1:": ["pkg3"], "@3": ["pkg4"]})


def test_drop_all_versions(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_all_versions")
    assert len(cls.versions) == 0


def test_drop_all_conflicts(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_all_conflicts")
    assert len(cls.conflicts) == 0


def test_drop_all_depends_on(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_all_depends_on")
    assert len(cls.dependencies) == 0


def test_drop_all_requires(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_all_requires")
    assert len(cls.dependencies) == 0


def test_drop_version(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_version")
    assert cls.versions == {spack.version.Version("1.2"): {}}


def test_drop_conflict(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_conflict")
    assert cls.conflicts == {spack.spec.Spec("@1.0"): [(spack.spec.Spec("%gcc"), None)]}


def test_drop_conflict_range(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_conflict_range")
    assert cls.conflicts == {spack.spec.Spec("@3:4"): [(spack.spec.Spec("mpi"), None)]}


def test_drop_depends_on(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_depends_on")
    assert cls.dependencies == {
        spack.spec.Spec("@1.0"): {"mpi": spack.dependency.Dependency(cls, spack.spec.Spec("mpi"))}
    }


def test_drop_require(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_require")
    print(f"cls.conflicts={cls.conflicts}")
    print(f"cls.requirements={cls.requirements}")
    assert cls.requirements == {
        spack.spec.Spec("@1.0"): [((spack.spec.Spec("mpi"),), "one_of", None)]
    }


def test_drop_patch(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop_patch")
    leftover_patch = next(iter(cls.patches.values()))[0]
    assert leftover_patch.sha256 == "abc"
    assert cls.patches == {spack.spec.Spec("@1.0"): [leftover_patch]}

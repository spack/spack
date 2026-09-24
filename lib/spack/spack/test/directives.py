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
from spack.directives import (
    _make_when_spec,
    conflicts,
    depends_on,
    deprecated,
    drop_conflict,
    drop_depends_on,
    drop_require,
    drop_version,
    extends,
    patch,
    requires,
    version,
)
from spack.directives_meta import DirectiveDictDescriptor, DirectiveError, DirectiveMeta
from spack.enums import LEGACY_DEPRECATION_LABEL, DeprecationReason, DeprecationSeverity
from spack.repo import RepoPath
from spack.spec import Spec


def test_false_directives_do_not_exist(mock_packages: RepoPath):
    """Ensure directives that evaluate to False at import time are added to
    dicts on packages.
    """
    cls = mock_packages.get_pkg_class("when-directives-false")
    assert not cls.dependencies
    assert not cls.resources
    assert not cls.patches


def test_true_directives_exist(mock_packages: RepoPath):
    """Ensure directives that evaluate to True at import time are added to
    dicts on packages.
    """
    cls = mock_packages.get_pkg_class("when-directives-true")

    assert cls.dependencies
    assert "extendee" in cls.dependencies[spack.spec.Spec()]
    assert "pkg-b" in cls.dependencies[spack.spec.Spec()]

    assert cls.resources
    assert spack.spec.Spec() in cls.resources

    assert cls.patches
    assert spack.spec.Spec() in cls.patches


def test_constraints_from_context(mock_packages: RepoPath):
    pkg_cls = mock_packages.get_pkg_class("with-constraint-met")

    assert pkg_cls.dependencies
    assert "pkg-b" in pkg_cls.dependencies[spack.spec.Spec("@1.0")]

    assert pkg_cls.conflicts
    assert (spack.spec.Spec("%gcc"), None) in pkg_cls.conflicts[spack.spec.Spec("+foo@1.0")]


@pytest.mark.regression("26656")
def test_constraints_from_context_are_merged(mock_packages: RepoPath):
    pkg_cls = mock_packages.get_pkg_class("with-constraint-met")

    assert pkg_cls.dependencies
    # The two ^pkg-b edges (one from the outer `when` context, one from depends_on's own when)
    # are both indirect, so nothing says they are one node, and they stay parallel instead of
    # being forced into a single @3.8:4.0 edge.
    assert "pkg-c" in pkg_cls.dependencies[spack.spec.Spec("@0.14:15 ^pkg-b@:4.0 ^pkg-b@3.8:")]


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
def test_error_on_anonymous_dependency(config, mock_packages: RepoPath):
    pkg = mock_packages.get_pkg_class("pkg-a")
    with pytest.raises(spack.directives.DependencyError):
        spack.directives._DependsOn(spack.spec.Spec("@4.5"))(pkg)


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
def test_maintainer_directive(config, mock_packages: RepoPath, package_name, expected_maintainers):
    pkg_cls = mock_packages.get_pkg_class(package_name)
    assert pkg_cls.maintainers == expected_maintainers


@pytest.mark.parametrize(
    "package_name,expected_licenses", [("licenses-1", [("MIT", "+foo"), ("Apache-2.0", "~foo")])]
)
def test_license_directive(config, mock_packages: RepoPath, package_name, expected_licenses):
    pkg_cls = mock_packages.get_pkg_class(package_name)
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
        spack.directives._License("MIT", "+foo")(package)


def test_overlapping_duplicate_licenses():
    package = namedtuple("package", ["licenses", "name"])
    package.licenses = {spack.spec.Spec("+foo"): "Apache-2.0"}
    package.name = "test_package"

    msg = (
        r"test_package is specified as being licensed as MIT when \+bar, but it is also "
        r"specified as being licensed under Apache-2.0 when \+foo, which conflict."
    )

    with pytest.raises(spack.directives.OverlappingLicenseError, match=msg):
        spack.directives._License("MIT", "+bar")(package)


def test_version_type_validation():
    # A version should be a string or an int, not a float, because it leads to subtle issues
    # such as 3.10 being interpreted as 3.1.

    package = namedtuple("package", ["name"])

    msg = r"python: declared version '.+' in package should be a string or int\."

    # Pass a float
    with pytest.raises(spack.version.VersionError, match=msg):
        spack.directives._Version(ver=3.10, kwargs={})(package(name="python"))

    # Try passing a bogus type; it's just that we want a nice error message
    with pytest.raises(spack.version.VersionError, match=msg):
        spack.directives._Version(ver={}, kwargs={})(package(name="python"))


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
def test_redistribute_directive(
    config, mock_packages: RepoPath, spec_str, distribute_src, distribute_bin
):
    spec = spack.spec.Spec(spec_str)
    assert mock_packages.get_pkg_class(spec.fullname).redistribute_source(spec) == distribute_src
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
    spack.directives._Redistribute(source=False, binary=None, when="@1.0")(cls)
    spec_key = spack.directives._make_when_spec("@1.0")
    assert not cls.disable_redistribute[spec_key].binary
    assert cls.disable_redistribute[spec_key].source
    spack.directives._Redistribute(source=None, binary=False, when="@1.0")(cls)
    assert cls.disable_redistribute[spec_key].binary
    assert cls.disable_redistribute[spec_key].source


@pytest.mark.regression("51248")
def test_direct_dependencies_from_when_context_are_retained(mock_packages: RepoPath):
    """Tests that direct dependencies from the "when" context manager don't lose the "direct"
    attribute when turned into directives on the package class.
    """
    pkg_cls = mock_packages.get_pkg_class("with-constraint-met")
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
    cls = spack.repo.PATH.get_pkg_class("drop-all-versions")
    assert len(cls.versions) == 0


def test_drop_all_conflicts(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-all-conflicts")
    assert len(cls.conflicts) == 0


def test_drop_all_depends_on(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-all-depends-on")
    assert len(cls.dependencies) == 0


def test_drop_all_requires(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-all-requires")
    assert len(cls.dependencies) == 0


def test_drop_version(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-version")
    assert cls.versions == {spack.version.Version("1.2"): {}}


def test_drop_conflict(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-conflict")
    assert cls.conflicts == {spack.spec.Spec("@1.0"): [(spack.spec.Spec("%gcc"), None)]}


def test_drop_conflict_range(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-conflict-range")
    assert cls.conflicts == {spack.spec.Spec("@3:4"): [(spack.spec.Spec("mpi"), None)]}


def test_drop_depends_on(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-depends-on")
    assert cls.dependencies == {
        spack.spec.Spec("@1.0"): {"mpi": spack.dependency.Dependency(spack.spec.Spec("mpi"))}
    }


def test_drop_require(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-require")
    assert cls.requirements == {
        spack.spec.Spec("@1.0"): [((spack.spec.Spec("mpi"),), "one_of", None)]
    }


def test_drop_patch(mock_packages):
    cls = spack.repo.PATH.get_pkg_class("drop-patch")
    leftover_patch = next(iter(cls.patches.values()))[0]
    assert leftover_patch.sha256 == "abc"
    assert cls.patches == {spack.spec.Spec("@1.0"): [leftover_patch]}


def test_directives_meta_combine_when():
    # The ^dep edges are indirect, so nothing says they are one node: combining two
    # when-conditions that each constrain it keeps them parallel instead of fusing them.
    x, y, z = "+x ^dep +a", "+y ^dep +b", "+z"
    assert _make_when_spec((x, y, z)) == Spec("+x +y +z ^dep+a ^dep+b")
    assert _make_when_spec((x, y)) == Spec("+x +y ^dep+a ^dep+b")
    assert _make_when_spec((x,)) == Spec("+x ^dep +a")


def test_directive_descriptor_init():
    # when `pkg.variants` is initialized, only the `variant` directive should run
    variants = DirectiveDictDescriptor("variants")
    assert variants.directives_to_run == ["variant"]
    assert variants.dicts_to_init == ["variants"]

    # when `pkg.dependencies` is initialized, `depends_on` and `extends` should run, and also
    # `pkg.extendees` should be initialized
    dependencies = DirectiveDictDescriptor("dependencies")
    assert dependencies.directives_to_run == [
        "depends_on",
        "drop_all_depends_on",
        "drop_depends_on",
        "extends",
    ]
    assert dependencies.dicts_to_init == ["dependencies", "extendees"]

    # when `pkg.provided` is initialized, so should `pkg.provided_together`, and only the
    # provides directive should run
    provided = DirectiveDictDescriptor("provided")
    assert provided.directives_to_run == ["provides"]
    assert provided.dicts_to_init == ["provided", "provided_together"]

    # idem for `pkg.provided_together`
    provided_together = DirectiveDictDescriptor("provided_together")
    assert provided_together.directives_to_run == ["provides"]
    assert provided_together.dicts_to_init == ["provided", "provided_together"]

    # when specifying patches on dependencies with `depends_on` and `extends`, the `pkg.patches`
    # dict is not affects -- they are stored on a Dependency object.
    # NOTE: the order of `directives_to_run` is not meaningful -- directives are executed in
    # source-declaration order at run time (see DirectiveDictDescriptor.__get__), so this list
    # is only sorted for determinism.
    patches = DirectiveDictDescriptor("patches")
    assert patches.directives_to_run == ["drop_patch", "patch"]
    assert patches.dicts_to_init == ["patches"]


def test_directive_laziness():
    class ExamplePackage(metaclass=DirectiveMeta):
        name = "example-package"
        depends_on("foo")
        extends("bar", when="+bar")

    # Initially, no directive dicts are initialized
    assert ExamplePackage._dependencies is None  # type: ignore
    assert ExamplePackage._extendees is None  # type: ignore
    assert ExamplePackage._variants is None  # type: ignore

    # Only when we access the dependencies descriptor, the relevant dicts (dependencies, extendees)
    # are initialized, while others remain None
    dependencies = ExamplePackage.dependencies  # type: ignore
    assert type(ExamplePackage._dependencies) is dict  # type: ignore
    assert type(ExamplePackage._extendees) is dict  # type: ignore
    assert ExamplePackage._variants is None  # type: ignore

    # The dependencies dict is populated with the expected entries
    assert "foo" in dependencies[spack.spec.Spec()]
    assert "bar" in dependencies[spack.spec.Spec("+bar")]


def test_non_commutative_directives_run_in_source_order():
    """Regression test: directives are executed in source-declaration order, not sorted by
    directive name. This matters for non-commutative directives such as ``drop_version``, which
    must run *after* the ``version`` it targets. A name-based ordering (e.g. sorting, which puts
    ``drop_version`` before ``version``) gets this wrong."""

    # drop_version declared AFTER the version: the version is removed.
    class DropAfter(metaclass=DirectiveMeta):
        name = "drop-after"
        version("1.0")
        version("2.0")
        drop_version("1.0")

    assert spack.version.Version("1.0") not in DropAfter.versions  # type: ignore
    assert spack.version.Version("2.0") in DropAfter.versions  # type: ignore

    # drop_version declared BEFORE the version it names: the drop runs first (no-op, nothing to
    # remove yet), then the version is added, so it survives. If directives were reordered by
    # name, drop_version would incorrectly run after version and delete it.
    class DropBefore(metaclass=DirectiveMeta):
        name = "drop-before"
        drop_version("1.0")
        version("1.0")
        version("2.0")

    assert spack.version.Version("1.0") in DropBefore.versions  # type: ignore
    assert spack.version.Version("2.0") in DropBefore.versions  # type: ignore


@pytest.mark.parametrize(
    "when,offender",
    [
        ("+foo", "variants"),
        ("%gcc", "dependencies"),
        ("^mpi", "dependencies"),
        ("cflags=-O3", "compiler flags"),
        ("target=x86_64", "architecture"),
        ("@1:2 +foo", "variants"),
    ],
)
def test_drop_directive_when_rejects_non_version_constraints(when, offender):
    """A ``drop_*`` ``when=`` clause may only constrain versions: we can compute a
    representable complement for a version range but not for variants, compilers, cflags,
    etc. (a general ``Spec.complement`` is infeasible -- see PR #48947). Anything else must
    fail loudly at package-definition time."""
    with pytest.raises(DirectiveError, match="may only constrain versions"):
        drop_conflict("mpi", when=when)


@pytest.mark.parametrize("when", ["@1.0:2.0", "@1.0:2.0,3.0", "@=1.0", None, True])
def test_drop_directive_when_accepts_version_only_constraints(when):
    """Version-only ``when=`` clauses (and the unconstrained ``None``/``True`` cases) are
    accepted by drop directives."""
    # Should not raise.
    drop_conflict("mpi", when=when)


def test_drop_depends_on_matches_by_satisfaction():

    class Parent(metaclass=DirectiveMeta):
        name = "satisfies-parent"
        depends_on("mpi@1:")

    class Child(Parent):
        name = "satisfies-child"
        drop_depends_on("mpi")

    assert "mpi" in Parent.dependencies[spack.spec.Spec()]  # type: ignore
    assert Child.dependencies == {}  # type: ignore


def test_drop_depends_on_subtracts_version_from_general_entry():
    """When a specific removal spec differs from a more general existing dependency *only* in
    its top-level version, the removal's version range is subtracted out of the existing spec's
    own version range instead of leaving the entry untouched. So ``drop_depends_on("mpi@1:")``
    turns an inherited ``depends_on("mpi")`` (i.e. ``mpi@:``) into ``depends_on("mpi@:0")`` --
    everything below ``@1``. This is a strict generalization of satisfaction matching (the
    satisfy case is the special case where the removal version is unconstrained). See
    PR #48947."""

    class Parent(metaclass=DirectiveMeta):
        name = "subtract-parent"
        depends_on("mpi")

    class Child(Parent):
        name = "subtract-child"
        drop_depends_on("mpi@1:")

    # Parent keeps the full range; child has the @1: range carved out.
    assert str(Parent.dependencies[spack.spec.Spec()]["mpi"].spec) == "mpi"  # type: ignore
    assert str(Child.dependencies[spack.spec.Spec()]["mpi"].spec) == "mpi@:0"  # type: ignore


def test_drop_depends_on_subtraction_empties_range_removes_entry():
    """When subtraction (or, equivalently, satisfaction) removes the entire version range, the
    entry is dropped completely. ``drop_depends_on("mpi@1:")`` against ``depends_on("mpi@1:")``
    leaves nothing."""

    class Parent(metaclass=DirectiveMeta):
        name = "subtract-empty-parent"
        depends_on("mpi@1:")

    class Child(Parent):
        name = "subtract-empty-child"
        drop_depends_on("mpi@1:")

    assert Child.dependencies == {}  # type: ignore


def test_drop_depends_on_subtraction_no_overlap_is_noop():
    """Subtracting a non-overlapping version range leaves the dependency spec unchanged."""

    class Parent(metaclass=DirectiveMeta):
        name = "subtract-noop-parent"
        depends_on("mpi@:0")

    class Child(Parent):
        name = "subtract-noop-child"
        drop_depends_on("mpi@5:")

    assert str(Child.dependencies[spack.spec.Spec()]["mpi"].spec) == "mpi@:0"  # type: ignore


def test_drop_depends_on_does_not_mutate_interned_dependency():
    """``Dependency`` objects are interned and shared across packages, so version subtraction
    must build a *new* dependency rather than mutate the shared one. A child that drops part of
    an inherited dependency's version range must not corrupt the parent's (shared) entry."""

    class Parent(metaclass=DirectiveMeta):
        name = "intern-parent"
        depends_on("mpi")

    parent_dep = Parent.dependencies[spack.spec.Spec()]["mpi"]  # type: ignore

    class Child(Parent):
        name = "intern-child"
        drop_depends_on("mpi@1:")

    # Parent's shared dependency object is untouched (same object, full range); child has a
    # brand-new, trimmed dependency.
    assert Parent.dependencies[spack.spec.Spec()]["mpi"] is parent_dep  # type: ignore
    assert str(parent_dep.spec) == "mpi"
    assert str(Child.dependencies[spack.spec.Spec()]["mpi"].spec) == "mpi@:0"  # type: ignore
    assert Child.dependencies[spack.spec.Spec()]["mpi"] is not parent_dep  # type: ignore


def test_drop_conflict_subtracts_top_level_version():
    """Version subtraction also applies to ``drop_conflict``."""

    class Parent(metaclass=DirectiveMeta):
        name = "conflict-subtract-parent"
        conflicts("mpi")

    class Child(Parent):
        name = "conflict-subtract-child"
        drop_conflict("mpi@1:")

    surviving = [spec for lst in Child.conflicts.values() for spec, _ in lst]  # type: ignore
    assert [str(s) for s in surviving] == ["mpi@:0"]


def test_drop_conflict_compiler_node_version_not_subtracted():
    """Version subtraction is scoped to *top-level* versions. A version carried on a child node
    (e.g. the compiler in ``%gcc@14:``) is out of scope: the entry is left unchanged. This is a
    deliberate, documented limitation -- only top-level versions have a representable
    complement in this machinery. See PR #48947."""

    class Parent(metaclass=DirectiveMeta):
        name = "conflict-compiler-parent"
        conflicts("%gcc")

    class Child(Parent):
        name = "conflict-compiler-child"
        drop_conflict("%gcc@14:")

    surviving = [spec for lst in Child.conflicts.values() for spec, _ in lst]  # type: ignore
    assert [str(s) for s in surviving] == ["%gcc"]


def test_drop_require_subtracts_top_level_version():
    """Version subtraction also applies to ``drop_require``; the requirement's policy and
    message are preserved."""

    class Parent(metaclass=DirectiveMeta):
        name = "require-subtract-parent"
        requires("mpi", policy="one_of", msg="need mpi")

    class Child(Parent):
        name = "require-subtract-child"
        drop_require("mpi@1:")

    entries = [entry for lst in Child.requirements.values() for entry in lst]  # type: ignore
    assert len(entries) == 1
    specs, policy, msg = entries[0]
    assert str(specs[0]) == "mpi@:0"
    assert policy == "one_of"
    assert msg.endswith("need mpi")


def test_drop_depends_on_subtraction_composes_with_when_trim():
    """Version subtraction on the dependency spec composes with the independent trimming of the
    directive's ``when=`` clause. Here the ``when`` range ``@2:4`` is trimmed against the
    removal's ``when`` ``@3`` while the dependency spec is trimmed against the removal's
    ``@1:``."""

    class Parent(metaclass=DirectiveMeta):
        name = "compose-parent"
        depends_on("mpi", when="@2:4")

    class Child(Parent):
        name = "compose-child"
        drop_depends_on("mpi@1:", when="@3")

    rendered = {  # type: ignore
        str(when): {name: str(dep.spec) for name, dep in inner.items()}
        for when, inner in Child.dependencies.items()
    }
    assert rendered == {"@2,4": {"mpi": "mpi@:0"}}


def test_drop_conflict_and_require_match_by_satisfaction():
    """Satisfaction-based matching also applies to ``drop_conflict`` and ``drop_require``:
    dropping ``%gcc`` removes an inherited ``%gcc@14:`` conflict/requirement."""

    class ConflictParent(metaclass=DirectiveMeta):
        name = "conflict-sat-parent"
        conflicts("%gcc@14:", when="@1.0")

    class ConflictChild(ConflictParent):
        name = "conflict-sat-child"
        drop_conflict("%gcc", when="@1.0")

    assert ConflictChild.conflicts == {}  # type: ignore

    class RequireParent(metaclass=DirectiveMeta):
        name = "require-sat-parent"
        requires("%gcc@14:", when="@1.0")

    class RequireChild(RequireParent):
        name = "require-sat-child"
        drop_require("%gcc", when="@1.0")

    assert RequireChild.requirements == {}  # type: ignore


def test_patched_dependencies_sets_class_attribute():
    sha256 = "a" * 64

    class PatchesDependencies(metaclass=DirectiveMeta):
        name = "patches-dependencies"
        depends_on("dependency", patches=patch("https://example.com/diff.patch", sha256=sha256))

    assert PatchesDependencies._patches_dependencies is True
    assert not PatchesDependencies.patches  # type: ignore

    class DoesNotPatchDependencies(metaclass=DirectiveMeta):
        name = "does-not-patch-dependencies"
        fullname = "does-not-patch-dependencies"
        patch("https://example.com/diff.patch", sha256=sha256)

    assert DoesNotPatchDependencies._patches_dependencies is False
    assert DoesNotPatchDependencies.patches  # type: ignore


def test_diamond_inheritance_runs_shared_directives_once():
    """A directive of a base class reachable through more than one base runs exactly once, and
    directives run base classes first, following the MRO."""

    class Base(metaclass=DirectiveMeta):
        name = "base"
        conflicts("%gcc")

    class Left(Base):
        conflicts("%clang")

    class Right(Base):
        conflicts("%intel")

    class Diamond(Left, Right):
        conflicts("%nvhpc")

    def conflict_specs(cls):
        return [str(spec) for spec, _ in cls.conflicts[Spec()]]

    assert conflict_specs(Base) == ["%gcc"]
    assert conflict_specs(Left) == ["%gcc", "%clang"]
    assert conflict_specs(Right) == ["%gcc", "%intel"]
    assert conflict_specs(Diamond) == ["%gcc", "%intel", "%clang", "%nvhpc"]


class MockPkg:
    name = "mypkg"
    deprecations: dict = {}


@pytest.fixture
def mock_pkg():
    pkg = MockPkg()
    pkg.deprecations = {}
    return pkg


class TestDeprecatedDirective:
    def test_severity_ordering(self):
        """Tests that severity values are kept in the correct order."""
        assert (
            DeprecationSeverity("none")
            < DeprecationSeverity("low")
            < DeprecationSeverity("medium")
            < DeprecationSeverity("high")
            < DeprecationSeverity("critical")
        )

    def test_severity_and_reason_invalid_values(self):
        """Tests that an invalid value raises a ValueError."""
        with pytest.raises(ValueError, match="bogus"):
            DeprecationSeverity("bogus")

        with pytest.raises(ValueError, match="foo"):
            DeprecationReason("foo")

    def test_deprecated_directive_version_constraint(self, mock_pkg):
        """Tests the basic use of the deprecated directive."""
        spack.directives._Deprecated(spec="@1.0", reason="vuln", severity="high")(mock_pkg)
        assert len(mock_pkg.deprecations) == 1
        constraint, entries = list(mock_pkg.deprecations.items())[0]
        assert constraint == spack.spec.Spec("@1.0")
        assert entries[0].reason == DeprecationReason.VULN
        assert entries[0].severity == DeprecationSeverity.HIGH
        assert entries[0].labels == ()

    def test_deprecated_directive_whole_package(self, mock_pkg):
        """Tests the deprecated directive on a package."""
        spack.directives._Deprecated(spec=None, reason="rename", severity="low")(mock_pkg)
        assert len(mock_pkg.deprecations) == 1
        constraint = list(mock_pkg.deprecations.keys())[0]
        assert constraint == spack.spec.EMPTY_SPEC

    def test_deprecated_directive_invalid_arguments(self, mock_pkg):
        """Tests that an invalid value is reported along with the values that are accepted."""
        with pytest.raises(DirectiveError, match="'bogus' is not a valid reason, use one of "):
            spack.directives._Deprecated(spec="@1.0", reason="bogus", severity="low")(mock_pkg)

        with pytest.raises(DirectiveError, match="'extreme' is not a valid severity, use one of "):
            spack.directives._Deprecated(spec="@1.0", reason="vuln", severity="extreme")(mock_pkg)

    def test_deprecated_directive_multiple_reasons(self, mock_pkg):
        """Tests cases where we have multiple deprecation reasons on the same constraint."""
        spack.directives._Deprecated(spec="@1.0", reason="vuln", severity="high")(mock_pkg)
        spack.directives._Deprecated(spec="@1.0", reason="rename", severity="low")(mock_pkg)
        assert len(mock_pkg.deprecations) == 1
        assert len(mock_pkg.deprecations[spack.spec.Spec("@1.0")]) == 2

    def test_deprecated_directive_labels(self, mock_pkg):
        """Tests that labels are stored as a tuple of strings."""
        spack.directives._Deprecated(
            spec="@1.0", reason="vuln", severity="high", labels=["CVE-1", "GHSA-2"]
        )(mock_pkg)
        entries = mock_pkg.deprecations[spack.spec.Spec("@1.0")]
        assert entries[0].labels == ("CVE-1", "GHSA-2")

    def test_deprecated_directive_labels_must_not_be_a_string(self, mock_pkg):
        """Tests that a bare string is refused, since iterating it would yield characters."""
        with pytest.raises(DirectiveError, match="must be a list of strings"):
            spack.directives._Deprecated(
                spec="@1.0", reason="vuln", severity="high", labels="CVE-1"
            )(mock_pkg)


def test_deprecated_directive_refuses_the_reserved_label():
    """Tests that a recipe cannot claim the label Spack records for 'deprecated=True'."""
    with pytest.raises(DirectiveError, match="reserved"):

        class Pkg(metaclass=DirectiveMeta):
            name = "mypkg"
            deprecated("@=1.0", reason="vuln", labels=[LEGACY_DEPRECATION_LABEL])


def test_deprecated_keyword_records_the_reserved_label():
    """Tests that 'version(..., deprecated=True)' records an unspecified reason, the highest
    severity, and the label that tells it apart from a recipe stating no reason.
    """

    class Pkg(metaclass=DirectiveMeta):
        name = "mypkg"
        version("1.0", deprecated=True)

    entries = Pkg.deprecations[Spec("@=1.0")]
    assert len(entries) == 1
    assert entries[0].reason == DeprecationReason.UNSPECIFIED
    assert entries[0].severity == DeprecationSeverity.CRITICAL
    assert entries[0].labels == (LEGACY_DEPRECATION_LABEL,)


def test_deprecated_directive_message(mock_pkg):
    """Tests that msg= is stored alongside the reason and the severity."""
    spack.directives._Deprecated(
        spec="@1.0", reason="retired", severity="high", msg="use @2.0 instead"
    )(mock_pkg)
    entries = mock_pkg.deprecations[spack.spec.Spec("@1.0")]
    assert entries[0].msg == "use @2.0 instead"


def test_deprecated_keyword_records_no_message():
    """Tests that 'version(..., deprecated=True)' records no guidance, since it states none."""

    class Pkg(metaclass=DirectiveMeta):
        name = "mypkg"
        version("1.0", deprecated=True)

    assert Pkg.deprecations[Spec("@=1.0")][0].msg is None


def test_deprecated_directive_accepts_an_unspecified_reason():
    """Tests that a recipe can state that a deprecation falls into none of the categories."""

    class Pkg(metaclass=DirectiveMeta):
        name = "mypkg"
        deprecated("@=1.0", reason="unspecified", severity="low", msg="use @=2.0")

    (entry,) = Pkg.deprecations[Spec("@=1.0")]
    assert entry.reason == DeprecationReason.UNSPECIFIED
    assert entry.labels == ()


def test_unspecified_reason_requires_a_message():
    """Tests that a recipe stating no category has to say why the spec is deprecated."""
    with pytest.raises(DirectiveError, match="requires a 'msg' argument"):

        class Pkg(metaclass=DirectiveMeta):
            name = "mypkg"
            deprecated("@=1.0", reason="unspecified")

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from collections import namedtuple

import pytest

import spack.concretize
import spack.directives
import spack.package_base
import spack.spec
import spack.variant
import spack.version
from spack.directives import _make_when_spec, depends_on, extends, patch
from spack.directives_meta import DirectiveDictDescriptor, DirectiveMeta
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
        spack.directives._execute_depends_on(pkg, spack.spec.Spec("@4.5"))


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
        spack.directives._execute_version(package(name="python"), ver=3.10, kwargs={})

    # Try passing a bogus type; it's just that we want a nice error message
    with pytest.raises(spack.version.VersionError, match=msg):
        spack.directives._execute_version(package(name="python"), ver={}, kwargs={})


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
    spack.directives._execute_redistribute(cls, source=False, binary=None, when="@1.0")
    spec_key = spack.directives._make_when_spec("@1.0")
    assert not cls.disable_redistribute[spec_key].binary
    assert cls.disable_redistribute[spec_key].source
    spack.directives._execute_redistribute(cls, source=None, binary=False, when="@1.0")
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


def test_directives_meta_combine_when():
    # The ^dep edges are indirect, so nothing says they are one node: combining two
    # when-conditions that each constrain it keeps them parallel instead of fusing them.
    x, y, z = "+x ^dep +a", "+y ^dep +b", "+z"
    assert _make_when_spec((x, y, z)) == Spec("+x +y +z ^dep+a ^dep+b")
    assert _make_when_spec((x, y)) == Spec("+x +y ^dep+a ^dep+b")
    assert _make_when_spec((x,)) == Spec("+x ^dep +a")


@pytest.mark.parametrize(
    "dict_name,directives_to_run,dicts_to_init",
    [
        # when `pkg.variants` is initialized, only the `variant` directive should run
        ("variants", ["variant"], ["variants"]),
        # idem for `pkg.usages` and the `usage` directive
        ("usages", ["usage"], ["usages"]),
        # when `pkg.dependencies` is initialized, `depends_on` and `extends` should run, and
        # also `pkg.extendees` should be initialized
        ("dependencies", ["depends_on", "extends"], ["dependencies", "extendees"]),
        # when `pkg.provided` is initialized, so should `pkg.provided_together`, and only the
        # provides directive should run
        ("provided", ["provides"], ["provided", "provided_together"]),
        # idem for `pkg.provided_together`
        ("provided_together", ["provides"], ["provided", "provided_together"]),
        # when specifying patches on dependencies with `depends_on` and `extends`, the
        # `pkg.patches` dict is not affected -- they are stored on a Dependency object.
        ("patches", ["patch"], ["patches"]),
    ],
)
def test_directive_descriptor_init(dict_name, directives_to_run, dicts_to_init):
    descriptor = DirectiveDictDescriptor(dict_name)
    assert descriptor.directives_to_run == directives_to_run
    assert descriptor.dicts_to_init == dicts_to_init


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


_OPTION_DIRECTIVE_DEFAULTS = {
    "default": None,
    "description": "",
    "values": None,
    "multi": None,
    "validator": None,
    "when": None,
    "sticky": False,
}


def _execute_variant_directive(pkg, name, **kwargs):
    kwargs = {**_OPTION_DIRECTIVE_DEFAULTS, **kwargs}
    spack.directives._execute_variant(pkg, name=name, **kwargs)


def _execute_usage_directive(pkg, name, **kwargs):
    kwargs = {**_OPTION_DIRECTIVE_DEFAULTS, **kwargs}
    spack.directives._execute_usage(pkg, name=name, unified=False, **kwargs)


class MockOptionPackage:
    """Stand-in package class with just what ``_execute_option`` needs."""

    name = "test-package"

    def __init__(self):
        self.variants = {}
        self.usages = {}

    # This cannot be a classmethod (as it is on PackageBase) because we don't have the rest
    # of the infrastructure stood up here that attaches directives to classes
    def num_definitions(self, dict_name):
        return spack.package_base._num_definitions(getattr(self, dict_name))


@pytest.fixture(
    params=[
        (_execute_variant_directive, spack.variant.Variant, "variants"),
        (_execute_usage_directive, spack.variant.Usage, "usages"),
    ],
    ids=["variant", "usage"],
)
def option_directive(request):
    """(execute function, option class, package dict name) for the variant/usage directives."""
    return request.param


def test_option_directive_stores_definition(option_directive):
    """Executing the directive stores an option of the right type under its when spec, and
    does not touch the dict of the other option type.
    """
    execute, option_cls, dict_name = option_directive
    pkg = MockOptionPackage()

    validator = lambda pkg_name, name, values: None
    execute(
        pkg,
        "foo",
        default="bar",
        description="  a foo option  ",
        values=("bar", "baz"),
        multi=True,
        validator=validator,
        sticky=True,
    )

    definition = getattr(pkg, dict_name)[spack.spec.Spec()]["foo"]
    assert type(definition) is option_cls
    assert definition.name == "foo"
    assert definition.default == "bar"
    assert definition.description == "a foo option"
    assert definition.values == ("bar", "baz")
    assert definition.multi is True
    assert definition.group_validator is validator
    assert definition.sticky is True

    other_dict_name = "usages" if dict_name == "variants" else "variants"
    assert not getattr(pkg, other_dict_name)

    # a conditional definition is stored under its when spec
    execute(pkg, "foo", default="bar", values=("bar", "baz"), when="@1.0")
    assert "foo" in getattr(pkg, dict_name)[spack.spec.Spec("@1.0")]


def test_option_directive_values_inference(option_directive):
    """When ``values`` is not given, it is inferred from the default."""
    execute, _, dict_name = option_directive
    pkg = MockOptionPackage()

    # boolean default (or boolean-looking string) implies boolean values
    execute(pkg, "bool_opt", default=True)
    execute(pkg, "bool_str_opt", default="False")
    definitions = getattr(pkg, dict_name)[spack.spec.Spec()]
    assert definitions["bool_opt"].values == (True, False)
    assert definitions["bool_str_opt"].values == (True, False)

    # any other default implies any value is allowed
    execute(pkg, "str_opt", default="bar")
    assert definitions["str_opt"].values is None
    assert definitions["str_opt"].single_value_validator("anything")

    # a tuple default is stored as a comma-separated string
    execute(pkg, "multi_opt", default=("a", "b"), values=("a", "b", "c"), multi=True)
    assert definitions["multi_opt"].default == "a,b"


def test_option_directive_errors_on_unset_or_empty_default(option_directive):
    execute, _, _ = option_directive
    pkg = MockOptionPackage()

    with pytest.raises(
        spack.directives.DirectiveError, match="either a default was not explicitly set"
    ):
        execute(pkg, "foo", default=None)

    with pytest.raises(
        spack.directives.DirectiveError, match="the default cannot be an empty string"
    ):
        execute(pkg, "foo", default="")


def test_option_directive_errors_on_invalid_name(option_directive):
    execute, _, dict_name = option_directive
    pkg = MockOptionPackage()

    with pytest.raises(
        spack.directives.DirectiveError, match=f"Invalid {dict_name[:-1]} name"
    ):
        execute(pkg, "!foo", default="bar")


def test_option_directive_errors_on_arguments_duplicated_by_values(option_directive):
    """Arguments that the values object supplies itself cannot also be passed explicitly."""
    execute, _, _ = option_directive
    pkg = MockOptionPackage()
    values = spack.variant.disjoint_sets(("a", "b"), ("c", "d"))

    for argument, value in (
        ("default", "a"),
        ("multi", False),
        ("validator", lambda pkg_name, name, values: None),
    ):
        with pytest.raises(
            spack.directives.DirectiveError, match=f"Remove specification of {argument} argument"
        ):
            execute(pkg, "foo", values=values, **{argument: value})


def test_option_directive_adopts_values_object_attributes(option_directive):
    """Default, multi and validator are taken from the values object when not passed."""
    execute, _, dict_name = option_directive
    pkg = MockOptionPackage()

    execute(pkg, "foo", values=spack.variant.disjoint_sets(("a", "b"), ("c", "d")))

    definition = getattr(pkg, dict_name)[spack.spec.Spec()]["foo"]
    assert definition.default == "none"
    assert definition.multi is True
    assert callable(definition.group_validator)


def test_option_directive_definition_precedence(option_directive):
    """Precedence increases with each definition, across names and conditions."""
    execute, _, dict_name = option_directive
    pkg = MockOptionPackage()

    execute(pkg, "foo", default="a", values=("a", "b"))
    execute(pkg, "bar", default="a", values=("a", "b"), when="@1.0")
    execute(pkg, "foo", default="b", values=("a", "b"), when="@2.0")

    definitions = getattr(pkg, dict_name)
    assert definitions[spack.spec.Spec()]["foo"].precedence == 0
    assert definitions[spack.spec.Spec("@1.0")]["bar"].precedence == 1
    assert definitions[spack.spec.Spec("@2.0")]["foo"].precedence == 2


def test_option_directive_last_definition_wins_per_condition(option_directive):
    """Two definitions of the same name with the same when spec: the last one wins."""
    execute, _, dict_name = option_directive
    pkg = MockOptionPackage()

    execute(pkg, "foo", default="a", values=("a", "b"), when="@1.0")
    execute(pkg, "foo", default="b", values=("a", "b"), when="@1.0")

    definitions = getattr(pkg, dict_name)
    assert len(definitions) == 1
    assert len(definitions[spack.spec.Spec("@1.0")]) == 1
    assert definitions[spack.spec.Spec("@1.0")]["foo"].default == "b"


def test_variant_and_usage_directives_are_independent():
    """A variant and a usage with the same name coexist, with independent precedence."""
    pkg = MockOptionPackage()

    _execute_variant_directive(pkg, "foo", default="a", values=("a", "b"))
    _execute_usage_directive(pkg, "foo", default="b", values=("a", "b"))

    variant_def = pkg.variants[spack.spec.Spec()]["foo"]
    usage_def = pkg.usages[spack.spec.Spec()]["foo"]
    assert type(variant_def) is spack.variant.Variant
    assert type(usage_def) is spack.variant.Usage
    assert variant_def.default == "a"
    assert usage_def.default == "b"

    # the precedence counters of the two dicts do not interact
    assert variant_def.precedence == 0
    assert usage_def.precedence == 0

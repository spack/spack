# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import numbers

import pytest

import spack.concretize
import spack.error
import spack.repo
import spack.spec
import spack.variant
from spack.spec import Spec, VariantMap
from spack.variant import (
    BoolValuedVariant,
    DuplicateVariantError,
    InconsistentValidationError,
    InvalidVariantValueError,
    MultipleValuesInExclusiveVariantError,
    MultiValuedVariant,
    SingleValuedVariant,
    UnsatisfiableVariantSpecError,
    Variant,
    VariantValue,
    disjoint_sets,
)


class TestMultiValuedVariant:
    def test_initialization(self):
        # Basic properties
        a = MultiValuedVariant("foo", ("bar", "baz"))
        assert str(a) == "foo:=bar,baz"
        assert a.values == ("bar", "baz")
        assert a.value == ("bar", "baz")
        assert "bar" in a
        assert "baz" in a

        # Order is not important
        c = MultiValuedVariant("foo", ("baz", "bar"))
        assert str(c) == "foo:=bar,baz"
        assert c.values == ("bar", "baz")
        assert "bar" in c
        assert "baz" in c
        assert a == c
        assert hash(a) == hash(c)

        # Check the copy
        d = a.copy()
        assert str(a) == str(d)
        assert d.values == ("bar", "baz")
        assert "bar" in d
        assert "baz" in d
        assert a == d
        assert a is not d
        assert hash(a) == hash(d)

    def test_satisfies(self):
        a = MultiValuedVariant("foo", ("bar", "baz"))
        b = MultiValuedVariant("foo", ("bar",))
        c = MultiValuedVariant("fee", ("bar", "baz"))
        d = MultiValuedVariant("foo", (True,))

        # concrete, different values do not satisfy each other
        assert not a.satisfies(b) and not b.satisfies(a)
        assert not a.satisfies(c) and not c.satisfies(a)

        # SingleValuedVariant and MultiValuedVariant with the same single concrete value do satisfy
        # eachother
        b_sv = SingleValuedVariant("foo", "bar")
        assert b.satisfies(b_sv) and b_sv.satisfies(b)
        d_sv = SingleValuedVariant("foo", True)
        assert d.satisfies(d_sv) and d_sv.satisfies(d)
        almost_d_bv = SingleValuedVariant("foo", True)
        assert d.satisfies(almost_d_bv)

        d_bv = BoolValuedVariant("foo", True)
        assert d.satisfies(d_bv) and d_bv.satisfies(d)

    def test_intersects(self):
        a = MultiValuedVariant("foo", ("bar", "baz"))
        b = MultiValuedVariant("foo", (True,))
        c = MultiValuedVariant("fee", ("bar", "baz"))
        d = MultiValuedVariant("foo", ("bar", "barbaz"))

        # concrete, different values do not intersect.
        assert not a.intersects(b) and not b.intersects(a)
        assert not a.intersects(c) and not c.intersects(a)
        assert not a.intersects(d) and not d.intersects(a)
        assert not b.intersects(c) and not c.intersects(b)
        assert not b.intersects(d) and not d.intersects(b)
        assert not c.intersects(d) and not d.intersects(c)

        # SV and MV intersect if they have the same concrete value.
        b_sv = SingleValuedVariant("foo", True)
        assert b.intersects(b_sv)
        assert not c.intersects(b_sv)

        # BoolValuedVariant intersects if the value is the same
        b_bv = BoolValuedVariant("foo", True)
        assert b.intersects(b_bv)
        assert not c.intersects(b_bv)

    def test_constrain(self):
        # Concrete values cannot be constrained
        a = MultiValuedVariant("foo", ("bar", "baz"))
        b = MultiValuedVariant("foo", ("bar",))
        with pytest.raises(UnsatisfiableVariantSpecError):
            a.constrain(b)
        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on the same value
        a = MultiValuedVariant("foo", ("bar", "baz"))
        b = a.copy()

        assert not a.constrain(b)
        assert a == b == MultiValuedVariant("foo", ("bar", "baz"))

        # Try to constrain on a different name
        a = MultiValuedVariant("foo", ("bar", "baz"))
        b = MultiValuedVariant("fee", ("bar",))

        with pytest.raises(UnsatisfiableVariantSpecError):
            a.constrain(b)

    def test_yaml_entry(self):
        a = MultiValuedVariant("foo", ("bar", "baz", "barbaz"))
        expected = ("foo", sorted(("bar", "baz", "barbaz")))

        assert a.yaml_entry() == expected

        a = MultiValuedVariant("foo", ("bar",))
        expected = ("foo", sorted(["bar"]))

        assert a.yaml_entry() == expected


class TestSingleValuedVariant:
    def test_initialization(self):
        # Basic properties
        a = SingleValuedVariant("foo", "bar")
        assert str(a) == "foo=bar"
        assert a.values == ("bar",)
        assert a.value == "bar"
        assert "bar" in a

        # Check the copy
        b = a.copy()
        assert str(a) == str(b)
        assert b.values == ("bar",)
        assert b.value == "bar"
        assert "bar" in b
        assert a == b
        assert a is not b
        assert hash(a) == hash(b)

    def test_satisfies(self):
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "bar")
        c = SingleValuedVariant("foo", "baz")
        d = SingleValuedVariant("fee", "bar")

        # concrete, different values do not satisfy each other
        assert not a.satisfies(c) and not c.satisfies(a)
        assert not a.satisfies(d) and not d.satisfies(a)
        assert not b.satisfies(c) and not c.satisfies(b)
        assert not b.satisfies(d) and not d.satisfies(b)
        assert not c.satisfies(d) and not d.satisfies(c)

        assert a.satisfies(b) and b.satisfies(a)

    def test_intersects(self):
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("fee", "bar")
        c = SingleValuedVariant("foo", "baz")
        d = SingleValuedVariant("foo", "bar")

        # concrete, different values do not intersect
        assert not a.intersects(b) and not b.intersects(a)
        assert not a.intersects(c) and not c.intersects(a)
        assert not b.intersects(c) and not c.intersects(b)
        assert not b.intersects(d) and not d.intersects(b)
        assert not c.intersects(d) and not d.intersects(c)

        assert a.intersects(d) and d.intersects(a)

    def test_constrain(self):
        # Try to constrain on a value equal to self
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "bar")

        assert not a.constrain(b)
        assert a == SingleValuedVariant("foo", "bar")

        # Try to constrain on a value with a different value
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("foo", "baz")

        # Try to constrain on a value with a different value
        a = SingleValuedVariant("foo", "bar")
        b = SingleValuedVariant("fee", "bar")

        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on the same value
        a = SingleValuedVariant("foo", "bar")
        b = a.copy()

        assert not a.constrain(b)
        assert a == SingleValuedVariant("foo", "bar")

    def test_yaml_entry(self):
        a = SingleValuedVariant("foo", "bar")
        expected = ("foo", "bar")

        assert a.yaml_entry() == expected


class TestBoolValuedVariant:
    def test_initialization(self):
        # Basic properties - True value
        a = BoolValuedVariant("foo", True)
        assert str(a) == "+foo"
        assert a.value is True
        assert a.values == (True,)
        assert True in a

        # Copy - True value
        b = a.copy()
        assert str(a) == str(b)
        assert b.value is True
        assert b.values == (True,)
        assert True in b
        assert a == b
        assert a is not b
        assert hash(a) == hash(b)

        # Copy - False value
        a = BoolValuedVariant("foo", False)
        b = a.copy()
        assert str(a) == str(b)
        assert b.value is False
        assert b.values == (False,)
        assert False in b
        assert a == b
        assert a is not b

    def test_satisfies(self):
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("foo", False)
        c = BoolValuedVariant("fee", False)
        d = BoolValuedVariant("foo", True)

        # concrete, different values do not satisfy each other
        assert not a.satisfies(b) and not b.satisfies(a)
        assert not a.satisfies(c) and not c.satisfies(a)
        assert not b.satisfies(c) and not c.satisfies(b)
        assert not b.satisfies(d) and not d.satisfies(b)
        assert not c.satisfies(d) and not d.satisfies(c)

        assert a.satisfies(d) and d.satisfies(a)

        # # BV variants are case insensitive to 'True' or 'False'
        # d_mv = MultiValuedVariant("foo", "True")
        # assert d.satisfies(d_mv)
        # assert not b.satisfies(d_mv)

        # d_mv = MultiValuedVariant("foo", "FaLsE")
        # assert not d.satisfies(d_mv)
        # assert b.satisfies(d_mv)

        # d_mv = MultiValuedVariant("foo", "bar")
        # assert not d.satisfies(d_mv)
        # assert not b.satisfies(d_mv)

        # d_sv = SingleValuedVariant("foo", "True")
        # assert d.satisfies(d_sv)

    def test_intersects(self):
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("fee", True)
        c = BoolValuedVariant("foo", False)
        d = BoolValuedVariant("foo", True)

        # concrete, different values do not intersect each other
        assert not a.intersects(b) and not b.intersects(a)
        assert not a.intersects(c) and not c.intersects(a)
        assert not b.intersects(c) and not c.intersects(b)
        assert not b.intersects(d) and not d.intersects(b)
        assert not c.intersects(d) and not d.intersects(c)

        assert a.intersects(d) and d.intersects(a)

        # for value in ("True", "TrUe", "TRUE"):
        #     d_mv = MultiValuedVariant("foo", value)
        #     assert d.intersects(d_mv)
        #     assert not c.intersects(d_mv)

        #     d_sv = SingleValuedVariant("foo", value)
        #     assert d.intersects(d_sv)
        #     assert not c.intersects(d_sv)

    def test_constrain(self):
        # Try to constrain on a value equal to self
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("foo", True)

        assert not a.constrain(b)
        assert a == BoolValuedVariant("foo", True)

        # Try to constrain on a value with a different value
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("foo", False)

        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on a value with a different value
        a = BoolValuedVariant("foo", True)
        b = BoolValuedVariant("fee", True)

        with pytest.raises(UnsatisfiableVariantSpecError):
            b.constrain(a)

        # Try to constrain on the same value
        a = BoolValuedVariant("foo", True)
        b = a.copy()

        assert not a.constrain(b)
        assert a == BoolValuedVariant("foo", True)

    def test_yaml_entry(self):
        a = BoolValuedVariant("foo", True)
        expected = ("foo", True)
        assert a.yaml_entry() == expected

        a = BoolValuedVariant("foo", False)
        expected = ("foo", False)
        assert a.yaml_entry() == expected


def test_from_node_dict():
    a = VariantValue.from_node_dict("foo", ["bar"])
    assert a.type == spack.variant.VariantType.MULTI

    a = VariantValue.from_node_dict("foo", "bar")
    assert a.type == spack.variant.VariantType.SINGLE

    a = VariantValue.from_node_dict("foo", "true")
    assert a.type == spack.variant.VariantType.BOOL


class TestVariant:
    def test_validation(self):
        a = Variant(
            "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
        )
        # Valid vspec, shouldn't raise
        vspec = a.make_variant("bar")
        a.validate_or_raise(vspec, "test-package")

        # Multiple values are not allowed
        with pytest.raises(MultipleValuesInExclusiveVariantError):
            vspec.set("bar", "baz")

        # Inconsistent vspec
        vspec.name = "FOO"
        with pytest.raises(InconsistentValidationError):
            a.validate_or_raise(vspec, "test-package")

        # Valid multi-value vspec
        a.multi = True
        vspec = a.make_variant("bar", "baz")
        a.validate_or_raise(vspec, "test-package")
        # Add an invalid value
        vspec.set("bar", "baz", "barbaz")
        with pytest.raises(InvalidVariantValueError):
            a.validate_or_raise(vspec, "test-package")

    def test_callable_validator(self):
        def validator(x):
            try:
                return isinstance(int(x), numbers.Integral)
            except ValueError:
                return False

        a = Variant("foo", default="1024", description="", values=validator, multi=False)
        vspec = a.make_default()
        a.validate_or_raise(vspec, "test-package")
        vspec.set("2056")
        a.validate_or_raise(vspec, "test-package")
        vspec.set("foo")
        with pytest.raises(InvalidVariantValueError):
            a.validate_or_raise(vspec, "test-package")

    def test_representation(self):
        a = Variant(
            "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
        )
        assert a.allowed_values == "bar, baz, foobar"

    def test_str(self):
        string = str(
            Variant(
                "foo", default="", description="", values=("bar", "baz", "foobar"), multi=False
            )
        )
        assert "'foo'" in string
        assert "default=''" in string
        assert "description=''" in string
        assert "values=('foo', 'bar', 'baz') in string"


class TestVariantMapTest:
    def test_invalid_values(self) -> None:
        # Value with invalid type
        a = VariantMap(Spec())
        with pytest.raises(TypeError):
            a["foo"] = 2

        # Duplicate variant
        a["foo"] = MultiValuedVariant("foo", ("bar", "baz"))
        with pytest.raises(DuplicateVariantError):
            a["foo"] = MultiValuedVariant("foo", ("bar",))

        with pytest.raises(DuplicateVariantError):
            a["foo"] = SingleValuedVariant("foo", "bar")

        with pytest.raises(DuplicateVariantError):
            a["foo"] = BoolValuedVariant("foo", True)

        # Non matching names between key and vspec.name
        with pytest.raises(KeyError):
            a["bar"] = MultiValuedVariant("foo", ("bar",))

    def test_set_item(self) -> None:
        # Check that all the three types of variants are accepted
        a = VariantMap(Spec())

        a["foo"] = BoolValuedVariant("foo", True)
        a["bar"] = SingleValuedVariant("bar", "baz")
        a["foobar"] = MultiValuedVariant("foobar", ("a", "b", "c", "d", "e"))

    def test_substitute(self) -> None:
        # Check substitution of a key that exists
        a = VariantMap(Spec())
        a["foo"] = BoolValuedVariant("foo", True)
        a.substitute(SingleValuedVariant("foo", "bar"))

        # Trying to substitute something that is not
        # in the map will raise a KeyError
        with pytest.raises(KeyError):
            a.substitute(BoolValuedVariant("bar", True))

    def test_satisfies_and_constrain(self) -> None:
        # foo=bar foobar=fee feebar=foo
        a = VariantMap(Spec())
        a["foo"] = MultiValuedVariant("foo", ("bar",))
        a["foobar"] = SingleValuedVariant("foobar", "fee")
        a["feebar"] = SingleValuedVariant("feebar", "foo")

        # foo=bar,baz foobar=fee shared=True
        b = VariantMap(Spec())
        b["foo"] = MultiValuedVariant("foo", ("bar", "baz"))
        b["foobar"] = SingleValuedVariant("foobar", "fee")
        b["shared"] = BoolValuedVariant("shared", True)

        # concrete, different values do not intersect / satisfy each other
        assert not a.intersects(b) and not b.intersects(a)
        assert not a.satisfies(b) and not b.satisfies(a)

        # foo=bar,baz foobar=fee feebar=foo shared=True
        c = VariantMap(Spec())
        c["foo"] = MultiValuedVariant("foo", ("bar", "baz"))
        c["foobar"] = SingleValuedVariant("foobar", "fee")
        c["feebar"] = SingleValuedVariant("feebar", "foo")
        c["shared"] = BoolValuedVariant("shared", True)

        # concrete values cannot be constrained
        with pytest.raises(spack.variant.UnsatisfiableVariantSpecError):
            a.constrain(b)

    def test_copy(self) -> None:
        a = VariantMap(Spec())
        a["foo"] = BoolValuedVariant("foo", True)
        a["bar"] = SingleValuedVariant("bar", "baz")
        a["foobar"] = MultiValuedVariant("foobar", ("a", "b", "c", "d", "e"))

        c = a.copy()
        assert a == c

    def test_str(self) -> None:
        c = VariantMap(Spec())
        c["foo"] = MultiValuedVariant("foo", ("bar", "baz"))
        c["foobar"] = SingleValuedVariant("foobar", "fee")
        c["feebar"] = SingleValuedVariant("feebar", "foo")
        c["shared"] = BoolValuedVariant("shared", True)
        assert str(c) == "+shared feebar=foo foo:=bar,baz foobar=fee"


def test_disjoint_set_initialization_errors():
    # Constructing from non-disjoint sets should raise an exception
    with pytest.raises(spack.error.SpecError) as exc_info:
        disjoint_sets(("a", "b"), ("b", "c"))
    assert "sets in input must be disjoint" in str(exc_info.value)

    # A set containing the reserved item 'none' along with other items
    # should raise an exception
    with pytest.raises(spack.error.SpecError) as exc_info:
        disjoint_sets(("a", "b"), ("none", "c"))
    assert "The value 'none' represents the empty set," in str(exc_info.value)


def test_disjoint_set_initialization():
    # Test that no error is thrown when the sets are disjoint
    d = disjoint_sets(("a",), ("b", "c"), ("e", "f"))

    assert d.default == "none"
    assert d.multi is True
    assert set(x for x in d) == set(["none", "a", "b", "c", "e", "f"])


def test_disjoint_set_fluent_methods():
    # Construct an object without the empty set
    d = disjoint_sets(("a",), ("b", "c"), ("e", "f")).prohibit_empty_set()
    assert set(("none",)) not in d.sets

    # Call this 2 times to check that no matter whether
    # the empty set was allowed or not before, the state
    # returned is consistent.
    for _ in range(2):
        d = d.allow_empty_set()
        assert set(("none",)) in d.sets
        assert "none" in d
        assert "none" in [x for x in d]
        assert "none" in d.feature_values

    # Marking a value as 'non-feature' removes it from the
    # list of feature values, but not for the items returned
    # when iterating over the object.
    d = d.with_non_feature_values("none")
    assert "none" in d
    assert "none" in [x for x in d]
    assert "none" not in d.feature_values

    # Call this 2 times to check that no matter whether
    # the empty set was allowed or not before, the state
    # returned is consistent.
    for _ in range(2):
        d = d.prohibit_empty_set()
        assert set(("none",)) not in d.sets
        assert "none" not in d
        assert "none" not in [x for x in d]
        assert "none" not in d.feature_values


@pytest.mark.regression("32694")
@pytest.mark.parametrize("other", [True, False])
def test_conditional_value_comparable_to_bool(other):
    value = spack.variant.ConditionalValue("98", when=Spec("@1.0"))
    comparison = value == other
    assert comparison is False


@pytest.mark.regression("40405")
def test_wild_card_valued_variants_equivalent_to_str():
    """
    There was a bug prioro to PR 40406 in that variants with wildcard values "*"
    were being overwritten in the variant constructor.
    The expected/appropriate behavior is for it to behave like value=str and this
    test demonstrates that the two are now equivalent
    """
    str_var = spack.variant.Variant(
        name="str_var",
        default="none",
        values=str,
        description="str variant",
        multi=True,
        validator=None,
    )

    wild_var = spack.variant.Variant(
        name="wild_var",
        default="none",
        values="*",
        description="* variant",
        multi=True,
        validator=None,
    )

    several_arbitrary_values = ("doe", "re", "mi")
    # "*" case
    wild_output = wild_var.make_variant(*several_arbitrary_values)
    wild_var.validate_or_raise(wild_output, "test-package")
    # str case
    str_output = str_var.make_variant(*several_arbitrary_values)
    str_var.validate_or_raise(str_output, "test-package")
    # equivalence each instance already validated
    assert str_output.value == wild_output.value


def test_variant_definitions(mock_packages):
    pkg = spack.repo.PATH.get_pkg_class("variant-values")

    # two variant names
    assert len(pkg.variant_names()) == 2
    assert "build_system" in pkg.variant_names()
    assert "v" in pkg.variant_names()

    # this name doesn't exist
    assert len(pkg.variant_definitions("no-such-variant")) == 0

    # there are 4 definitions but one is completely shadowed by another
    assert len(pkg.variants) == 4

    # variant_items ignores the shadowed definition
    assert len(list(pkg.variant_items())) == 3

    # variant_definitions also ignores the shadowed definition
    defs = [vdef for _, vdef in pkg.variant_definitions("v")]
    assert len(defs) == 2
    assert defs[0].default == "foo"
    assert defs[0].values == ("foo",)

    assert defs[1].default == "bar"
    assert defs[1].values == ("foo", "bar")


@pytest.mark.parametrize(
    "pkg_name,value,spec,def_ids",
    [
        ("variant-values", "foo", "", [0, 1]),
        ("variant-values", "bar", "", [1]),
        ("variant-values", "foo", "@1.0", [0]),
        ("variant-values", "foo", "@2.0", [1]),
        ("variant-values", "foo", "@3.0", [1]),
        ("variant-values", "foo", "@4.0", []),
        ("variant-values", "bar", "@2.0", [1]),
        ("variant-values", "bar", "@3.0", [1]),
        ("variant-values", "bar", "@4.0", []),
        # now with a global override
        ("variant-values-override", "bar", "", [0]),
        ("variant-values-override", "bar", "@1.0", [0]),
        ("variant-values-override", "bar", "@2.0", [0]),
        ("variant-values-override", "bar", "@3.0", [0]),
        ("variant-values-override", "bar", "@4.0", [0]),
        ("variant-values-override", "baz", "", [0]),
        ("variant-values-override", "baz", "@2.0", [0]),
        ("variant-values-override", "baz", "@3.0", [0]),
        ("variant-values-override", "baz", "@4.0", [0]),
    ],
)
def test_prevalidate_variant_value(mock_packages, pkg_name, value, spec, def_ids):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)

    all_defs = [vdef for _, vdef in pkg.variant_definitions("v")]

    valid_defs = spack.variant.prevalidate_variant_value(
        pkg, SingleValuedVariant("v", value), spack.spec.Spec(spec)
    )
    assert len(valid_defs) == len(def_ids)

    for vdef, i in zip(valid_defs, def_ids):
        assert vdef is all_defs[i]


@pytest.mark.parametrize(
    "pkg_name,value,spec",
    [
        ("variant-values", "baz", ""),
        ("variant-values", "bar", "@1.0"),
        ("variant-values", "bar", "@4.0"),
        ("variant-values", "baz", "@3.0"),
        ("variant-values", "baz", "@4.0"),
        # and with override
        ("variant-values-override", "foo", ""),
        ("variant-values-override", "foo", "@1.0"),
        ("variant-values-override", "foo", "@2.0"),
        ("variant-values-override", "foo", "@3.0"),
        ("variant-values-override", "foo", "@4.0"),
    ],
)
def test_strict_invalid_variant_values(mock_packages, pkg_name, value, spec):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)

    with pytest.raises(spack.variant.InvalidVariantValueError):
        spack.variant.prevalidate_variant_value(
            pkg, SingleValuedVariant("v", value), spack.spec.Spec(spec), strict=True
        )


@pytest.mark.parametrize(
    "pkg_name,spec,satisfies,def_id",
    [
        ("variant-values", "@1.0", "v=foo", 0),
        ("variant-values", "@2.0", "v=bar", 1),
        ("variant-values", "@3.0", "v=bar", 1),
        ("variant-values-override", "@1.0", "v=baz", 0),
        ("variant-values-override", "@2.0", "v=baz", 0),
        ("variant-values-override", "@3.0", "v=baz", 0),
    ],
)
def test_concretize_variant_default_with_multiple_defs(
    mock_packages, config, pkg_name, spec, satisfies, def_id
):
    pkg = spack.repo.PATH.get_pkg_class(pkg_name)
    pkg_defs = [vdef for _, vdef in pkg.variant_definitions("v")]

    spec = spack.concretize.concretize_one(f"{pkg_name}{spec}")
    assert spec.satisfies(satisfies)
    assert spec.package.get_variant("v") is pkg_defs[def_id]


@pytest.mark.parametrize(
    "spec,variant_name,narrowed_type",
    [
        # dev_path is a special case
        ("foo dev_path=/path/to/source", "dev_path", spack.variant.VariantType.SINGLE),
        # reserved name: won't be touched
        ("foo patches=2349dc44", "patches", spack.variant.VariantType.MULTI),
        # simple case -- one definition applies
        ("variant-values@1.0 v=foo", "v", spack.variant.VariantType.SINGLE),
        # simple, but with bool valued variant
        ("pkg-a bvv=true", "bvv", spack.variant.VariantType.BOOL),
        # takes the second definition, which overrides the single-valued one
        ("variant-values@2.0 v=bar", "v", spack.variant.VariantType.MULTI),
    ],
)
def test_substitute_abstract_variants_narrowing(mock_packages, spec, variant_name, narrowed_type):
    spec = Spec(spec)
    spack.spec.substitute_abstract_variants(spec)
    assert spec.variants[variant_name].type == narrowed_type


def test_substitute_abstract_variants_failure(mock_packages):
    with pytest.raises(spack.spec.InvalidVariantForSpecError):
        # variant doesn't exist at version
        spack.spec.substitute_abstract_variants(Spec("variant-values@4.0 v=bar"))


def test_abstract_variant_satisfies_abstract_abstract():
    # rhs should be a subset of lhs
    assert Spec("foo=bar").satisfies("foo=bar")
    assert Spec("foo=bar,baz").satisfies("foo=bar")
    assert Spec("foo=bar,baz").satisfies("foo=bar,baz")
    assert not Spec("foo=bar").satisfies("foo=baz")
    assert not Spec("foo=bar").satisfies("foo=bar,baz")
    assert Spec("foo=bar").satisfies("foo=*")  # rhs empty set
    assert Spec("foo=*").satisfies("foo=*")  # lhs and rhs empty set
    assert not Spec("foo=*").satisfies("foo=bar")  # lhs empty set, rhs not


def test_abstract_variant_satisfies_concrete_abstract():
    # rhs should be a subset of lhs
    assert Spec("foo:=bar").satisfies("foo=bar")
    assert Spec("foo:=bar,baz").satisfies("foo=bar")
    assert Spec("foo:=bar,baz").satisfies("foo=bar,baz")
    assert not Spec("foo:=bar").satisfies("foo=baz")
    assert not Spec("foo:=bar").satisfies("foo=bar,baz")
    assert Spec("foo:=bar").satisfies("foo=*")  # rhs empty set


def test_abstract_variant_satisfies_abstract_concrete():
    # always false since values can be added to the lhs
    assert not Spec("foo=bar").satisfies("foo:=bar")
    assert not Spec("foo=bar,baz").satisfies("foo:=bar")
    assert not Spec("foo=bar,baz").satisfies("foo:=bar,baz")
    assert not Spec("foo=bar").satisfies("foo:=baz")
    assert not Spec("foo=bar").satisfies("foo:=bar,baz")
    assert not Spec("foo=*").satisfies("foo:=bar")  # lhs empty set


def test_abstract_variant_satisfies_concrete_concrete():
    # concrete values only satisfy each other when equal
    assert Spec("foo:=bar").satisfies("foo:=bar")
    assert not Spec("foo:=bar,baz").satisfies("foo:=bar")
    assert not Spec("foo:=bar").satisfies("foo:=bar,baz")
    assert Spec("foo:=bar,baz").satisfies("foo:=bar,baz")


def test_abstract_variant_intersects_abstract_abstract():
    # always true since the union of values satisfies both
    assert Spec("foo=bar").intersects("foo=bar")
    assert Spec("foo=bar,baz").intersects("foo=bar")
    assert Spec("foo=bar,baz").intersects("foo=bar,baz")
    assert Spec("foo=bar").intersects("foo=baz")
    assert Spec("foo=bar").intersects("foo=bar,baz")
    assert Spec("foo=bar").intersects("foo=*")  # rhs empty set
    assert Spec("foo=*").intersects("foo=*")  # lhs and rhs empty set
    assert Spec("foo=*").intersects("foo=bar")  # lhs empty set, rhs not


def test_abstract_variant_intersects_concrete_abstract():
    assert Spec("foo:=bar").intersects("foo=bar")
    assert Spec("foo:=bar,baz").intersects("foo=bar")
    assert Spec("foo:=bar,baz").intersects("foo=bar,baz")
    assert not Spec("foo:=bar").intersects("foo=baz")  # rhs has at least baz, lhs has not
    assert not Spec("foo:=bar").intersects("foo=bar,baz")  # rhs has at least baz, lhs has not
    assert Spec("foo:=bar").intersects("foo=*")  # rhs empty set


def test_abstract_variant_intersects_abstract_concrete():
    assert Spec("foo=bar").intersects("foo:=bar")
    assert not Spec("foo=bar,baz").intersects("foo:=bar")  # lhs has at least baz, rhs has not
    assert Spec("foo=bar,baz").intersects("foo:=bar,baz")
    assert not Spec("foo=bar").intersects("foo:=baz")  # lhs has at least bar, rhs has not
    assert Spec("foo=bar").intersects("foo:=bar,baz")
    assert Spec("foo=*").intersects("foo:=bar")  # lhs empty set


def test_abstract_variant_intersects_concrete_concrete():
    # concrete values only intersect each other when equal
    assert Spec("foo:=bar").intersects("foo:=bar")
    assert not Spec("foo:=bar,baz").intersects("foo:=bar")
    assert not Spec("foo:=bar").intersects("foo:=bar,baz")
    assert Spec("foo:=bar,baz").intersects("foo:=bar,baz")


def test_abstract_variant_constrain_abstract_abstract():
    s1 = Spec("foo=bar")
    s2 = Spec("foo=*")
    assert s1.constrain("foo=baz")
    assert s1 == Spec("foo=bar,baz")
    assert s2.constrain("foo=baz")
    assert s2 == Spec("foo=baz")


def test_abstract_variant_constrain_abstract_concrete_fail():
    with pytest.raises(UnsatisfiableVariantSpecError):
        Spec("foo=bar").constrain("foo:=baz")


def test_abstract_variant_constrain_abstract_concrete_ok():
    s1 = Spec("foo=bar")
    s2 = Spec("foo=*")
    assert s1.constrain("foo:=bar")  # the change is concreteness
    assert s1 == Spec("foo:=bar")
    assert s2.constrain("foo:=bar")
    assert s2 == Spec("foo:=bar")


def test_abstract_variant_constrain_concrete_concrete_fail():
    with pytest.raises(UnsatisfiableVariantSpecError):
        Spec("foo:=bar").constrain("foo:=bar,baz")


def test_abstract_variant_constrain_concrete_concrete_ok():
    s = Spec("foo:=bar")
    assert not s.constrain("foo:=bar")  # no change


def test_abstract_variant_constrain_concrete_abstract_fail():
    s = Spec("foo:=bar")
    with pytest.raises(UnsatisfiableVariantSpecError):
        s.constrain("foo=baz")


def test_abstract_variant_constrain_concrete_abstract_ok():
    s = Spec("foo:=bar,baz")
    assert not s.constrain("foo=bar")  # no change in value or concreteness
    assert not s.constrain("foo=*")


def test_patches_variant():
    """patches=x,y,z is a variant with special satisfies behavior when the rhs is abstract; it
    allows string prefix matching of the lhs."""
    assert Spec("patches:=abcdef").satisfies("patches=ab")
    assert Spec("patches:=abcdef").satisfies("patches=abcdef")
    assert not Spec("patches:=abcdef").satisfies("patches=xyz")
    assert Spec("patches:=abcdef,xyz").satisfies("patches=xyz")
    assert not Spec("patches:=abcdef").satisfies("patches=abcdefghi")

    # but when the rhs is concrete, it must match exactly
    assert Spec("patches:=abcdef").satisfies("patches:=abcdef")
    assert not Spec("patches:=abcdef").satisfies("patches:=ab")
    assert not Spec("patches:=abcdef,xyz").satisfies("patches:=abc,xyz")
    assert not Spec("patches:=abcdef").satisfies("patches:=abcdefghi")


def test_constrain_narrowing():
    s = Spec("foo=*")
    assert s.variants["foo"].type == spack.variant.VariantType.MULTI
    assert not s.variants["foo"].concrete
    s.constrain("+foo")
    assert s.variants["foo"].type == spack.variant.VariantType.BOOL
    assert s.variants["foo"].concrete

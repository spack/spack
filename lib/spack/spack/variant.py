# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""The variant module contains data structures that are needed to manage
variants both in packages and in specs.
"""

import collections.abc
import enum
import functools
import inspect
import itertools
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import spack.error
import spack.spec_parser
import spack.util.tty.color
from spack.util import lang

if TYPE_CHECKING:
    import spack.package_base
    import spack.spec

#: These are variant names used by Spack internally; packages can't use them
RESERVED_NAMES = {
    "arch",
    "architecture",
    "branch",
    "commit",
    "dev_path",
    "namespace",
    "operating_system",
    "os",
    "patches",
    "platform",
    "ref",
    "tag",
    "target",
}


class VariantType(enum.IntEnum):
    """Enum representing the three concrete variant types."""

    BOOL = 1
    SINGLE = 2
    MULTI = 3
    INDICATOR = 4  # special type for placeholder variant values

    @property
    def string(self) -> str:
        """Convert the variant type to a string."""
        if self == VariantType.BOOL:
            return "bool"
        elif self == VariantType.SINGLE:
            return "single"
        elif self == VariantType.MULTI:
            return "multi"
        else:
            return "indicator"


class Option:
    """Base class for Variant and Usage"""

    name: str
    default: Union[bool, str]
    description: str
    values: Optional[Collection]  #: if None, valid values are defined only by validators
    multi: bool
    single_value_validator: Callable
    group_validator: Optional[Callable]
    sticky: bool
    precedence: int

    def __init__(
        self,
        name: str,
        *,
        default: Union[bool, str],
        description: str,
        values: Union[Collection, Callable] = (True, False),
        multi: bool = False,
        validator: Optional[Callable] = None,
        sticky: bool = False,
        precedence: int = 0,
    ):
        """Initialize a package option.

        Args:
            name: name of the option
            default: default value for the option, used when nothing is explicitly specified
            description: purpose of the option
            values: sequence of allowed values or a callable accepting a single value as argument
                and returning True if the value is good, False otherwise
            multi: whether multiple values are allowed
            validator: optional callable that can be used to perform additional validation
            sticky: if true the option is set to the default value at concretization time
            precedence: int indicating precedence of this option definition in the solve
                (definition with highest precedence is used when multiple definitions are possible)
        """
        self.name = name
        self.default = default
        self.description = str(description)

        self.values = None
        if values == "*":
            # wildcard is a special case to make it easy to say any value is ok
            self.single_value_validator = lambda v: True

        elif isinstance(values, type):
            # supplying a type means any value *of that type*
            def isa_type(v):
                try:
                    values(v)
                    return True
                except ValueError:
                    return False

            self.single_value_validator = isa_type

        elif callable(values):
            # If 'values' is a callable, assume it is a single value
            # validator and reset the values to be explicit during debug
            self.single_value_validator = values
        else:
            # Otherwise, assume values is the set of allowed explicit values
            values = _flatten(values)
            self.values = values
            self.single_value_validator = lambda v: v in values

        self.multi = multi
        self.group_validator = validator
        self.sticky = sticky
        self.precedence = precedence

    def values_defined_by_validator(self) -> bool:
        return self.values is None

    def validate_or_raise(self, ospec: "OptionValue", pkg_name: str):
        """Validate an option spec against this package option. Raises an
        exception if any error is found.

        Args:
            ospec: option spec to be validated
            pkg_name: the name of the package class that required this validation (for errors)

        Raises:
            InconsistentValidationError: if ``ospec.name != self.name``

            MultipleValuesInExclusiveOptionError: if ``ospec`` has
                multiple values but ``self.multi == False``

            InvalidOptionValueError: if ``ospec.value`` contains
                invalid values
        """
        # Check the name of the variant
        if self.name != ospec.name:
            raise InconsistentValidationError(ospec, self)

        # If the value is exclusive there must be at most one
        value = ospec.values
        if not self.multi and len(value) != 1:
            raise MultipleValuesInExclusiveOptionError(ospec, pkg_name)

        # Check and record the values that are not allowed
        invalid_vals = ", ".join(
            f"'{v}'" for v in value if v != "*" and self.single_value_validator(v) is False
        )
        if invalid_vals:
            t_str = type(self).__name__.lower()
            raise InvalidOptionValueError(
                f"invalid values for {t_str} '{self.name}' in package {pkg_name}: {invalid_vals}\n"
            )

        # Validate the group of values if needed
        if self.group_validator is not None and value != ("*",):
            self.group_validator(pkg_name, self.name, value)

    @property
    def allowed_values(self):
        """Returns a string representation of the allowed values for
        printing purposes

        Returns:
            str: representation of the allowed values
        """
        # Join an explicit set of allowed values
        if self.values is not None:
            v = tuple(str(x) for x in self.values)
            return ", ".join(v)
        # In case we were given a single-value validator
        # print the docstring
        docstring = inspect.getdoc(self.single_value_validator)
        v = docstring if docstring else ""
        return v

    @property
    def variant_type(self) -> VariantType:
        """String representation of the type of this variant (single/multi/bool)"""
        if self.multi:
            return VariantType.MULTI
        elif self.values == (True, False):
            return VariantType.BOOL
        else:
            return VariantType.SINGLE

    def __str__(self) -> str:
        return (
            f"{type(self)}('{self.name}', "
            f"default='{self.default}', "
            f"description='{self.description}', "
            f"values={self.values}, "
            f"multi={self.multi}, "
            f"single_value_validator={self.single_value_validator}, "
            f"group_validator={self.group_validator}, "
            f"sticky={self.sticky}, "
            f"precedence={self.precedence})"
        )


class Variant(Option):
    """Represents a variant definition, created by the ``variant()`` directive.

    There can be multiple definitions of the same variant, and they are given precedence
    by order of appearance in the package. Later definitions have higher precedence.
    Similarly, definitions in derived classes have higher precedence than those in their
    superclasses.

    """

    def make_default(self) -> "VariantValue":
        """Factory that creates a variant holding the default value(s)."""
        variant = VariantValue.from_string_or_bool(self.name, self.default)
        variant.type = self.variant_type
        return variant

    def make_variant(self, *value: Union[str, bool]) -> "VariantValue":
        """Factory that creates a variant holding the value(s) passed."""
        return VariantValue(self.variant_type, self.name, value)


class Usage(Option):
    """Represents a usage definition, created by the ``usage()`` directive.

    There can be multiple definitions of the same usage, and they are given precedence
    by order of appearance in the package. Later definitions have higher precedence.
    Similarly, definitions in derived classes have higher precedence than those in their
    superclasses.
    """

    def make_default(self) -> "UsageValue":
        """Factory that creates a variant holding the default value(s)."""
        variant = UsageValue.from_string_or_bool(self.name, self.default)
        variant.type = self.variant_type
        return variant

    def make_variant(self, *value: Union[str, bool]) -> "UsageValue":
        """Factory that creates a variant holding the value(s) passed."""
        return UsageValue(self.variant_type, self.name, value)


def _flatten(values) -> Collection:
    """Flatten instances of _ConditionalVariantValues for internal representation"""
    if isinstance(values, DisjointSetsOfValues):
        return values

    flattened: List = []
    for item in values:
        if isinstance(item, ConditionalVariantValues):
            flattened.extend(item)
        else:
            flattened.append(item)
    # There are parts of the variant checking mechanism that expect to find tuples
    # here, so it is important to convert the type once we flattened the values.
    return tuple(flattened)


#: Type for value of a variant
ValueType = Tuple[Union[bool, str], ...]

#: Type of variant value when output for JSON, YAML, etc.
SerializedValueType = Union[str, bool, List[Union[str, bool]]]

OptionType = TypeVar("OptionType", bound="OptionValue")


@lang.lazy_lexicographic_ordering
class OptionValue:
    name: str
    concrete: bool
    type: VariantType
    _values: ValueType

    __slots__ = ("name", "concrete", "type", "_values")

    def __init__(
        self, type: VariantType, name: str, value: ValueType, *, concrete: bool = False
    ) -> None:
        self.name = name
        self.type = type
        # only multi-valued variants can be abstract
        self.concrete = concrete or type in (VariantType.BOOL, VariantType.SINGLE)

        # Invokes property setter
        self.set(*value)

    @classmethod
    def from_node_dict(
        cls: Type[OptionType], name: str, value: Union[str, List[str]], *, abstract: bool = False
    ) -> OptionType:
        """Reconstruct a variant from a node dict."""
        if isinstance(value, list):
            return cls(VariantType.MULTI, name, tuple(value), concrete=not abstract)

        # todo: is this necessary? not literal true / false in json/yaml?
        elif str(value).upper() == "TRUE" or str(value).upper() == "FALSE":
            return cls(VariantType.BOOL, name, (str(value).upper() == "TRUE",))

        return cls(VariantType.SINGLE, name, (value,))

    @classmethod
    def from_string_or_bool(
        cls: Type[OptionType], name: str, value: Union[str, bool], *, concrete: bool = False
    ) -> OptionType:
        if value is True or value is False:
            return cls(VariantType.BOOL, name, (value,))

        elif value.upper() in ("TRUE", "FALSE"):
            return cls(VariantType.BOOL, name, (value.upper() == "TRUE",))

        elif value == "*":
            return cls(VariantType.MULTI, name, ())

        return cls(VariantType.MULTI, name, tuple(value.split(",")), concrete=concrete)

    @classmethod
    def from_concretizer(cls: Type[OptionType], name: str, value: str, type: str) -> OptionType:
        """Reconstruct a variant from concretizer output."""
        if type == "bool":
            return cls(VariantType.BOOL, name, (value == "True",))
        elif type == "multi":
            return cls(VariantType.MULTI, name, (value,), concrete=True)
        else:
            return cls(VariantType.SINGLE, name, (value,))

    def yaml_entry(self) -> Tuple[str, SerializedValueType]:
        """Returns a (key, value) tuple suitable to be an entry in a yaml dict.

        Returns:
            tuple: (name, value_representation)
        """
        if self.type == VariantType.MULTI:
            return self.name, list(self.values)
        return self.name, self.values[0]

    @property
    def values(self) -> ValueType:
        return self._values

    @property
    def value(self) -> Union[ValueType, bool, str]:
        return self._values[0] if self.type != VariantType.MULTI else self._values

    def set(self, *value: Union[bool, str]) -> None:
        """Set the value(s) of the option."""
        if len(value) > 1:
            value = tuple(sorted(set(value)))

        if self.type != VariantType.MULTI:
            if len(value) != 1:
                raise MultipleValuesInExclusiveOptionError(self)
            unwrapped = value[0]
            if self.type == VariantType.BOOL and unwrapped not in (True, False):
                t_str = type(self).__name__.lower()
                raise ValueError(
                    f"cannot set a boolean {t_str} to a value that is not a boolean: {unwrapped}"
                )

        if "*" in value:
            raise InvalidOptionValueError("cannot use reserved value '*'")

        self._values = value

    def _cmp_iter(self) -> Iterable:
        yield self.name
        yield self.concrete
        yield from (str(v) for v in self.values)

    def copy(self: OptionType) -> OptionType:
        return type(self)(self.type, self.name, self.values, concrete=self.concrete)

    def _merged_values(self: OptionType, other: OptionType) -> Tuple[Union[str, bool], ...]:
        """The values of both sides."""
        values = (*self.values, *other.values)
        return values

    def _contains(self, value: Union[str, bool]) -> bool:
        return value in self.values

    def satisfies(self, other: "OptionValue") -> bool:
        """The lhs satisfies the rhs if all possible concretizations of lhs are also
        possible concretizations of rhs."""
        if self.name != other.name:
            return False

        if not other.concrete:
            return all(self._contains(v) for v in other.values)
        if self.concrete:
            # both concrete: they must be equal
            return self.values == other.values
        return False

    def intersects(self, other: "OptionValue") -> bool:
        """True iff there exists a concretization that satisfies both lhs and rhs."""
        if self.name != other.name:
            return False
        if self.concrete:
            if other.concrete:
                return self.values == other.values
            return all(self._contains(v) for v in other.values)
        if other.concrete:
            return all(other._contains(v) for v in self.values)
        # both abstract: the union is a valid concretization of both
        return True

    def constrain(self: OptionType, other: OptionType) -> bool:
        """Constrain self with other if they intersect. Returns true iff self was changed."""
        if not self.intersects(other):
            raise UnsatisfiableOptionSpecError(self, other)
        old_values = self.values
        self.set(*self._merged_values(other))
        changed = old_values != self.values
        if not self.concrete and other.concrete:
            self.concrete = True
            changed = True
        if self.type > other.type:
            self.type = other.type
            changed = True
        return changed

    def append(self, value: Union[str, bool]) -> None:
        self.set(*self.values, value)

    def __contains__(self, item: Union[str, bool]) -> bool:
        return item in self.values

    def __str__(self) -> str:
        # boolean variants are printed +foo or ~foo
        if self.type == VariantType.BOOL:
            sigil = "+" if self.value else "~"
            return f"{sigil}{self.name}"

        # concrete multi-valued foo:=bar,baz
        concrete = ":" if self.type == VariantType.MULTI and self.concrete else ""
        if not self.values:
            value_str = "*"
        else:
            value_str = ",".join(str(x) for x in self.values)
        return f"{self.name}{concrete}={spack.spec_parser.quote_if_needed(value_str)}"

    def __repr__(self):
        return (
            f"{type(self).__name__}({self.type!r}, {self.name!r}, {self.values!r}, "
            f"concrete={self.concrete!r})"
        )


@lang.lazy_lexicographic_ordering
class VariantValue(OptionValue):
    """A VariantValue is a key-value pair that represents a variant. It can have zero or more
    values. Values have set semantics, so they are unordered and unique. The variant type can
    be narrowed from multi to single to boolean, this limits the number of values that can be
    stored in the variant. Multi-valued variants can either be concrete or abstract: abstract
    means that the variant takes at least the values specified, but may take more when concretized.
    Concrete means that the variant takes exactly the values specified. Lastly, a variant can be
    marked as propagating, which means that it should be propagated to dependencies."""

    propagate: bool

    # _patches_in_order_of_appearance is attached to the "patches" variant after concretization
    __slots__ = (
        "name",
        "propagate",
        "concrete",
        "type",
        "_values",
        "_patches_in_order_of_appearance",
    )

    def __init__(
        self,
        type: VariantType,
        name: str,
        value: ValueType,
        *,
        propagate: bool = False,
        concrete: bool = False,
    ) -> None:
        self.propagate = propagate
        super().__init__(type, name, value, concrete=concrete)

    @classmethod
    def from_node_dict(
        cls,
        name: str,
        value: Union[str, List[str]],
        *,
        propagate: bool = False,
        abstract: bool = False,
    ) -> "VariantValue":
        """Reconstruct a variant from a node dict."""
        variantvalue = super().from_node_dict(name, value, abstract=abstract)
        variantvalue.propagate = propagate
        return variantvalue

    @classmethod
    def from_string_or_bool(
        cls, name: str, value: Union[str, bool], *, propagate: bool = False, concrete: bool = False
    ) -> "VariantValue":
        variantvalue = super().from_string_or_bool(name, value, concrete=concrete)
        variantvalue.propagate = propagate
        return variantvalue

    def _cmp_iter(self) -> Iterable:
        # Yield propagate before values)
        super_iter = super()._cmp_iter()
        yield from itertools.islice(super_iter, 2)
        yield self.propagate
        yield from super_iter

    def copy(self) -> "VariantValue":
        dup = super().copy()
        dup.propagate = self.propagate
        return dup

    def _merged_values(self, other: "VariantValue") -> Tuple[Union[str, bool], ...]:
        """The values of both sides. For patches a value identified by a checksum prefix and the
        full checksum name the same patch, so only the longer one is kept."""
        if self.name != "patches":
            return super()._merged_values(other)
        values = (*self.values, *other.values)
        return tuple(
            v
            for v in values
            if not any(
                w != v and isinstance(w, str) and isinstance(v, str) and w.startswith(v)
                for w in values
            )
        )

    def _contains(self, value: Union[str, bool]) -> bool:
        """Whether this variant covers a single value of another one. A patch is identified by a
        prefix of its checksum, so a shorter value is covered by any value starting with it.
        """
        if self.name == "patches" and isinstance(value, str):
            return any(isinstance(w, str) and w.startswith(value) for w in self.values)
        return super()._contains(value)

    def constrain(self, other: "VariantValue") -> bool:
        """Constrain self with other if they intersect. Returns true iff self was changed."""
        changed = super().constrain(other)
        if self.propagate and not other.propagate:
            self.propagate = False
            changed = True
        return changed

    def __str__(self) -> str:
        # boolean variants are printed +foo or ~foo
        if self.type == VariantType.BOOL:
            sigil = "+" if self.value else "~"
            if self.propagate:
                sigil *= 2
            return f"{sigil}{self.name}"

        # concrete multi-valued foo:=bar,baz
        concrete = ":" if self.type == VariantType.MULTI and self.concrete else ""
        delim = "==" if self.propagate else "="
        if not self.values:
            value_str = "*"
        elif self.name == "patches" and self.concrete:
            value_str = ",".join(str(x)[:7] for x in self.values)
        else:
            value_str = ",".join(str(x) for x in self.values)
        return f"{self.name}{concrete}{delim}{spack.spec_parser.quote_if_needed(value_str)}"

    def __repr__(self):
        return (
            f"VariantValue({self.type!r}, {self.name!r}, {self.values!r}, "
            f"propagate={self.propagate!r}, concrete={self.concrete!r})"
        )


class UsageValue(OptionValue):
    """A UsageValue is a key-value pair that represents a usage. It can have zero or more
    values. Values have set semantics, so they are unordered and unique. The usage type can
    be narrowed from multi to single to boolean, this limits the number of values that can be
    stored in the usage. Multi-valued usages can either be concrete or abstract: abstract
    means that the usage takes at least the values specified, but may take more when concretized.
    Concrete means that the usage takes exactly the values specified. Lastly, a usage can be
    marked as propagating, which means that it should be propagated to dependencies."""

    # currently no special logic
    pass


def MultiValuedVariant(name: str, value: ValueType, propagate: bool = False) -> VariantValue:
    return VariantValue(VariantType.MULTI, name, value, propagate=propagate, concrete=True)


def SingleValuedVariant(
    name: str, value: Union[bool, str], propagate: bool = False
) -> VariantValue:
    return VariantValue(VariantType.SINGLE, name, (value,), propagate=propagate)


def BoolValuedVariant(name: str, value: bool, propagate: bool = False) -> VariantValue:
    return VariantValue(VariantType.BOOL, name, (value,), propagate=propagate)


class VariantValueRemoval(VariantValue):
    """Indicator class for Spec.mutate to remove a variant"""

    __slots__ = ()

    def __init__(self, name):
        super().__init__(VariantType.INDICATOR, name, (None,))


# The class below inherit from Sequence to disguise as a tuple and comply
# with the semantic expected by the 'values' argument of the variant directive
class DisjointSetsOfValues(collections.abc.Sequence):
    """Allows combinations from one of many mutually exclusive sets.

    The value ``('none',)`` is reserved to denote the empty set
    and therefore no other set can contain the item ``'none'``.

    Args:
        *sets (list): mutually exclusive sets of values
    """

    _empty_set = ("none",)

    def __init__(self, *sets: Tuple[str, ...]) -> None:
        self.sets = [tuple(_flatten(x)) for x in sets]

        # 'none' is a special value and can appear only in a set of a single element
        if any("none" in s and s != self._empty_set for s in self.sets):
            raise spack.error.SpecError(
                "The value 'none' represents the empty set, and must appear alone in a set. "
                "Use the method 'allow_empty_set' to add it."
            )

        # Sets should not intersect with each other
        cumulated: Set[str] = set()
        for current_set in self.sets:
            if not cumulated.isdisjoint(current_set):
                duplicates = ", ".join(sorted(cumulated.intersection(current_set)))
                raise spack.error.SpecError(
                    f"sets in input must be disjoint, but {duplicates} appeared more than once"
                )
            cumulated.update(current_set)

        #: Attribute used to track values which correspond to
        #: features which can be enabled or disabled as understood by the
        #: package's build system.
        self.feature_values = tuple(itertools.chain.from_iterable(self.sets))
        self.default = None
        self.multi = True
        self.error_fmt = (
            "this variant accepts combinations of values from "
            "exactly one of the following sets '{values}' "
            "@*r{{[{package}, variant '{variant}']}}"
        )

    def with_default(self, default):
        """Sets the default value and returns self."""
        self.default = default
        return self

    def with_error(self, error_fmt):
        """Sets the error message format and returns self."""
        self.error_fmt = error_fmt
        return self

    def with_non_feature_values(self, *values):
        """Marks a few values as not being tied to a feature."""
        self.feature_values = tuple(x for x in self.feature_values if x not in values)
        return self

    def allow_empty_set(self):
        """Adds the empty set to the current list of disjoint sets."""
        if self._empty_set in self.sets:
            return self

        # Create a new object to be returned
        object_with_empty_set = type(self)(("none",), *self.sets)
        object_with_empty_set.error_fmt = self.error_fmt
        object_with_empty_set.feature_values = self.feature_values + ("none",)
        return object_with_empty_set

    def prohibit_empty_set(self):
        """Removes the empty set from the current list of disjoint sets."""
        if self._empty_set not in self.sets:
            return self

        # Create a new object to be returned
        sets = [s for s in self.sets if s != self._empty_set]
        object_without_empty_set = type(self)(*sets)
        object_without_empty_set.error_fmt = self.error_fmt
        object_without_empty_set.feature_values = tuple(
            x for x in self.feature_values if x != "none"
        )
        return object_without_empty_set

    def __iter__(self):
        return itertools.chain.from_iterable(self.sets)

    def __getitem__(self, idx):
        return tuple(itertools.chain.from_iterable(self.sets))[idx]

    def __len__(self):
        return sum(len(x) for x in self.sets)

    @property
    def validator(self):
        def _disjoint_set_validator(pkg_name, variant_name, values):
            # If for any of the sets, all the values are in it return True
            if any(all(x in s for x in values) for s in self.sets):
                return

            format_args = {"variant": variant_name, "package": pkg_name, "values": values}
            msg = self.error_fmt + " @*r{{[{package}, variant '{variant}']}}"
            msg = spack.util.tty.color.colorize(msg.format(**format_args))
            raise spack.error.SpecError(msg)

        return _disjoint_set_validator


def _a_single_value_or_a_combination(single_value: str, *values: str) -> DisjointSetsOfValues:
    error = f"the value '{single_value}' is mutually exclusive with any of the other values"
    return (
        DisjointSetsOfValues((single_value,), values)
        .with_default(single_value)
        .with_error(error)
        .with_non_feature_values(single_value)
    )


# TODO: The factories below are used by package writers to set values of
# TODO: multi-valued variants. It could be worthwhile to gather them in
# TODO: a common namespace (like 'multi') in the future.


def any_combination_of(*values: str) -> DisjointSetsOfValues:
    """Multi-valued variant that allows either any combination of the specified values, or none
    at all (using ``variant=none``). The literal value ``none`` is used as sentinel for the empty
    set, since in the spec DSL we have to always specify a value for a variant.

    It is up to the package implementation to handle the value ``none`` specially, if at all.

    See also :func:`auto_or_any_combination_of` and :func:`disjoint_sets`.

    Args:
        *values: allowed variant values

    Example::

        variant("cuda_arch", values=any_combination_of("10", "11"))

    Returns:
        a properly initialized instance of :class:`~spack.variant.DisjointSetsOfValues`
    """
    return _a_single_value_or_a_combination("none", *values)


def auto_or_any_combination_of(*values: str) -> DisjointSetsOfValues:
    """Multi-valued variant that allows any combination of a set of values (but not the empty set)
    or ``auto``.

    See also :func:`any_combination_of` and :func:`disjoint_sets`.

    Args:
        *values: allowed variant values

    Example::

       variant(
           "file_systems",
           values=auto_or_any_combination_of("lustre", "gpfs", "nfs", "ufs"),
       )

    Returns:
        a properly initialized instance of :class:`~spack.variant.DisjointSetsOfValues`
    """
    return _a_single_value_or_a_combination("auto", *values)


def disjoint_sets(*sets: Tuple[str, ...]) -> DisjointSetsOfValues:
    """Multi-valued variant that allows any combination picking from one of multiple disjoint sets
    of values, and also allows the user to specify ``none`` to choose none of them.

    It is up to the package implementation to handle the value ``none`` specially, if at all.

    See also :func:`any_combination_of` and :func:`auto_or_any_combination_of`.

    Args:
        *sets: sets of allowed values, each set is a tuple of strings

    Returns:
        a properly initialized instance of :class:`~spack.variant.DisjointSetsOfValues`
    """
    return DisjointSetsOfValues(*sets).allow_empty_set().with_default("none")


@functools.total_ordering
class ConditionalValue:
    """Conditional value for a variant."""

    value: Any

    # optional because statically disabled values (when=False) are set to None
    # when=True results in spack.spec.Spec()
    when: Optional["spack.spec.Spec"]

    def __init__(self, value: Any, when: Optional["spack.spec.Spec"]):
        self.value = value
        self.when = when

    def __repr__(self):
        return f"ConditionalValue({self.value}, when={self.when})"

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        # Needed to allow testing the presence of a variant in a set by its value
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, (str, bool)):
            return self.value == other
        return self.value == other.value

    def __lt__(self, other):
        if isinstance(other, str):
            return self.value < other
        return self.value < other.value


def prevalidate_variant_value(
    pkg_cls: "Type[spack.package_base.PackageBase]",
    variant: VariantValue,
    spec: Optional["spack.spec.Spec"] = None,
    strict: bool = False,
) -> List[Variant]:
    """Do as much validation of a variant value as is possible before concretization.

    This checks that the variant value is valid for *some* definition of the variant, and
    it raises if we know *before* concretization that the value cannot occur. On success
    it returns the variant definitions for which the variant is valid.

    Arguments:
        pkg_cls: package in which variant is (potentially multiply) defined
        variant: variant spec with value to validate
        spec: optionally restrict validation only to variants defined for this spec
        strict: if True, raise an exception if no variant definition is valid for any
            constraint on the spec.

    Return:
        list of variant definitions that will accept the given value. List will be empty
        only if the variant is a reserved variant.
    """
    # do not validate non-user variants or optional variants
    if variant.name in RESERVED_NAMES or variant.propagate:
        return []

    # raise if there is no definition at all
    if not pkg_cls.has_variant(variant.name):
        raise UnknownVariantError(
            f"No such variant '{variant.name}' in package {pkg_cls.name}", [variant.name]
        )

    # do as much prevalidation as we can -- check only those
    # variants whose when constraint intersects this spec
    errors = []
    possible_definitions = []
    valid_definitions = []

    for when, pkg_variant_def in pkg_cls.variant_definitions(variant.name):
        if spec and not spec.intersects(when):
            continue
        possible_definitions.append(pkg_variant_def)

        try:
            pkg_variant_def.validate_or_raise(variant, pkg_cls.name)
            valid_definitions.append(pkg_variant_def)
        except spack.error.SpecError as e:
            errors.append(e)

    # value is valid for at least one definition -- return them all
    if valid_definitions:
        return valid_definitions

    # no when spec intersected, so no possible definition for the variant in this configuration
    if strict and not possible_definitions:
        when_clause = f" when {spec}" if spec else ""
        raise InvalidOptionValueError(
            f"variant '{variant.name}' does not exist for '{pkg_cls.name}'{when_clause}"
        )

    # There are only no errors if we're not strict and there are no possible_definitions.
    # We are strict for audits but not for specs on the CLI or elsewhere. Being strict
    # in these cases would violate our rule of being able to *talk* about any configuration,
    # regardless of what the package.py currently says.
    if not errors:
        return []

    # if there is just one error, raise the specific error
    if len(errors) == 1:
        raise errors[0]

    # otherwise combine all the errors and raise them together
    raise InvalidOptionValueError("multiple variant issues:", "\n".join(e.message for e in errors))


class ConditionalVariantValues(lang.TypedMutableSequence):
    """A list, just with a different type"""


class DuplicateOptionError(spack.error.SpecError):
    """Raised when the same variant or usage occurs in a spec twice."""


class UnknownVariantError(spack.error.SpecError):
    """Raised when an unknown variant occurs in a spec."""

    def __init__(self, msg: str, unknown_variants: List[str]):
        super().__init__(msg)
        self.unknown_variants = unknown_variants


class InconsistentValidationError(spack.error.SpecError):
    """Raised if the wrong validator is used to validate a variant."""

    def __init__(self, vspec, variant):
        msg = 'trying to validate variant "{0.name}" with the validator of "{1.name}"'
        super().__init__(msg.format(vspec, variant))


class MultipleValuesInExclusiveOptionError(spack.error.SpecError, ValueError):
    """Raised when multiple values are present in a variant that wants
    only one.
    """

    def __init__(self, option: OptionValue, pkg_name: Optional[str] = None):
        pkg_info = "" if pkg_name is None else f" in package '{pkg_name}'"
        type_str = type(option).__name__
        msg = f"multiple values are not allowed for {type_str} '{option.name}'{pkg_info}"
        super().__init__(msg)


class InvalidOptionValueError(spack.error.SpecError):
    """Raised when variants have invalid values."""


class UnsatisfiableOptionSpecError(spack.error.UnsatisfiableSpecError):
    """Raised when a spec variant conflicts with package constraints."""

    def __init__(self, provided, required):
        super().__init__(provided, required, type(self).__name__.lower())

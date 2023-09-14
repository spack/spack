# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Data structures that represent Spack's edge types."""

from typing import List, Tuple, Union

#: Type hint for the low-level dependency input (enum.Flag is too slow)
DepFlag = int

#: Type hint for the high-level dependency input
DepTypes = Union[str, List[str], Tuple[str, ...]]

#: Individual dependency types that make up CanonicalDepTypes
DepType = str  # Python 3.8: Literal["build", "link", "run", "test"]

#: Canonical dependency types
CanonicalDepTypes = Tuple[DepType, ...]

# Flag values. NOTE: these values are not arbitrary, since hash computation imposes
# the order (link, run, build, test) when depending on the same package multiple times,
# and we rely on default integer comparison to sort dependency types.
# New dependency types should be appended.
LINK = 0b0001
RUN = 0b0010
BUILD = 0b0100
TEST = 0b1000

#: The types of dependency relationships that Spack understands.
all_types: CanonicalDepTypes = ("build", "link", "run", "test")

#: An iterator of all dependency types
flag_iterator: Tuple[DepFlag, DepFlag, DepFlag, DepFlag] = (BUILD, LINK, RUN, TEST)

#: A flag with all dependency types set
all_flag = BUILD | LINK | RUN | TEST

#: Default dependency type if none is specified
default_deptype: CanonicalDepTypes = ("build", "link")

#: Default dependency type if none is specified
default_deptype_flag: DepFlag = BUILD | LINK


def flag_from_string(s: str) -> DepFlag:
    if s == "build":
        return BUILD
    elif s == "link":
        return LINK
    elif s == "run":
        return RUN
    elif s == "test":
        return TEST
    else:
        raise ValueError(f"Invalid dependency type: {s}")


def type_to_flag(deptype: CanonicalDepTypes) -> DepFlag:
    """Take a canonical deptype tuple and return a DepFlag."""
    flag = 0
    for deptype_str in deptype:
        flag |= flag_from_string(deptype_str)
    return flag


def flag_to_types(x: DepFlag) -> CanonicalDepTypes:
    deptype: List[DepType] = []
    if x & BUILD:
        deptype.append("build")
    if x & LINK:
        deptype.append("link")
    if x & RUN:
        deptype.append("run")
    if x & TEST:
        deptype.append("test")
    return tuple(deptype)


def flag_to_type(x: DepFlag) -> DepType:
    if x == BUILD:
        return "build"
    elif x == LINK:
        return "link"
    elif x == RUN:
        return "run"
    elif x == TEST:
        return "test"
    else:
        raise ValueError(f"Invalid dependency type flag: {x}")


def canonicalize(deptype: DepTypes) -> DepFlag:
    """Convert deptype user input to a DepFlag, or raise ValueError.

    Args:
        deptype: string representing dependency type, or a list/tuple of such strings.
            Can also be the builtin function ``all`` or the string 'all', which result in
            a tuple of all dependency types known to Spack.
    """
    if deptype in ("all", all):
        return all_flag

    if isinstance(deptype, str):
        return flag_from_string(deptype)

    if isinstance(deptype, (tuple, list, set)):
        flag = 0
        for t in deptype:
            flag |= flag_from_string(t)
        return flag

    raise ValueError(f"Invalid dependency type: {deptype!r}")


def flag_to_chars(depflag: DepFlag) -> str:
    """Create a string representing deptypes for many dependencies.

    The string will be some subset of 'blrt', like 'bl ', 'b t', or
    ' lr ' where each letter in 'blrt' stands for 'build', 'link',
    'run', and 'test' (the dependency types).

    For a single dependency, this just indicates that the dependency has
    the indicated deptypes. For a list of dependnecies, this shows
    whether ANY dpeendency in the list has the deptypes (so the deptypes
    are merged)."""
    return "".join(
        t_str[0] if t_flag & depflag else " " for t_str, t_flag in zip(all_types, flag_iterator)
    )

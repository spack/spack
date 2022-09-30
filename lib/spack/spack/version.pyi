# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import (  # novm
    Any,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import overload

from six import add_metaclass

import spack.error


infinity_versions: List[str]


_ComparedTo = TypeVar('_ComparedTo')


# NB: we want to have nice types (e.g. with the use of Generic) for these abstract classes, so we
# define their types here, but we *also* define the same abstract base classes in version.py,
# *without* any parameterized types. The stronger types in this .pyi file will be consumed by mypy
# when type checking *other* files, but we still want to actually ensure that all the
# abstractmethods are implemented within version.py itself! Mirroring these abstract base classes
# without the type signatures in version.py ensures we get the runtime checking of whether methods
# are implemented that ABCMeta has always provided.
@add_metaclass(ABCMeta)
class Comparable(Generic[_ComparedTo]):

    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...

    def __ne__(self, other: Any) -> bool: ...

    @abstractmethod
    def __lt__(self, other: _ComparedTo) -> bool: ...

    def __le__(self, other: _ComparedTo) -> bool: ...

    @abstractmethod
    def __gt__(self, other: _ComparedTo) -> bool: ...

    def __ge__(self, other: _ComparedTo) -> bool: ...


_SingleElement = TypeVar('_SingleElement')


@add_metaclass(ABCMeta)
class Extrema(Generic[_SingleElement]):

    @abstractmethod
    def lowest(self) -> Optional[_SingleElement]: ...

    @abstractmethod
    def highest(self) -> Optional[_SingleElement]: ...

    @abstractproperty
    def concrete(self) -> Optional[_SingleElement]: ...


_Joined = TypeVar('_Joined')


@add_metaclass(ABCMeta)
class Interval(Generic[_ComparedTo, _Joined]):

    @abstractmethod
    def __contains__(self, other: _ComparedTo) -> bool: ...

    @abstractmethod
    def satisfies(self, other: _ComparedTo, strict: bool) -> bool: ...

    @abstractmethod
    def overlaps(self, other: _ComparedTo) -> bool: ...

    @abstractmethod
    def union(self, other: _ComparedTo) -> _Joined: ...

    @abstractmethod
    def intersection(self, other: _ComparedTo) -> _Joined: ...


@add_metaclass(ABCMeta)
class Point(Generic[_ComparedTo]):

    @abstractmethod
    def is_predecessor(self, other: _ComparedTo) -> bool: ...

    def is_successor(self, other: _ComparedTo) -> bool: ...


_Self = TypeVar('_Self')


@add_metaclass(ABCMeta)
class Serializable(object):

    @classmethod
    @abstractmethod
    def parse(cls: Type[_Self], string: str) -> _Self: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool: ...

    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...


class VersionStrComponent(Serializable, Comparable[Union[VersionStrComponent, int, str]]):
    inf_ver: Optional[int]
    data: str

    # @abstractmethod impls from abstract parent classes:
    @classmethod
    def parse(cls: Type[_Self], string: str) -> _Self: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: Any) -> bool: ...

    def __str__(self) -> str: ...

    def __lt__(self, other: Union[VersionStrComponent, int, str]) -> bool: ...

    def __gt__(self, other: Union[VersionStrComponent, int, str]) -> bool: ...

    # Concrete methods defined and implemented in this class:
    def __init__(self, string: str) -> None: ...


def Version(string: Union[str, GitVersion, VersionBase]) -> Union[GitVersion, VersionBase]: ...


class VersionBase(
    Comparable[VersionBase],
    Extrema[VersionBase],
    Interval[VersionBase, Union[VersionBase, VersionList]],
    Point[VersionBase],
    Serializable,
):

    version: Tuple[Union[int, VersionStrComponent], ...]
    separators: Tuple[str, ...]
    string: str

    # @abstractmethod impls from abstract parent classes:
    @classmethod
    def parse(cls: Type[_Self], string: str) -> _Self: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: Any) -> bool: ...

    def __str__(self) -> str: ...

    def __lt__(self, other: VersionBase) -> bool: ...

    def __gt__(self, other: VersionBase) -> bool: ...

    def lowest(self: _Self) -> _Self: ...

    def highest(self: _Self) -> _Self: ...

    @property
    def concrete(self: _Self) -> _Self: ...

    def __contains__(self, other: VersionBase) -> bool: ...

    def satisfies(self, other: VersionBase, strict: bool = False) -> bool: ...

    def overlaps(self, other: VersionBase) -> bool: ...

    def union(self, other: VersionBase) -> Union[VersionBase, VersionList]: ...

    def intersection(self, other: VersionBase) -> Union[VersionBase, VersionList]: ...

    def is_predecessor(self, other: VersionBase) -> bool: ...

    def is_successor(self, other: VersionBase) -> bool: ...

    # Concrete methods defined and implemented in this class:
    def __init__(self, string: str) -> None: ...

    @property
    def dotted(self: _Self) -> _Self: ...

    @property
    def underscored(self: _Self) -> _Self: ...

    @property
    def dashed(self: _Self) -> _Self: ...

    @property
    def joined(self: _Self) -> _Self: ...

    def up_to(self: _Self, index: int) -> _Self: ...

    def isdevelop(self) -> bool: ...

    def __iter__(self) -> Iterator[VersionStrComponent]: ...

    def __len__(self) -> int: ...

    @overload
    def __getitem__(self, idx: int) -> Union[int, VersionStrComponent]: ...

    @overload
    def __getitem__(self: _Self, idx: slice) -> _Self: ...

    def __format__(self, format_spec: str) -> str: ...


class GitVersion(VersionBase):

    user_supplied_reference: bool
    _ref_lookup: Optional[CommitLookup]
    ref_version: Optional[Tuple[VersionStrComponent, ...]]
    ref: Optional[str]
    ref_version_str: Optional[str]
    is_commit: bool
    is_ref: bool

    @property
    def ref_lookup(self) -> Optional[str]: ...

    def generate_git_lookup(self, pkg_name: str) -> None: ...

    def __init__(self, string: Union[str, VersionBase, GitVersion]) -> None: ...


class CommitLookup(object):

    pkg_name: str
    data: Dict[str, str]

    def __init__(self, pkg_name: str) -> None: ...

    def get(self, ref: str) -> str: ...


class VersionRange(
    Comparable[VersionRange],
    Extrema[VersionBase],
    Interval[VersionRange, Union[VersionRange, VersionList]],
    Serializable,
):

    start: VersionBase
    end: VersionBase

    # @abstractmethod impls from abstract parent classes:
    @classmethod
    def parse(cls: Type[_Self], string: str) -> _Self: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: Any) -> bool: ...

    def __str__(self) -> str: ...

    def __lt__(self, other: VersionRange) -> bool: ...

    def __gt__(self, other: VersionRange) -> bool: ...

    def lowest(self) -> Optional[VersionBase]: ...

    def highest(self) -> Optional[VersionBase]: ...

    @property
    def concrete(self) -> Optional[VersionBase]: ...

    def __contains__(self, other: VersionRange) -> bool: ...

    def satisfies(self, other: VersionRange, strict: bool = False) -> bool: ...

    def overlaps(self, other: VersionRange) -> bool: ...

    def union(self, other: VersionRange) -> Union[VersionRange, VersionList]: ...

    def intersection(self, other: VersionRange) -> Union[VersionRange, VersionList]: ...

    # Concrete methods defined and implemented in this class:
    def __init__(
        self,
        start: Optional[Union[str, VersionBase]],
        end: Optional[Union[str, VersionBase]],
    ) -> None: ...


_AllVersionTypes = Union[VersionList, VersionBase, GitVersion, VersionRange]


class VersionList(
    Comparable[VersionList],
    Extrema[VersionBase],
    Interval[VersionList, VersionList],
    Serializable,
):

    versions: List[Union[VersionBase, GitVersion, VersionRange]]

    # @abstractmethod impls from abstract parent classes:
    @classmethod
    def parse(cls: Type[_Self], string: str) -> _Self: ...

    def __hash__(self) -> int: ...

    def __eq__(self, other: Any) -> bool: ...

    def __str__(self) -> str: ...

    def __lt__(self, other: VersionList) -> bool: ...

    def __gt__(self, other: VersionList) -> bool: ...

    def lowest(self) -> Optional[VersionBase]: ...

    def highest(self) -> Optional[VersionBase]: ...

    @property
    def concrete(self) -> Optional[VersionBase]: ...

    def __contains__(self, other: VersionList) -> bool: ...

    def satisfies(self, other: VersionList, strict: bool = False) -> bool: ...

    def overlaps(self, other: VersionList) -> bool: ...

    def union(self, other: VersionList) -> VersionList: ...

    def intersection(self, other: VersionList) -> VersionList: ...

    # Concrete methods defined and implemented in this class:
    def __init__(self, vlist: Optional[Union[str, Iterable[Any]]] = None) -> None: ...

    def add(self, version: _AllVersionTypes) -> None: ...

    def update(self, other: VersionList) -> None: ...

    def copy(self: _Self) -> _Self: ...

    def highest_numeric(self) -> Optional[VersionBase]: ...

    def preferred(self) -> Optional[VersionBase]: ...

    def to_dict(self) -> Dict[str, Union[str, List[str]]]: ...

    @classmethod
    def from_dict(cls: Type[_Self], dictionary: Dict[str, Union[str, List[str]]]) -> _Self: ...

    def __getitem__(self, index: int) -> Union[VersionBase, VersionRange]: ...

    def __iter__(self) -> Iterator[Union[VersionBase, VersionRange]]: ...

    def __reversed__(self) -> Iterator[Union[VersionBase, VersionRange]]: ...

    def __len__(self) -> int: ...

    def __bool__(self) -> bool: ...


@overload
def ver(obj: Union[List[Any], Tuple[Any, ...]]) -> VersionList: ...

@overload
def ver(obj: str) -> _AllVersionTypes: ...

@overload
def ver(obj: Union[int, float]) -> VersionBase: ...


class VersionError(spack.error.SpackError): ...


class VersionChecksumError(VersionError): ...

class VersionLookupError(VersionError): ...

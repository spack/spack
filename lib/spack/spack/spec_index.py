# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import time
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import (Any, ClassVar, Dict, FrozenSet, Iterable, Iterator, List,  # novm
                    Optional, Union)                                           # novm

from six import add_metaclass

from llnl.util.lang import key_ordering, memoized

import spack.spec


@key_ordering
class InstallStatus(object):
    _known_statuses = [
        'INSTALLED',
        'DEPRECATED',
        'MISSING',
    ]                                                       # type: ClassVar[List[str]]

    status = None                                           # type: str

    def __init__(self, status):
        # type: (str) -> None
        assert status in self._known_statuses, (status, self._known_statuses)
        self.status = status

    def _cmp_key(self):
        return (type(self), self.status)

    @classmethod
    def INSTALLED(cls):
        # type: () -> InstallStatus
        return cls('INSTALLED')

    @classmethod
    def DEPRECATED(cls):
        # type: () -> InstallStatus
        return cls('DEPRECATED')

    @classmethod
    def MISSING(cls):
        # type: () -> InstallStatus
        return cls('MISSING')

    @classmethod
    def all_values(cls):
        # type: () -> Iterable[InstallStatus]
        return [cls(st) for st in cls._known_statuses]

    def __repr__(self):
        return '{0}(status={1!r})'.format(type(self).__name__, self.status)


class InstallStatuses(object):
    statuses = None                                     # type: FrozenSet[InstallStatus]

    def __repr__(self):
        return '{0}(statuses={1!r})'.format(type(self).__name__, self.statuses)

    def __init__(self, statuses):
        # type: (Iterable[InstallStatus]) -> None
        self.statuses = frozenset(statuses)

    def __contains__(self, other):
        # type: (InstallStatus) -> bool
        return other in self.statuses

    @classmethod
    @memoized
    def any_status(cls):
        # type: () -> InstallStatuses
        return cls(InstallStatus.all_values())

    def satisfies_install_statuses(self, other):
        # type: (InstallStatuses) -> bool
        return not bool(other.statuses - self.statuses)

    @classmethod
    def canonical_statuses(cls, query_arg):
        # type: (Any) -> InstallStatuses
        if isinstance(query_arg, InstallStatuses):
            return query_arg
        return cls(cls._canonicalize(query_arg))

    @classmethod
    def _canonicalize(cls, query_arg):
        # type: (Any) -> Iterable[InstallStatus]
        if query_arg is True:
            return [InstallStatus.INSTALLED()]
        elif query_arg is False:
            return [InstallStatus.MISSING()]
        elif query_arg is any:
            return list(InstallStatus.all_values())
        elif isinstance(query_arg, InstallStatus):
            return [query_arg]
        else:
            try:  # Try block catches if it is not an iterable at all
                query_arg = list(query_arg)
                if any(type(x) != InstallStatus for x in query_arg):
                    raise TypeError
            except TypeError:
                raise TypeError(
                    'installation query must be `any`, boolean, '
                    'InstallStatus, or iterable of InstallStatus. was: {0}'
                    .format(query_arg))
            return query_arg


def now():
    # type: () -> float
    """Returns the time since the epoch"""
    return time.time()


class InstallRecord(object):
    """A record represents one installation in the DB.

    The record keeps track of the spec for the installation, its
    install path, AND whether or not it is installed.  We need the
    installed flag in case a user either:

        a) blew away a directory, or
        b) used spack uninstall -f to get rid of it

    If, in either case, the package was removed but others still
    depend on it, we still need to track its spec, so we don't
    actually remove from the database until a spec has no installed
    dependents left.

    Args:
        spec (spack.spec.Spec): spec tracked by the install record
        path (str): path where the spec has been installed
        installed (bool): whether or not the spec is currently installed
        ref_count (int): number of specs that depend on this one
        explicit (bool, optional): whether or not this spec was explicitly
            installed, or pulled-in as a dependency of something else
        installation_time (time, optional): time of the installation
    """
    include_fields = ['spec', 'path', 'installed', 'ref_count', 'explicit',
                      'installation_time', 'deprecated_for',
                      ]                                     # type: ClassVar[List[str]]

    spec = None                                             # type: spack.spec.Spec
    path = None                                             # type: Optional[str]
    installed = None                                        # type: bool
    ref_count = None                                        # type: int
    explicit = None                                         # type: bool
    installation_time = None                                # type: float
    deprecated_for = None                                   # type: Optional[str]

    def __init__(self, spec, path, installed, ref_count=0, explicit=False,
                 installation_time=None, deprecated_for=None):
        # type: (spack.spec.Spec, Optional[str], bool, int, bool, float, Optional[str]) -> None # noqa
        self.spec = spec
        self.path = str(path) if path else None
        self.installed = installed
        self.ref_count = ref_count
        self.explicit = explicit
        self.installation_time = installation_time or now()
        self.deprecated_for = deprecated_for

    def __repr__(self):
        return (
            '{0}(spec={1!r}, path={2!r}, installed={3!r}, ref_count={4!r}, '
            'explicit={5!r}, installation_time={6!r}, deprecated_for={7!r})'
        ).format(type(self).__name__, self.spec, self.path, self.installed,
                 self.ref_count, self.explicit, self.installation_time,
                 self.deprecated_for)

    def install_type_matches(self, installed):
        # type: (Any) -> bool
        installed = InstallStatuses.canonical_statuses(installed)
        if self.installed:
            return InstallStatus.INSTALLED() in installed
        elif self.deprecated_for:
            return InstallStatus.DEPRECATED() in installed
        else:
            return InstallStatus.MISSING() in installed

    def to_dict(self, include_fields=None):
        # type: (Optional[Iterable[str]]) -> Dict
        if include_fields is None:
            include_fields = self.include_fields
        rec_dict = {}

        for field_name in include_fields:
            if field_name == 'spec':
                rec_dict.update({'spec': self.spec.node_dict_with_hashes()})
            elif field_name == 'deprecated_for' and self.deprecated_for:
                rec_dict.update(
                    {'deprecated_for': self.deprecated_for})
            else:
                rec_dict.update({field_name: getattr(self, field_name)})

        return rec_dict

    @classmethod
    def from_dict(cls, spec, dictionary):
        # type: (spack.spec.Spec, Dict) -> InstallRecord
        d = dict(dictionary.items())
        d.pop('spec', None)

        # Old databases may have "None" for path for externals
        if 'path' not in d or d['path'] == 'None':
            d['path'] = None

        if 'installed' not in d:
            d['installed'] = False

        return cls(spec, **d)


@key_ordering
class ConcretizedSpec(object):
    spec = None  # type: spack.spec.Spec

    def __init__(self, spec):
        # type: (spack.spec.Spec) -> None
        if not spec.concrete:
            raise TypeError('spec given to {0} must be fully concrete! was: {1}'
                            .format(type(self).__name__, spec))
        self.spec = spec

    @classmethod
    def from_abstract_spec(cls, spec):
        # type: (spack.spec.Spec) -> ConcretizedSpec
        return cls(spec.concretized())

    @classmethod
    def from_hash(cls, hash_str):
        # type: (str) -> ConcretizedSpec
        return cls.from_abstract_spec(spack.spec.Spec(full_hash=hash_str))

    def _cmp_key(self):
        return self.spec._cmp_key()

    def into_hash(self):
        # type: () -> ConcreteHash
        return ConcreteHash(self.spec.dag_hash())

    @property
    def spec_string_name_hash_only(self):
        # type: () -> str
        return '{0}/{1}'.format(self.spec.name, self.into_hash().complete_hash)

    def __repr__(self):
        return '{0}(spec={1!r})'.format(type(self).__name__, self.spec)


class IndexEntry(object):
    concretized_spec = None  # type: ConcretizedSpec
    record = None            # type: InstallRecord

    def __init__(self, concretized_spec, record):
        # type: (ConcretizedSpec, InstallRecord) -> None
        self.concretized_spec = concretized_spec
        self.record = record

    def __repr__(self):
        return '{0}(concretized_spec={1!r}, record={2!r})'.format(
            type(self).__name__, self.concretized_spec, self.record)


@add_metaclass(ABCMeta)
class PartialHash(object):
    FULL_HASH_STRING_LENGTH = 32  # type: ClassVar[int]

    @abstractproperty
    def hash_prefix(self):
        # type: () -> str
        pass

    def __contains__(self, other):
        # type: (PartialHash) -> bool
        return other.hash_prefix.startswith(self.hash_prefix)


@key_ordering
class HashPrefix(PartialHash):
    hash_prefix = None            # type: str

    def __init__(self, hash_prefix):
        # type: (str) -> None
        assert len(hash_prefix) <= self.FULL_HASH_STRING_LENGTH, (
            hash_prefix, self.FULL_HASH_STRING_LENGTH,
        )
        self.hash_prefix = hash_prefix.lower()

    def _cmp_key(self):
        return (self.hash_prefix,)

    def __repr__(self):
        return '{0}(hash_prefix={1!r})'.format(type(self).__name__, self.hash_prefix)


class CompleteHash(PartialHash):
    @abstractproperty
    def complete_hash(self):
        # type: () -> str
        pass


@key_ordering
class ConcreteHash(CompleteHash):
    complete_hash = None  # type: str

    def __init__(self, complete_hash):
        # type: (str) -> None
        assert len(complete_hash) == self.FULL_HASH_STRING_LENGTH, (
            complete_hash, self.FULL_HASH_STRING_LENGTH,
        )
        self.complete_hash = complete_hash.lower()

    def _cmp_key(self):
        return (self.complete_hash,)

    @property
    def hash_prefix(self):
        # type: () -> str
        return self.complete_hash

    def as_abstract_spec(self):
        # type: () -> spack.spec.Spec
        return spack.spec.Spec('/{0}'.format(self.complete_hash))

    def __repr__(self):
        return '{0}(complete_hash={1!r})'.format(
            type(self).__name__, self.complete_hash)


class IndexQuery(object):
    query_specs = None   # type: Optional[List[spack.spec.Spec]]
    known = None         # type: Optional[bool]
    installed = None     # type: InstallStatuses
    explicit = None      # type: Optional[bool]
    start_date = None    # type: Optional[float]
    end_date = None      # type: Optional[float]
    hashes = None        # type: Optional[List[str]]
    for_all_architectures = None                            # type: bool

    def __repr__(self):
        return (
            '{0}(query_specs={1!r}, known={2!r}, installed={3!r}, explicit={4!r}, '
            'start_date={5!r}, end_date={6!r}, hashes={7!r}, '
            'for_all_architectures={8!r})').format(
                type(self).__name__, self.query_specs, self.known, self.installed,
                self.explicit, self.start_date, self.end_date, self.hashes,
                self.for_all_architectures)

    def __init__(
            self,
            query_specs=None,  # type: Optional[Union[spack.spec.Spec, List[spack.spec.Spec]]] # noqa
            known=None,        # type: Optional[bool]
            installed=True,    # type: Any
            explicit=None,     # type: Optional[bool]
            start_date=None,   # type: Optional[float]
            end_date=None,     # type: Optional[float]
            hashes=None,       # type: Optional[List[str]]
            for_all_architectures=False,                    # type: bool
    ):
        if isinstance(query_specs, spack.spec.Spec):
            query_specs = [query_specs]
        self.query_specs = query_specs
        self.known = known
        self.installed = InstallStatuses.canonical_statuses(installed)
        self.explicit = explicit
        self.start_date = start_date
        self.end_date = end_date
        self.hashes = hashes
        self.for_all_architectures = for_all_architectures

    @classmethod
    def from_query_args(cls, **kwargs):
        # type: (Any) -> IndexQuery
        for field, value in kwargs.items():
            if value is any:
                kwargs[field] = None
        kwargs['query_specs'] = kwargs.pop('query_spec', None)
        return cls(**kwargs)

    def to_query_args(self):
        # type: () -> Dict
        return dict(
            query_spec=self.query_specs or any,
            known=(self.known is not None) or any,
            installed=self.installed,
            explicit=(self.explicit is not None) or any,
            start_date=self.start_date,
            end_date=self.end_date,
            hashes=self.hashes,
            for_all_architectures=self.for_all_architectures,
        )


@add_metaclass(ABCMeta)
class SpecIndexable(object):
    """Interface to look up and traverse known specs from multiple sources."""

    @abstractmethod
    def spec_index_lookup(self, hash_prefix):
        # type: (PartialHash) -> Iterator[IndexEntry]
        pass

    @abstractmethod
    def spec_index_query(self, query):
        # type: (IndexQuery) -> Iterator[ConcretizedSpec]
        pass


class SpecIndex(object):
    """A merged database spanning several SpecIndexable instances."""
    indices = None                                          # type: List[SpecIndexable]

    @classmethod
    def _local_db(cls):
        import spack.store
        return spack.store.db.instance

    @classmethod
    @memoized
    def with_local_db(cls):
        # type: () -> SpecIndex
        return cls([cls._local_db()])

    @classmethod
    def _remote_db(cls):
        import spack.binary_distribution
        return (
            spack.binary_distribution.BinaryCacheIndex.with_spack_configured_mirrors())

    @classmethod
    @memoized
    def with_remote_db(cls):
        # type: () -> SpecIndex
        return cls([cls._remote_db()])

    @classmethod
    @memoized
    def with_local_and_remote_dbs(cls):
        # type: () -> SpecIndex
        return cls([cls._local_db(), cls._remote_db()])

    def __init__(self, indices):
        # type: (List[SpecIndexable]) -> None
        self.indices = indices

    def lookup(self, hash_prefix):
        # type: (PartialHash) -> Iterator[IndexEntry]
        for index in self.indices:
            for entry in index.spec_index_lookup(hash_prefix):
                yield entry

    def lookup_ensuring_single_match(self, hash_prefix):
        # type: (PartialHash) -> IndexEntry
        # (1) Deduplicate results by their dag_hash:
        matching_specs = tuple(dict(
            (entry.concretized_spec.into_hash(), entry)
            for entry in self.lookup(hash_prefix)
        ).values())
        # (2) Error if more than one concrete spec matches the prefix:
        prefix_str = hash_prefix.hash_prefix
        if not matching_specs:
            raise spack.spec.NoSuchHashError(prefix_str)
        if len(matching_specs) > 1:
            raise spack.spec.AmbiguousHashError(
                "Multiple packages specify hash beginning '{0}'.".format(prefix_str),
                *matching_specs)
        # (3) Return the single result.
        return matching_specs[0]

    def query(self, query):
        # type: (IndexQuery) -> Iterator[ConcretizedSpec]
        for index in self.indices:
            for result in index.spec_index_query(query):
                yield result

    def __repr__(self):
        return '{0}(indices={1!r})'.format(type(self).__name__, self.indices)


@key_ordering
class IndexLocation(object):
    _known_locations = ['LOCAL', 'REMOTE', 'LOCAL_AND_REMOTE']

    def __init__(self, location):
        # type: (str) -> None
        assert location in self._known_locations, (location, self._known_locations)
        self.location = location

    def _cmp_key(self):
        return (type(self), self.location)

    @classmethod
    def LOCAL(cls):
        # type: () -> IndexLocation
        return cls('LOCAL')

    @classmethod
    def REMOTE(cls):
        # type: () -> IndexLocation
        return cls('REMOTE')

    @classmethod
    def LOCAL_AND_REMOTE(cls):
        # type: () -> IndexLocation
        return cls('LOCAL_AND_REMOTE')

    @classmethod
    def all_values(cls):
        # type: () -> Iterable[IndexLocation]
        return [cls(loc) for loc in cls._known_locations]

    def __repr__(self):
        return '{0}(location={1!r})'.format(type(self).__name__, self.location)

    def spec_index_for(self):
        # type: () -> SpecIndex
        if self == type(self).LOCAL():
            return SpecIndex.with_local_db()
        if self == type(self).REMOTE():
            return SpecIndex.with_remote_db()
        assert self == type(self).LOCAL_AND_REMOTE()
        return SpecIndex.with_local_and_remote_dbs()

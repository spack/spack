# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from abc import ABCMeta, abstractmethod, abstractproperty
from collections import defaultdict
from typing import Any, ClassVar, Dict, Iterable, Iterator, List  # novm

from six import add_metaclass

from llnl.util.lang import memoized

import spack.database
import spack.spec


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

    def __eq__(self, other):
        return isinstance(other, ConcretizedSpec) and self.spec == other.spec

    def __ne__(self, other):
        return not self == other

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
    record = None            # type: spack.database.InstallRecord

    def __init__(self, concretized_spec, record):
        # type: (ConcretizedSpec, spack.database.InstallRecord) -> None
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

    def __hash__(self):
        # type: () -> int
        return hash(self.hash_prefix)

    def __eq__(self, other):
        # type: (Any) -> bool
        return isinstance(other, PartialHash) and self.hash_prefix == other.hash_prefix

    def __ne__(self, other):
        # type: (Any) -> bool
        return not self == other


class HashPrefix(PartialHash):
    hash_prefix = None            # type: str

    def __init__(self, hash_prefix):
        # type: (str) -> None
        assert len(hash_prefix) <= self.FULL_HASH_STRING_LENGTH, (
            hash_prefix, self.FULL_HASH_STRING_LENGTH,
        )
        self.hash_prefix = hash_prefix.lower()

    def __repr__(self):
        return '{0}(hash_prefix={1!r})'.format(type(self).__name__, self.hash_prefix)


class CompleteHash(PartialHash):
    @abstractproperty
    def complete_hash(self):
        # type: () -> str
        pass


class ConcreteHash(CompleteHash):
    complete_hash = None  # type: str

    def __init__(self, complete_hash):
        # type: (str) -> None
        assert len(complete_hash) == self.FULL_HASH_STRING_LENGTH, (
            complete_hash, self.FULL_HASH_STRING_LENGTH,
        )
        self.complete_hash = complete_hash.lower()

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
    kwargs = None  # type: Dict[str, Any]

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __getattr__(self, name):
        if name == 'kwargs':
            return super(IndexQuery, self).__getattr__('kwargs')
        return self.kwargs.get(name, None)

    def __repr__(self):
        return 'IndexQuery({0})'.format(', '.join(
            '{0}={1}'.format(k, repr(v)) for k, v in self.kwargs.items()
        ))

    @classmethod
    def from_query_args(cls, **kwargs):
        # type: (Any) -> IndexQuery
        for field, value in kwargs.items():
            if value is any:
                kwargs[field] = None
        if 'query_spec' in kwargs:
            kwargs['query_specs'] = kwargs.pop('query_spec')
        return cls(**kwargs)

    def to_query_args(self):
        # type: () -> Dict
        return dict(
            query_spec=any if self.query_specs is None else self.query_specs,
            known=any if self.known is None else self.known,
            installed=True if self.installed is None else self.installed,
            explicit=any if self.explicit is None else self.explicit,
            start_date=self.start_date,
            end_date=self.end_date,
            hashes=self.hashes,
            for_all_architectures=(False if self.for_all_architectures is None
                                   else self.for_all_architectures),
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
        return spack.store.db

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

    def query_collecting_result_map(self, query):
        # type: (IndexQuery) -> Dict[spack.spec.Spec, List[ConcretizedSpec]]
        if not isinstance(query.query_specs, list):
            raise TypeError('expected a list of input specs from query {0}'
                            .format(query))

        spec_to_results = (
            defaultdict(list))  # type: Dict[spack.spec.Spec, List[ConcretizedSpec]]
        for concretized_spec in self.query(query):
            for spec in query.query_specs:
                if concretized_spec.spec.satisfies(spec, strict=True):
                    spec_to_results[spec].append(concretized_spec)

        return spec_to_results

    def __repr__(self):
        return '{0}(indices={1!r})'.format(type(self).__name__, self.indices)


class IndexLocation(object):
    _known_locations = ['LOCAL', 'REMOTE', 'LOCAL_AND_REMOTE']

    def __init__(self, location):
        # type: (str) -> None
        assert location in self._known_locations, (location, self._known_locations)
        self.location = location

    def __eq__(self, other):
        return isinstance(other, IndexLocation) and self.location == other.location

    def __ne__(self, other):
        return not self == other

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

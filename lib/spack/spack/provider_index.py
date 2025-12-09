# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage providers of virtual dependencies"""
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Set, Union

import spack.error
import spack.util.spack_json as sjson

if TYPE_CHECKING:
    import spack.repo
    import spack.spec


class ProviderIndex:
    #: This is a dict of dicts used for finding providers of particular
    #: virtual dependencies. The dict of dicts looks like:
    #:
    #:    { vpkg name :
    #:        { full vpkg spec : set(packages providing spec) } }
    #:
    #: Callers can use this to first find which packages provide a vpkg,
    #: then find a matching full spec.  e.g., in this scenario:
    #:
    #:    { 'mpi' :
    #:        { mpi@:1.1 : set([mpich]),
    #:          mpi@:2.3 : set([mpich2@1.9:]) } }
    #:
    #: Calling providers_for(spec) will find specs that provide a
    #: matching implementation of MPI. Derived class need to construct
    #: this attribute according to the semantics above.
    providers: Dict[str, Dict["spack.spec.Spec", Set["spack.spec.Spec"]]]

    def __init__(
        self,
        repository: "spack.repo.RepoType",
        specs: Optional[Iterable["spack.spec.Spec"]] = None,
        restrict: bool = False,
    ):
        """Provider index based on a single mapping of providers.

        Args:
            specs: if provided, will call update on each
                single spec to initialize this provider index.

            restrict: "restricts" values to the verbatim input specs; do not
                pre-apply package's constraints.

        TODO: rename this.  It is intended to keep things as broad
        TODO: as possible without overly restricting results, so it is
        TODO: not the best name.
        """
        self.repository = repository
        self.restrict = restrict
        self.providers = {}

        specs = specs or []
        for spec in specs:
            if isinstance(spec, str):
                from spack.spec import Spec

                spec = Spec(spec)

            if self.repository.is_virtual_safe(spec.name):
                continue

            self.update(spec)

    def providers_for(self, virtual: Union[str, "spack.spec.Spec"]) -> List["spack.spec.Spec"]:
        """Return a list of specs of all packages that provide virtual packages with the supplied
        spec.

        Args:
            virtual: either a Spec or a string name of a virtual package
        """
        result: Set["spack.spec.Spec"] = set()

        if isinstance(virtual, str):
            # In the common case where just a package name is passed, we can avoid running the
            # spec parser and intersects, since intersects is always true.
            if virtual.isalnum():
                if virtual in self.providers:
                    for p_spec, spec_set in self.providers[virtual].items():
                        result.update(spec_set)
                return list(result)

            from spack.spec import Spec

            virtual = Spec(virtual)

        # Add all the providers that satisfy the vpkg spec.
        if virtual.name in self.providers:
            for p_spec, spec_set in self.providers[virtual.name].items():
                if p_spec.intersects(virtual, deps=False):
                    result.update(spec_set)

        return list(result)

    def __contains__(self, name):
        return name in self.providers

    def __eq__(self, other):
        return self.providers == other.providers

    def _transform(self, transform_fun, out_mapping_type=dict):
        """Transform this provider index dictionary and return it.

        Args:
            transform_fun: transform_fun takes a (vpkg, pset) mapping and runs
                it on each pair in nested dicts.
            out_mapping_type: type to be used internally on the
                transformed (vpkg, pset)

        Returns:
            Transformed mapping
        """
        return _transform(self.providers, transform_fun, out_mapping_type)

    def __str__(self):
        return str(self.providers)

    def __repr__(self):
        return repr(self.providers)

    def update(self, spec: Union[str, "spack.spec.Spec"]) -> None:
        """Update the provider index with additional virtual specs.

        Args:
            spec: spec potentially providing additional virtual specs
        """
        if isinstance(spec, str):
            from spack.spec import Spec

            spec = Spec(spec)

        if not spec.name:
            # Empty specs do not have a package
            return

        msg = "cannot update an index passing the virtual spec '{}'".format(spec.name)
        assert not self.repository.is_virtual_safe(spec.name), msg

        pkg_cls = self.repository.get_pkg_class(spec.name)
        for provider_spec_readonly, provided_specs in pkg_cls.provided.items():
            for provided_spec in provided_specs:
                # TODO: fix this comment.
                # We want satisfaction other than flags
                provider_spec = provider_spec_readonly.copy()
                provider_spec.compiler_flags = spec.compiler_flags.copy()

                if spec.intersects(provider_spec, deps=False):
                    provided_name = provided_spec.name

                    provider_map = self.providers.setdefault(provided_name, {})
                    if provided_spec not in provider_map:
                        provider_map[provided_spec] = set()

                    if self.restrict:
                        provider_set = provider_map[provided_spec]

                        # If this package existed in the index before,
                        # need to take the old versions out, as they're
                        # now more constrained.
                        old = set([s for s in provider_set if s.name == spec.name])
                        provider_set.difference_update(old)

                        # Now add the new version.
                        provider_set.add(spec)

                    else:
                        # Before putting the spec in the map, constrain
                        # it so that it provides what was asked for.
                        constrained = spec.copy()
                        constrained.constrain(provider_spec)
                        provider_map[provided_spec].add(constrained)

    def to_json(self, stream=None):
        """Dump a JSON representation of this object.

        Args:
            stream: stream where to dump
        """
        provider_list = self._transform(
            lambda vpkg, pset: [vpkg.to_node_dict(), [p.to_node_dict() for p in pset]], list
        )

        sjson.dump({"provider_index": {"providers": provider_list}}, stream)

    def merge(self, other):
        """Merge another provider index into this one.

        Args:
            other (ProviderIndex): provider index to be merged
        """
        other = other.copy()  # defensive copy.

        for pkg in other.providers:
            if pkg not in self.providers:
                self.providers[pkg] = other.providers[pkg]
                continue

            spdict, opdict = self.providers[pkg], other.providers[pkg]
            for provided_spec in opdict:
                if provided_spec not in spdict:
                    spdict[provided_spec] = opdict[provided_spec]
                    continue

                spdict[provided_spec] = spdict[provided_spec].union(opdict[provided_spec])

    def remove_provider(self, pkg_name):
        """Remove a provider from the ProviderIndex."""
        empty_pkg_dict = []
        for pkg, pkg_dict in self.providers.items():
            empty_pset = []
            for provided, pset in pkg_dict.items():
                same_name = set(p for p in pset if p.fullname == pkg_name)
                pset.difference_update(same_name)

                if not pset:
                    empty_pset.append(provided)

            for provided in empty_pset:
                del pkg_dict[provided]

            if not pkg_dict:
                empty_pkg_dict.append(pkg)

        for pkg in empty_pkg_dict:
            del self.providers[pkg]

    def copy(self):
        """Return a deep copy of this index."""
        clone = ProviderIndex(repository=self.repository)
        clone.providers = self._transform(lambda vpkg, pset: (vpkg, set((p.copy() for p in pset))))
        return clone

    @staticmethod
    def from_json(stream, repository):
        """Construct a provider index from its JSON representation.

        Args:
            stream: stream where to read from the JSON data
        """
        data = sjson.load(stream)

        if not isinstance(data, dict):
            raise ProviderIndexError("JSON ProviderIndex data was not a dict.")

        if "provider_index" not in data:
            raise ProviderIndexError("YAML ProviderIndex does not start with 'provider_index'")

        index = ProviderIndex(repository=repository)
        providers = data["provider_index"]["providers"]
        from spack.spec import SpecfileLatest

        index.providers = _transform(
            providers,
            lambda vpkg, plist: (
                SpecfileLatest.from_node_dict(vpkg),
                set(SpecfileLatest.from_node_dict(p) for p in plist),
            ),
        )
        return index


def _transform(providers, transform_fun, out_mapping_type=dict):
    """Syntactic sugar for transforming a providers dict.

    Args:
        providers: provider dictionary
        transform_fun: transform_fun takes a (vpkg, pset) mapping and runs
            it on each pair in nested dicts.
        out_mapping_type: type to be used internally on the
            transformed (vpkg, pset)

    Returns:
        Transformed mapping
    """

    def mapiter(mappings):
        if isinstance(mappings, dict):
            return mappings.items()
        else:
            return iter(mappings)

    return dict(
        (name, out_mapping_type([transform_fun(vpkg, pset) for vpkg, pset in mapiter(mappings)]))
        for name, mappings in providers.items()
    )


class ProviderIndexError(spack.error.SpackError):
    """Raised when there is a problem with a ProviderIndex."""

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage providers of virtual dependencies"""

import copy
from typing import TYPE_CHECKING, Dict, Iterable, List, Set, Tuple

import spack.error
import spack.util.spack_json as sjson

if TYPE_CHECKING:
    import spack.repo

#: specfile format version. Must increase monotonically
SPECFILE_FORMAT_VERSION = 5


class ProviderIndex:
    #: This is a dict used for finding providers of particular virtual dependencies, mapping
    #: a virtual package name to a list of (virtual spec node dict, [provider node dicts])
    #: entries, one per distinct virtual spec provided. Node dicts use the specfile format,
    #: which allows this index to be cached as JSON and materialized as ``Spec`` objects with
    #: the specfile readers in ``spack.spec``.
    providers: Dict[str, List[Tuple[dict, List[dict]]]]

    def __init__(self):
        self.providers = {}

    def __contains__(self, name):
        return name in self.providers

    def __eq__(self, other):
        return self.providers == other.providers

    def __str__(self):
        return str(self.providers)

    def __repr__(self):
        return repr(self.providers)

    def update_packages(self, pkgs_fullname: Iterable[str], repository: "spack.repo.RepoType"):
        """Update the provider index with additional packages.

        Args:
            pkgs_fullname: package names, optionally qualified with a namespace
            repository: repository the packages belong to
        """
        for fullname in pkgs_fullname:
            namespace, _, name = fullname.rpartition(".")

            if not name or repository.is_virtual_safe(name):
                # Only non-virtual packages with name can provide virtual specs.
                continue

            pkg_cls = repository.get_pkg_class(name)
            for when_spec, provided_specs in pkg_cls.provided.items():
                # A provide condition named after a different package cannot apply.
                if when_spec.name and when_spec.name != name:
                    continue

                provider = when_spec.copy()
                provider.name = name
                provider.namespace = namespace or None
                provider.compiler_flags.clear()
                provider_node = provider.to_node_dict()

                for provided_spec in provided_specs:
                    vpkg_node = provided_spec.to_node_dict()
                    entries = self.providers.setdefault(provided_spec.name, [])
                    for vpkg, providers in entries:
                        if vpkg == vpkg_node:
                            if provider_node not in providers:
                                providers.append(provider_node)
                            break
                    else:
                        entries.append((vpkg_node, [provider_node]))

    def merge(self, other: "ProviderIndex"):
        """Merge another provider index into this one.

        Args:
            other: provider index to be merged
        """
        # Deep copy, so that self does not alias node dicts owned by other.
        for vname, other_entries in copy.deepcopy(other.providers).items():
            entries = self.providers.setdefault(vname, [])
            for other_vpkg, other_providers in other_entries:
                for vpkg, providers in entries:
                    if vpkg == other_vpkg:
                        providers.extend(p for p in other_providers if p not in providers)
                        break
                else:
                    entries.append((other_vpkg, other_providers))

    def remove_providers(self, pkg_names: Set[str]):
        """Remove the given packages from the ProviderIndex."""
        for vname in list(self.providers):
            new_entries = []
            for vpkg, providers in self.providers[vname]:
                providers = [p for p in providers if p["name"] not in pkg_names]
                if providers:
                    new_entries.append((vpkg, providers))
            if new_entries:
                self.providers[vname] = new_entries
            else:
                del self.providers[vname]

    def copy(self) -> "ProviderIndex":
        """Return a deep copy of this index."""
        clone = ProviderIndex()
        clone.providers = copy.deepcopy(self.providers)
        return clone

    def to_json(self, stream=None):
        """Dump a JSON representation of this object.

        Args:
            stream: stream where to dump
        """
        sjson.dump({"provider_index": {"providers": self.providers}}, stream)

    @staticmethod
    def from_json(stream) -> "ProviderIndex":
        """Construct a provider index from its JSON representation.

        Args:
            stream: stream where to read from the JSON data
        """
        data = sjson.load(stream)

        if not isinstance(data, dict):
            raise ProviderIndexError("JSON ProviderIndex data was not a dict.")

        if "provider_index" not in data:
            raise ProviderIndexError("YAML ProviderIndex does not start with 'provider_index'")

        index = ProviderIndex()
        index.providers = {
            vname: [(vpkg, providers) for vpkg, providers in entries]
            for vname, entries in data["provider_index"]["providers"].items()
        }
        return index


class ProviderIndexError(spack.error.SpackError):
    """Raised when there is a problem with a ProviderIndex."""

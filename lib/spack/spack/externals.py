# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Any, Callable, Dict, List, Union

from spack.vendor.typing_extensions import TypedDict

import spack.archspec
import spack.spec


class ExternalDict(TypedDict, total=False):
    """Dictionary representation of an external spec."""

    spec: str
    prefix: str
    modules: List[str]
    extra_attributes: Dict[str, Any]
    external_id: str


def node_from_dict(external_dict: ExternalDict) -> spack.spec.Spec:
    """Returns an external spec node from a dictionary representation."""
    extra_attributes = external_dict.get("extra_attributes", {})
    result = spack.spec.Spec(
        # Allow `@x.y.z` instead of `@=x.y.z`
        str(spack.spec.parse_with_version_concrete(external_dict["spec"])),
        external_path=external_dict.get("prefix"),
        external_modules=external_dict.get("modules"),
    )
    result.extra_attributes = extra_attributes
    return result


def complete_architecture(node: spack.spec.Spec) -> None:
    """Completes a node with architecture information."""
    if node.architecture:
        node.architecture.complete_with_defaults()
    else:
        node.constrain(spack.spec.Spec.default_arch())
    node.architecture.target = spack.archspec.HOST_TARGET_FAMILY


def extract_dicts_from_configuration(packages_yaml) -> List[ExternalDict]:
    """Extracts external specs from a configuration dictionary."""
    result = []
    for name, entry in packages_yaml.items():
        result.extend([current for current in entry.get("externals", [])])
    return result


class ExternalSpecsParser:
    def __init__(
        self,
        external_dicts: List[ExternalDict],
        *,
        complete_node: Callable[[spack.spec.Spec], None] = complete_architecture,
    ):
        self.external_dicts = external_dicts
        self.specs_by_external_id: Dict[str, spack.spec.Spec] = {}
        self.specs_by_name: Dict[str, List[spack.spec.Spec]] = {}
        self.nodes: List[spack.spec.Spec] = []
        # Fill the data structures above (can be done lazily)
        self.complete_node = complete_node
        self._parse()

    def _parse(self) -> None:
        for external_dict in self.external_dicts:
            node = node_from_dict(external_dict)
            self.complete_node(node)
            external_id = external_dict.get("external_id")
            if external_id:
                self.specs_by_external_id[external_id] = node
            self.specs_by_name.setdefault(node.name, []).append(node)
            self.nodes.append(node)

        # TODO (externals as concrete specs): attach dependencies here

        for node in self.nodes:
            node._finalize_concretization()

    def get_specs_for_package(self, package_name: str) -> List[spack.spec.Spec]:
        """Returns the external specs for a given package name."""
        return self.specs_by_name.get(package_name, [])

    def all_specs(self) -> List[spack.spec.Spec]:
        """Returns all the external specs."""
        return self.nodes

    def query(self, query: Union[str, spack.spec.Spec]) -> List[spack.spec.Spec]:
        """Returns the external specs matching a query spec."""
        result = []
        for node in self.nodes:
            if node.satisfies(query):
                result.append(node)
        return result


def external_spec(config: ExternalDict) -> spack.spec.Spec:
    """Returns an external spec from a dictionary representation."""
    return ExternalSpecsParser([config]).all_specs()[0]

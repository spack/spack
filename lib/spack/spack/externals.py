# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import uuid
from typing import Any, Callable, Dict, List, NamedTuple, Union

from spack.vendor.typing_extensions import TypedDict

import spack.archspec
import spack.repo
import spack.spec
from spack.error import SpackError


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


class ExternalSpecAndConfig(NamedTuple):
    spec: spack.spec.Spec
    config: ExternalDict


class ExternalSpecsParser:
    def __init__(
        self,
        external_dicts: List[ExternalDict],
        *,
        complete_node: Callable[[spack.spec.Spec], None] = complete_architecture,
        allow_nonexisting: bool = True,
    ):
        """Initializes a class to manage and process external specifications.

        Args:
            external_dicts: list of ExternalDict objects to provide external specifications.
            complete_node: a callable that completes a node with missing variants, targets, etc.
                Defaults to `complete_architecture`.
            allow_nonexisting: whether to allow non-existing packages. Defaults to True.

        Raises:
            spack.repo.UnknownPackageError: if a package does not exist,
                and allow_nonexisting is False.
        """
        self.external_dicts = external_dicts
        self.specs_by_external_id: Dict[str, ExternalSpecAndConfig] = {}
        self.specs_by_name: Dict[str, List[spack.spec.Spec]] = {}
        self.nodes: List[spack.spec.Spec] = []
        self.allow_nonexisting = allow_nonexisting
        # Fill the data structures above (can be done lazily)
        self.complete_node = complete_node
        self._parse()

    def _parse(self) -> None:
        for external_dict in self.external_dicts:
            node = node_from_dict(external_dict)
            package_exists = spack.repo.PATH.exists(node.name)

            # If we allow non-existing packages, just continue
            if not package_exists and self.allow_nonexisting:
                continue

            if not package_exists and not self.allow_nonexisting:
                raise spack.repo.UnknownPackageError(node.name, repo=spack.repo.PATH)

            if not package_exists:
                raise ValueError(f"Package '{node.name}' does not exist")

            eid = external_dict.setdefault("external_id", str(uuid.uuid4()))
            if eid in self.specs_by_external_id:
                other_node = self.specs_by_external_id[eid].spec
                raise DuplicateExternalError(
                    f"Specs {node} and {other_node} have the same external id {eid}."
                    f" Fix your packages.yaml configuration."
                )

            self.complete_node(node)
            # Normalize internally so that each node has a unique id
            self.specs_by_external_id[eid] = ExternalSpecAndConfig(spec=node, config=external_dict)
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


class DuplicateExternalError(SpackError):
    """Raised when a duplicate external is detected."""

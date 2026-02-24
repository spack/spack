# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
This module turns the configuration data in the ``packages`` section into a list of concrete specs.

This is mainly done by the ``ExternalSpecsParser`` class, which is responsible for:

 1. Transforming an intermediate representation of the YAML configuration into a set of nodes
 2. Ensuring the dependency specifications are not ambiguous
 3. Inferring missing information about the external specs (e.g. architecture, deptypes)
 4. Wiring up the external specs to their dependencies

The helper function ``extract_dicts_from_configuration`` is used to transform the configuration
into the intermediate representation.
"""
import re
import uuid
import warnings
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, Union

from spack.vendor.typing_extensions import TypedDict

import spack.archspec
import spack.deptypes
import spack.repo
import spack.spec
from spack.error import SpackError
from spack.llnl.util import tty


class DependencyDict(TypedDict, total=False):
    id: str
    spec: str
    deptypes: spack.deptypes.DepTypes
    virtuals: str


class ExternalDict(TypedDict, total=False):
    """Dictionary representation of an external spec.

    This representation mostly follows the one used in the configuration files, with a few
    exceptions needed to support specific features.
    """

    spec: str
    prefix: str
    modules: List[str]
    extra_attributes: Dict[str, Any]
    id: str
    dependencies: List[DependencyDict]
    # Target requirement from configuration. Not in the external schema
    required_target: str


def node_from_dict(external_dict: ExternalDict) -> spack.spec.Spec:
    """Returns an external spec node from a dictionary representation."""
    extra_attributes = external_dict.get("extra_attributes", {})
    result = spack.spec.Spec(
        # Allow `@x.y.z` instead of `@=x.y.z`
        str(spack.spec.parse_with_version_concrete(external_dict["spec"])),
        external_path=external_dict.get("prefix"),
        external_modules=external_dict.get("modules"),
    )
    if not result.versions.concrete:
        raise ExternalSpecError(
            f"The external spec '{external_dict['spec']}' doesn't have a concrete version"
        )

    result.extra_attributes = extra_attributes
    if "required_target" in external_dict:
        result.constrain(f"target={external_dict['required_target']}")
    return result


def complete_architecture(node: spack.spec.Spec) -> None:
    """Completes a node with architecture information.

    Undefined targets are set to the default host target family (e.g. ``x86_64``).
    The operating system and platform are set based on the current host.
    """
    if node.architecture:
        if not node.architecture.target:
            node.architecture.target = spack.archspec.HOST_TARGET_FAMILY
        node.architecture.complete_with_defaults()
    else:
        node.constrain(spack.spec.Spec.default_arch())
        node.architecture.target = spack.archspec.HOST_TARGET_FAMILY

    node.namespace = spack.repo.PATH.repo_for_pkg(node.name).namespace
    for flag_type in spack.spec.FlagMap.valid_compiler_flags():
        node.compiler_flags.setdefault(flag_type, [])


def complete_variants_and_architecture(node: spack.spec.Spec) -> None:
    """Completes a node with variants and architecture information.

    Architecture is completed first, delegating to ``complete_architecture``.
    Variants are then added to the node, using their default value.
    """
    complete_architecture(node)
    pkg_class = spack.repo.PATH.get_pkg_class(node.name)
    variants_dict = pkg_class.variants.copy()
    changed = True

    while variants_dict and changed:
        changed = False
        items = list(variants_dict.items())  # copy b/c loop modifies dict

        for when, variants_by_name in items:
            if not node.satisfies(when):
                continue
            variants_dict.pop(when)
            for name, vdef in variants_by_name.items():
                if name not in node.variants:
                    # Cannot use Spec.constrain, because we lose information on the variant type
                    node.variants[name] = vdef.make_default()
            changed = True


def extract_dicts_from_configuration(packages_yaml) -> List[ExternalDict]:
    """Transforms the packages.yaml configuration into a list of external dictionaries.

    The default required target is extracted from ``packages:all:require``, if present.
    Any package-specific required target overrides the default.
    """
    result = []
    default_required_target = ""
    if "all" in packages_yaml:
        default_required_target = _required_target(packages_yaml["all"])

    for name, entry in packages_yaml.items():
        pkg_required_target = _required_target(entry) or default_required_target
        partial_result = [current for current in entry.get("externals", [])]
        if pkg_required_target:
            for partial in partial_result:
                partial["required_target"] = pkg_required_target
        result.extend(partial_result)
    return result


def _line_info(config_dict: Any) -> str:
    result = getattr(config_dict, "line_info", "")
    return "" if not result else f" [{result}]"


_TARGET_RE = re.compile(r"target=([^\s:]+)")


def _required_target(entry) -> str:
    """Parses the YAML configuration for a single external spec and returns the required target
    if defined. Returns an empty string otherwise.
    """
    if "require" not in entry:
        return ""

    requirements = entry["require"]
    if not isinstance(requirements, list):
        requirements = [requirements]

    results = []
    for requirement in requirements:
        if not isinstance(requirement, str):
            continue

        matches = _TARGET_RE.match(requirement)
        if matches:
            results.append(matches.group(1))

    if len(results) == 1:
        return results[0]

    return ""


class ExternalSpecAndConfig(NamedTuple):
    spec: spack.spec.Spec
    config: ExternalDict


class ExternalSpecsParser:
    """Transforms a list of external dicts into a list of specs."""

    def __init__(
        self,
        external_dicts: List[ExternalDict],
        *,
        complete_node: Callable[[spack.spec.Spec], None] = complete_variants_and_architecture,
        allow_nonexisting: bool = True,
    ):
        """Initializes a class to manage and process external specifications in ``packages.yaml``.

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
        self.specs_by_name: Dict[str, List[ExternalSpecAndConfig]] = {}
        self.nodes: List[spack.spec.Spec] = []
        self.allow_nonexisting = allow_nonexisting
        # Fill the data structures above (can be done lazily)
        self.complete_node = complete_node
        self._parse()

    def _parse(self) -> None:
        # Parse all nodes without creating edges among them
        self._parse_all_nodes()
        # Map dependencies specified as specs to a single id
        self._ensure_dependencies_have_single_id()
        # Attach dependencies to externals
        self._create_edges()
        # Mark the specs as concrete
        for node in self.nodes:
            node._finalize_concretization()

    def _create_edges(self):
        for eid, entry in self.specs_by_external_id.items():
            current_node, current_dict = entry.spec, entry.config
            line_info = _line_info(current_dict)
            spec_str = current_dict["spec"]

            # Compute the dependency types for this spec
            pkg_class, deptypes_by_package = spack.repo.PATH.get_pkg_class(current_node.name), {}
            for when, by_name in pkg_class.dependencies.items():
                if not current_node.satisfies(when):
                    continue
                for name, dep in by_name.items():
                    if name not in deptypes_by_package:
                        deptypes_by_package[name] = dep.depflag
                    deptypes_by_package[name] |= dep.depflag

            for dependency_dict in current_dict.get("dependencies", []):
                dependency_id = dependency_dict.get("id")
                if not dependency_id:
                    raise ExternalDependencyError(
                        f"A dependency for {spec_str} does not have an external id{line_info}"
                    )
                elif dependency_id not in self.specs_by_external_id:
                    raise ExternalDependencyError(
                        f"A dependency for {spec_str} has an external id "
                        f"{dependency_id} that cannot be found in packages.yaml{line_info}"
                    )

                dependency_node = self.specs_by_external_id[dependency_id].spec

                # Compute dependency types and virtuals
                depflag = spack.deptypes.NONE
                if "deptypes" in dependency_dict:
                    depflag = spack.deptypes.canonicalize(dependency_dict["deptypes"])

                virtuals: Tuple[str, ...] = ()
                if "virtuals" in dependency_dict:
                    virtuals = tuple(dependency_dict["virtuals"].split(","))

                # Infer dependency types and virtuals if the user didn't specify them
                if depflag == spack.deptypes.NONE and not virtuals:
                    # Infer the deptype if only '%' was used in the spec
                    inferred_virtuals = []
                    for name, current_flag in deptypes_by_package.items():
                        if not dependency_node.intersects(name):
                            continue
                        depflag |= current_flag
                        if spack.repo.PATH.is_virtual(name):
                            inferred_virtuals.append(name)
                    virtuals = tuple(inferred_virtuals)
                elif depflag == spack.deptypes.NONE:
                    depflag = spack.deptypes.DEFAULT

                current_node._add_dependency(dependency_node, depflag=depflag, virtuals=virtuals)

    def _ensure_dependencies_have_single_id(self):
        for eid, entry in self.specs_by_external_id.items():
            current_node, current_dict = entry.spec, entry.config
            spec_str = current_dict["spec"]
            line_info = _line_info(current_dict)

            if current_node.dependencies() and "dependencies" in current_dict:
                raise ExternalSpecError(
                    f"the spec {spec_str} cannot specify dependencies both in the root spec and"
                    f"in the 'dependencies' field{line_info}"
                )

            # Transform inline entries like 'mpich %gcc' to a canonical form using 'dependencies'
            for edge in current_node.edges_to_dependencies():
                entry: DependencyDict = {"spec": str(edge.spec)}

                # Handle entries with more options specified
                if edge.depflag != 0:
                    entry["deptypes"] = spack.deptypes.flag_to_tuple(edge.depflag)

                if edge.virtuals:
                    entry["virtuals"] = ",".join(edge.virtuals)

                current_dict.setdefault("dependencies", []).append(entry)
            current_node.clear_edges()

            # Map a spec: to id:
            for dependency_dict in current_dict.get("dependencies", []):
                if "id" in dependency_dict:
                    continue

                if "spec" not in dependency_dict:
                    raise ExternalDependencyError(
                        f"the spec {spec_str} needs to specify either the id or the spec "
                        f"of its dependencies{line_info}"
                    )

                query_spec = spack.spec.Spec(dependency_dict["spec"])
                candidates = [
                    x
                    for x in self.specs_by_name.get(query_spec.name, [])
                    if x.spec.satisfies(query_spec)
                ]
                if len(candidates) == 0:
                    raise ExternalDependencyError(
                        f"the spec '{spec_str}' depends on '{query_spec}', but there is no such "
                        f"external spec in packages.yaml{line_info}"
                    )
                elif len(candidates) > 1:
                    candidates_str = (
                        f" [candidates are {', '.join([str(x.spec) for x in candidates])}]"
                    )
                    raise ExternalDependencyError(
                        f"the spec '{spec_str}' depends on '{query_spec}', but there are multiple "
                        f"external specs that could satisfy the request{candidates_str}{line_info}"
                    )

                dependency_dict["id"] = candidates[0].config["id"]

    def _parse_all_nodes(self) -> None:
        """Parses all the nodes from the external dicts but doesn't add any edge."""
        for external_dict in self.external_dicts:
            line_info = _line_info(external_dict)
            try:
                node = node_from_dict(external_dict)
            except spack.spec.UnsatisfiableArchitectureSpecError:
                spec_str, target_str = external_dict["spec"], external_dict["required_target"]
                tty.debug(
                    f"[{__name__}]{line_info} Skipping external spec '{spec_str}' because it "
                    f"cannot be constrained with the required target '{target_str}'."
                )
                continue
            except ExternalSpecError as e:
                warnings.warn(f"{e}{line_info}")
                continue

            package_exists = spack.repo.PATH.exists(node.name)

            # If we allow non-existing packages, just continue
            if not package_exists and self.allow_nonexisting:
                continue

            if not package_exists and not self.allow_nonexisting:
                raise ExternalSpecError(f"Package '{node.name}' does not exist{line_info}")

            eid = external_dict.setdefault("id", str(uuid.uuid4()))
            if eid in self.specs_by_external_id:
                other_node = self.specs_by_external_id[eid]
                other_line_info = _line_info(other_node.config)
                raise DuplicateExternalError(
                    f"Specs {node} and {other_node.spec} cannot have the same external id {eid}"
                    f"{line_info}{other_line_info}"
                )

            self.complete_node(node)

            # Add a Python dependency to Python extensions that don't specify it
            pkg_class = spack.repo.PATH.get_pkg_class(node.name)
            if (
                "dependencies" not in external_dict
                and not node.dependencies()
                and any([c.__name__ == "PythonExtension" for c in pkg_class.__mro__])
            ):
                warnings.warn(
                    f"Spack is trying attach a Python dependency to '{node}'. This feature is "
                    f"deprecated, and will be removed in v1.2. Please make the dependency "
                    f"explicit in your configuration."
                )
                external_dict.setdefault("dependencies", []).append({"spec": "python"})

            # Normalize internally so that each node has a unique id
            spec_and_config = ExternalSpecAndConfig(spec=node, config=external_dict)
            self.specs_by_external_id[eid] = spec_and_config
            self.specs_by_name.setdefault(node.name, []).append(spec_and_config)
            self.nodes.append(node)

    def get_specs_for_package(self, package_name: str) -> List[spack.spec.Spec]:
        """Returns the external specs for a given package name."""
        result = self.specs_by_name.get(package_name, [])
        return [x.spec for x in result]

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


class ExternalDependencyError(SpackError):
    """Raised when a dependency on an external package is specified wrongly."""


class ExternalSpecError(SpackError):
    """Raised when a dependency on an external package is specified wrongly."""

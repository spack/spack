# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
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


class DependencyDict(TypedDict, total=False):
    external_id: str
    deptypes: spack.deptypes.DepTypes
    virtuals: str


class ExternalDict(TypedDict, total=False):
    """Dictionary representation of an external spec."""

    spec: str
    prefix: str
    modules: List[str]
    extra_attributes: Dict[str, Any]
    external_id: str
    dependencies: List[DependencyDict]
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
            f"The external spec '{external_dict['spec']}' doesn't have a concrete version."
        )

    result.extra_attributes = extra_attributes
    if "required_target" in external_dict:
        result.constrain(f"target={external_dict['required_target']}")
    return result


def complete_architecture(node: spack.spec.Spec) -> None:
    """Completes a node with architecture information."""
    if node.architecture:
        if not node.architecture.target:
            node.architecture.target = spack.archspec.HOST_TARGET_FAMILY
        node.architecture.complete_with_defaults()
    else:
        node.constrain(spack.spec.Spec.default_arch())
        node.architecture.target = spack.archspec.HOST_TARGET_FAMILY

    for flag_type in spack.spec.FlagMap.valid_compiler_flags():
        node.compiler_flags.setdefault(flag_type, [])


def complete_variants_and_architecture(node: spack.spec.Spec) -> None:
    """Completes a node with variants and architecture information."""
    complete_architecture(node)
    pkg_class = spack.repo.PATH.get_pkg_class(node.name)
    variants_dict = pkg_class.variants.copy()

    progress = True
    while progress:
        progress = False
        current_keys = list(variants_dict.keys())
        for key in current_keys:
            if not node.satisfies(key):
                continue
            applicable_variants = variants_dict.pop(key)
            for v in applicable_variants.values():
                if not node.satisfies(f"{v.name}=*"):
                    # Cannot use Spec.constrain, because we lose information on the variant type
                    node.variants[v.name] = v.make_default()
            progress = True


def extract_dicts_from_configuration(packages_yaml) -> List[ExternalDict]:
    """Extracts external specs from a configuration dictionary."""
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


_TARGET_RE = re.compile(r"target=(\S+)")


def _required_target(entry) -> str:
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
    def __init__(
        self,
        external_dicts: List[ExternalDict],
        *,
        complete_node: Callable[[spack.spec.Spec], None] = complete_variants_and_architecture,
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
        self.specs_by_name: Dict[str, List[ExternalSpecAndConfig]] = {}
        self.nodes: List[spack.spec.Spec] = []
        self.allow_nonexisting = allow_nonexisting
        # Fill the data structures above (can be done lazily)
        self.complete_node = complete_node
        self._parse()

    def _parse(self) -> None:
        for external_dict in self.external_dicts:
            try:
                node = node_from_dict(external_dict)
            except spack.spec.UnsatisfiableArchitectureSpecError:
                warnings.warn(
                    f"cannot constrain external spec '{external_dict['spec']}' with target "
                    f"'{external_dict['required_target']}'. This spec will not be considered "
                    f"during concretization."
                )
                continue
            except ExternalSpecError as e:
                warnings.warn(f"{e} Fix your packages.yaml configuration.")
                continue

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
            spec_and_config = ExternalSpecAndConfig(spec=node, config=external_dict)
            self.specs_by_external_id[eid] = spec_and_config
            self.specs_by_name.setdefault(node.name, []).append(spec_and_config)
            self.nodes.append(node)

        # Guess how to convert old entries like 'mpich %gcc' to a dependency in the dict
        for eid, entry in self.specs_by_external_id.items():
            current_node = entry.spec
            current_dict = entry.config
            for edge in current_node.edges_to_dependencies():
                # We don't want to accept foo %[deptypes=build,link] mpich as a spec
                if edge.depflag != 0:
                    raise ExternalDependencyError(
                        f"The external spec '{current_dict['spec']}' has an invalid dependency"
                        f" specification. Fix your packages.yaml configuration."
                    )

                if edge.spec.name not in self.specs_by_name:
                    raise ExternalDependencyError(
                        f"The external spec '{current_dict['spec']}' depends on "
                        f"'{edge.spec.name}', but there is no such external spec in packages.yaml."
                    )

                candidates = [
                    x
                    for x in self.specs_by_name[edge.spec.name]
                    if x.spec.satisfies(edge.spec)
                    and x.spec.architecture.satisfies(current_node.architecture)
                ]
                if not candidates:
                    raise ExternalDependencyError(
                        f"The external spec '{current_dict['spec']}' depends on '{edge.spec}',"
                        f" but there is no '{edge.spec.name}' that satisfies the request "
                        f"in packages.yaml."
                    )

                candidates.sort(key=lambda x: x.spec)  # type: ignore
                selected = candidates[-1]
                warnings.warn(
                    f"the external spec '{current_dict['spec']}' has been guessed to depend on "
                    f"'{selected.config['spec']}'. If this is incorrect, fix your packages.yaml."
                )
                current_dict.setdefault("dependencies", []).append(
                    {
                        "external_id": selected.config["external_id"],
                        "deptypes": "build",
                        "virtuals": "c",
                    }
                )
            current_node.clear_edges()

        # Attach dependencies to externals
        for eid, entry in self.specs_by_external_id.items():
            current_node = entry.spec
            current_dict = entry.config

            for dependency_dict in current_dict.get("dependencies", []):
                dependency_id = dependency_dict.get("external_id")
                if not dependency_id:
                    raise ExternalDependencyError(
                        f"A dependency for {current_dict['spec']} does not have an external id"
                    )
                elif dependency_id not in self.specs_by_external_id:
                    raise ExternalDependencyError(
                        f"A dependency for {current_dict['spec']} has an external id "
                        f"{dependency_id} that is not defined in packages.yaml"
                    )

                dependency_node = self.specs_by_external_id[dependency_id].spec
                depflag = spack.deptypes.canonicalize(
                    dependency_dict.get("deptypes", spack.deptypes.DEFAULT_TYPES)
                )
                virtuals: Tuple[str, ...] = ()
                if "virtuals" in dependency_dict:
                    virtuals = tuple(dependency_dict["virtuals"].split(","))

                current_node._add_dependency(dependency_node, depflag=depflag, virtuals=virtuals)

        for node in self.nodes:
            node._finalize_concretization()

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

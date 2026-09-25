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

import hashlib
import pathlib
import re
import warnings
from typing import Any, Callable, Dict, Iterable, List, NamedTuple, Optional, Tuple, Union

from spack.vendor.typing_extensions import TypedDict

import spack.archspec
import spack.deptypes
import spack.repo
import spack.spec
import spack.variant as vt
from spack.error import SpackError
from spack.util import tty


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


def complete_architecture(node: spack.spec.Spec, repo: spack.repo.RepoPath) -> None:
    """Completes a node with architecture information.

    Undefined targets are set to the default host target family (e.g. ``x86_64``).
    The operating system and platform are set based on the current host.

    Args:
        node: spec to complete.
        repo: package repository to query.
    """
    if node.architecture:
        if not node.architecture.target:
            node.architecture.target = spack.archspec.HOST_TARGET_FAMILY
        node.architecture.complete_with_defaults()
    else:
        node.architecture = spack.spec.ArchSpec.default_arch()
        node.architecture.target = spack.archspec.HOST_TARGET_FAMILY

    node.namespace = repo.repo_for_pkg(node.name).namespace
    for flag_type in spack.spec.FlagMap.valid_compiler_flags():
        node.compiler_flags.setdefault(flag_type, [])


def _default_variant_value(node: spack.spec.Spec, vdef: vt.Variant) -> Optional[vt.VariantValue]:
    """Returns the default value of a variant definition, restricted to the values that are
    available for this node, or None if no value is available.
    """
    default, available = vdef.make_default(), vdef.possible_values(when=node)
    if available is None:
        return default

    selected = tuple(value for value in default.values if value in available)
    if len(selected) == len(default.values):
        return default
    elif selected:
        return vdef.make_variant(*selected)
    elif vdef.multi or not available:
        return None
    return vdef.make_variant(available[0])


def complete_variants_and_architecture(node: spack.spec.Spec, repo: spack.repo.RepoPath) -> None:
    """Completes a node with variants and architecture information.

    Architecture is completed first, delegating to ``complete_architecture``.
    Variants are then added to the node, using their default value where possible.
    For conditional variant values, the evaluation is greedy and may currently fail if the
    conditional value is gated on another variant.

    Args:
        node: spec to complete.
        repo: package repository to query.
    """
    complete_architecture(node, repo)
    pkg_class = repo.get_pkg_class(node.name)
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
                    default = _default_variant_value(node, vdef)
                    if default is None:
                        continue
                    # Cannot use Spec.constrain, because we lose information on the variant type
                    node.variants.set(default)
                elif (
                    node.variants[name].type != vdef.variant_type
                    and len(node.variants[name].values) == 1
                ):
                    # Spec parsing defaults to MULTI for non-boolean variants. Correct the type
                    # using the package definition, preserving the user-specified value.
                    existing = node.variants[name]
                    corrected = vdef.make_variant(*existing.values)
                    node.variants.set(corrected)
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


def derived_external_id(spec: spack.spec.Spec) -> str:
    """Returns the id of an external spec that has no explicit ``id`` in configuration.

    The id has the form ``<name>-<version>-<digest>``, where the digest hashes only the prefix of
    the external, or its modules if it has no prefix. Externals with the same prefix share the
    digest.
    """
    if spec.external_path:
        location = pathlib.PurePath(spec.external_path).as_posix()
    else:
        location = ",".join(spec.external_modules or [])
    digest = hashlib.sha256(location.encode("utf-8")).hexdigest()[:7]
    return f"{spec.name}-{spec.version}-{digest}"


def dependency_types(
    node: spack.spec.Spec, repo: spack.repo.RepoPath
) -> Dict[str, spack.deptypes.DepFlag]:
    """Returns the dependency types of each package or virtual a node depends on, from the
    ``depends_on`` directives whose condition the node satisfies.
    """
    result: Dict[str, spack.deptypes.DepFlag] = {}
    for when, by_name in repo.get_pkg_class(node.name).dependencies.items():
        if not node.satisfies(when):
            continue
        for name, dep in by_name.items():
            result[name] = result.get(name, spack.deptypes.NONE) | dep.depflag
    return result


def matches_package_or_virtual(
    spec: spack.spec.Spec, name: str, repo: spack.repo.RepoPath
) -> bool:
    """Returns True if ``spec`` matches the package ``name``, or a provider of the virtual
    ``name``.
    """
    # An abstract node matches a virtual only through its providers
    candidates = repo.providers_for(name) if repo.is_virtual(name) else (name,)
    return any(spec.intersects(c) for c in candidates)


def infer_dependency(
    dependency: spack.spec.Spec,
    types_by_name: Dict[str, spack.deptypes.DepFlag],
    repo: spack.repo.RepoPath,
) -> Tuple[spack.deptypes.DepFlag, Tuple[str, ...]]:
    """Returns the dependency types and virtuals of an edge to ``dependency``, given the output of
    ``dependency_types`` for the dependent node.
    """
    depflag, virtuals = spack.deptypes.NONE, []
    for name, current_flag in types_by_name.items():
        if not matches_package_or_virtual(dependency, name, repo):
            continue
        depflag |= current_flag
        if repo.is_virtual(name):
            virtuals.append(name)
    return depflag, tuple(virtuals)


class ExternalSpecAndConfig(NamedTuple):
    spec: spack.spec.Spec
    config: ExternalDict


class ExternalId(NamedTuple):
    #: Explicit id of the external, or its derived id if it has none
    id: str
    #: Why a dependency cannot reference the external by ``id``, or None if it can
    conflict: Optional[str]


CompleteNodeFn = Callable[[spack.spec.Spec, spack.repo.RepoPath], None]


class ExternalSpecsParser:
    """Transforms a list of external dicts into a list of specs."""

    def __init__(
        self,
        external_dicts: List[ExternalDict],
        *,
        repo: spack.repo.RepoPath,
        complete_node: CompleteNodeFn = complete_variants_and_architecture,
        allow_nonexisting: bool = True,
        nodes_only: bool = False,
    ):
        """Initializes a class to manage and process external specifications in ``packages.yaml``.

        Args:
            external_dicts: list of ExternalDict objects to provide external specifications.
            repo: package repository to query
            complete_node: a callable ``(node, repo)`` that completes a node with missing variants,
                targets, etc. It is invoked with this parser's ``repo``.
            allow_nonexisting: whether to allow non-existing packages. Defaults to True.
            nodes_only: if True, parse the externals and their ids, but neither resolve
                dependencies nor mark the specs concrete. Errors in dependencies are not raised.

        Raises:
            spack.repo.UnknownPackageError: if a package does not exist,
                and allow_nonexisting is False.
        """
        self.repo = repo
        self.external_dicts = external_dicts
        self.specs_by_external_id: Dict[str, ExternalSpecAndConfig] = {}
        self.specs_by_name: Dict[str, List[ExternalSpecAndConfig]] = {}
        self.nodes: List[spack.spec.Spec] = []
        #: Derived ids shared by more than one external without an explicit id
        self._ambiguous_ids: Dict[str, List[ExternalSpecAndConfig]] = {}
        #: Keys of externals without an explicit id that are not registered under their derived
        #: id, mapped to the derived id
        self._suffixed_keys: Dict[str, str] = {}
        self.allow_nonexisting = allow_nonexisting
        # Fill the data structures above (can be done lazily)
        self.complete_node = complete_node
        self._parse(nodes_only=nodes_only)

    def _parse(self, *, nodes_only: bool) -> None:
        # Parse all nodes without creating edges among them
        self._parse_all_nodes()
        if nodes_only:
            return
        # Map dependencies specified as specs to a single id
        self._ensure_dependencies_have_single_id()
        # Attach dependencies to externals
        self._create_edges()
        # Mark the specs as concrete
        spack.repo.freeze_provided_virtuals(self.nodes, repo=self.repo)
        spack.spec.assign_hashes(self.nodes, repo=self.repo)

    def _create_edges(self):
        for eid, entry in self.specs_by_external_id.items():
            current_node, current_dict = entry.spec, entry.config
            line_info = _line_info(current_dict)
            spec_str = current_dict["spec"]

            deptypes_by_package = dependency_types(current_node, self.repo)

            for dependency_dict in current_dict.get("dependencies", []):
                dependency_id = dependency_dict.get("id")
                if not dependency_id:
                    raise ExternalDependencyError(
                        f"A dependency for {spec_str} does not have an external id{line_info}"
                    )
                elif dependency_id in self._ambiguous_ids:
                    candidates_str = ", ".join(
                        f"{x.spec}{_line_info(x.config)}"
                        for x in self._ambiguous_ids[dependency_id]
                    )
                    raise ExternalDependencyError(
                        f"A dependency for {spec_str} has an external id {dependency_id} that "
                        f"matches multiple externals in packages.yaml [candidates are "
                        f"{candidates_str}]. Set an explicit id on the intended one{line_info}"
                    )
                elif dependency_id not in self.specs_by_external_id:
                    known_ids = self._ids_of_externals_matching(deptypes_by_package)
                    known_ids_str = ""
                    if known_ids:
                        known_ids_str = (
                            f" [ids of externals {current_node.name} can depend on: "
                            f"{', '.join(known_ids)}]"
                        )
                    raise ExternalDependencyError(
                        f"A dependency for {spec_str} has an external id "
                        f"{dependency_id} that cannot be found in packages.yaml"
                        f"{known_ids_str}{line_info}"
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
                    depflag, virtuals = infer_dependency(
                        dependency_node, deptypes_by_package, self.repo
                    )
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
        without_id: Dict[str, List[ExternalSpecAndConfig]] = {}
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

            package_exists = self.repo.exists(node.name)

            # If we allow non-existing packages, just continue
            if not package_exists and self.allow_nonexisting:
                continue

            if not package_exists and not self.allow_nonexisting:
                raise ExternalSpecError(f"Package '{node.name}' does not exist{line_info}")

            self.complete_node(node, self.repo)

            # Add a Python dependency to Python extensions that don't specify it
            pkg_class = self.repo.get_pkg_class(node.name)
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

            spec_and_config = ExternalSpecAndConfig(spec=node, config=external_dict)
            if "id" in external_dict:
                eid = external_dict["id"]
                if eid in self.specs_by_external_id:
                    other_node = self.specs_by_external_id[eid]
                    other_line_info = _line_info(other_node.config)
                    raise DuplicateExternalError(
                        f"Specs {node} and {other_node.spec} cannot have the same external id "
                        f"{eid}{line_info}{other_line_info}"
                    )
                self.specs_by_external_id[eid] = spec_and_config
            else:
                without_id.setdefault(derived_external_id(node), []).append(spec_and_config)

            self.specs_by_name.setdefault(node.name, []).append(spec_and_config)
            self.nodes.append(node)

        self._assign_derived_ids(without_id)

    def _assign_derived_ids(self, without_id: Dict[str, List[ExternalSpecAndConfig]]) -> None:
        """Registers externals without an explicit id under their derived id.

        A derived id that is also an explicit id refers to the explicit entry. A derived id shared
        by several entries is ambiguous, and referencing it is an error. In both cases the entries
        are registered under the derived id with a ``#<n>`` suffix, and can still be referenced
        through ``spec:``.
        """
        for derived_id, entries in without_id.items():
            if len(entries) > 1 and derived_id not in self.specs_by_external_id:
                self._ambiguous_ids[derived_id] = entries

            for entry in entries:
                eid, counter = derived_id, 0
                while eid in self.specs_by_external_id or eid in self._ambiguous_ids:
                    eid, counter = f"{derived_id}#{counter}", counter + 1
                entry.config["id"] = eid
                self.specs_by_external_id[eid] = entry
                if eid != derived_id:
                    self._suffixed_keys[eid] = derived_id

    def external_id(self, entry: ExternalSpecAndConfig) -> ExternalId:
        """Returns the id of a parsed external, and whether dependencies can reference it."""
        key = entry.config["id"]
        if key not in self._suffixed_keys:
            return ExternalId(id=key, conflict=None)

        derived_id = self._suffixed_keys[key]
        if derived_id in self._ambiguous_ids:
            return ExternalId(id=derived_id, conflict="derived by multiple externals")
        return ExternalId(id=derived_id, conflict="explicit id of another external")

    def _ids_of_externals_matching(self, names: Iterable[str]) -> List[str]:
        """Returns the referenceable ids of the externals that match any of the names."""
        result = []
        for entry in self.specs_by_external_id.values():
            if not any(matches_package_or_virtual(entry.spec, name, self.repo) for name in names):
                continue
            eid = self.external_id(entry)
            if eid.conflict is None:
                result.append(eid.id)
        return sorted(result)

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


def external_spec(config: ExternalDict, *, repo: spack.repo.RepoPath) -> spack.spec.Spec:
    """Returns an external spec from a dictionary representation."""
    return ExternalSpecsParser([config], repo=repo).all_specs()[0]


class DuplicateExternalError(SpackError):
    """Raised when a duplicate external is detected."""


class ExternalDependencyError(SpackError):
    """Raised when a dependency on an external package is specified wrongly."""


class ExternalSpecError(SpackError):
    """Raised when a dependency on an external package is specified wrongly."""

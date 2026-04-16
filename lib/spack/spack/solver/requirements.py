# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
import warnings
from typing import List, NamedTuple, Optional, Sequence, Tuple, Union

import spack.vendor.archspec.cpu

import spack.config
import spack.error
import spack.package_base
import spack.repo
import spack.spec
import spack.spec_parser
import spack.traverse
import spack.util.spack_yaml
from spack.enums import PropagationPolicy
from spack.llnl.util import tty
from spack.util.spack_yaml import get_mark_from_yaml_data


def _mark_str(raw) -> str:
    """Return a 'file:line: ' prefix from the YAML mark on *raw*, or empty string."""
    mark = get_mark_from_yaml_data(raw)
    return f"{mark.name}:{mark.line + 1}: " if mark else ""


def _check_unknown_targets(
    raw_strs: List[str], specs: List["spack.spec.Spec"], *, always_warn: bool = False
) -> None:
    """Either warns or raises for unknown concrete target names in a set of specs.

    UserWarnings are emitted if *always_warn* is True or if there is at least one spec without
    unknown targets. If all the specs have unknown targets raises an error.
    """
    specs_with_unknown_targets = [
        (raw, spec)
        for raw, spec in zip(raw_strs, specs)
        if spec.architecture
        and spec.architecture.target_concrete
        and spec.target.name not in spack.vendor.archspec.cpu.TARGETS
    ]
    if not specs_with_unknown_targets:
        return

    errors = [
        f"{_mark_str(raw)}'{spec}' contains unknown targets"
        for raw, spec in specs_with_unknown_targets
    ]
    if len(errors) == 1:
        msg = f"{errors[0]}. Run 'spack arch --known-targets' to see valid targets."
    else:
        details = "\n".join([f"{idx}. {part}" for idx, part in enumerate(errors, 1)])
        msg = (
            f"unknown targets have been detected in requirements\n{details}\n"
            f"Run 'spack arch --known-targets' to see valid targets."
        )
    if not always_warn and len(specs_with_unknown_targets) == len(specs):
        raise spack.error.SpecError(msg)
    warnings.warn(msg)


class RequirementKind(enum.Enum):
    """Purpose / provenance of a requirement"""

    #: Default requirement expressed under the 'all' attribute of packages.yaml
    DEFAULT = enum.auto()
    #: Requirement expressed on a virtual package
    VIRTUAL = enum.auto()
    #: Requirement expressed on a specific package
    PACKAGE = enum.auto()


class RequirementOrigin(enum.Enum):
    """Origin of a requirement"""

    REQUIRE_YAML = enum.auto()
    PREFER_YAML = enum.auto()
    CONFLICT_YAML = enum.auto()
    DIRECTIVE = enum.auto()
    INPUT_SPECS = enum.auto()


class RequirementRule(NamedTuple):
    """Data class to collect information on a requirement"""

    pkg_name: str
    policy: str
    origin: RequirementOrigin
    requirements: Sequence[spack.spec.Spec]
    condition: spack.spec.Spec
    kind: RequirementKind
    message: Optional[str]


def preference(
    pkg_name: str,
    constraint: spack.spec.Spec,
    condition: spack.spec.Spec = spack.spec.Spec(),
    origin: RequirementOrigin = RequirementOrigin.PREFER_YAML,
    kind: RequirementKind = RequirementKind.PACKAGE,
    message: Optional[str] = None,
) -> RequirementRule:
    """Returns a preference rule"""
    # A strong preference is defined as:
    #
    # require:
    # - any_of: [spec_str, "@:"]
    return RequirementRule(
        pkg_name=pkg_name,
        policy="any_of",
        requirements=[constraint, spack.spec.Spec("@:")],
        kind=kind,
        condition=condition,
        origin=origin,
        message=message,
    )


def conflict(
    pkg_name: str,
    constraint: spack.spec.Spec,
    condition: spack.spec.Spec = spack.spec.Spec(),
    origin: RequirementOrigin = RequirementOrigin.CONFLICT_YAML,
    kind: RequirementKind = RequirementKind.PACKAGE,
    message: Optional[str] = None,
) -> RequirementRule:
    """Returns a conflict rule"""
    # A conflict is defined as:
    #
    # require:
    # - one_of: [spec_str, "@:"]
    return RequirementRule(
        pkg_name=pkg_name,
        policy="one_of",
        requirements=[constraint, spack.spec.Spec("@:")],
        kind=kind,
        condition=condition,
        origin=origin,
        message=message,
    )


class RequirementParser:
    """Parses requirements from package.py files and configuration, and returns rules."""

    def __init__(self, configuration: spack.config.Configuration):
        self.config = configuration
        self.runtime_pkgs = spack.repo.PATH.packages_with_tags("runtime")
        self.compiler_pkgs = spack.repo.PATH.packages_with_tags("compiler")
        self.preferences_from_input: List[Tuple[spack.spec.Spec, str]] = []
        self.toolchains = configuration.get_config("toolchains")
        self._warned_compiler_all: set = set()

    def _parse_and_expand(self, string: str, *, named: bool = False) -> spack.spec.Spec:
        result = parse_spec_from_yaml_string(string, named=named)
        if self.toolchains:
            spack.spec_parser.expand_toolchains(result, self.toolchains)
        return result

    def rules(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        result = []
        result.extend(self.rules_from_input_specs(pkg))
        result.extend(self.rules_from_package_py(pkg))
        result.extend(self.rules_from_require(pkg))
        result.extend(self.rules_from_prefer(pkg))
        result.extend(self.rules_from_conflict(pkg))
        return result

    def parse_rules_from_input_specs(self, specs: Sequence[spack.spec.Spec]):
        self.preferences_from_input.clear()
        for edge in spack.traverse.traverse_edges(specs, root=False):
            if edge.propagation == PropagationPolicy.PREFERENCE:
                for constraint in _split_edge_on_virtuals(edge):
                    root_name = edge.parent.name
                    self.preferences_from_input.append((constraint, root_name))

    def rules_from_input_specs(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        return [
            preference(
                pkg.name,
                constraint=s,
                condition=spack.spec.Spec(f"{root_name} ^[deptypes=link,run]{pkg.name}"),
                origin=RequirementOrigin.INPUT_SPECS,
            )
            for s, root_name in self.preferences_from_input
        ]

    def rules_from_package_py(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        rules = []
        for when_spec, requirement_list in pkg.requirements.items():
            for requirements, policy, message in requirement_list:
                rules.append(
                    RequirementRule(
                        pkg_name=pkg.name,
                        policy=policy,
                        requirements=requirements,
                        kind=RequirementKind.PACKAGE,
                        condition=when_spec,
                        message=message,
                        origin=RequirementOrigin.DIRECTIVE,
                    )
                )
        return rules

    def rules_from_virtual(self, virtual_str: str) -> List[RequirementRule]:
        kind, requests = self._raw_yaml_data(virtual_str, section="require", virtual=True)
        result = self._rules_from_requirements(virtual_str, requests, kind=kind)

        kind, requests = self._raw_yaml_data(virtual_str, section="prefer", virtual=True)
        result.extend(self._rules_from_preferences(virtual_str, preferences=requests, kind=kind))

        kind, requests = self._raw_yaml_data(virtual_str, section="conflict", virtual=True)
        result.extend(self._rules_from_conflicts(virtual_str, conflicts=requests, kind=kind))

        return result

    def rules_from_require(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        kind, requirements = self._raw_yaml_data(pkg.name, section="require")
        return self._rules_from_requirements(pkg.name, requirements, kind=kind)

    def rules_from_prefer(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        kind, preferences = self._raw_yaml_data(pkg.name, section="prefer")
        return self._rules_from_preferences(pkg.name, preferences=preferences, kind=kind)

    def _rules_from_preferences(
        self, pkg_name: str, *, preferences, kind: RequirementKind
    ) -> List[RequirementRule]:
        result = []
        for item in preferences:
            if kind == RequirementKind.DEFAULT:
                # Warn about %gcc type of preferences under `all`.
                self._maybe_warn_compiler_in_all(item, "prefer")
            spec, condition, msg = self._parse_prefer_conflict_item(item)
            result.append(
                preference(pkg_name, constraint=spec, condition=condition, kind=kind, message=msg)
            )
        return result

    def rules_from_conflict(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        kind, conflicts = self._raw_yaml_data(pkg.name, section="conflict")
        return self._rules_from_conflicts(pkg.name, conflicts=conflicts, kind=kind)

    def _rules_from_conflicts(
        self, pkg_name: str, *, conflicts, kind: RequirementKind
    ) -> List[RequirementRule]:
        result = []
        for item in conflicts:
            spec, condition, msg = self._parse_prefer_conflict_item(item)
            result.append(
                conflict(pkg_name, constraint=spec, condition=condition, kind=kind, message=msg)
            )
        return result

    def _parse_prefer_conflict_item(self, item):
        # The item is either a string or an object with at least a "spec" attribute
        if isinstance(item, str):
            spec = self._parse_and_expand(item)
            condition = spack.spec.Spec()
            message = None
        else:
            spec = self._parse_and_expand(item["spec"])
            condition = spack.spec.Spec(item.get("when"))
            message = item.get("message")
        raw_key = item if isinstance(item, str) else item.get("spec", item)
        _check_unknown_targets([raw_key], [spec], always_warn=True)
        return spec, condition, message

    def _raw_yaml_data(self, pkg_name: str, *, section: str, virtual: bool = False):
        config = self.config.get_config("packages")
        data = config.get(pkg_name, {}).get(section, [])
        kind = RequirementKind.PACKAGE

        if virtual:
            return RequirementKind.VIRTUAL, data

        if not data:
            data = config.get("all", {}).get(section, [])
            kind = RequirementKind.DEFAULT
        return kind, data

    def _rules_from_requirements(
        self, pkg_name: str, requirements, *, kind: RequirementKind
    ) -> List[RequirementRule]:
        """Manipulate requirements from packages.yaml, and return a list of tuples
        with a uniform structure (name, policy, requirements).
        """
        if isinstance(requirements, str):
            requirements = [requirements]

        rules = []
        for requirement in requirements:
            # A string is equivalent to a one_of group with a single element
            if isinstance(requirement, str):
                requirement = {"one_of": [requirement]}

            for policy in ("spec", "one_of", "any_of"):
                if policy not in requirement:
                    continue

                constraints = requirement[policy]
                # "spec" is for specifying a single spec
                if policy == "spec":
                    constraints = [constraints]
                    policy = "one_of"

                if kind == RequirementKind.DEFAULT:
                    # Warn about %gcc type of requirements under `all`.
                    self._maybe_warn_compiler_in_all(constraints, "require")

                # validate specs from YAML first, and fail with line numbers if parsing fails.
                raw_strs = list(constraints)
                constraints = [
                    self._parse_and_expand(constraint, named=kind == RequirementKind.VIRTUAL)
                    for constraint in raw_strs
                ]
                _check_unknown_targets(raw_strs, constraints)
                when_str = requirement.get("when")
                when = self._parse_and_expand(when_str) if when_str else spack.spec.Spec()

                constraints = [
                    x
                    for x in constraints
                    if not self.reject_requirement_constraint(pkg_name, constraint=x, kind=kind)
                ]
                if not constraints:
                    continue

                rules.append(
                    RequirementRule(
                        pkg_name=pkg_name,
                        policy=policy,
                        requirements=constraints,
                        kind=kind,
                        message=requirement.get("message"),
                        condition=when,
                        origin=RequirementOrigin.REQUIRE_YAML,
                    )
                )
        return rules

    def reject_requirement_constraint(
        self, pkg_name: str, *, constraint: spack.spec.Spec, kind: RequirementKind
    ) -> bool:
        """Returns True if a requirement constraint should be rejected"""
        # If it's a specific package requirement, it's never rejected
        if kind != RequirementKind.DEFAULT:
            return False

        # Reject requirements with dependencies for runtimes and compilers
        # These are usually requests on compilers, in the form of %<compiler>
        involves_dependencies = bool(constraint.dependencies())
        if involves_dependencies and (
            pkg_name in self.runtime_pkgs or pkg_name in self.compiler_pkgs
        ):
            tty.debug(f"[{__name__}] Rejecting '{constraint}' for compiler package {pkg_name}")
            return True

        # Requirements under all: are applied only if they are satisfiable considering only
        # package rules, so e.g. variants must exist etc. Otherwise, they are rejected.
        try:
            s = spack.spec.Spec(pkg_name)
            s.constrain(constraint)
            s.validate_or_raise()
        except spack.error.SpackError as e:
            tty.debug(
                f"[{__name__}] Rejecting the default '{constraint}' requirement "
                f"on '{pkg_name}': {str(e)}"
            )
            return True
        return False

    def _maybe_warn_compiler_in_all(self, items: Union[str, list, dict], section: str) -> None:
        """Warn once if a packages:all: prefer/require entry has compiler dependencies."""
        # Stick to single items, not complex one_of / any_of groups to keep things simple.
        if isinstance(items, str):
            spec_str = items
        elif isinstance(items, dict) and "spec" in items and isinstance(items["spec"], str):
            spec_str = items["spec"]
        elif isinstance(items, list) and len(items) == 1 and isinstance(items[0], str):
            spec_str = items[0]
        else:
            return
        if spec_str in self._warned_compiler_all:
            return
        self._warned_compiler_all.add(spec_str)
        suggestions = []
        for edge in self._parse_and_expand(spec_str).edges_to_dependencies():
            if edge.when != spack.spec.EMPTY_SPEC:
                # Conditional dependencies are fine (includes toolchains after expansion).
                continue
            elif edge.virtuals:
                # The case `%c,cxx=gcc` or similar.
                keys = edge.virtuals
                comment = ""
            elif edge.spec.name in self.compiler_pkgs:
                # Just a package `%gcc`.
                keys = ("c",)
                comment = "# For each language virtual (c, cxx, fortran, ...):\n"
            else:
                # Maybe %mpich or so? Just give a generic suggestion.
                keys = ("<virtual>",)
                comment = "# For each virtual:\n"
            data = {"packages": {k: {section: [str(edge.spec)]} for k in keys}}
            suggestion = spack.util.spack_yaml.dump(data).rstrip()
            suggestions.append(f"{comment}{suggestion}")
        if suggestions:
            mark = get_mark_from_yaml_data(spec_str)
            location = f"{mark.name}:{mark.line + 1}: " if mark else ""
            prefix = (
                f"{location}'packages: all: {section}: [\"{spec_str}\"]' applies a dependency "
                f"constraint to all packages"
            )
            suffix = "Consider instead:\n" + "\n".join(suggestions)
            if section == "prefer":
                warnings.warn(
                    f"{prefix}. This can lead to unexpected concretizations. This was likely "
                    f"intended as a preference for a provider of a (language) virtual. {suffix}"
                )
            else:
                warnings.warn(
                    f"{prefix}. This often leads to concretization errors. This was likely "
                    f"intended as a requirement for a provider of a (language) virtual. {suffix}"
                )


def _split_edge_on_virtuals(edge: spack.spec.DependencySpec) -> List[spack.spec.Spec]:
    """Split the edge on virtuals and removes the parent."""
    if not edge.virtuals:
        return [spack.spec.Spec(str(edge.copy(keep_parent=False)))]

    result = []
    # We split on virtuals so that "%%c,cxx=gcc" enforces "%%c=gcc" and "%%cxx=gcc" separately
    for v in edge.virtuals:
        t = edge.copy(keep_parent=False, keep_virtuals=False)
        t.update_virtuals(v)
        t.when = spack.spec.Spec(f"%{v}")
        result.append(spack.spec.Spec(str(t)))

    return result


def parse_spec_from_yaml_string(string: str, *, named: bool = False) -> spack.spec.Spec:
    """Parse a spec from YAML and add file/line info to errors, if it's available.

    Parse a ``Spec`` from the supplied string, but also intercept any syntax errors and
    add file/line information for debugging using file/line annotations from the string.

    Args:
        string: a string representing a ``Spec`` from config YAML.
        named: if True, the spec must have a name
    """
    try:
        result = spack.spec.Spec(string)
    except spack.error.SpecSyntaxError as e:
        mark = get_mark_from_yaml_data(string)
        if mark:
            msg = f"{mark.name}:{mark.line + 1}: {str(e)}"
            raise spack.error.SpecSyntaxError(msg) from e
        raise e

    if named is True and not result.name:
        msg = f"expected a named spec, but got '{string}' instead"
        mark = get_mark_from_yaml_data(string)

        # Add a hint in case it's dependencies
        deps = result.dependencies()
        if len(deps) == 1:
            msg = f"{msg}. Did you mean '{deps[0]}'?"

        if mark:
            msg = f"{mark.name}:{mark.line + 1}: {msg}"

        raise spack.error.SpackError(msg)

    return result

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import itertools
from typing import Tuple

import spack.compilers.config
import spack.compilers.libraries
import spack.repo
import spack.spec
import spack.version

from .core import SourceContext, fn, using_libc_compatibility
from .versions import DeclaredVersion, Provenance


class RuntimePropertyRecorder:
    """An object of this class is injected in callbacks to compilers, to let them declare
    properties of the runtimes they support and of the runtimes they provide, and to add
    runtime dependencies to the nodes using said compiler.

    The usage of the object is the following. First, a runtime package name or the wildcard
    "*" are passed as an argument to __call__, to set which kind of package we are referring to.
    Then we can call one method with a directive-like API.

    Examples:
        >>> pkg = RuntimePropertyRecorder(setup)
        >>> # Every package compiled with %gcc has a link dependency on 'gcc-runtime'
        >>> pkg("*").depends_on(
        ...     "gcc-runtime",
        ...     when="%gcc",
        ...     type="link",
        ...     description="If any package uses %gcc, it depends on gcc-runtime"
        ... )
        >>> # The version of gcc-runtime is the same as the %gcc used to "compile" it
        >>> pkg("gcc-runtime").requires("@=9.4.0", when="%gcc@=9.4.0")
    """

    def __init__(self, setup):
        self._setup = setup
        self.rules = []
        self.runtime_conditions = set()
        self.injected_dependencies = set()
        # State of this object set in the __call__ method, and reset after
        # each directive-like method
        self.current_package = None

    def __call__(self, package_name: str) -> "RuntimePropertyRecorder":
        """Sets a package name for the next directive-like method call"""
        assert self.current_package is None, f"state was already set to '{self.current_package}'"
        self.current_package = package_name
        return self

    def reset(self):
        """Resets the current state."""
        self.current_package = None

    def depends_on(self, dependency_str: str, *, when: str, type: str, description: str) -> None:
        """Injects conditional dependencies on packages.

        Conditional dependencies can be either "real" packages or virtual dependencies.

        Args:
            dependency_str: the dependency spec to inject
            when: anonymous condition to be met on a package to have the dependency
            type: dependency type
            description: human-readable description of the rule for adding the dependency
        """
        # TODO: The API for this function is not final, and is still subject to change. At
        # TODO: the moment, we implemented only the features strictly needed for the
        # TODO: functionality currently provided by Spack, and we assert nothing else is required.
        msg = "the 'depends_on' method can be called only with pkg('*')"
        assert self.current_package == "*", msg

        when_spec = spack.spec.Spec(when)
        assert when_spec.name is None, "only anonymous when specs are accepted"

        dependency_spec = spack.spec.Spec(dependency_str)
        if dependency_spec.versions != spack.version.any_version:
            self._setup.version_constraints.add((dependency_spec.name, dependency_spec.versions))

        self.injected_dependencies.add(dependency_spec)
        body_str, node_variable = self.rule_body_from(when_spec)

        head_clauses = self._setup.spec_clauses(dependency_spec, body=False)
        runtime_pkg = dependency_spec.name
        is_virtual = head_clauses[0].args[0] == "virtual_node"
        main_rule = (
            f"% {description}\n"
            f'1 {{ attr("depends_on", {node_variable}, node(0..X-1, "{runtime_pkg}"), "{type}") :'
            f' max_dupes("{runtime_pkg}", X)}} 1:-\n'
            f"{body_str}.\n\n"
        )
        if is_virtual:
            main_rule = (
                f"% {description}\n"
                f'attr("dependency_holds", {node_variable}, "{runtime_pkg}", "{type}") :-\n'
                f"{body_str}.\n\n"
            )

        self.rules.append(main_rule)
        for clause in head_clauses:
            if clause.args[0] == "node":
                continue
            runtime_node = f'node(RuntimeID, "{runtime_pkg}")'
            head_str = str(clause).replace(f'"{runtime_pkg}"', runtime_node)
            depends_on_constraint = (
                f'  attr("depends_on", {node_variable}, {runtime_node}, "{type}"),\n'
            )
            if is_virtual:
                depends_on_constraint = (
                    f'  attr("depends_on", {node_variable}, ProviderNode, "{type}"),\n'
                    f"  provider(ProviderNode, {runtime_node}),\n"
                )

            rule = f"{head_str} :-\n" f"{depends_on_constraint}" f"{body_str}.\n\n"
            self.rules.append(rule)

        self.reset()

    @staticmethod
    def node_for(name: str) -> str:
        return f'node(ID{name.replace("-", "_")}, "{name}")'

    def rule_body_from(self, when_spec: "spack.spec.Spec") -> Tuple[str, str]:
        """Computes the rule body from a "when" spec, and returns it, along with the
        node variable.
        """

        node_placeholder = "XXX"
        node_variable = "node(ID, Package)"
        when_substitutions = {}
        for s in when_spec.traverse(root=False):
            when_substitutions[f'"{s.name}"'] = self.node_for(s.name)
        when_spec.name = node_placeholder
        body_clauses = self._setup.spec_clauses(when_spec, body=True)
        for clause in body_clauses:
            if clause.args[0] == "virtual_on_incoming_edges":
                # Substitute: attr("virtual_on_incoming_edges", ProviderNode, Virtual)
                # with: attr("virtual_on_edge", ParentNode, ProviderNode, Virtual)
                # (avoid adding virtuals everywhere, if a single edge needs it)
                _, provider, virtual = clause.args
                clause.args = "virtual_on_edge", node_placeholder, provider, virtual
        body_str = ",\n".join(f"  {x}" for x in body_clauses)
        body_str += f",\n  not external({node_variable})"
        body_str = body_str.replace(f'"{node_placeholder}"', f"{node_variable}")
        for old, replacement in when_substitutions.items():
            body_str = body_str.replace(old, replacement)
        return body_str, node_variable

    def requires(self, impose: str, *, when: str):
        """Injects conditional requirements on a given package.

        Args:
            impose: constraint to be imposed
            when: condition triggering the constraint
        """
        msg = "the 'requires' method cannot be called with pkg('*') or without setting the package"
        assert self.current_package is not None and self.current_package != "*", msg

        imposed_spec = spack.spec.Spec(f"{self.current_package}{impose}")
        when_spec = spack.spec.Spec(f"{self.current_package}{when}")

        assert imposed_spec.versions.concrete, f"{impose} must have a concrete version"

        # Add versions to possible versions
        for s in (imposed_spec, when_spec):
            if not s.versions.concrete:
                continue
            self._setup.possible_versions[s.name].add(s.version)
            self._setup.declared_versions[s.name].append(
                DeclaredVersion(version=s.version, idx=0, origin=Provenance.RUNTIME)
            )

        self.runtime_conditions.add((imposed_spec, when_spec))
        self.reset()

    def propagate(self, constraint_str: str, *, when: str):
        msg = "the 'propagate' method can be called only with pkg('*')"
        assert self.current_package == "*", msg

        when_spec = spack.spec.Spec(when)
        assert when_spec.name is None, "only anonymous when specs are accepted"

        when_substitutions = {}
        for s in when_spec.traverse(root=False):
            when_substitutions[f'"{s.name}"'] = self.node_for(s.name)

        body_str, node_variable = self.rule_body_from(when_spec)
        constraint_spec = spack.spec.Spec(constraint_str)

        constraint_clauses = self._setup.spec_clauses(constraint_spec, body=False)
        for clause in constraint_clauses:
            if clause.args[0] == "node_version_satisfies":
                self._setup.version_constraints.add(
                    (constraint_spec.name, constraint_spec.versions)
                )
                args = f'"{constraint_spec.name}", "{constraint_spec.versions}"'
                head_str = f"propagate({node_variable}, node_version_satisfies({args}))"
                rule = f"{head_str} :-\n{body_str}.\n\n"
                self.rules.append(rule)

        self.reset()

    def default_flags(self, spec: "spack.spec.Spec"):
        if not spec.external or "flags" not in spec.extra_attributes:
            self.reset()
            return

        when_spec = spack.spec.Spec(f"%[deptypes=build] {spec}")
        body_str, node_variable = self.rule_body_from(when_spec)

        node_placeholder = "XXX"
        flags = spec.extra_attributes["flags"]
        root_spec_str = f"{node_placeholder}"
        for flag_type, default_values in flags.items():
            root_spec_str = f"{root_spec_str} {flag_type}='{default_values}'"
        root_spec = spack.spec.Spec(root_spec_str)
        head_clauses = self._setup.spec_clauses(
            root_spec, body=False, context=SourceContext(source="compiler")
        )
        self.rules.append(f"% Default compiler flags for {spec}\n")
        for clause in head_clauses:
            if clause.args[0] == "node":
                continue
            head_str = str(clause).replace(f'"{node_placeholder}"', f"{node_variable}")
            rule = f"{head_str} :-\n{body_str}.\n\n"
            self.rules.append(rule)

        self.reset()

    def consume_facts(self):
        """Consume the facts collected by this object, and emits rules and
        facts for the runtimes.
        """
        self._setup.gen.h2("Runtimes: declarations")
        runtime_pkgs = sorted(
            {x.name for x in self.injected_dependencies if not spack.repo.PATH.is_virtual(x.name)}
        )
        for runtime_pkg in runtime_pkgs:
            self._setup.gen.fact(fn.runtime(runtime_pkg))
        self._setup.gen.newline()

        self._setup.gen.h2("Runtimes: rules")
        self._setup.gen.newline()
        for rule in self.rules:
            self._setup.gen.append(rule)
        self._setup.gen.newline()

        self._setup.gen.h2("Runtimes: requirements")
        for imposed_spec, when_spec in sorted(self.runtime_conditions):
            msg = f"{when_spec} requires {imposed_spec} at runtime"
            _ = self._setup.condition(when_spec, imposed_spec=imposed_spec, msg=msg)

        self._setup.trigger_rules()
        self._setup.effect_rules()


def _normalize_packages_yaml(packages_yaml):
    normalized_yaml = copy.copy(packages_yaml)
    for pkg_name in packages_yaml:
        is_virtual = spack.repo.PATH.is_virtual(pkg_name)
        if pkg_name == "all" or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = normalized_yaml.pop(pkg_name)
        is_buildable = data.get("buildable", True)
        if not is_buildable:
            for provider in spack.repo.PATH.providers_for(pkg_name):
                entry = normalized_yaml.setdefault(provider.name, {})
                entry["buildable"] = False

        externals = data.get("externals", [])

        def keyfn(x):
            return spack.spec.Spec(x["spec"]).name

        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = normalized_yaml.setdefault(provider, {})
            entry.setdefault("externals", []).extend(specs)

    return normalized_yaml


def _external_config_with_implicit_externals(configuration):
    # Read packages.yaml and normalize it so that it will not contain entries referring to
    # virtual packages.
    packages_yaml = _normalize_packages_yaml(configuration.get("packages"))

    # Add externals for libc from compilers on Linux
    if not using_libc_compatibility():
        return packages_yaml

    seen = set()
    for compiler in spack.compilers.config.all_compilers_from(configuration):
        libc = spack.compilers.libraries.CompilerPropertyDetector(compiler).default_libc()
        if libc and libc not in seen:
            seen.add(libc)
            entry = {"spec": f"{libc}", "prefix": libc.external_path}
            packages_yaml.setdefault(libc.name, {}).setdefault("externals", []).append(entry)
    return packages_yaml

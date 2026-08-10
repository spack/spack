# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes to analyze the input of a solve, and provide information to set up the ASP problem"""

import collections
from typing import Dict, List, NamedTuple, Set, Tuple, Union

import spack.vendor.archspec.cpu

import spack.binary_distribution
import spack.concretize
import spack.config
import spack.deptypes as dt
import spack.platforms
import spack.repo
import spack.spec
import spack.store
import spack.variant as vt
from spack.error import SpackError
from spack.spec import EMPTY_SPEC
from spack.util import lang, tty


class PossibleGraph(NamedTuple):
    real_pkgs: Set[str]
    virtuals: Set[str]
    edges: Dict[str, Set[str]]


class PossibleDependencyGraph:
    """Returns information needed to set up an ASP problem"""

    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        raise NotImplementedError

    def candidate_targets(self) -> List[spack.vendor.archspec.cpu.Microarchitecture]:
        """Returns a list of targets that are candidate for concretization"""
        raise NotImplementedError

    def possible_dependencies(
        self,
        *specs: Union[spack.spec.Spec, str],
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
        expand_virtuals: bool = True,
    ) -> PossibleGraph:
        """Returns the set of possible dependencies, and the set of possible virtuals.

        Runtime packages, which may be injected by compilers, needs to be added to specs if
        the dependency is not explicit in the package.py recipe.

        Args:
            transitive: return transitive dependencies if True, only direct dependencies if False
            allowed_deps: dependency types to consider
            strict_depflag: if True, only the specific dep type is considered, if False any
                deptype that intersects with allowed deptype is considered
            expand_virtuals: expand virtual dependencies into all possible implementations
        """
        raise NotImplementedError


class NoStaticAnalysis(PossibleDependencyGraph):
    """Implementation that tries to minimize the setup time (i.e. defaults to give fast
    answers), rather than trying to reduce the ASP problem size with more complex analysis.
    """

    def __init__(self, *, configuration: spack.config.Configuration, repo: spack.repo.RepoPath):
        self.configuration = configuration
        self.repo = repo
        self._platform_condition = spack.spec.Spec(
            f"platform={spack.platforms.host()} target={spack.vendor.archspec.cpu.host().family}:"
        )

        try:
            self.libc_pkgs = [x.name for x in self.providers_for("libc")]
        except spack.repo.UnknownPackageError:
            self.libc_pkgs = []

    def is_virtual(self, name: str) -> bool:
        return self.repo.is_virtual(name)

    @lang.memoized
    def is_allowed_on_this_platform(self, *, pkg_name: str) -> bool:
        """Returns true if a package is allowed on the current host"""
        pkg_cls = self.repo.get_pkg_class(pkg_name)
        for when_spec, conditions in pkg_cls.requirements.items():
            # Restrict analysis to unconditional requirements
            if when_spec != EMPTY_SPEC:
                continue
            for requirements, _, _ in conditions:
                if not any(x.intersects(self._platform_condition) for x in requirements):
                    tty.debug(f"[{__name__}] {pkg_name} is not for this platform")
                    return False
        return True

    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        """Returns a list of possible providers for the virtual string in input."""
        return self.repo.providers_for(virtual_str)

    def can_be_installed(self, *, pkg_name) -> bool:
        """Returns True if a package can be installed, False otherwise."""
        return True

    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        return False

    def variants_unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the variant constraints in
        when_spec cannot ever be met on pkg_name.
        """
        return False

    def candidate_targets(self) -> List[spack.vendor.archspec.cpu.Microarchitecture]:
        """Returns a list of targets that are candidate for concretization"""
        platform = spack.platforms.host()
        default_target = spack.vendor.archspec.cpu.TARGETS[platform.default]

        # Construct the list of targets which are compatible with the host
        candidate_targets = [default_target] + default_target.ancestors
        granularity = self.configuration.get("concretizer:targets:granularity")
        host_compatible = self.configuration.get("concretizer:targets:host_compatible")

        # Add targets which are not compatible with the current host
        if not host_compatible:
            additional_targets_in_family = sorted(
                [
                    t
                    for t in spack.vendor.archspec.cpu.TARGETS.values()
                    if (t.family.name == default_target.family.name and t not in candidate_targets)
                ],
                key=lambda x: len(x.ancestors),
                reverse=True,
            )
            candidate_targets += additional_targets_in_family

        # Check if we want only generic architecture
        if granularity == "generic":
            candidate_targets = [t for t in candidate_targets if t.vendor == "generic"]

        return candidate_targets

    def possible_dependencies(
        self,
        *specs: Union[spack.spec.Spec, str],
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
        expand_virtuals: bool = True,
    ) -> PossibleGraph:
        stack = [x for x in self._package_list(specs)]
        virtuals: Set[str] = set()
        edges: Dict[str, Set[str]] = {}

        while stack:
            pkg_name = stack.pop()

            if pkg_name in edges:
                continue

            edges[pkg_name] = set()

            # Since libc is not buildable, there is no need to extend the
            # search space with libc dependencies.
            if pkg_name in self.libc_pkgs:
                continue

            pkg_cls = self.repo.get_pkg_class(pkg_name=pkg_name)
            for when_spec, dependencies in pkg_cls.dependencies.items():
                # Check if we need to process this condition at all. We can skip the unreachable
                # check if all dependencies in this condition are already accounted for.
                new_dependencies: List[str] = []
                for name, dep in dependencies.items():
                    if strict_depflag:
                        if dep.depflag != allowed_deps:
                            continue
                    elif not (dep.depflag & allowed_deps):
                        continue

                    if name in edges[pkg_name] or name in virtuals:
                        continue

                    new_dependencies.append(name)

                if not new_dependencies:
                    continue

                if self.unreachable(
                    pkg_name=pkg_name, when_spec=when_spec
                ) or self.variants_unreachable(pkg_name=pkg_name, when_spec=when_spec):
                    tty.debug(
                        f"[{__name__}] Skipping {', '.join(new_dependencies)} dependencies of "
                        f"{pkg_name}, because {when_spec} is not met"
                    )
                    continue

                for name in new_dependencies:
                    dep_names: Set[str] = set()
                    if self.is_virtual(name):
                        virtuals.add(name)
                        if expand_virtuals:
                            providers = self.providers_for(name)
                            dep_names = {spec.name for spec in providers}
                    else:
                        dep_names = {name}

                    edges[pkg_name].update(dep_names)

                    if not transitive:
                        continue

                    for dep_name in dep_names:
                        if dep_name in edges:
                            continue

                        if not self._is_possible(pkg_name=dep_name):
                            continue

                        stack.append(dep_name)

        real_packages = set(edges)
        if not transitive:
            # We exit early, so add children from the edges information
            for root, children in edges.items():
                real_packages.update(x for x in children if self._is_possible(pkg_name=x))

        return PossibleGraph(real_pkgs=real_packages, virtuals=virtuals, edges=edges)

    def _package_list(self, specs: Tuple[Union[spack.spec.Spec, str], ...]) -> List[str]:
        stack = []
        for current_spec in specs:
            if isinstance(current_spec, str):
                current_spec = spack.spec.Spec(current_spec)

            if self.repo.is_virtual(current_spec.name):
                stack.extend([p.name for p in self.providers_for(current_spec.name)])
                continue

            stack.append(current_spec.name)
        return sorted(set(stack))

    def _has_deptypes(self, dependencies, *, allowed_deps: dt.DepFlag, strict: bool) -> bool:
        if strict is True:
            return any(
                dep.depflag == allowed_deps for deplist in dependencies.values() for dep in deplist
            )
        return any(
            dep.depflag & allowed_deps for deplist in dependencies.values() for dep in deplist
        )

    def _is_possible(self, *, pkg_name):
        try:
            return self.is_allowed_on_this_platform(pkg_name=pkg_name) and self.can_be_installed(
                pkg_name=pkg_name
            )
        except spack.repo.UnknownPackageError:
            return False


class StaticAnalysis(NoStaticAnalysis):
    """Performs some static analysis of the configuration, store, etc. to provide more precise
    answers on whether some packages can be installed, or used as a provider.

    It increases the setup time, but might decrease the grounding and solve time considerably,
    especially when requirements restrict the possible choices for providers.
    """

    def __init__(
        self,
        *,
        configuration: spack.config.Configuration,
        repo: spack.repo.RepoPath,
        store: spack.store.Store,
        binary_index: spack.binary_distribution.BinaryIndexCache,
    ):
        self.store = store
        self.binary_index = binary_index
        super().__init__(configuration=configuration, repo=repo)

        # Variant reachability state, accumulated across possible_dependencies calls. A
        # conditional dependency is pruned when its when-spec pins a variant to a value that
        # is neither the default nor imposable by any constraint in the problem. Keyed by
        # package name ("" applies to any package), then by variant name ("*" means every
        # variant); "*" among the values means every value.
        self._imposable: Dict[str, Dict[str, Set]] = collections.defaultdict(dict)
        #: package names that must be part of the closure although no surviving edge may
        #: reach them (named in the input, or nodes of reusable installed specs)
        self._extra_seeds: Set[str] = set()
        #: names of packages mentioned as dependencies in the input specs
        self._input_dep_names: Set[str] = set()
        #: packages whose requirements/conflicts/externals were already scanned
        self._scanned_pkgs: Set[str] = set()
        self._pruning_active = False
        self._config_seeded = False
        self._demand_cones_done = False

    @lang.memoized
    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        candidates = super().providers_for(virtual_str)
        result = []
        for spec in candidates:
            if not self._is_provider_candidate(pkg_name=spec.name, virtual=virtual_str):
                continue
            result.append(spec)
        return result

    @lang.memoized
    def buildcache_specs(self) -> List[spack.spec.Spec]:
        self.binary_index.update()
        return self.binary_index.get_all_built_specs()

    @lang.memoized
    def can_be_installed(self, *, pkg_name) -> bool:
        if self.configuration.get(f"packages:{pkg_name}:buildable", True):
            return True

        if self.configuration.get(f"packages:{pkg_name}:externals", []):
            return True

        reuse = self.configuration.get("concretizer:reuse")
        if reuse is not False and self.store.db.query(pkg_name):
            return True

        if reuse is not False and any(x.name == pkg_name for x in self.buildcache_specs()):
            return True

        tty.debug(f"[{__name__}] {pkg_name} cannot be installed")
        return False

    @lang.memoized
    def _is_provider_candidate(self, *, pkg_name: str, virtual: str) -> bool:
        if not self.is_allowed_on_this_platform(pkg_name=pkg_name):
            return False

        if not self.can_be_installed(pkg_name=pkg_name):
            return False

        virtual_spec = spack.spec.Spec(virtual)
        if self.unreachable(pkg_name=virtual_spec.name, when_spec=pkg_name):
            tty.debug(f"[{__name__}] {pkg_name} cannot be a provider for {virtual}")
            return False

        return True

    @lang.memoized
    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        candidates = self.configuration.get(f"packages:{pkg_name}:require", [])
        if not candidates and pkg_name != "all":
            return self.unreachable(pkg_name="all", when_spec=when_spec)

        if not candidates:
            return False

        if isinstance(candidates, str):
            candidates = [candidates]

        union_requirement = spack.spec.Spec()
        for c in candidates:
            if not isinstance(c, str):
                continue
            try:
                union_requirement.constrain(c)
            except SpackError:
                # Less optimized, but shouldn't fail
                pass

        if not union_requirement.intersects(when_spec):
            return True

        return False

    def possible_dependencies(
        self,
        *specs: Union[spack.spec.Spec, str],
        allowed_deps: dt.DepFlag,
        transitive: bool = True,
        strict_depflag: bool = False,
        expand_virtuals: bool = True,
    ) -> PossibleGraph:
        if not transitive:
            # Direct-dependency queries are used to validate input specs, and must not be
            # subject to variant pruning.
            return super().possible_dependencies(
                *specs,
                allowed_deps=allowed_deps,
                transitive=transitive,
                strict_depflag=strict_depflag,
                expand_virtuals=expand_virtuals,
            )

        self._seed_free_variants(specs)
        root_names = self._package_list(specs)
        self._pruning_active = True
        try:
            while True:
                graph = super().possible_dependencies(
                    *specs,
                    *sorted(self._extra_seeds),
                    allowed_deps=allowed_deps,
                    transitive=transitive,
                    strict_depflag=strict_depflag,
                    expand_virtuals=expand_virtuals,
                )
                changed = self._extend_free_variants(graph)
                changed |= self._add_reusable_spec_nodes(graph)
                if not changed and not self._demand_cones_done:
                    changed = self._add_demand_cones(root_names, graph)
                    self._demand_cones_done = True
                if not changed:
                    return graph
        finally:
            self._pruning_active = False

    def variants_unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        if not self._pruning_active:
            return False

        arch = when_spec.architecture
        if arch is not None and not arch.intersects(self._platform_condition.architecture):
            return True

        if not when_spec.variants:
            return False

        # Constraints on other nodes cannot be analyzed here: keep the condition
        if when_spec.dependencies():
            return False

        global_imposable = self._imposable.get("", {})
        pkg_imposable = self._imposable.get(pkg_name, {})
        if "*" in global_imposable or "*" in pkg_imposable:
            return False

        try:
            pkg_cls = self.repo.get_pkg_class(pkg_name)
        except spack.repo.UnknownPackageError:
            return False

        for name, constraint in when_spec.variants.items():
            candidates: Set = set()
            candidates.update(pkg_imposable.get(name, ()))
            candidates.update(global_imposable.get(name, ()))
            if "*" in candidates:
                continue
            definitions = pkg_cls.variant_definitions(name)
            if not definitions:
                # Not a variant this analysis knows about (e.g. dev_path)
                continue
            # The when-spec of a definition only gates its existence, so the possible
            # default values are the union over all definitions
            for _, variant_definition in definitions:
                candidates.update(variant_definition.make_default().values)
            if set(constraint.values) <= candidates:
                continue
            return True

        return False

    def _impose(self, target: str, variant_name: str, values) -> bool:
        """Records that the given values can be imposed on a variant of target ("" means
        on any package), and returns True if that was not known before."""
        known = self._imposable[target].setdefault(variant_name, set())
        before = len(known)
        known.update(values)
        return len(known) != before

    def _mark_node_variants(
        self, node: spack.spec.Spec, target: str, complement: bool = False
    ) -> bool:
        """Marks the variant values constrained on this single node as imposable on
        target. With complement=True the opposite values are marked instead: a constraint
        appearing in a conflict can force any value but its own."""
        changed = False
        for variant_name, variant in node.variants.items():
            where = "" if variant.propagate else target
            if not complement:
                values = variant.values
            elif variant.type == vt.VariantType.BOOL:
                values = [not v for v in variant.values]
            else:
                values = ["*"]
            changed |= self._impose(where, variant_name, values)
        return changed

    def _mark_spec_variants(
        self, spec: spack.spec.Spec, default_target: str, complement: bool = False
    ) -> bool:
        """Marks every variant value constrained by any node of spec as imposable on that
        node's package (anonymous nodes count towards default_target)."""
        changed = False
        for node in spec.traverse():
            changed |= self._mark_node_variants(node, node.name or default_target, complement)
        return changed

    def _mark_constraint_string(self, constraint_str: str, default_target: str) -> bool:
        try:
            constraint = spack.spec.Spec(constraint_str)
        except SpackError:
            # An unparsable constraint disables pruning for its target
            return self._impose(default_target, "*", ["*"])
        return self._mark_spec_variants(constraint, default_target)

    def _seed_free_variants(self, specs: Tuple[Union[spack.spec.Spec, str], ...]) -> None:
        if not self._config_seeded:
            self._config_seeded = True
            self._seed_from_configuration()

        for current_spec in specs:
            if not isinstance(current_spec, spack.spec.Spec):
                continue
            for node in current_spec.traverse():
                if node.concrete:
                    # Concrete nodes are imposed by hash, and only need their packages in
                    # the closure
                    self._add_seed(node.name)
                    continue
                self._mark_node_variants(node, node.name or "")
                if node is not current_spec and node.name:
                    self._input_dep_names.add(node.name)
                    self._add_seed(node.name)

    def _add_seed(self, name: str) -> bool:
        """Adds a package to the closure roots, if it exists in the repo."""
        if name in self._extra_seeds:
            return False
        if self.is_virtual(name):
            self._extra_seeds.add(name)
            return True
        try:
            self.repo.get_pkg_class(name)
        except spack.repo.UnknownPackageError:
            return False
        self._extra_seeds.add(name)
        return True

    def _seed_from_configuration(self) -> None:
        for pkg_name, entry in self.configuration.get("packages", {}).items():
            target = "" if pkg_name == "all" else pkg_name
            for constraint_str in _requirement_strings(entry.get("require", [])):
                self._mark_constraint_string(constraint_str, target)
            preferences = entry.get("variants", [])
            if isinstance(preferences, str):
                preferences = [preferences]
            for preference in preferences:
                self._mark_constraint_string(preference, target)
            for external in entry.get("externals", []):
                self._mark_constraint_string(external.get("spec", ""), target)

    def _extend_free_variants(self, graph: PossibleGraph) -> bool:
        """Marks variants settable by directives of the packages in the graph. Constraints
        from conditional dependencies only count when their condition can still hold, so
        this is repeated until a fixpoint is reached."""
        changed = False
        for pkg_name in sorted(graph.real_pkgs):
            try:
                pkg_cls = self.repo.get_pkg_class(pkg_name)
            except spack.repo.UnknownPackageError:
                continue

            for when_spec, deps_by_name in pkg_cls.dependencies.items():
                if self.unreachable(
                    pkg_name=pkg_name, when_spec=when_spec
                ) or self.variants_unreachable(pkg_name=pkg_name, when_spec=when_spec):
                    continue
                for dep_name, dep in deps_by_name.items():
                    changed |= self._mark_spec_variants(dep.spec, default_target=dep_name)

            if pkg_name in self._scanned_pkgs:
                continue
            self._scanned_pkgs.add(pkg_name)

            for when_spec, requirement_list in pkg_cls.requirements.items():
                for requirements, _, _ in requirement_list:
                    for requirement in requirements:
                        changed |= self._mark_spec_variants(requirement, default_target=pkg_name)

            # A conflict can force the complement of any variant value it mentions
            for when_spec, conflict_list in pkg_cls.conflicts.items():
                changed |= self._mark_spec_variants(
                    when_spec, default_target=pkg_name, complement=True
                )
                for conflict_spec, _ in conflict_list:
                    changed |= self._mark_spec_variants(
                        conflict_spec, default_target=pkg_name, complement=True
                    )

        return changed

    @lang.memoized
    def _reusable_specs(self) -> List[spack.spec.Spec]:
        if self.configuration.get("concretizer:reuse") is False:
            return []
        # TODO: this considers installed specs, but not buildcache specs, as roots that
        # can be reused and impose their whole DAG
        return self.store.db.query()

    def _add_reusable_spec_nodes(self, graph: PossibleGraph) -> bool:
        """Adds to the closure the nodes of reusable specs whose root package is in the
        closure: imposing such a spec by hash requires all packages of its DAG."""
        changed = False
        for spec in self._reusable_specs():
            if spec.name not in graph.real_pkgs:
                continue
            for node in spec.traverse(root=False):
                if node.name in graph.real_pkgs:
                    continue
                changed |= self._add_seed(node.name)
        return changed

    def _add_demand_cones(self, root_names: List[str], graph: PossibleGraph) -> bool:
        """Frees all variants of packages that can lead to a package mentioned in the
        input but not reachable through surviving edges, so the solver can toggle a path
        to it (e.g. ``cmake ^mpich``)."""
        targets: Set[str] = set()
        for name in self._input_dep_names:
            if self.is_virtual(name):
                targets.update(x.name for x in self.providers_for(name))
            else:
                targets.add(name)
        targets.difference_update(_forward_reachable(root_names, graph.edges))
        if not targets:
            return False

        self._pruning_active = False
        try:
            full = super().possible_dependencies(*root_names, allowed_deps=dt.ALL)
        finally:
            self._pruning_active = True

        parents: Dict[str, Set[str]] = collections.defaultdict(set)
        for parent, children in full.edges.items():
            for child in children:
                parents[child].add(parent)

        changed = False
        for target in targets:
            for ancestor in _forward_reachable([target], parents):
                changed |= self._impose(ancestor, "*", ["*"])
        return changed


def _forward_reachable(roots: List[str], edges: Dict[str, Set[str]]) -> Set[str]:
    """Returns the set of nodes reachable from roots in the given adjacency map."""
    reachable = set(roots)
    stack = list(roots)
    while stack:
        for child in edges.get(stack.pop(), ()):
            if child not in reachable:
                reachable.add(child)
                stack.append(child)
    return reachable


def _requirement_strings(value) -> List[str]:
    """Flattens a packages:<name>:require config entry into its constraint strings."""
    if isinstance(value, str):
        return [value]
    result = []
    entries = value if isinstance(value, list) else [value]
    for entry in entries:
        if isinstance(entry, str):
            result.append(entry)
        elif isinstance(entry, dict):
            for key in ("one_of", "any_of"):
                result.extend(x for x in entry.get(key, []) if isinstance(x, str))
            if isinstance(entry.get("spec"), str):
                result.append(entry["spec"])
    return result


def create_graph_analyzer() -> PossibleDependencyGraph:
    static_analysis = spack.config.CONFIG.get("concretizer:static_analysis", False)
    if static_analysis:
        return StaticAnalysis(
            configuration=spack.config.CONFIG,
            repo=spack.repo.PATH,
            store=spack.store.STORE,
            binary_index=spack.binary_distribution.BINARY_INDEX,
        )
    return NoStaticAnalysis(configuration=spack.config.CONFIG, repo=spack.repo.PATH)


class Counter:
    """Computes the possible packages and the maximum number of duplicates
    allowed for each of them.

    Args:
        specs: abstract specs to concretize
        tests: if True, add test dependencies to the list of possible packages
    """

    def __init__(
        self,
        specs: List[spack.spec.Spec],
        tests: spack.concretize.TestsType,
        possible_graph: PossibleDependencyGraph,
    ) -> None:
        self.possible_graph = possible_graph
        self.specs = specs
        self.link_run_types: dt.DepFlag = dt.LINK | dt.RUN | dt.TEST
        self.all_types: dt.DepFlag = dt.ALL
        if not tests:
            self.link_run_types = dt.LINK | dt.RUN
            self.all_types = dt.LINK | dt.RUN | dt.BUILD

        self._possible_dependencies: Set[str] = set()
        self._possible_virtuals: Set[str] = {
            x.name for x in specs if spack.repo.PATH.is_virtual(x.name)
        }

    def possible_dependencies(self) -> Set[str]:
        """Returns the list of possible dependencies"""
        self.ensure_cache_values()
        return self._possible_dependencies

    def possible_virtuals(self) -> Set[str]:
        """Returns the list of possible virtuals"""
        self.ensure_cache_values()
        return self._possible_virtuals

    def ensure_cache_values(self) -> None:
        """Ensure the cache values have been computed"""
        if self._possible_dependencies:
            return
        self._compute_cache_values()

    def possible_packages_facts(self, gen: "spack.solver.asp.ProblemInstanceBuilder", fn) -> None:
        """Emit facts associated with the possible packages"""
        raise NotImplementedError("must be implemented by derived classes")

    def _compute_cache_values(self) -> None:
        raise NotImplementedError("must be implemented by derived classes")


class NoDuplicatesCounter(Counter):
    def _compute_cache_values(self) -> None:
        self._possible_dependencies, virtuals, _ = self.possible_graph.possible_dependencies(
            *self.specs, allowed_deps=self.all_types
        )
        self._possible_virtuals.update(virtuals)

    def possible_packages_facts(self, gen: "spack.solver.asp.ProblemInstanceBuilder", fn) -> None:
        gen.h2("Maximum number of nodes (packages)")
        for package_name in sorted(self.possible_dependencies()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()
        gen.h2("Maximum number of nodes (virtual packages)")
        for package_name in sorted(self.possible_virtuals()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()
        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self.possible_dependencies()):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()


class MinimalDuplicatesCounter(NoDuplicatesCounter):
    def __init__(
        self,
        specs: List[spack.spec.Spec],
        tests: spack.concretize.TestsType,
        possible_graph: PossibleDependencyGraph,
    ) -> None:
        super().__init__(specs, tests, possible_graph)
        self._link_run: Set[str] = set()
        self._direct_build: Set[str] = set()
        self._total_build: Set[str] = set()
        self._link_run_virtuals: Set[str] = set()

    def _compute_cache_values(self) -> None:
        self._link_run, virtuals, _ = self.possible_graph.possible_dependencies(
            *self.specs, allowed_deps=self.link_run_types
        )
        self._possible_virtuals.update(virtuals)
        self._link_run_virtuals.update(virtuals)
        if self._link_run:
            reals, virtuals, _ = self.possible_graph.possible_dependencies(
                *self._link_run, allowed_deps=dt.BUILD, transitive=False, strict_depflag=True
            )
            self._possible_virtuals.update(virtuals)
            self._direct_build.update(reals)

        self._total_build, virtuals, _ = self.possible_graph.possible_dependencies(
            *self._direct_build, allowed_deps=self.all_types
        )
        self._possible_virtuals.update(virtuals)
        self._possible_dependencies = set(self._link_run) | set(self._total_build)

    def possible_packages_facts(self, gen, fn):
        build_tools = set()
        for current_tag in ("build-tools", "compiler"):
            build_tools.update(spack.repo.PATH.packages_with_tags(current_tag))

        gen.h2("Packages with at most a single node")
        for package_name in sorted(self.possible_dependencies() - build_tools):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()

        gen.h2("Packages with multiple possible nodes (build-tools)")
        default = spack.config.CONFIG.get("concretizer:duplicates:max_dupes:default", 1)
        duplicates = spack.config.CONFIG.get("concretizer:duplicates:max_dupes", {})
        for package_name in sorted(self.possible_dependencies() & build_tools):
            max_dupes = duplicates.get(package_name, default)
            gen.fact(fn.max_dupes(package_name, max_dupes))
            if max_dupes > 1:
                gen.fact(fn.multiple_unification_sets(package_name))
        gen.newline()

        gen.h2("Maximum number of nodes (virtuals)")
        for package_name in sorted(self.possible_virtuals()):
            max_dupes = duplicates.get(package_name, default)
            gen.fact(fn.max_dupes(package_name, max_dupes))
        gen.newline()

        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self._link_run):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()


class FullDuplicatesCounter(MinimalDuplicatesCounter):
    def possible_packages_facts(self, gen, fn):
        counter = collections.Counter(
            list(self._link_run) + list(self._total_build) + list(self._direct_build)
        )
        gen.h2("Maximum number of nodes")
        for pkg, count in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            count = min(count, 2)
            gen.fact(fn.max_dupes(pkg, count))
        gen.newline()

        gen.h2("Build unification sets ")
        build_tools = set()
        for current_tag in ("build-tools", "compiler"):
            build_tools.update(spack.repo.PATH.packages_with_tags(current_tag))

        for name in sorted(self.possible_dependencies() & build_tools):
            gen.fact(fn.multiple_unification_sets(name))
        gen.newline()

        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self._link_run):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()

        counter = collections.Counter(
            list(self._link_run_virtuals) + list(self._possible_virtuals)
        )
        gen.h2("Maximum number of virtual nodes")
        for pkg, count in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            gen.fact(fn.max_dupes(pkg, count))
        gen.newline()


def create_counter(
    specs: List[spack.spec.Spec],
    tests: spack.concretize.TestsType,
    possible_graph: PossibleDependencyGraph,
) -> Counter:
    strategy = spack.config.CONFIG.get("concretizer:duplicates:strategy", "none")
    if strategy == "full":
        return FullDuplicatesCounter(specs, tests=tests, possible_graph=possible_graph)
    if strategy == "minimal":
        return MinimalDuplicatesCounter(specs, tests=tests, possible_graph=possible_graph)
    return NoDuplicatesCounter(specs, tests=tests, possible_graph=possible_graph)

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Translation of specs into the ASP facts that describe them."""

import collections
import itertools
from typing import Dict, List, Optional, Set, Tuple, Type, Union

import spack.vendor.archspec.cpu

import spack.deptypes as dt
import spack.package_base
import spack.platforms
import spack.repo
import spack.spec
import spack.variant as vt
import spack.version as vn
from spack.spec import EMPTY_SPEC

from .core import AspFunction, SourceContext, fn


def libc_is_compatible(lhs: spack.spec.Spec, rhs: spack.spec.Spec) -> bool:
    return (
        lhs.name == rhs.name
        and lhs.external_path == rhs.external_path
        and lhs.version >= rhs.version
    )


class _Head:
    """ASP functions used to express spec clauses in the HEAD of a rule"""

    node = fn.attr("node")
    namespace = fn.attr("namespace_set")
    virtual_node = fn.attr("virtual_node")
    node_platform = fn.attr("node_platform_set")
    node_os = fn.attr("node_os_set")
    node_target = fn.attr("node_target_set")
    variant_value = fn.attr("variant_set")
    node_flag = fn.attr("node_flag_set")
    propagate = fn.attr("propagate")


class _Body:
    """ASP functions used to express spec clauses in the BODY of a rule"""

    node = fn.attr("node")
    namespace = fn.attr("namespace")
    virtual_node = fn.attr("virtual_node")
    node_platform = fn.attr("node_platform")
    node_os = fn.attr("node_os")
    node_target = fn.attr("node_target")
    variant_value = fn.attr("variant_value")
    node_flag = fn.attr("node_flag")
    propagate = fn.attr("propagate")


class SpecClauseGenerator:
    """Translates specs into the ASP facts that describe them.

    Generating clauses also discovers constraints that the solver setup turns into facts
    later: the version and target constraints that were mentioned, and the variant values
    that were seen. They accumulate here, and are read back once clause generation is done.
    """

    def __init__(
        self,
        *,
        libcs: Optional[List[spack.spec.Spec]] = None,
        explicitly_required_namespaces: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Arguments:
            libcs: libcs available on the system, used for compatibility clauses
            explicitly_required_namespaces: package name to namespace, for specs that
                requested one explicitly
        """
        self.libcs = libcs if libcs is not None else []
        self.explicitly_required_namespaces = (
            explicitly_required_namespaces if explicitly_required_namespaces is not None else {}
        )
        self.version_constraints: Dict[str, Set] = collections.defaultdict(set)
        self.target_constraints: Set = set()
        self.variant_values_from_specs: Set = set()

    def record_version_constraint(self, name: str, versions) -> None:
        """Record that `versions` was requested for package `name`."""
        self.version_constraints[name].add(versions)

    def record_variant_value(self, pkg_name: str, variant_def, value) -> None:
        """Record that `value` was seen for a variant defined by `variant_def`."""
        self.variant_values_from_specs.add((pkg_name, id(variant_def), value))

    def spec_versions(
        self, spec: spack.spec.Spec, *, name: Optional[str] = None
    ) -> List[AspFunction]:
        """Return list of clauses expressing spec's version constraints."""
        name = spec.name or name
        assert name, "Internal Error: spec with no name occurred. Please file an issue."

        if spec.concrete:
            return [fn.attr("version", name, spec.version)]

        if spec.versions == vn.any_version:
            return []

        # record all version constraints for later
        self.version_constraints[name].add(spec.versions)
        return [fn.attr("node_version_satisfies", name, spec.versions)]

    def target_ranges(
        self, spec: spack.spec.Spec, single_target_fn, *, name: Optional[str] = None
    ) -> List[AspFunction]:
        name = spec.name or name
        assert name, "Internal Error: spec with no name occurred. Please file an issue."
        target = spec.architecture.target

        # target is unconstrained
        if str(target) == ":":
            return []

        # Check if the target is a concrete target
        if str(target) in spack.vendor.archspec.cpu.TARGETS:
            return [single_target_fn(name, target)]

        self.target_constraints.add(target)
        return [fn.attr("node_target_satisfies", name, target)]

    def spec_clauses(
        self,
        spec: spack.spec.Spec,
        *,
        name: Optional[str] = None,
        body: bool = False,
        transitive: bool = True,
        expand_hashes: bool = False,
        concrete_build_deps=False,
        include_runtimes=False,
        required_from: Optional[str] = None,
        context: Optional[SourceContext] = None,
    ) -> List[AspFunction]:
        """Wrap a call to ``_spec_clauses()`` into a try/except block with better error handling.

        Arguments are as for ``_spec_clauses()`` except ``required_from``.

        Arguments:
            required_from: name of package that caused this call.
        """
        try:
            clauses = self._spec_clauses(
                spec,
                name=spec.name or name,
                body=body,
                transitive=transitive,
                expand_hashes=expand_hashes,
                concrete_build_deps=concrete_build_deps,
                include_runtimes=include_runtimes,
                context=context,
            )
        except RuntimeError as exc:
            msg = str(exc)
            if required_from:
                msg += f" [required from package '{required_from}']"
            raise RuntimeError(msg)
        return clauses

    def _arch_clauses(self, spec: spack.spec.Spec, f, *, name: str) -> List[AspFunction]:
        """Return clauses for the architecture of a spec."""
        # seed architecture at the root (we'll propagate later)
        # TODO: use better semantics.
        arch = spec.architecture
        if not arch:
            return []

        clauses = []
        if arch.platform:
            clauses.append(f.node_platform(name, arch.platform))
        if arch.os:
            clauses.append(f.node_os(name, arch.os))
        if arch.target:
            clauses.extend(self.target_ranges(spec, f.node_target, name=name))
        return clauses

    def _variant_clauses(
        self, spec: spack.spec.Spec, f, *, name: str, body: bool
    ) -> List[AspFunction]:
        """Return clauses for the variants of a spec."""
        clauses = []
        for vname, variant in sorted(spec.variants.items()):
            # TODO: variant="*" means 'variant is defined to something', which used to
            # be meaningless in concretization, as all variants had to be defined. But
            # now that variants can be conditional, it should force a variant to exist.
            if not variant.values:
                continue

            for value in variant.values:
                # ensure that the value *can* be valid for the spec
                if name and not spec.concrete and not spack.repo.PATH.is_virtual(name):
                    variant_defs = vt.prevalidate_variant_value(
                        self.pkg_class(name), variant, spec
                    )

                    # Record that that this is a valid possible value. Accounts for
                    # int/str/etc., where valid values can't be listed in the package
                    for variant_def in variant_defs:
                        self.variant_values_from_specs.add((name, id(variant_def), value))

                if variant.propagate:
                    clauses.append(f.propagate(name, fn.variant_value(vname, value)))
                    if self.pkg_class(name).has_variant(vname):
                        clauses.append(f.variant_value(name, vname, value))
                    continue

                variant_clause = f.variant_value(name, vname, value)
                if variant.concrete and variant.type == vt.VariantType.MULTI and not spec.concrete:
                    if body is False:
                        variant_clause.args = (
                            f"concrete_{variant_clause.args[0]}",
                            *variant_clause.args[1:],
                        )
                    else:
                        clauses.append(fn.attr("concrete_variant_request", name, vname, value))
                clauses.append(variant_clause)
        return clauses

    def _flag_clauses(
        self, spec: spack.spec.Spec, f, *, name: str, context: Optional[SourceContext]
    ) -> List[AspFunction]:
        """Return clauses for the compiler flags of a spec."""
        source = context.source if context else "none"
        clauses = []
        for flag_type, flags in spec.compiler_flags.items():
            flag_group = " ".join(flags)
            for flag in flags:
                clauses.append(
                    f.node_flag(name, fn.node_flag(flag_type, flag, flag_group, source))
                )
                if not spec.concrete and flag.propagate is True:
                    clauses.append(
                        f.propagate(
                            name,
                            fn.node_flag(flag_type, flag, flag_group, source),
                            fn.edge_types("link", "run"),
                        )
                    )
        return clauses

    def _virtuals_from_dependents(
        self, spec: spack.spec.Spec, *, name: str, body: bool
    ) -> List[AspFunction]:
        """Return clauses for the virtuals a spec provides on its incoming edges."""
        # TODO: a loop over `edges_to_dependencies` is preferred over `edges_from_dependents`
        # since dependents can point to specs out of scope for the solver.
        edges = spec.edges_from_dependents()
        clauses = []
        if not body and not spec.concrete:
            virtuals = sorted(set(itertools.chain.from_iterable(edge.virtuals for edge in edges)))
            for virtual in virtuals:
                clauses.append(fn.attr("provider_set", name, virtual))
                clauses.append(fn.attr("virtual_node", virtual))
            return clauses

        # direct dependencies are handled under `edges_to_dependencies()`
        virtual_iter = (edge.virtuals for edge in edges if not edge.direct)
        virtuals = sorted(set(itertools.chain.from_iterable(virtual_iter)))
        for virtual in virtuals:
            clauses.append(fn.attr("virtual_on_incoming_edges", name, virtual))
        return clauses

    def _concrete_edge_clauses(
        self,
        dspec: spack.spec.DependencySpec,
        *,
        name: str,
        concrete_build_deps: bool,
        include_runtimes: bool,
    ) -> Tuple[List[AspFunction], bool]:
        """Return clauses for an edge of a concrete spec, and whether the dependency at the
        other end still has to be traversed."""
        dep = dspec.spec
        clauses: List[AspFunction] = []

        # GCC runtime is solved again by clingo, even on concrete specs, to give
        # the possibility to reuse specs built against a different runtime.
        if dep.name == "gcc-runtime":
            clauses.append(fn.attr("compatible_runtime", name, dep.name, f"{dep.version}:"))
            constraint_spec = spack.spec.Spec(f"{dep.name}@{dep.version}")
            self.spec_versions(constraint_spec)
            if not include_runtimes:
                return clauses, False

        # libc is also solved again by clingo, but in this case the compatibility
        # is not encoded in the parent node - so we need to emit explicit facts
        if "libc" in dspec.virtuals:
            clauses.append(fn.attr("needs_libc", name))
            for libc in self.libcs:
                if libc_is_compatible(libc, dep):
                    clauses.append(fn.attr("compatible_libc", name, libc.name, libc.version))
            if not include_runtimes:
                return clauses, False

        # We know dependencies are real for concrete specs. For abstract
        # specs they just mean the dep is somehow in the DAG.
        for dtype in dt.ALL_FLAGS:
            if not dspec.depflag & dtype:
                continue
            # skip build dependencies of already-installed specs
            if concrete_build_deps or dtype != dt.BUILD:
                clauses.append(fn.attr("depends_on", name, dep.name, dt.flag_to_string(dtype)))
                for virtual_name in dspec.virtuals:
                    clauses.append(fn.attr("virtual_on_edge", name, dep.name, virtual_name))
                    clauses.append(fn.attr("virtual_node", virtual_name))

        # imposing hash constraints for all but pure build deps of
        # already-installed concrete specs.
        if concrete_build_deps or dspec.depflag != dt.BUILD:
            clauses.append(fn.attr("hash", dep.name, dep.dag_hash()))
        elif not concrete_build_deps and dspec.depflag:
            clauses.append(fn.attr("concrete_build_dependency", name, dep.name, dep.dag_hash()))
            for virtual_name in dspec.virtuals:
                clauses.append(fn.attr("virtual_on_build_edge", name, dep.name, virtual_name))

        return clauses, True

    def _dependency_edge_clauses(
        self,
        dspec: spack.spec.DependencySpec,
        dependency_clauses: List[AspFunction],
        *,
        name: str,
        body: bool,
        context: Optional[SourceContext],
    ) -> List[AspFunction]:
        """Return the clauses of a dependency, attached to the edge that reaches it."""
        ###
        # Dependency expressed with "^"
        ###
        if not dspec.direct:
            return dependency_clauses

        ###
        # Direct dependencies expressed with "%"
        ###
        dep = dspec.spec
        clauses = [
            fn.attr("depends_on", name, dep.name, dependency_type)
            for dependency_type in dt.flag_to_tuple(dspec.depflag)
        ]

        for virtual in dspec.virtuals:
            dependency_clauses.append(fn.attr("virtual_on_edge", name, dep.name, virtual))

        # By default, wrap head of rules, unless the context says otherwise
        wrap_node_requirement = body is False
        if context and context.wrap_node_requirement is not None:
            wrap_node_requirement = context.wrap_node_requirement

        if not wrap_node_requirement:
            clauses.extend(dependency_clauses)
            return clauses

        for clause in dependency_clauses:
            clause.name = "node_requirement"
            clauses.append(fn.attr("direct_dependency", name, clause))
        return clauses

    def _spec_clauses(
        self,
        spec: spack.spec.Spec,
        *,
        name: Optional[str] = None,
        body: bool = False,
        transitive: bool = True,
        expand_hashes: bool = False,
        concrete_build_deps: bool = False,
        include_runtimes: bool = False,
        context: Optional[SourceContext] = None,
        seen: Optional[Set[int]] = None,
    ) -> List[AspFunction]:
        """Return a list of clauses for a spec mandates are true.

        Arguments:
            spec: the spec to analyze
            name: optional fallback of spec.name (used for anonymous roots)
            body: if True, generate clauses to be used in rule bodies (final values) instead
                of rule heads (setters).
            transitive: if False, don't generate clauses from dependencies (default True)
            expand_hashes: if True, descend into hashes of concrete specs (default False)
            concrete_build_deps: if False, do not include pure build deps of concrete specs
                (as they have no effect on runtime constraints)
            include_runtimes: generate full dependency clauses from runtime libraries that
                are omitted from the solve.
            context: tracks what constraint this clause set is generated for (e.g. a
                ``depends_on`` constraint in a package.py file)
            seen: set of ids of specs that have already been processed (for internal use only)

        Normally, if called with ``transitive=True``, ``spec_clauses()`` just generates
        hashes for the dependency requirements of concrete specs. If ``expand_hashes``
        is ``True``, we'll *also* output all the facts implied by transitive hashes,
        which are redundant during a solve but useful outside of one (e.g.,
        for spec ``diff``).
        """
        clauses = []
        seen = seen if seen is not None else set()
        name = spec.name or name or ""
        seen.add(id(spec))

        f: Union[Type[_Head], Type[_Body]] = _Body if body else _Head

        if name:
            clauses.append(
                f.node(name) if not spack.repo.PATH.is_virtual(name) else f.virtual_node(name)
            )
        if spec.namespace:
            clauses.append(f.namespace(name, spec.namespace))

        clauses.extend(self.spec_versions(spec, name=name))
        clauses.extend(self._arch_clauses(spec, f, name=name))
        clauses.extend(self._variant_clauses(spec, f, name=name, body=body))
        clauses.extend(self._flag_clauses(spec, f, name=name, context=context))

        # Hash for concrete specs
        if spec.concrete:
            # older specs do not have package hashes, so we have to do this carefully
            package_hash = getattr(spec, "_package_hash", None)
            if package_hash:
                clauses.append(fn.attr("package_hash", name, package_hash))
            clauses.append(fn.attr("hash", name, spec.dag_hash()))
            if spec.external:
                clauses.append(fn.attr("external", name))

        clauses.extend(self._virtuals_from_dependents(spec, name=name, body=body))

        # If the spec is external and concrete, we allow all the libcs on the system
        if spec.external and spec.concrete and spack.platforms.using_libc_compatibility():
            clauses.append(fn.attr("needs_libc", name))
            for libc in self.libcs:
                clauses.append(fn.attr("compatible_libc", name, libc.name, libc.version))

        if not transitive:
            return clauses

        # Dependencies
        edge_clauses = []
        for dspec in spec.edges_to_dependencies():
            # Ignore conditional dependencies, they are handled by caller
            if dspec.when != EMPTY_SPEC:
                continue

            dep = dspec.spec

            if spec.concrete:
                concrete_clauses, traverse = self._concrete_edge_clauses(
                    dspec,
                    name=name,
                    concrete_build_deps=concrete_build_deps,
                    include_runtimes=include_runtimes,
                )
                edge_clauses.extend(concrete_clauses)
                if not traverse:
                    continue

            # if the spec is abstract, descend into dependencies.
            # if it's concrete, then the hashes above take care of dependency
            # constraints, but expand the hashes if asked for.
            if (not spec.concrete or expand_hashes) and id(dep) not in seen:
                dependency_clauses = self._spec_clauses(
                    dep,
                    body=body,
                    expand_hashes=expand_hashes,
                    concrete_build_deps=concrete_build_deps,
                    context=context,
                    seen=seen,
                )
                edge_clauses.extend(
                    self._dependency_edge_clauses(
                        dspec, dependency_clauses, name=name, body=body, context=context
                    )
                )

        clauses.extend(edge_clauses)
        return clauses

    def pkg_class(self, pkg_name: str) -> Type[spack.package_base.PackageBase]:
        request = pkg_name
        if pkg_name in self.explicitly_required_namespaces:
            namespace = self.explicitly_required_namespaces[pkg_name]
            request = f"{namespace}.{pkg_name}"
        return spack.repo.PATH.get_pkg_class(request)

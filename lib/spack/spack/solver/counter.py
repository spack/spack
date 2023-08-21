# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
from typing import List, Set, Tuple

import spack.dependency
import spack.package_base

PossibleDependencies = Set[str]


class Counter:
    """Computes the possible packages and the maximum number of duplicates
    allowed for each of them.

    Args:
        specs: abstract specs to concretize
        tests: if True, add test dependencies to the list of possible packages
    """

    def __init__(self, specs: List["spack.spec.Spec"], tests: bool) -> None:
        self.specs = specs

        self.link_run_types: Tuple[str, ...] = ("link", "run", "test")
        self.all_types: Tuple[str, ...] = spack.dependency.all_deptypes
        if not tests:
            self.link_run_types = ("link", "run")
            self.all_types = ("link", "run", "build")

        self._possible_dependencies: PossibleDependencies = set()
        self._possible_virtuals: Set[str] = set(x.name for x in specs if x.virtual)

    def possible_dependencies(self) -> PossibleDependencies:
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

    def possible_packages_facts(self, gen: "spack.solver.asp.PyclingoDriver", fn) -> None:
        """Emit facts associated with the possible packages"""
        raise NotImplementedError("must be implemented by derived classes")

    def _compute_cache_values(self):
        raise NotImplementedError("must be implemented by derived classes")


class NoDuplicatesCounter(Counter):
    def _compute_cache_values(self):
        result = spack.package_base.possible_dependencies(
            *self.specs, virtuals=self._possible_virtuals, deptype=self.all_types
        )
        self._possible_dependencies = set(result)

    def possible_packages_facts(self, gen, fn):
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
    def __init__(self, specs, tests):
        super().__init__(specs, tests)
        self._link_run: PossibleDependencies = set()
        self._direct_build: PossibleDependencies = set()
        self._total_build: PossibleDependencies = set()
        self._link_run_virtuals: Set[str] = set()

    def _compute_cache_values(self):
        self._link_run = set(
            spack.package_base.possible_dependencies(
                *self.specs, virtuals=self._possible_virtuals, deptype=self.link_run_types
            )
        )
        self._link_run_virtuals.update(self._possible_virtuals)
        for x in self._link_run:
            current = spack.repo.PATH.get_pkg_class(x).dependencies_of_type("build")
            self._direct_build.update(current)

        self._total_build = set(
            spack.package_base.possible_dependencies(
                *self._direct_build, virtuals=self._possible_virtuals, deptype=self.all_types
            )
        )
        self._possible_dependencies = set(self._link_run) | set(self._total_build)

    def possible_packages_facts(self, gen, fn):
        build_tools = set(spack.repo.PATH.packages_with_tags("build-tools"))
        gen.h2("Packages with at most a single node")
        for package_name in sorted(self.possible_dependencies() - build_tools):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()

        gen.h2("Packages with at multiple possible nodes (build-tools)")
        for package_name in sorted(self.possible_dependencies() & build_tools):
            gen.fact(fn.max_dupes(package_name, 2))
            gen.fact(fn.multiple_unification_sets(package_name))
        gen.newline()

        gen.h2("Maximum number of nodes (virtual packages)")
        for package_name in sorted(self.possible_virtuals()):
            gen.fact(fn.max_dupes(package_name, 1))
        gen.newline()

        gen.h2("Possible package in link-run subDAG")
        for name in sorted(self._link_run):
            gen.fact(fn.possible_in_link_run(name))
        gen.newline()


class FullDuplicatesCounter(MinimalDuplicatesCounter):
    def possible_packages_facts(self, gen, fn):
        build_tools = set(spack.repo.PATH.packages_with_tags("build-tools"))
        counter = collections.Counter(
            list(self._link_run) + list(self._total_build) + list(self._direct_build)
        )
        gen.h2("Maximum number of nodes")
        for pkg, count in sorted(counter.items(), key=lambda x: (x[1], x[0])):
            count = min(count, 2)
            gen.fact(fn.max_dupes(pkg, count))
        gen.newline()

        gen.h2("Build unification sets ")
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

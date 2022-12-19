# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import collections.abc
from typing import List

import spack.environment.environment as ev
import spack.spec

from .asp import (
    OutputConfiguration,
    PyclingoDriver,
    Solver,
    SolverMode,
    SpackSolverSetup,
    SpecBuilder,
    _develop_specs_from_env,
)


def _merge_spec_strings(specs: List[str]) -> spack.spec.Spec:
    starting_spec, *constraints = specs
    result = spack.spec.Spec(starting_spec)
    for constraint in constraints:
        result.constrain(constraint)
    return result


class SinglePackageRequirements(collections.abc.MutableSequence):
    """Collect and manipulate requirements for a single build spec.

    This class contains requirements for a single build spec, and behaves like a built-in list.
    It's client responsibility to ensure the requirements are all for the same package.
    """

    def __init__(self):
        self.requirements: List[str] = []

    def __getitem__(self, item):
        return self.requirements[item]

    def __setitem__(self, key, value):
        self.requirements[key] = value

    def __delitem__(self, key):
        del self.requirements[key]

    def __len__(self):
        return len(self.requirements)

    def insert(self, index: int, value: str) -> None:
        self.requirements.insert(index, value)

    def merged(self) -> spack.spec.Spec:
        """Return a single spec with all the constraints merged"""
        if not self.requirements:
            return spack.spec.Spec()

        starting_spec, *constraints = self.requirements
        result = spack.spec.Spec(starting_spec)
        for constraint in constraints:
            result.constrain(constraint)
        return result

    def errors(self, pkg):
        # TODO: implement errors
        raise NotImplementedError("Still to be implemented")


class BuildRequirements:
    """Collect all the build requirement from a single package"""

    def __init__(self):
        self.requirements = collections.defaultdict(SinglePackageRequirements)

    def add(self, requirement: str):
        """Add a new build requirement to the ones managed by this object"""
        requirement_spec = spack.spec.Spec(requirement)
        key = requirement_spec.name
        self.requirements[key].append(requirement_spec)

    def items(self):
        return self.requirements.items()


class PartialSpecBuilder(SpecBuilder):
    def build_requirement(self, pkg, requirement_str):
        if not hasattr(self._specs[pkg], "build_requirements"):
            self._specs[pkg].build_requirements = BuildRequirements()
        self._specs[pkg].build_requirements.add(requirement_str)

    def finalize_specs(self, roots_to_be_installed):
        pass


PartialResult = collections.namedtuple("PartialResult", ["result", "build_requirements"])


def is_extension(abstract_spec):
    if abstract_spec.virtual:
        return False
    return spack.repo.path.get_pkg_class(abstract_spec.name)(abstract_spec).is_extension


def extension_for(abstract_spec):
    return set(spack.repo.path.get_pkg_class(abstract_spec.name)(abstract_spec).extendees).pop()


def missing_extensions(partial_solve, *asp_results):
    missing = []
    all_extensions = [
        x
        for asp_result in asp_results
        for x in asp_result.all_specs_by_package.values()
        if is_extension(x)
    ]

    keys = list(partial_solve.build_requirements)
    for build_requirement in keys:
        if not is_extension(build_requirement):
            continue

        for known_extension in all_extensions:
            if known_extension.satisfies(build_requirement):
                requestors = partial_solve.build_requirements[build_requirement]
                for requestor in requestors:
                    requestor.add_build_dependency(known_extension)
                partial_solve.build_requirements.pop(build_requirement)
                break
        else:
            extended_package_name = extension_for(build_requirement)
            extended_spec = [
                asp_result.all_specs_by_package[extended_package_name]
                for asp_result in asp_results
            ][0]
            item = build_requirement.copy()
            item.constrain(f"^{extended_spec.format()}")
            missing.append(item)

    return missing


class SpecComposer:
    def __init__(self):
        #: Used as a stack of partial results
        # self.solve_stack = []

        #: The top level solve requested by the user
        self.top_solve = None

        #: The build tools to be composed last
        self.build_tools = None
        #: True when push_final is called
        self.closed = False

    def push_partial(self, *results):
        assert self.closed is False, "cannot push a partial result when the stack is closed"
        build_requirements = collections.defaultdict(list)

        for result in results:
            for root_spec in result.all_specs_by_package.values():
                br = getattr(root_spec, "build_requirements", None)
                if br is None:
                    continue
                for pkg_name, requirements in br.items():
                    if is_extension(root_spec) and extension_for(root_spec) == pkg_name:
                        extended_spec = result.all_specs_by_package[pkg_name]
                        required_spec = requirements.merged()
                        if extended_spec.satisfies(required_spec):
                            root_spec.add_build_dependency(extended_spec)
                            continue
                    build_requirements[requirements.merged()].append(root_spec)

        partial = PartialResult(result=results, build_requirements=build_requirements)

        # self.solve_stack.append(partial)
        self.top_solve = partial
        return list(build_requirements)

    def push_final(self, *results):
        assert self.closed is False, "cannot push a final result when the stack is closed"
        partial = PartialResult(result=results, build_requirements=None)
        self.build_tools = partial
        self.closed = True

    def pop(self, invalidate):
        raise NotImplementedError("Still to be implemented")

    def compose(self):
        assert self.closed is True, "cannot compose from an open stack"
        current_concrete = self.build_tools
        current_partial = self.top_solve

        for build_result in current_concrete.result:
            for input_spec, build_spec in build_result.specs_by_input.items():
                root_specs = current_partial.build_requirements[input_spec]
                for root_spec in root_specs:
                    root_spec.add_build_dependency(build_spec)

        # TODO: find a more robust way to extract this
        result = current_partial.result[0]

        # FIXME: Unify duplicated code from UnifiedBuilder.finalize_specs
        # Add external paths to specs with just external modules
        for s in result.all_specs_by_package.values():
            spack.spec.Spec.ensure_external_path_if_external(s)

        for s in result.all_specs_by_package.values():
            _develop_specs_from_env(s, ev.active_environment())

        # mark concrete and assign hashes to all specs in the solve
        for root in result.all_specs_by_package.values():
            root._finalize_concretization()

        for s in result.all_specs_by_package.values():
            spack.spec.Spec.ensure_no_deprecated(s)

        # Add git version lookup info to concrete Specs (this is generated for
        # abstract specs as well but the Versions may be replaced during the
        # concretization process)
        for root in result.all_specs_by_package.values():
            for spec in root.traverse():
                if isinstance(spec.version, spack.version.GitVersion):
                    spec.version.generate_git_lookup(spec.fullname)

        # Add synthetic edges for externals that are extensions
        for root in result.all_specs_by_package.values():
            for dep in root.traverse():
                if dep.external:
                    dep.package.update_external_dependencies()

        # Unify specs
        keys = list(result.answers[0][2])
        for key in keys:
            item = result.answers[0][2][key]
            result.answers[0][2][key] = spack.spec.Spec.from_json(item.to_json())

        return result


class IterativeSolver:
    def __init__(self):
        self.driver = PyclingoDriver()
        # These properties are settable via spack configuration, and overridable
        # by setting them directly as properties.
        self.reuse = spack.config.get("concretizer:reuse", False)
        self.composer = SpecComposer()

    def solve(self, specs, out=None, timers=False, stats=False, tests=False):
        # FIXME: Add back reusable specs and solve in rounds
        setup = SpackSolverSetup(tests=tests)

        setup.mode = SolverMode.SEPARATE_BUILD_DEPENDENCIES
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=False)
        result, _, _ = self.driver.solve(
            setup, specs, reuse=[], output=output, builder_cls=PartialSpecBuilder
        )

        self.composer.push_partial(result)
        missing = missing_extensions(self.composer.top_solve, result)

        solver = Solver()
        while missing:
            abstract_specs = missing
            results = [
                x
                for x in solver.solve_in_rounds(
                    abstract_specs, setup=setup, builder_cls=PartialSpecBuilder, tests=tests
                )
            ]
            all_results = self.composer.top_solve.result + tuple(results)
            self.composer.push_partial(*all_results)
            missing = missing_extensions(self.composer.top_solve, *all_results)

        build_requirements = list(self.composer.top_solve.build_requirements)
        build_results = [x for x in solver.solve_in_rounds(build_requirements, tests=tests)]
        self.composer.push_final(*build_results)

        result = self.composer.compose()
        return result

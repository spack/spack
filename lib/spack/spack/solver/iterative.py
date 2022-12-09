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


class SpecComposer:
    def __init__(self):
        #: Used as a stack of partial results
        self.solve_stack = []
        #: True when push_final is called
        self.closed = False

    def push_partial(self, result):
        assert self.closed is False, "cannot push a partial result when the stack is closed"
        build_requirements = collections.defaultdict(list)

        for root_spec in result.all_specs_by_package.values():
            br = getattr(root_spec, "build_requirements", None)
            if br is None:
                continue
            for pkg_name, requirements in br.items():
                build_requirements[requirements.merged()].append(root_spec)
        partial = PartialResult(
            result=result,
            build_requirements=build_requirements,
        )
        self.solve_stack.append(partial)
        return list(build_requirements)

    def push_final(self, *results):
        assert self.closed is False, "cannot push a final result when the stack is closed"
        partial = PartialResult(
            result=results,
            build_requirements=None,
        )
        self.solve_stack.append(partial)
        self.closed = True

    def pop(self, invalidate):
        raise NotImplementedError("Still to be implemented")

    def compose(self):
        assert self.closed is True, "cannot compose from an open stack"
        current_concrete = self.solve_stack.pop()
        current_partial = self.solve_stack.pop()

        for build_result in current_concrete.result:
            for input_spec, build_spec in build_result.specs_by_input.items():
                root_specs = current_partial.build_requirements[input_spec]
                for root_spec in root_specs:
                    root_spec.add_build_dependency(build_spec)

        result = current_partial.result

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

    def solve(
        self,
        specs,
        out=None,
        timers=False,
        stats=False,
        tests=False,
    ):
        # FIXME: Add back reusable specs
        setup = SpackSolverSetup(tests=tests)

        setup.mode = SolverMode.SEPARATE_BUILD_DEPENDENCIES
        output = OutputConfiguration(timers=timers, stats=stats, out=out, setup_only=False)
        result, _, _ = self.driver.solve(
            setup, specs, reuse=[], output=output, builder_cls=PartialSpecBuilder
        )

        build_requirements = self.composer.push_partial(result)

        solver = Solver()
        build_results = [x for x in solver.solve_in_rounds(build_requirements, tests=tests)]
        self.composer.push_final(*build_results)

        result = self.composer.compose()
        return result

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Callable, List

import spack.spec


class SpecFilter:
    """Given a method to produce a list of specs, this class can filter them according to
    different criteria.
    """

    def __init__(
        self,
        factory: Callable[[], List[spack.spec.Spec]],
        is_usable: Callable[[spack.spec.Spec], bool],
        include: List[str],
        exclude: List[str],
    ) -> None:
        """
        Args:
            factory: factory to produce a list of specs
            is_usable: predicate that takes a spec in input and returns False if the spec
                should not be considered for this filter, True otherwise.
            include: if present, a spec must match at least one entry in the list,
                to be in the output
            exclude: if present, a spec must not match any entry in the list to be in the output
        """
        self.factory = factory
        self.is_usable = is_usable
        self.include = include
        self.exclude = exclude

    def is_selected(self, s: spack.spec.Spec) -> bool:
        if not self.is_usable(s):
            return False

        if self.include and not any(s.satisfies(c) for c in self.include):
            return False

        if self.exclude and any(s.satisfies(c) for c in self.exclude):
            return False

        return True

    def selected_specs(self) -> List[spack.spec.Spec]:
        return [s for s in self.factory() if self.is_selected(s)]

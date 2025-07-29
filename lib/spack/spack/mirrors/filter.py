# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List

import spack.spec
from spack.mirrors.mirror import Mirror


class MirrorSpecFilter:
    def __init__(self, mirror: Mirror):
        self.exclude = [spack.spec.Spec(spec) for spec in mirror.exclusions]
        self.include = [spack.spec.Spec(spec) for spec in mirror.inclusions]

    def __call__(self, specs: List[spack.spec.Spec]):
        """
        Determine the intersection of include/exclude filters
        Tie goes to keeping

        skip  | keep  | outcome
        ------------------------
        False | False | Keep
        True  | True  | Keep
        False | True  | Keep
        True  | False | Skip
        """
        filter = []
        filtrate = []
        for spec in specs:
            skip = any([spec.satisfies(test) for test in self.exclude])
            keep = any([spec.satisfies(test) for test in self.include])

            if skip and not keep:
                filtrate.append(spec)
            else:
                filter.append(spec)

        return filter, filtrate

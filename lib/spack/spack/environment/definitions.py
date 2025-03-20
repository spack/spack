# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Dict

import spack.spec

from .list import SpecList


class DefinitionBuilder:
    def __init__(self):
        self.spec_lists: Dict[str, SpecList] = {}

    def parse_definitions(self, data) -> Dict[str, SpecList]:
        self.spec_lists = {}
        for item in data:
            self._process_definition(item)
        return self.spec_lists

    def _process_definition(self, entry):
        """Process a single spec definition item."""
        when_string = entry.get("when")
        if when_string is not None:
            when = spack.spec.eval_conditional(when_string)
            assert len([x for x in entry if x != "when"]) == 1
        else:
            when = True
            assert len(entry) == 1

        if when:
            for name, spec_list in entry.items():
                if name == "when":
                    continue
                user_specs = SpecList(name, spec_list, self.spec_lists.copy())
                if name in self.spec_lists:
                    self.spec_lists[name].extend(user_specs)
                else:
                    self.spec_lists[name] = user_specs

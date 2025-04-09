# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
from typing import Any, Dict, List, NamedTuple, Optional, Union

import spack.spec
import spack.util.spack_yaml
import spack.variant
from spack.error import SpackError
from spack.spec import Spec


class SpecList:
    def __init__(self, *, name: str = "specs", yaml_list=None, expanded_list=None):
        self.name = name
        self.yaml_list = yaml_list[:] if yaml_list is not None else []
        # Expansions can be expensive to compute and difficult to keep updated
        # We cache results and invalidate when self.yaml_list changes
        self.specs_as_yaml_list = expanded_list or []
        self._constraints = None
        self._specs: Optional[List[Spec]] = None

    @property
    def is_matrix(self):
        for item in self.specs_as_yaml_list:
            if isinstance(item, dict):
                return True
        return False

    @property
    def specs_as_constraints(self):
        if self._constraints is None:
            constraints = []
            for item in self.specs_as_yaml_list:
                if isinstance(item, dict):  # matrix of specs
                    constraints.extend(_expand_matrix_constraints(item))
                else:  # individual spec
                    constraints.append([Spec(item)])
            self._constraints = constraints

        return self._constraints

    @property
    def specs(self) -> List[Spec]:
        if self._specs is None:
            specs: List[Spec] = []
            # This could be slightly faster done directly from yaml_list,
            # but this way is easier to maintain.
            for constraint_list in self.specs_as_constraints:
                spec = constraint_list[0].copy()
                for const in constraint_list[1:]:
                    spec.constrain(const)
                specs.append(spec)
            self._specs = specs

        return self._specs

    def add(self, spec: Spec):
        spec_str = str(spec)
        self.yaml_list.append(spec_str)

        # expanded list can be updated without invalidation
        if self.specs_as_yaml_list is not None:
            self.specs_as_yaml_list.append(spec_str)

        # Invalidate cache variables when we change the list
        self._constraints = None
        self._specs = None

    def remove(self, spec):
        # Get spec to remove from list
        remove = [
            s
            for s in self.yaml_list
            if (isinstance(s, str) and not s.startswith("$")) and Spec(s) == Spec(spec)
        ]
        if not remove:
            msg = f"Cannot remove {spec} from SpecList {self.name}.\n"
            msg += f"Either {spec} is not in {self.name} or {spec} is "
            msg += "expanded from a matrix and cannot be removed directly."
            raise SpecListError(msg)

        # Remove may contain more than one string representation of the same spec
        for item in remove:
            self.yaml_list.remove(item)
            self.specs_as_yaml_list.remove(item)

        # invalidate cache variables when we change the list
        self._constraints = None
        self._specs = None

    def extend(self, other: "SpecList", copy_reference=True) -> None:
        self.yaml_list.extend(other.yaml_list)
        self.specs_as_yaml_list.extend(other.specs_as_yaml_list)
        self._constraints = None
        self._specs = None

    def __len__(self):
        return len(self.specs)

    def __getitem__(self, key):
        return self.specs[key]

    def __iter__(self):
        return iter(self.specs)


def _expand_matrix_constraints(matrix_config):
    # recurse so we can handle nested matrices
    expanded_rows = []
    for row in matrix_config["matrix"]:
        new_row = []
        for r in row:
            if isinstance(r, dict):
                # Flatten the nested matrix into a single row of constraints
                new_row.extend(
                    [
                        [" ".join([str(c) for c in expanded_constraint_list])]
                        for expanded_constraint_list in _expand_matrix_constraints(r)
                    ]
                )
            else:
                new_row.append([r])
        expanded_rows.append(new_row)

    excludes = matrix_config.get("exclude", [])  # only compute once
    sigil = matrix_config.get("sigil", "")

    results = []
    for combo in itertools.product(*expanded_rows):
        # Construct a combined spec to test against excludes
        flat_combo = [Spec(constraint) for constraints in combo for constraint in constraints]

        test_spec = flat_combo[0].copy()
        for constraint in flat_combo[1:]:
            test_spec.constrain(constraint)

        # Abstract variants don't have normal satisfaction semantics
        # Convert all variants to concrete types.
        # This method is best effort, so all existing variants will be
        # converted before any error is raised.
        # Catch exceptions because we want to be able to operate on
        # abstract specs without needing package information
        try:
            spack.spec.substitute_abstract_variants(test_spec)
        except spack.variant.UnknownVariantError:
            pass

        # Resolve abstract hashes for exclusion criteria
        if any(test_spec.lookup_hash().satisfies(x) for x in excludes):
            continue

        if sigil:
            flat_combo[0] = Spec(sigil + str(flat_combo[0]))

        # Add to list of constraints
        results.append(flat_combo)

    return results


def _sigilify(item, sigil):
    if isinstance(item, dict):
        if sigil:
            item["sigil"] = sigil
        return item
    else:
        return sigil + item


class Definition(NamedTuple):
    name: str
    yaml_list: List[Union[str, Dict]]
    when: Optional[str]


class SpecListParser:
    """Parse definitions and user specs from data in environments"""

    def __init__(self):
        self.definitions: Dict[str, SpecList] = {}

    def parse_definitions(self, *, data: List[Dict[str, Any]]) -> Dict[str, SpecList]:
        definitions_from_yaml: Dict[str, List[Definition]] = {}
        for item in data:
            value = self._parse_yaml_definition(item)
            definitions_from_yaml.setdefault(value.name, []).append(value)

        self.definitions = {}
        self._build_definitions(definitions_from_yaml)
        return self.definitions

    def parse_user_specs(self, *, name, yaml_list) -> SpecList:
        definition = Definition(name=name, yaml_list=yaml_list, when=None)
        return self._speclist_from_definitions(name, [definition])

    def _parse_yaml_definition(self, yaml_entry) -> Definition:
        when_string = yaml_entry.get("when")

        if (when_string and len(yaml_entry) > 2) or (not when_string and len(yaml_entry) > 1):
            mark = spack.util.spack_yaml.get_mark_from_yaml_data(yaml_entry)
            attributes = ", ".join(x for x in yaml_entry if x != "when")
            error_msg = f"definition must have a single attribute, got many: {attributes}"
            raise SpecListError(f"{mark.name}:{mark.line + 1}: {error_msg}")

        for name, yaml_list in yaml_entry.items():
            if name == "when":
                continue
            return Definition(name=name, yaml_list=yaml_list, when=when_string)

        # If we are here, it means only "when" is in the entry
        mark = spack.util.spack_yaml.get_mark_from_yaml_data(yaml_entry)
        error_msg = "definition must have a single attribute, got none"
        raise SpecListError(f"{mark.name}:{mark.line + 1}: {error_msg}")

    def _build_definitions(self, definitions_from_yaml: Dict[str, List[Definition]]):
        for name, definitions in definitions_from_yaml.items():
            self.definitions[name] = self._speclist_from_definitions(name, definitions)

    def _speclist_from_definitions(self, name, definitions) -> SpecList:
        combined_yaml_list = []
        for def_part in definitions:
            if def_part.when is not None and not spack.spec.eval_conditional(def_part.when):
                continue
            combined_yaml_list.extend(def_part.yaml_list)
        expanded_list = self._expand_yaml_list(combined_yaml_list)
        return SpecList(name=name, yaml_list=combined_yaml_list, expanded_list=expanded_list)

    def _expand_yaml_list(self, raw_yaml_list):
        result = []
        for item in raw_yaml_list:
            if isinstance(item, str) and item.startswith("$"):
                result.extend(self._expand_reference(item))
                continue

            value = item
            if isinstance(item, dict):
                value = self._expand_yaml_matrix(item)
            result.append(value)
        return result

    def _expand_reference(self, item: str):
        sigil, name = "", item[1:]
        if name.startswith("^") or name.startswith("%"):
            sigil, name = name[0], name[1:]

        if name not in self.definitions:
            mark = spack.util.spack_yaml.get_mark_from_yaml_data(item)
            error_msg = f"trying to expand the name '{name}', which is not defined yet"
            raise UndefinedReferenceError(f"{mark.name}:{mark.line + 1}: {error_msg}")

        value = self.definitions[name].specs_as_yaml_list
        if not sigil:
            return value
        return [_sigilify(x, sigil) for x in value]

    def _expand_yaml_matrix(self, matrix_yaml):
        extra_attributes = set(matrix_yaml) - {"matrix", "exclude"}
        if extra_attributes:
            mark = spack.util.spack_yaml.get_mark_from_yaml_data(matrix_yaml)
            error_msg = f"extra attributes in spec matrix: {','.join(sorted(extra_attributes))}"
            raise SpecListError(f"{mark.name}:{mark.line + 1}: {error_msg}")

        if "matrix" not in matrix_yaml:
            mark = spack.util.spack_yaml.get_mark_from_yaml_data(matrix_yaml)
            error_msg = "matrix is missing the 'matrix' attribute"
            raise SpecListError(f"{mark.name}:{mark.line + 1}: {error_msg}")

        # Assume data has been validated against the YAML schema
        result = {"matrix": [self._expand_yaml_list(row) for row in matrix_yaml["matrix"]]}
        if "exclude" in matrix_yaml:
            result["exclude"] = matrix_yaml["exclude"]
        return result


class SpecListError(SpackError):
    """Error class for all errors related to SpecList objects."""


class UndefinedReferenceError(SpecListError):
    """Error class for undefined references in Spack stacks."""


class InvalidSpecConstraintError(SpecListError):
    """Error class for invalid spec constraints at concretize time."""

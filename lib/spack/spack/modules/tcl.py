# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

import collections
import re
from typing import Any, Dict, List, Tuple

import spack.projections as proj
import spack.spec
import spack.store
from spack.variant import RESERVED_NAMES, VariantType, VariantValue

from .common import BaseConfiguration, BaseModuleFileWriter


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""

    module_system = "tcl"

    def manipulate_path(self, token: str) -> str:
        if token in self.hierarchy_tokens:
            return "${{{0}_name}} ${{{0}_version}}".format(token)
        return '"' + token + '"'

    def format_condition(self, services_needed: Tuple[str, ...]) -> str:
        return " && ".join(["[string length $" + x + "_name]" for x in services_needed])

    def join_path(self, parts: Tuple[str, ...]) -> str:
        return " ".join([self.manipulate_path(token) for token in parts])

    @property
    def variants_mode(self) -> str:
        """Returns module file variants definition mode."""
        return self._config.get("variants", "none")

    def _variant_to_str_dict(self, v: VariantValue) -> Dict[str, str]:
        """Returns a dictionary entry representing variant object passed as argument.
        A boolean value is written 1 or 0, as the module file expects it."""
        if v.type == VariantType.BOOL:
            return {"value": "1" if v.value else "0", "type": v.type.string, "spec": str(v)}
        value = "_".join(map(str, v.value)) if isinstance(v.value, tuple) else str(v.value)
        return {"value": value, "type": v.type.string, "spec": f"{v.name}={value}"}

    @property
    def folds_installations(self) -> bool:
        """Whether several installations may share this module file, which then folds them.
        This is the case when variants are enabled and the module file name does not include
        the hash, as different installations of the same package version then map to the same
        file name.
        """
        if "folds_installations" not in self._cache:
            self._cache["folds_installations"] = self._compute_folds_installations()
        return self._cache["folds_installations"]

    def _compute_folds_installations(self) -> bool:
        if self.variants_mode == "none" or self.conf.get("hash_length", 7) != 0:
            return False
        projection = proj.get_projection(self.projections, self.spec)
        if not projection:
            projection = self.default_projections["all"]
        return re.search(r"{[^}]*hash", projection) is None

    def _variant_dict_for_spec(
        self, spec: spack.spec.Spec, add_hash_variant: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of defined variants for given spec keyed by variant name.
        Any multi-valued variant is transformed into a single-valued one, joining values
        If asked, "hash" variant is defined last into the dictionary.
        The dictionary is sorted by its keys, with the "hash" variant last if defined.
        """
        # Variants reserved by Spack (like patches or dev_path) describe how the
        # package was built rather than what it provides, they are not defined
        variant_dict = {
            v.name: self._variant_to_str_dict(v)
            for v in sorted(spec.variants.values(), key=lambda x: x.name)
            if v.name not in RESERVED_NAMES
        }

        if add_hash_variant:
            variant_dict["hash"] = {
                "value": spec.dag_hash(7),
                "type": "single",
                "spec": f"hash={spec.dag_hash(7)}",
            }

        return variant_dict

    @property
    def variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of defined variants keyed by variant name.
        Returns an empty dictionary if variant mode is disabled.
        """
        if "variants" not in self._cache:
            self._cache["variants"] = self._compute_variants()
        return self._cache["variants"]

    def _compute_variants(self) -> Dict[str, Dict[str, Any]]:
        if self.variants_mode == "none":
            return {}

        need_hash_variant = self.spec in self._specs_need_hash_variant()
        return self._variant_dict_for_spec(self.spec, need_hash_variant)

    def _variants_spec_for_spec(self, spec: spack.spec.Spec) -> str:
        """Returns aggregated spec string of variants for given spec."""
        return " ".join(v["spec"] for v in self._variant_dict_for_spec(spec).values())

    @property
    def variants_spec(self) -> str:
        """Returns aggregated spec string of variants."""
        return " ".join(v["spec"] for v in self.variants.values())

    @property
    def variant_values(self) -> str:
        """Returns the values of the variants of this installation, in the order of the
        aggregated variants. A variant this installation does not define takes the neutral
        value that the aggregated variants give to it."""
        variants = self.variants
        return " ".join(
            variants[name]["value"] if name in variants else self._neutral_value(v)
            for name, v in self.aggregated_variants.items()
        )

    @staticmethod
    def _neutral_value(aggregated_variant: Dict[str, Any]) -> str:
        """Value standing for a variant on installations that do not define it."""
        return "0" if aggregated_variant["type"] == "bool" else "none"

    @property
    def installed_specs(self) -> List[spack.spec.Spec]:
        return self._specs_sharing_modulefile()

    def _specs_sharing_modulefile(self) -> List[spack.spec.Spec]:
        """All installed specs of same name@version that map to the same module filename."""
        if "specs_sharing_modulefile" not in self._cache:
            self._cache["specs_sharing_modulefile"] = self._compute_specs_sharing_modulefile()
        return self._cache["specs_sharing_modulefile"]

    def _compute_specs_sharing_modulefile(self) -> List[spack.spec.Spec]:
        # A module file that cannot be shared holds this installation only, skip the database
        # query in this case
        if not self.folds_installations:
            return [self.spec] if self.add_op else []

        name_version_spec = self.spec.format("{name} {@version}")
        spec_list = set(spack.store.STORE.db.query(name_version_spec, installed=True))

        if self.add_op:
            spec_list.add(self.spec)
        # remove this spec if it is currently being uninstalled
        elif self.spec in spec_list:
            spec_list.remove(self.spec)
        if self.extra_spec_sharing:
            spec_list.add(self.extra_spec_sharing)

        # Returns only specs that share the same module filename, sorted by their variant
        # values as the module file selects the first installation matching a load request
        my_filename = self.make_layout(
            self.spec,
            self.name,
            self.explicit,
            add_op=self.add_op,
            extra_spec_sharing=self.extra_spec_sharing,
            cache=self._configuration_cache,
        ).filename
        sharing_specs = [
            spec
            for spec in spec_list
            if self.make_layout(
                spec,
                self.name,
                self.explicit,
                add_op=self.add_op,
                extra_spec_sharing=self.extra_spec_sharing,
                cache=self._configuration_cache,
            ).filename
            == my_filename
        ]
        return sorted(sharing_specs, key=self._variant_values_key)

    def _variant_values_key(self, spec: spack.spec.Spec) -> Tuple[Tuple[str, ...], str]:
        """Sort key listing installations by their variant values, then by their hash."""
        values = tuple(v["value"] for v in self._variant_dict_for_spec(spec).values())
        return (values, spec.dag_hash())

    @property
    def other_installed_specs(self) -> List[spack.spec.Spec]:
        """Returns a list of all the other installed spec for this package version"""
        # Copy the list: _specs_sharing_modulefile() is cached and shared with other
        # consumers, so it must not be mutated in place.
        spec_list = list(self._specs_sharing_modulefile())
        if self.spec in spec_list:
            spec_list.remove(self.spec)

        return spec_list

    def _specs_need_hash_variant(self) -> List[spack.spec.Spec]:
        """List of installed specs that needs to define a hash variant to disambiguate."""
        if "specs_need_hash_variant" not in self._cache:
            self._cache["specs_need_hash_variant"] = self._compute_specs_need_hash_variant()
        return self._cache["specs_need_hash_variant"]

    def _compute_specs_need_hash_variant(self) -> List[spack.spec.Spec]:
        spec_groups = collections.defaultdict(list)
        for spec in self._specs_sharing_modulefile():
            spec_groups[self._variants_spec_for_spec(spec)].append(spec)

        return [spec for group in spec_groups.values() if len(group) > 1 for spec in group]

    @property
    def aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a consolidated dictionary of defined variants across installations, with
        their type and sorted values. A variant that only some installations define also
        takes the neutral value standing for it on the others.
        This dictionary is sorted by its keys, which are variant names, with the "hash"
        variant last if defined.
        Returns an empty dictionary if variant mode is disabled.
        """
        if "aggregated_variants" not in self._cache:
            self._cache["aggregated_variants"] = self._compute_aggregated_variants()
        return self._cache["aggregated_variants"]

    def _compute_aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        if self.variants_mode == "none":
            return {}

        aggregated = {}
        seen_in = {}
        install_specs = self._specs_sharing_modulefile()
        total_installs = len(install_specs)

        specs_need_hash = set(self._specs_need_hash_variant())
        for spec in install_specs:
            variant_dict = self._variant_dict_for_spec(spec, spec in specs_need_hash)
            for name, v in variant_dict.items():
                if name not in aggregated:
                    aggregated[name] = {"type": v["type"], "values": set()}
                    seen_in[name] = 0
                aggregated[name]["values"].add(v["value"])
                seen_in[name] += 1

        for name, v in aggregated.items():
            # Conditional variant: some installations do not define it
            if seen_in[name] < total_installs:
                v["values"].add(self._neutral_value(v))
            # Sort variant values for deterministic module file content across regenerations,
            # since dict/set iteration order of strings is not guaranteed to be stable
            v["values"] = sorted(v["values"])

        # Keep the "hash" variant last, as it ends the depends-on lines of dependent modules
        return dict(sorted(aggregated.items(), key=lambda item: (item[0] == "hash", item[0])))


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    configuration_class = TclConfiguration

    default_template = "modules/modulefile.tcl"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

    def remove_installation(self):
        """Removes this installation from module file. Module file is deleted if it
        does not reference any other package installation."""
        if self.layout.hold_other_installations:
            self.write()
        else:
            self.remove()

    def update_module_hiddenness(self, remove=False):
        """Update modulerc file corresponding to module to add or remove
        command that hides module depending on its hidden state.

        Args:
            remove (bool): if True, hiddenness information for module is
                removed from modulerc.
        """
        remove_hiddenness = remove

        # do not hide this module if another installation stored same module file is not hidden
        if not remove_hiddenness and self.layout.hold_other_installations:
            remove_hiddenness = any(
                not install.conf.hidden for install in self.context.installations
            )

        super().update_module_hiddenness(remove_hiddenness)

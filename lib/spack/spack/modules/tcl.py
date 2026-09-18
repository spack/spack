# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

from typing import Any, Dict, Tuple

from spack.variant import VariantType, VariantValue

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
        """Returns a dictionary entry representing variant object passed as argument."""
        value = "_".join(map(str, v.value)) if isinstance(v.value, tuple) else str(v.value)
        spec = str(v) if v.type == VariantType.BOOL else f"{v.name}={value}"
        return {"value": value, "type": v.type.string, "spec": spec}

    @property
    def variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of defined variants keyed by variant name.
        Any multi-valued variant is transformed into a single-valued one, joining values
        The dictionary is sorted by its keys

        Returns an empty dictionary if variant mode is disabled.
        """
        if "variants" not in self._cache:
            self._cache["variants"] = self._compute_variants()
        return self._cache["variants"]

    def _compute_variants(self) -> Dict[str, Dict[str, Any]]:
        if self.variants_mode == "none":
            return {}

        return {
            v.name: self._variant_to_str_dict(v)
            for v in sorted(self.spec.variants.values(), key=lambda x: x.name)
            if v.name not in self.exclude_variants
        }

    @property
    def variants_spec(self) -> str:
        """Returns aggregated spec string of variants."""
        return " ".join(v["spec"] for v in self.variants.values())


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    configuration_class = TclConfiguration

    default_template = "modules/modulefile.tcl"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

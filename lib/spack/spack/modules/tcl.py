# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

import math
import os
import re
from typing import Any, Dict, List, Tuple

import spack.error
import spack.projections as proj
import spack.spec
import spack.store
from spack.variant import RESERVED_NAMES, VariantType, VariantValue

from .common import BaseConfiguration, BaseModuleFileWriter, FileLayout

#: Words the module command reads as booleans, any prefix of them included
_MODULE_BOOLEAN_WORDS = ("true", "false", "yes", "no", "on", "off")


def module_variant_value(value: str) -> str:
    """Returns a variant value in the form the module command reads back once loaded:
    ``++`` is spelled ``xx`` as in ``cxx``, any other character than letters, digits,
    ``_``, ``-``, ``.`` and ``/`` becomes ``_``, and a value the module command reads as a
    boolean gets a trailing ``_``."""
    value = value.replace("++", "xx")
    # The module command records loaded modules as name{+a:b=c}, where "+", "~", "@", ":",
    # "," and "=" are syntax, and it cannot unload a module whose values hold them. Other
    # non-alphanumeric characters break the Tcl lists of the module file or need quoting on
    # the module command line.
    value = re.sub(r"[^A-Za-z0-9_.\-/]", "_", value)
    # The variant command refuses a boolean-looking value on a non-boolean variant, and the
    # module command accepts any prefix of a boolean word but the ambiguous "o"
    lower = value.lower()
    if lower not in ("", "o") and any(word.startswith(lower) for word in _MODULE_BOOLEAN_WORDS):
        value += "_"
    return value


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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # The hash variant tells installations apart once module names drop the hash, a
        # hashed name with variants defined would tell them apart twice
        if self.variants_mode != "none" and self._config.get("hash_length", 7) != 0:
            raise spack.error.ConfigError(
                f"'variants: {self.variants_mode}' in the tcl configuration of the "
                f"'{self.name}' module set requires 'hash_length: 0', as module variants "
                "replace the hash in module names"
            )

    @property
    def variants_mode(self) -> str:
        """Returns module file variants definition mode."""
        return self._config.get("variants", "none")

    def _variant_to_str_dict(self, v: VariantValue) -> Dict[str, str]:
        """Returns a dictionary entry representing variant object passed as argument.
        A boolean value is written 1 or 0, as the module file expects it. Any other value
        is written in the form the module command reads back, see :func:`module_variant_value`,
        with the values of a multi-valued variant joined by underscores."""
        if v.type == VariantType.BOOL:
            return {"value": "1" if v.value else "0", "type": v.type.string, "spec": str(v)}
        value = "_".join(map(str, v.value)) if isinstance(v.value, tuple) else str(v.value)
        value = module_variant_value(value)
        return {"value": value, "type": v.type.string, "spec": f"{v.name}={value}"}

    @property
    def folds_installations(self) -> bool:
        """Whether several installations may share this module file, which then folds them.
        This is the case when variants are enabled and the module file name does not include
        the hash, as different installations of the same package version then map to the same
        file name. A "hash" variant then identifies each installation in the module file.
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

    def _variant_dict_for_spec(self, spec: spack.spec.Spec) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of defined variants for given spec keyed by variant name.
        Any multi-valued variant is transformed into a single-valued one, joining values
        The dictionary is sorted by its keys, with the "hash" variant last if used.
        """
        # Variants reserved by Spack (like patches or dev_path) describe how the
        # package was built rather than what it provides, they are not defined
        variant_dict = {
            v.name: self._variant_to_str_dict(v)
            for v in sorted(spec.variants.values(), key=lambda x: x.name)
            if v.name not in RESERVED_NAMES
        }

        if self.folds_installations:
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

        return self._variant_dict_for_spec(self.spec)

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
            return [] if self.spec in self.removed_specs else [self.spec]

        # Upstream installations are left out: their module files belong to the upstream
        name_version_spec = self.spec.format("{name} {@version}")
        spec_list = set(
            spack.store.STORE.db.query(name_version_spec, installed=True, install_tree="local")
        )

        # The installations being added may not be recorded yet, the ones being removed are
        # still recorded until uninstalled
        spec_list.add(self.spec)
        if self.extra_spec_sharing:
            spec_list.add(self.extra_spec_sharing)
        spec_list.difference_update(self.removed_specs)

        # Keep only specs that share the same module filename and are not excluded from module
        # file generation, this installation included, in the order a plain load request
        # selects them, as the module file selects the first installation matching a request
        my_filename = FileLayout(self).filename
        sharing_confs = []
        for spec in spec_list:
            conf = self if spec == self.spec else self.make_folded_configuration(spec)
            if not conf.excluded and FileLayout(conf).filename == my_filename:
                sharing_confs.append(conf)
        sharing_confs.sort(key=self._installation_order_key)
        sharing_specs = [conf.spec for conf in sharing_confs]

        # The other installations compute the same list, hand it over to spare them the
        # database query
        for spec in sharing_specs:
            if spec != self.spec:
                other_conf = self.make_folded_configuration(spec)
                other_conf._cache.setdefault("specs_sharing_modulefile", sharing_specs)

        return sharing_specs

    @staticmethod
    def _installation_order_key(conf: BaseConfiguration) -> Tuple[bool, bool, float, str]:
        """Sort key listing the installations matching a configured default first, then the
        explicit ones before the implicit ones, in installation order, then by hash.

        This order holds as installations are added: a new installation is listed after the
        existing ones, unless it is explicit and they are implicit, or it matches a default.
        """
        spec = conf.spec
        matches_default = any(spec.satisfies(default) for default in conf.defaults)
        # An installation not recorded yet is being added, it comes after the recorded ones
        try:
            record = spack.store.STORE.db.get_record(spec)
        except KeyError:
            record = None
        installation_time = record.installation_time if record else math.inf
        return (not matches_default, not conf.explicit, installation_time, spec.dag_hash())

    @property
    def other_installed_specs(self) -> List[spack.spec.Spec]:
        """Returns a list of all the other installed spec for this package version"""
        # Copy the list: _specs_sharing_modulefile() is cached and shared with other
        # consumers, so it must not be mutated in place.
        spec_list = list(self._specs_sharing_modulefile())
        if self.spec in spec_list:
            spec_list.remove(self.spec)

        return spec_list

    @property
    def aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a consolidated dictionary of defined variants across installations, with
        their type and sorted values. A variant that only some installations define also
        takes the neutral value standing for it on the others.
        This dictionary is sorted by its keys, which are variant names, with the "hash"
        variant last if used.
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

        for spec in install_specs:
            variant_dict = self._variant_dict_for_spec(spec)
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
        if self.layout.hold_other_installations and os.path.exists(self.layout.filename):
            self.write()
            # The removed installation may have been the one making this module the default
            if not self._holds_default():
                self.remove_module_defaults()
        else:
            self.remove()

    def _holds_default(self) -> bool:
        """Whether an installation held by the module file matches a configured default."""
        return any(self.matches_default(install.spec) for install in self.context.installations)

    def update_module_defaults(self) -> None:
        """Points the ``default`` symlink to this module file if it holds an installation
        matching a configured default, whichever installation is being written."""
        if self._holds_default():
            self.link_default()

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

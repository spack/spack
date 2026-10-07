# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

import math
import os
import re
import warnings
from typing import Any, Dict, List, Optional, Set, Tuple, cast

import spack.config
import spack.error
import spack.spec
import spack.store
from spack import tengine
from spack.variant import RESERVED_NAMES, VariantType, VariantValue

from .common import BaseConfiguration, BaseModuleFileWriter, FileLayout, ModuleContext

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


#: Module sets already warned about a hash_length ignored with variants defined
_hash_length_warned: Set[str] = set()


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
        if self.variants_mode != "none":
            self._warn_hash_length_ignored()

    @property
    def variants_mode(self) -> str:
        """Returns module file variants definition mode."""
        return self._config.get("variants", "none")

    @property
    def hash(self) -> Optional[str]:
        """Hash appended to the module file name, or None when variants are defined, as the
        hash variant then replaces the hash in module names."""
        if self.variants_mode != "none":
            return None
        return super().hash

    def _warn_hash_length_ignored(self) -> None:
        """Warns, once per process and module set, that a non-zero hash_length set in some
        configuration scope has no effect with variants defined."""
        hash_length = self._config.get("hash_length", 0)
        if hash_length == 0 or self.name in _hash_length_warned:
            return
        _hash_length_warned.add(self.name)
        scope = self._hash_length_scope()
        where = f" in the '{scope}' configuration scope" if scope else ""
        warnings.warn(
            f"'hash_length: {hash_length}' set{where} is ignored, as 'variants: "
            f"{self.variants_mode}' in the tcl configuration of the '{self.name}' module set "
            "replaces the hash in module names with the hash variant"
        )

    def _hash_length_scope(self) -> Optional[str]:
        """Returns the name of the highest precedence scope setting hash_length in the tcl
        configuration of this module set, or None if no scope is found."""
        for scope in spack.config.CONFIG.scopes.reversed_values():
            section = scope.get_section("modules") or {}
            tcl_cfg = section.get("modules", {}).get(self.name, {}).get("tcl", {})
            if "hash_length" in tcl_cfg:
                return scope.name
        return None

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
        file name.
        """
        if self.variants_mode == "none":
            return False
        tokens = spack.spec.SPEC_FORMAT_RE.finditer(self.projection)
        return not any(token.group(4) for token in tokens)

    def _make_layout(self) -> FileLayout:
        return TclFileLayout(self)

    @property
    def variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a dictionary of defined variants keyed by variant name.
        Any multi-valued variant is transformed into a single-valued one, joining values.
        The dictionary is sorted by its keys, followed by the "hash" variant, which identifies
        the installation.
        Returns an empty dictionary if variant mode is disabled.
        """
        if "variants" not in self._cache:
            self._cache["variants"] = self._compute_variants()
        return self._cache["variants"]

    def _compute_variants(self) -> Dict[str, Dict[str, Any]]:
        if self.variants_mode == "none":
            return {}

        # Variants reserved by Spack (like patches or dev_path) describe how the
        # package was built rather than what it provides, they are not defined
        variant_dict = {
            v.name: self._variant_to_str_dict(v)
            for v in sorted(self.spec.variants.values(), key=lambda x: x.name)
            if v.name not in RESERVED_NAMES
        }

        short_hash = self.spec.dag_hash(7)
        variant_dict["hash"] = {
            "value": short_hash,
            "type": "single",
            "spec": f"hash={short_hash}",
        }
        return variant_dict

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
    def configurations_in_file(self) -> List["TclConfiguration"]:
        """Returns the configuration of each installed spec of same name@version that maps to
        the same module filename, in the order the module file lists them."""
        if "configurations_in_file" not in self._cache:
            self._cache["configurations_in_file"] = self._compute_configurations_in_file()
        return self._cache["configurations_in_file"]

    def _compute_configurations_in_file(self) -> List["TclConfiguration"]:
        # A module file that cannot be shared holds this installation only, skip the database
        # query in this case
        if not self.folds_installations:
            return cast(List[TclConfiguration], super().configurations_in_file)

        # One read transaction for the query and the records read for each installation
        with spack.store.STORE.db.read_transaction():
            # Upstream installations are left out: their module files belong to the upstream
            name_version_spec = f"{self.spec.name}@={self.spec.version}"
            spec_list = set(
                spack.store.STORE.db.query(
                    name_version_spec, installed=True, install_tree="local", sort=False
                )
            )

            # A module file may be requested for an installation not recorded yet, the ones
            # being removed are still recorded until uninstalled
            spec_list.add(self.spec)
            spec_list.difference_update(self.removed_specs)

            # Keep only specs that share the same module filename and are not excluded from
            # module file generation, this installation included, in the order a plain load
            # request selects them, as the module file selects the first installation matching
            # a request
            confs_in_file = []
            for spec in spec_list:
                conf = self.sibling_configuration(spec)
                if conf.excluded:
                    continue
                if conf is self or conf.layout.filename == self.layout.filename:
                    confs_in_file.append(conf)
            confs_in_file.sort(key=self._installation_order_key)

        # The other installations compute the same list, hand it over to spare them the
        # database query
        for conf in confs_in_file:
            if conf is not self:
                conf._cache.setdefault("configurations_in_file", confs_in_file)

        return confs_in_file

    def sibling_configuration(self, spec: spack.spec.Spec) -> "TclConfiguration":
        """Returns the configuration of an installation held by the same module file, which is
        this one for its own spec. For another spec, explicitness is read from the database,
        as it may differ from this one's, and the installations being removed are handed over.
        """
        if spec == self.spec:
            return self
        conf = self.make_configuration(
            spec, self.name, removed_specs=self.removed_specs, cache=self._configuration_cache
        )
        return cast(TclConfiguration, conf)

    @staticmethod
    def _installation_order_key(conf: BaseConfiguration) -> Tuple[bool, float, str]:
        """Sort key listing the installations matching a configured default first, then the
        others in installation order, then by hash.

        A new installation is listed after the existing ones, unless it matches a default.
        """
        spec = conf.spec
        # An installation not recorded yet is being added, it comes after the recorded ones
        _, record = spack.store.STORE.db.query_by_spec_hash(spec.dag_hash())
        installation_time = record.installation_time if record else math.inf
        return (not conf.matches_default, installation_time, spec.dag_hash())

    @property
    def aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        """Returns a consolidated dictionary of defined variants across installations, with
        their type and sorted values. A variant that only some installations define also
        takes the neutral value standing for it on the others.
        This dictionary is sorted by its keys, which are variant names, followed by the "hash"
        variant.
        Returns an empty dictionary if variant mode is disabled.
        """
        if "aggregated_variants" not in self._cache:
            self._cache["aggregated_variants"] = self._compute_aggregated_variants()
        return self._cache["aggregated_variants"]

    def _compute_aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        aggregated = {}
        seen_in = {}
        confs_in_file = self.configurations_in_file
        total_installs = len(confs_in_file)

        for conf in confs_in_file:
            for name, v in conf.variants.items():
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
        result = dict(sorted(aggregated.items(), key=lambda item: (item[0] == "hash", item[0])))

        # The other installations compute the same dictionary, hand it over
        for conf in confs_in_file:
            if conf is not self:
                conf._cache.setdefault("aggregated_variants", result)

        return result


class TclFileLayout(FileLayout):
    """Layout of tcl module files, whose names may be followed by variants."""

    @property
    def use_name(self) -> str:
        """Returns the name used to load the module, followed by its variants if defined."""
        # Boolean variants are appended to the name, as a shell expands a word starting with
        # ``~`` to a home directory, and the other variants follow as separate words.
        variants = self.conf.variants.values()
        booleans = "".join(v["spec"] for v in variants if v["type"] == "bool")
        valued = "".join(f" {v['spec']}" for v in variants if v["type"] != "bool")
        return f"{self.name}{booleans}{valued}"

    @property
    def unique_use_name(self) -> str:
        """Returns the name that selects this installation from a dependent module file.
        The "hash" variant is the only one stated when variants are defined, so the name stays
        valid whatever variants the module file defines later on."""
        variants = self.conf.variants
        if variants:
            return f"{self.name} {variants['hash']['spec']}"
        return self.name


class TclModuleContext(ModuleContext):
    """Template context of tcl module files, which may hold several installations."""

    def __init__(self, configuration, layout: FileLayout) -> None:
        super().__init__(configuration, layout)
        self._installations: Optional[List["TclModuleContext"]] = None

    @tengine.context_property
    def hash(self) -> str:
        """Returns hash of this installation"""
        return self.spec.dag_hash(7)

    @tengine.context_property
    def variants_mode(self) -> str:
        """Returns the module file variants definition mode, "none" when variants are not
        defined in module files."""
        return self.conf.variants_mode

    @tengine.context_property
    def installations(self) -> List["TclModuleContext"]:
        """Returns the context of each installation held by the module file, in the order
        the module file selects them."""
        if self._installations is None:
            self._installations = [
                self if conf is self.conf else type(self)(conf, conf.layout)
                for conf in self.conf.configurations_in_file
            ]
        return self._installations

    @tengine.context_property
    def any_installation_has_autoload(self) -> bool:
        """Whether an installation held by the module file has a dependency to auto load."""
        return any(install.autoload for install in self.installations)

    @tengine.context_property
    def aggregated_variants(self) -> Dict[str, Dict[str, Any]]:
        """Expose aggregated variant metadata to templates."""
        return self.conf.aggregated_variants

    @tengine.context_property
    def variant_values(self) -> str:
        """Returns the values of the variants of this installation."""
        return self.conf.variant_values


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    configuration_class = TclConfiguration

    context_class = TclModuleContext

    default_template = "modules/modulefile.tcl"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

    conf: TclConfiguration

    def write(self, overwrite: bool = False) -> None:
        # A module file shared with other installations is written again for all of them
        if not self.conf.excluded and self.has_other_installations:
            self._ensure_folded_installations_share_template()
            overwrite = True
        super().write(overwrite)

    def _ensure_folded_installations_share_template(self) -> None:
        """Raises a configuration error when the installations folded in this module file are
        configured with different templates, as the module file is rendered from one of them."""
        templates = {conf.spec: conf.template for conf in self.conf.configurations_in_file}
        if len(set(templates.values())) < 2:
            return

        # A template rule matching only some of the folded installations wins or loses with the
        # order the installations are written, name them all so the rule can be reworked
        details = ", ".join(
            spec.format("{name}{@version}{variants}{/hash:7}")
            + (f" uses template '{template}'" if template else " uses the default template")
            for spec, template in templates.items()
        )
        raise spack.error.ConfigError(
            f"the installations folded in the module file '{self.layout.filename}' are "
            "configured with different templates, which cannot apply to one module file: "
            f"{details}. Set 'template' for the whole package version instead."
        )

    def remove_installation(self) -> None:
        """Removes this installation from its module file, which is deleted if it holds no
        other installation."""
        remaining = self.conf.other_specs_in_file
        if not remaining or not os.path.exists(self.layout.filename):
            super().remove_installation()
            return

        # Written for an installation the file keeps, as the prefix of this one may be gone
        writer = type(self)(self.conf.sibling_configuration(remaining[0]))
        writer.write(overwrite=True)
        # The removed installation may have been the one making this module the default
        if not any(conf.matches_default for conf in writer.conf.configurations_in_file):
            self.remove_module_defaults()

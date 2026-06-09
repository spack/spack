# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import ClassVar, Dict, List, Optional, Tuple

import spack.config
import spack.spec
import spack.tengine as tengine

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


#: lmod specific part of the configuration
def configuration(module_set_name: str) -> dict:
    return spack.config.get(f"modules:{module_set_name}:lmod", {})


# Caches the configuration {spec_hash: configuration}
configuration_registry: Dict[Tuple[str, str, bool], BaseConfiguration] = {}


def make_configuration(
    spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
) -> BaseConfiguration:
    """Returns the lmod configuration for spec"""
    explicit = bool(spec._installed_explicitly()) if explicit is None else explicit
    key = (spec.dag_hash(), module_set_name, explicit)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, LmodConfiguration(spec, module_set_name, explicit)
        )


def make_layout(
    spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
) -> BaseFileLayout:
    """Returns the layout information for spec"""
    return LmodFileLayout(make_configuration(spec, module_set_name, explicit))


def make_context(
    spec: spack.spec.Spec,
    module_set_name: str,
    *,
    explicit: Optional[bool] = None,
    layout: BaseFileLayout,
) -> BaseContext:
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name, explicit)
    return LmodContext(conf, layout)


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    module_system = "lmod"

    @property
    def hierarchical(self) -> bool:
        """Returns if hierarchical mode has been enabled, True if not set."""
        return self.module.configuration(self.name).get("hierarchical", True)


class LmodFileLayout(BaseFileLayout):
    """File layout for lmod module files."""

    #: file extension of lua module files
    extension = "lua"

    @property
    def modulerc(self) -> str:
        """Returns the modulerc file associated with current module file"""
        return os.path.join(os.path.dirname(self.filename), f".modulerc.{self.extension}")


class LmodContext(BaseContext):
    """Context class for lmod module files."""

    @tengine.context_property
    def conditionally_unlocked_paths(self) -> List[Tuple[str, str]]:
        """Returns the list of paths that are unlocked conditionally.
        Each item in the list is a tuple with the structure (condition, path).
        """
        value: List[Tuple[str, str]] = []
        conditional_paths = self.layout.unlocked_paths

        def manipulate_path(token: str) -> str:
            if token in self.conf.hierarchy_tokens:
                return "{0}_name, {0}_version".format(token)
            return '"' + token + '"'

        for services_needed, list_of_path_parts in conditional_paths.items():
            if services_needed is None:
                continue

            condition = " and ".join([x + "_name" for x in services_needed])
            for parts in list_of_path_parts:
                path = ", ".join([manipulate_path(x) for x in parts])
                value.append((condition, path))

        return value


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""

    configuration_class = LmodConfiguration

    default_template = "modules/modulefile.lua"

    modulerc_header = []

    hide_cmd_format = 'hide_version("%s")'

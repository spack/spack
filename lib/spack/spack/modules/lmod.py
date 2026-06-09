# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import Dict, Optional, Tuple

import spack.config
import spack.spec

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
    explicit: Optional[bool] = None,
    layout: Optional[BaseFileLayout] = None,
) -> BaseContext:
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name, explicit)
    if layout is None:
        layout = make_layout(spec, module_set_name, explicit)
    return LmodContext(conf, layout)


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    module_system = "lmod"
    _default_hierarchical = True


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

    def _manipulate_path(self, token: str) -> str:
        if token in self.conf.hierarchy_tokens:
            return "{0}_name, {0}_version".format(token)
        return '"' + token + '"'

    def _format_condition(self, services_needed: Tuple[str, ...]) -> str:
        return " and ".join([x + "_name" for x in services_needed])

    def _join_path(self, parts: Tuple[str, ...]) -> str:
        return ", ".join([self._manipulate_path(x) for x in parts])


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""

    make_configuration = staticmethod(make_configuration)
    make_layout = staticmethod(make_layout)
    make_context = staticmethod(make_context)

    default_template = "modules/modulefile.lua"

    modulerc_header = []

    hide_cmd_format = 'hide_version("%s")'

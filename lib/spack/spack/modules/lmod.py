# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import ClassVar, Dict, Tuple

from .common import BaseConfiguration, BaseModuleFileWriter


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    module_system = "lmod"
    _default_hierarchical = True
    _registry: ClassVar[Dict] = {}
    file_extension = "lua"

    def _manipulate_path(self, token: str) -> str:
        if token in self.hierarchy_tokens:
            return "{0}_name, {0}_version".format(token)
        return '"' + token + '"'

    def _format_condition(self, services_needed: Tuple[str, ...]) -> str:
        return " and ".join([x + "_name" for x in services_needed])

    def _join_path(self, parts: Tuple[str, ...]) -> str:
        return ", ".join([self._manipulate_path(token) for token in parts])


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""

    configuration_class = LmodConfiguration

    default_template = "modules/modulefile.lua"

    modulerc_header = []

    hide_cmd_format = 'hide_version("%s")'

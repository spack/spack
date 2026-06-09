# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from typing import ClassVar, Dict, Tuple

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


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


class LmodConfiguration(BaseConfiguration):
    """Configuration class for lmod module files."""

    module_system = "lmod"
    _default_hierarchical = True
    _registry: ClassVar[Dict] = {}
    layout_class = LmodFileLayout
    context_class = LmodContext


class LmodModulefileWriter(BaseModuleFileWriter):
    """Writer class for lmod module files."""

    configuration_class = LmodConfiguration

    default_template = "modules/modulefile.lua"

    modulerc_header = []

    hide_cmd_format = 'hide_version("%s")'

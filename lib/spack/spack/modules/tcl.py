# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

from typing import Tuple

from . import cache
from .common import BaseConfiguration, BaseModuleFileWriter


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""

    module_system = "tcl"

    @property
    def update_cache(self) -> bool:
        """Returns True if the module cache of the modulepath directories changed by
        Spack should be kept updated, False otherwise."""
        return self._config.get("update_cache", False)

    def manipulate_path(self, token: str) -> str:
        if token in self.hierarchy_tokens:
            return "${{{0}_name}} ${{{0}_version}}".format(token)
        return '"' + token + '"'

    def format_condition(self, services_needed: Tuple[str, ...]) -> str:
        return " && ".join(["[string length $" + x + "_name]" for x in services_needed])

    def join_path(self, parts: Tuple[str, ...]) -> str:
        return " ".join([self.manipulate_path(token) for token in parts])


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    conf: TclConfiguration

    configuration_class = TclConfiguration

    default_template = "modules/modulefile.tcl"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

    def register_cache_update(self) -> None:
        """Registers the modulepath directory of this module file for a module cache
        update, if enabled in configuration."""
        if self.conf.update_cache:
            cache.register(self.layout.modulepath)

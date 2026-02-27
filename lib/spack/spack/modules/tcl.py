# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl modules."""

import os
from typing import ClassVar, Dict, Optional

import spack.spec
import spack.tengine as tengine

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""

    module_system = "tcl"
    _registry: ClassVar[Dict] = {}

    @staticmethod
    def make_layout(
        spec: spack.spec.Spec, module_set_name: str, explicit: Optional[bool] = None
    ) -> BaseFileLayout:
        return TclFileLayout(TclConfiguration.make_configuration(spec, module_set_name, explicit))

    @staticmethod
    def make_context(
        spec: spack.spec.Spec,
        module_set_name: str,
        *,
        explicit: Optional[bool] = None,
        layout: BaseFileLayout,
    ) -> BaseContext:
        configuration = TclConfiguration.make_configuration(spec, module_set_name, explicit)
        return TclContext(configuration, layout)


class TclFileLayout(BaseFileLayout):
    """File layout for tcl module files."""

    @property
    def modulerc(self):
        """Returns the modulerc file associated with current module file"""
        return os.path.join(os.path.dirname(self.filename), ".modulerc")


class TclContext(BaseContext):
    """Context class for tcl module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of("specs_to_prereq")

    @tengine.context_property
    def conditionally_unlocked_paths(self):
        """Returns the list of paths that are unlocked conditionally.
        Each item in the list is a tuple with the structure (condition, path).
        """
        layout = make_layout(self.spec, self.conf.name)
        value = []
        conditional_paths = layout.unlocked_paths
        conditional_paths.pop(None)
        for services_needed, list_of_path_parts in conditional_paths.items():
            condition = " && ".join(["[string length $" + x + "_name]" for x in services_needed])
            for parts in list_of_path_parts:

                def manipulate_path(token):
                    if token in self.conf.hierarchy_tokens:
                        return "{0}_name, {0}_version".format(token)
                    return '"' + token + '"'

                path = " ".join([manipulate_path(x) for x in parts])

                value.append((condition, path))
        return value


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    configuration_class = TclConfiguration

    default_template = "modules/modulefile.tcl"

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

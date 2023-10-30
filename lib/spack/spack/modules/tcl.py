# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate Tcl
non-hierarchical modules.
"""
import os.path
import posixpath
from typing import Any, Dict

import spack.config
import spack.tengine as tengine

from .common import BaseConfiguration, BaseContext, BaseFileLayout, BaseModuleFileWriter


#: Tcl specific part of the configuration
def configuration(module_set_name):
    config_path = "modules:%s:tcl" % module_set_name
    config = spack.config.get(config_path, {})
    return config


# Caches the configuration {spec_hash: configuration}
configuration_registry: Dict[str, Any] = {}


def make_configuration(spec, module_set_name, explicit):
    """Returns the tcl configuration for spec"""
    key = (spec.dag_hash(), module_set_name, explicit)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, TclConfiguration(spec, module_set_name, explicit)
        )


def make_layout(spec, module_set_name, explicit):
    """Returns the layout information for spec"""
    conf = make_configuration(spec, module_set_name, explicit)
    return TclFileLayout(conf)


def make_context(spec, module_set_name, explicit):
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name, explicit)
    return TclContext(conf)


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""


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


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""

    # Note: Posixpath is used here as opposed to
    # os.path.join due to spack.spec.Spec.format
    # requiring forward slash path seperators at this stage
    default_template = posixpath.join("modules", "modulefile.tcl")

    modulerc_header = ["#%Module4.7"]

    hide_cmd_format = "module-hide --soft --hidden-loaded %s"

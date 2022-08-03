# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate TCL
non-hierarchical modules.
"""
import os.path
import string
from typing import Any, Dict  # novm

import llnl.util.tty as tty

import spack.config
import spack.tengine as tengine

from .common import (
    BaseConfiguration,
    BaseContext,
    BaseFileLayout,
    BaseModuleFileWriter,
    root_path,
)

# configuration = spack.config.get('module_roots:ups_table', {})


#: TCL specific part of the configuration
def configuration(module_set_name):
    config_path = "modules:%s:ups_table" % module_set_name
    config = spack.config.get(config_path, {})
    if not config and module_set_name == "default":
        # return old format for backward compatibility
        return spack.config.get("modules:ups_table", {})
    return config


#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}  # type: Dict[str, Any]


def make_configuration(spec, module_set_name):
    """Returns the ups_table configuration for spec"""
    key = (spec.dag_hash(), module_set_name)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(key, UpsTableConfiguration(spec, module_set_name))


def make_layout(spec, module_set_name):
    """Returns the layout information for spec"""
    conf = make_configuration(spec, module_set_name)
    return UpsTableFileLayout(conf)


def make_context(spec, module_set_name):
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name)
    return UpsTableContext(conf)


class UpsTableConfiguration(BaseConfiguration):
    """Configuration class for ups_table module files."""

    @property
    def conflicts(self):
        """Conflicts for this module file"""
        return self.conf.get("conflict", [])


class UpsTableFileLayout(BaseFileLayout):
    """File layout for ups_table module files."""

    extension = "table"

    def dirname(self):
        return root_path("ups_table", "ups")

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        subdirname = self.spec.format("{name}").replace("-", "_")
        if not os.access(os.path.join(self.dirname(), subdirname), os.F_OK):
            os.makedirs(os.path.join(self.dirname(), subdirname))
        fn = "{}-{}-{}.table".format(self.spec.name, self.spec.version, self.spec._hash)
        fp = os.path.join(self.dirname(), subdirname, fn.replace("-", "_"))
        return fp


class UpsTableContext(BaseContext):
    """Context class for ups_table module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of("specs_to_prereq")

    @tengine.context_property
    def conflicts(self):
        """List of conflicts for the ups_table module file."""
        fmts = []
        f = string.Formatter()
        for item in self.conf.conflicts:
            naming_scheme = self.conf["naming_scheme"]
            if len([x for x in f.parse(item)]) > 1:
                for naming_dir, conflict_dir in zip(naming_scheme.split("/"), item.split("/")):
                    if naming_dir != conflict_dir:
                        message = "conflict scheme does not match naming "
                        message += "scheme [{spec}]\n\n"
                        message += 'naming scheme   : "{nformat}"\n'
                        message += 'conflict scheme : "{cformat}"\n\n'
                        message += "** You may want to check your "
                        message += "`modules.yaml` configuration file **\n"
                        tty.error(
                            message.format(spec=self.spec, nformat=naming_scheme, cformat=item)
                        )
                        raise SystemExit("Module generation aborted.")
                item = self.spec.format(item)
            fmts.append(item)
        # Substitute spec tokens if present
        return [self.spec.format(x) for x in fmts]


class UpsTableModulefileWriter(BaseModuleFileWriter):
    """Writer class for ups_table module files."""

    default_template = os.path.join("modules", "modulefile.ups_table")

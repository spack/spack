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

#: TCL specific part of the configuration
# configuration = spack.config.get('module_roots:ups_version', {})


def configuration(module_set_name):
    config_path = "modules:%s:ups_version" % module_set_name
    config = spack.config.get(config_path, {})
    if not config and module_set_name == "default":
        # return old format for backward compatibility
        return spack.config.get("modules:ups_version", {})
    return config


#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}  # type: Dict[str, Any]


def make_configuration(spec, module_set_name):
    """Returns the ups_version configuration for spec"""
    key = (spec.dag_hash(), module_set_name)
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, UpsVersionConfiguration(spec, module_set_name)
        )


def make_layout(spec, module_set_name):
    """Returns the layout information for spec"""
    conf = make_configuration(spec, module_set_name)
    return UpsVersionFileLayout(conf)


def make_context(spec, module_set_name):
    """Returns the context information for spec"""
    conf = make_configuration(spec, module_set_name)
    return UpsVersionContext(conf)


class UpsVersionConfiguration(BaseConfiguration):
    """Configuration class for ups_version module files."""

    @property
    def conflicts(self):
        """Conflicts for this module file"""
        return self.conf.get("conflict", [])


class UpsVersionFileLayout(BaseFileLayout):
    """File layout for ups_version module files."""

    def dirname(self):
        return root_path("ups_version", "ups")

    @property
    def filename(self):
        """Name of the module file for the current spec."""
        # Just the name of the file
        filename = os.path.basename(self.use_name)
        subdirname = self.spec.format("{name}/{version}.version").replace("-", "_")
        if not os.access(os.path.join(self.dirname(), subdirname), os.F_OK):
            os.makedirs(os.path.join(self.dirname(), subdirname))
        return os.path.join(self.dirname(), subdirname, filename)


class UpsVersionContext(BaseContext):
    """Context class for ups_version module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of("specs_to_prereq")

    @tengine.context_property
    def conflicts(self):
        """List of conflicts for the ups_version module file."""
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


class UpsVersionModulefileWriter(BaseModuleFileWriter):
    """Writer class for ups_version module files."""

    default_template = os.path.join("modules", "modulefile.ups_version")

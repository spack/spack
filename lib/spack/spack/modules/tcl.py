# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate TCL
non-hierarchical modules.
"""
import os.path
import string

import llnl.util.tty as tty

import spack.config
import spack.tengine as tengine
from .common import BaseConfiguration, BaseFileLayout
from .common import BaseContext, BaseModuleFileWriter


#: TCL specific part of the configuration
def configuration():
    return spack.config.get('modules:tcl', {})


#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}


def make_configuration(spec):
    """Returns the tcl configuration for spec"""
    key = spec.dag_hash()
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(key, TclConfiguration(spec))


def make_layout(spec):
    """Returns the layout information for spec """
    conf = make_configuration(spec)
    return TclFileLayout(conf)


def make_context(spec):
    """Returns the context information for spec"""
    conf = make_configuration(spec)
    return TclContext(conf)


class TclConfiguration(BaseConfiguration):
    """Configuration class for tcl module files."""

    @property
    def conflicts(self):
        """Conflicts for this module file"""
        return self.conf.get('conflict', [])


class TclFileLayout(BaseFileLayout):
    """File layout for tcl module files."""


class TclContext(BaseContext):
    """Context class for tcl module files."""

    @tengine.context_property
    def prerequisites(self):
        """List of modules that needs to be loaded automatically."""
        return self._create_module_list_of('specs_to_prereq')

    @tengine.context_property
    def conflicts(self):
        """List of conflicts for the tcl module file."""
        fmts = []
        naming_scheme = self.conf.naming_scheme
        f = string.Formatter()
        for item in self.conf.conflicts:
            if len([x for x in f.parse(item)]) > 1:
                for naming_dir, conflict_dir in zip(
                        naming_scheme.split('/'), item.split('/')
                ):
                    if naming_dir != conflict_dir:
                        message = 'conflict scheme does not match naming '
                        message += 'scheme [{spec}]\n\n'
                        message += 'naming scheme   : "{nformat}"\n'
                        message += 'conflict scheme : "{cformat}"\n\n'
                        message += '** You may want to check your '
                        message += '`modules.yaml` configuration file **\n'
                        tty.error(message.format(spec=self.spec,
                                                 nformat=naming_scheme,
                                                 cformat=item))
                        raise SystemExit('Module generation aborted.')
                item = self.spec.format(item)
            fmts.append(item)
        # Substitute spec tokens if present
        return [self.spec.format(x) for x in fmts]


class TclModulefileWriter(BaseModuleFileWriter):
    """Writer class for tcl module files."""
    default_template = os.path.join('modules', 'modulefile.tcl')

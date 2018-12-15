# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module implements the classes necessary to generate dotkit modules."""
import os.path

import spack.config
from .common import BaseConfiguration, BaseFileLayout
from .common import BaseContext, BaseModuleFileWriter

#: Dotkit specific part of the configuration
configuration = spack.config.get('modules:dotkit', {})

#: Caches the configuration {spec_hash: configuration}
configuration_registry = {}


def make_configuration(spec):
    """Returns the dotkit configuration for spec"""
    key = spec.dag_hash()
    try:
        return configuration_registry[key]
    except KeyError:
        return configuration_registry.setdefault(
            key, DotkitConfiguration(spec)
        )


def make_layout(spec):
    """Returns the layout information for spec """
    conf = make_configuration(spec)
    return DotkitFileLayout(conf)


def make_context(spec):
    """Returns the context information for spec"""
    conf = make_configuration(spec)
    return DotkitContext(conf)


class DotkitConfiguration(BaseConfiguration):
    """Configuration class for dotkit module files."""


class DotkitFileLayout(BaseFileLayout):
    """File layout for dotkit module files."""

    #: file extension of dotkit module files
    extension = 'dk'


class DotkitContext(BaseContext):
    """Context class for dotkit module files."""


class DotkitModulefileWriter(BaseModuleFileWriter):
    """Writer class for dotkit module files."""
    default_template = os.path.join('modules', 'modulefile.dk')

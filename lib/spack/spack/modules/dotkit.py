##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module implements the classes necessary to generate dotkit modules."""
import os.path

from . import common

#: Dotkit specific part of the configuration
configuration = common.configuration.get('dotkit', {})

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


class DotkitConfiguration(common.BaseConfiguration):
    """Configuration class for dotkit module files."""


class DotkitFileLayout(common.BaseFileLayout):
    """File layout for dotkit module files."""

    #: file extension of dotkit module files
    extension = 'dk'


class DotkitContext(common.BaseContext):
    """Context class for dotkit module files."""
    fields = [
        'category',
        'short_description',
        'long_description',
        'autoload',
        'environment_modifications'
    ]


class DotkitModulefileWriter(common.BaseModuleFileWriter):
    """Writer class for dotkit module files."""
    default_template = os.path.join('modules', 'modulefile.dk')

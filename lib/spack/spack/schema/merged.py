# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for configuration merged into one file.

.. literalinclude:: ../spack/schema/merged.py
   :lines: 40-
"""
from llnl.util.lang import union_dicts

import spack.schema.compilers
import spack.schema.config
import spack.schema.mirrors
import spack.schema.modules
import spack.schema.packages
import spack.schema.repos


#: Properties for inclusion in other schemas
properties = union_dicts(
    spack.schema.compilers.properties,
    spack.schema.config.properties,
    spack.schema.mirrors.properties,
    spack.schema.modules.properties,
    spack.schema.packages.properties,
    spack.schema.repos.properties
)


#: Full schema with metadata
schema = {
    '$schema': 'http://json-schema.org/schema#',
    'title': 'Spack merged configuration file schema',
    'definitions': spack.schema.modules.definitions,
    'type': 'object',
    'additionalProperties': False,
    'properties': properties,
}

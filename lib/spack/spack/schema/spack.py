# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for spack environment configuration file

.. literalinclude:: _spack_root/lib/spack/spack/schema/spack.py
   :lines: 20-
"""
from typing import Any, Dict

from llnl.util.lang import union_dicts

import spack.schema
import spack.schema.gitlab_ci  # Deprecated
import spack.schema.merged

include_properties: Dict[str, Any] = {
    "include": {"type": "array", "default": [], "items": {"type": "string"}}
}

spec_properties: Dict[str, Any] = {"specs": spack.schema.spec_list_schema}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "spack": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": union_dicts(
            # deprecated "gitlab-ci" section
            spack.schema.gitlab_ci.properties,
            # merged configuration scope schemas
            spack.schema.merged.properties,
            # extra environment schema properties
            include_properties,
            spec_properties,
            # environments themselves
            {"$ref": "#"},
        ),
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack environment file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for spack environment

.. literalinclude:: _spack_root/lib/spack/spack/schema/spack.py
   :lines: 20-
"""
from typing import Any, Dict

from llnl.util.lang import union_dicts

import spack.schema
import spack.schema.gitlab_ci as ci_schema  # DEPRECATED
import spack.schema.merged as merged_schema

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "spack": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": union_dicts(
            # Include deprecated "gitlab-ci" section
            ci_schema.properties,
            # merged configuration scope schemas
            merged_schema.properties,
            # extra environment schema properties
            {
                "include": {"type": "array", "default": [], "items": {"type": "string"}},
                "specs": spack.schema.spec_list_schema,
            },
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

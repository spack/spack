# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for definitions

.. literalinclude:: _spack_root/lib/spack/spack/schema/definitions.py
   :lines: 13-
"""

import spack.schema

#: Properties for inclusion in other schemas
properties = {
    "definitions": {
        "type": "array",
        "default": [],
        "items": {
            "type": "object",
            "properties": {"when": {"type": "string"}},
            "patternProperties": {r"^(?!when$)\w*": spack.schema.spec_list_schema},
        },
    }
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack definitions configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}

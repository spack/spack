# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for toolchains.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/toolchains.py
   :lines: 13-
"""
from typing import Any, Dict

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "toolchains": {
        "type": "object",
        "default": {},
        "description": "Define named compiler sets (toolchains) that group compiler constraints "
        "under a single user-defined name for easy reference with specs like %my_toolchain",
        "additionalProperties": {
            "description": "Named toolchain definition that can be referenced in specs to apply "
            "a complex set of compiler choices for C, C++, and Fortran",
            "oneOf": [
                {
                    "type": "string",
                    "description": "Simple toolchain alias containing a spec string directly",
                },
                {
                    "type": "array",
                    "description": "List of conditional compiler constraints and specifications "
                    "that define the toolchain behavior",
                    "items": {
                        "type": "object",
                        "description": "Individual toolchain entry with a spec constraint and "
                        "optional condition for when it applies",
                        "properties": {
                            "spec": {
                                "type": "string",
                                "description": "Spec constraint to apply such as compiler "
                                "selection (%c=llvm), flags (cflags=-O3), or other virtual "
                                "dependencies (%mpi=openmpi)",
                            },
                            "when": {
                                "type": "string",
                                "description": "Condition that determines when this spec "
                                "constraint is applied, typically checking for language "
                                "dependencies like %c, %cxx, %fortran, or other virtual packages "
                                "like %mpi",
                            },
                        },
                    },
                },
            ],
            "default": [],
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack toolchain configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}

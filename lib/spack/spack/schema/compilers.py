# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for compilers.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/compilers.py
   :lines: 15-
"""
from typing import Any, Dict

import spack.schema.environment

flags: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "description": "Flags to pass to the compiler during compilation and linking",
    "properties": {
        "cflags": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags for C compiler, e.g. -std=c11",
        },
        "cxxflags": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags for C++ compiler, e.g. -std=c++14",
        },
        "fflags": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags for Fortran 77 compiler, e.g. -ffixed-line-length-none",
        },
        "cppflags": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags for C preprocessor, e.g. -DFOO=1",
        },
        "ldflags": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags passed to the compiler driver during linking, e.g. "
            "-Wl,--gc-sections",
        },
        "ldlibs": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Flags for linker libraries, e.g. -lpthread",
        },
    },
}


extra_rpaths: Dict[str, Any] = {
    "type": "array",
    "default": [],
    "items": {"type": "string"},
    "description": "List of extra rpaths to inject by Spack's compiler wrappers",
}

implicit_rpaths: Dict[str, Any] = {
    "anyOf": [{"type": "array", "items": {"type": "string"}}, {"type": "boolean"}],
    "description": "List of non-default link directories to register at runtime as rpaths",
}

#: Properties for inclusion in other schemas
properties: Dict[str, Any] = {
    "compilers": {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "compiler": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["paths", "spec", "modules", "operating_system"],
                    "properties": {
                        "paths": {
                            "type": "object",
                            "required": ["cc", "cxx", "f77", "fc"],
                            "additionalProperties": False,
                            "properties": {
                                "cc": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "cxx": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "f77": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                                "fc": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                            },
                        },
                        "flags": flags,
                        "spec": {"type": "string"},
                        "operating_system": {"type": "string"},
                        "target": {"type": "string"},
                        "alias": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                        "modules": {
                            "anyOf": [
                                {"type": "null"},
                                {"type": "array", "items": {"type": "string"}},
                            ]
                        },
                        "implicit_rpaths": implicit_rpaths,
                        "environment": spack.schema.environment.definition,
                        "extra_rpaths": extra_rpaths,
                    },
                }
            },
        },
    }
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack compiler configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}

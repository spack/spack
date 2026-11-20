# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for filter.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/filter.py
   :lines: 18-
"""

from typing import Any, Dict

import spack.schema.projections

projection_scheme = spack.schema.projections.projections

allow_block = {
    # Shared shape, not matching semantics: specs use constraints, whereas config
    # and packages use section and package names. Empty allow means unrestricted;
    # empty block excludes nothing, and blocks take precedence over allows.
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "allow": {"type": "array", "default": [], "items": {"type": "string"}},
        "block": {"type": "array", "default": [], "items": {"type": "string"}},
    },
}

packages_filter = {
    # These select whole package entries, not specs or individual externals.
    # externals_only keeps entries with an externals key, including other settings.
    "default": "all",
    "oneOf": [{"type": "string", "enum": ["all", "externals_only"]}, allow_block],
}

properties: Dict[str, Any] = {
    "filter": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "properties": {
            # Concrete root text only; abstract roots use str(spec), ignoring projections.
            "projections": projection_scheme,
            # False filters only manifest specs and explicit dependencies, with no
            # output lockfile. True preserves selected locked DAGs without reconcretizing.
            "concrete": {"type": "boolean", "default": False},
            # Promote dependencies only after block checks; never rescue rejected DAGs.
            "flatten": {"type": "boolean", "default": False},
            # In both modes, collect entire sub-DAGs at the first allow match on each
            # path, then reject any candidate containing a block match, then flatten.
            # Abstract mode never discovers implicit dependencies from package recipes.
            "specs": allow_block,
            # Applies only if config retains packages; specs:block also removes entries
            # by package name, but specs:allow does not restrict package configuration.
            "packages": packages_filter,
            # Select copied sections independently of spec selection. Includes are
            # never copied, and the selected specs are written regardless of this filter.
            "config": allow_block,
        },
    }
}

schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack filter configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}

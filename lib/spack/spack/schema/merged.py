# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for configuration merged into one file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/merged.py
   :lines: 32-
"""

from typing import Any, Dict

import spack.schema.merged_no_specs
import spack.schema.specs

#: Properties for inclusion in other schemas
sections: Dict[str, Any] = spack.schema.merged_no_specs.sections
sections.update(spack.schema.specs.properties)

#: Canonical definitions for JSON Schema $ref
defs: Dict[str, Any] = {
    # Section schemas, prefixed to avoid collisions with sub-schema definitions
    **{f"section_{name}": schema for name, schema in sections.items()},
    # Sub-schema definitions hoisted for $ref resolution in env.py
    "ci_job_attributes": spack.schema.ci.ci_job_attributes,
    "env_modifications": spack.schema.environment.env_modifications,
    "module_file_configuration": spack.schema.modules.module_file_configuration,
    "projections": spack.schema.projections.projections,
    "spec_list_schema": spack.schema.specs.spec_list_schema,
}

#: Properties using $ref pointers into $defs
ref_sections: Dict[str, Any] = {
    **spack.schema.merged_no_specs.ref_sections,
    "specs": {"$ref": f"#/definitions/section_specs"}
}

#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack merged configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": ref_sections,
    "definitions": defs,
}

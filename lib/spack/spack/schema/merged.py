# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for configuration merged into one file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/merged.py
   :lines: 32-
"""

from typing import Any, Dict

import spack.schema.bootstrap
import spack.schema.cdash
import spack.schema.ci
import spack.schema.compilers
import spack.schema.concretizer
import spack.schema.config
import spack.schema.container
import spack.schema.definitions
import spack.schema.develop
import spack.schema.env_vars
import spack.schema.environment
import spack.schema.include
import spack.schema.mirrors
import spack.schema.modules
import spack.schema.packages
import spack.schema.projections
import spack.schema.repos
import spack.schema.toolchains
import spack.schema.upstreams
import spack.schema.view

#: Properties for inclusion in other schemas
sections: Dict[str, Any] = {
    **spack.schema.bootstrap.properties,
    **spack.schema.cdash.properties,
    **spack.schema.compilers.properties,
    **spack.schema.concretizer.properties,
    **spack.schema.config.properties,
    **spack.schema.container.properties,
    **spack.schema.ci.properties,
    **spack.schema.definitions.properties,
    **spack.schema.develop.properties,
    **spack.schema.env_vars.properties,
    **spack.schema.include.properties,
    **spack.schema.mirrors.properties,
    **spack.schema.modules.properties,
    **spack.schema.packages.properties,
    **spack.schema.repos.properties,
    **spack.schema.toolchains.properties,
    **spack.schema.upstreams.properties,
    **spack.schema.view.properties,
}

#: Canonical definitions for JSON Schema $ref
defs: Dict[str, Any] = {
    # Section schemas, prefixed to avoid collisions with sub-schema definitions
    **{f"section_{name}": schema for name, schema in sections.items()},
    # Sub-schema definitions hoisted for $ref resolution in env.py
    "ci_job_attributes": spack.schema.ci.ci_job_attributes,
    "env_modifications": spack.schema.environment.env_modifications,
    "module_file_configuration": spack.schema.modules.module_file_configuration,
    "projections": spack.schema.projections.projections,
}

#: Properties using $ref pointers into $defs
ref_sections: Dict[str, Any] = {
    name: {"$ref": f"#/definitions/section_{name}"} for name in sections
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

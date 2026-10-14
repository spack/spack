# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""JSON pipeline generator."""

import json
import os

from .common import PipelineDag, PipelineOptions, SpackCIConfig
from .generator_registry import generator


@generator("json")
def generate_json_pipeline(
    pipeline: PipelineDag, spack_ci: SpackCIConfig, options: PipelineOptions
) -> None:
    """Write the pruned build graph to a JSON file."""
    output_file = options.output_file or os.path.abspath("ci.json")
    with open(output_file, "w", encoding="utf-8") as stream:
        json.dump(pipeline.to_dict(), stream, indent=2)
        stream.write("\n")

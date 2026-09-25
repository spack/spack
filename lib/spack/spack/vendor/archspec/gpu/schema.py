# Copyright 2019-2026 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Global objects with the content of the GPU microarchitecture JSON file and its schema"""

import os
import pathlib

from ..cpu.schema import LazyDictionary, _load

#: Environment variable that might point to a directory with a user defined JSON file
DIR_FROM_ENVIRONMENT = "ARCHSPEC_GPU_DIR"


def _json_file(filename: str, allow_custom: bool = False) -> pathlib.Path:
    """Given a filename, returns the absolute path for the GPU JSON file.

    Args:
        filename: filename for the JSON file
        allow_custom: if True, allows overriding the location where the file resides
    """
    json_dir = pathlib.Path(__file__).parent / ".." / "json" / "gpu"
    if allow_custom and DIR_FROM_ENVIRONMENT in os.environ:
        json_dir = pathlib.Path(os.environ[DIR_FROM_ENVIRONMENT])
    return (json_dir / filename).absolute()


#: In memory representation of the data in microarchitectures.json, loaded on first access
TARGETS_JSON = LazyDictionary(
    _load, _json_file("microarchitectures.json", allow_custom=True), None
)

#: JSON schema for microarchitectures.json, loaded on first access
TARGETS_JSON_SCHEMA = LazyDictionary(_load, _json_file("microarchitectures_schema.json"), None)

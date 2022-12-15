# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Schema for mirrors.yaml configuration file.

.. literalinclude:: _spack_root/lib/spack/spack/schema/mirrors.py
   :lines: 14-46
"""

import spack.util.url as url_util

#: Properties for inclusion in other schemas
properties = {
    "mirrors": {
        "type": "object",
        "default": {},
        "additionalProperties": False,
        "patternProperties": {
            r"\w[\w-]*": {
                "anyOf": [
                    {"type": "string"},
                    {
                        "type": "object",
                        "required": ["fetch", "push"],
                        "properties": {
                            "fetch": {"type": ["string", "object"]},
                            "push": {"type": ["string", "object"]},
                        },
                    },
                ]
            },
        },
    },
}


#: Full schema with metadata
schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Spack mirror configuration file schema",
    "type": "object",
    "additionalProperties": False,
    "properties": properties,
}


def update(data):
    # Look for filesystem paths that should be replaced by URLs
    changed = False

    for mirror, info in data.items():
        if isinstance(info, str):
            if not url_util.is_path_instead_of_url(info):
                continue
            data[mirror] = url_util.path_to_file_url(info)
            changed = True
        elif isinstance(info, dict):
            for key in ("fetch", "push"):
                entry = info.get(key, None)
                if not isinstance(entry, dict):
                    continue
                url = entry.get("url", None)
                if not isinstance(url, str) or not url_util.is_path_instead_of_url(url):
                    continue
                entry["url"] = url_util.path_to_file_url(url)
                changed = True
    return changed

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Schema for environment modifications. Meant for inclusion in other
schemas.
"""

import collections.abc
from typing import Any, Dict

dictionary_of_strings_or_num = {
    "type": "object",
    "additionalProperties": {"anyOf": [{"type": "string"}, {"type": "number"}]},
}

env_modifications: Dict[str, Any] = {
    "type": "object",
    "description": "Environment variable modifications to apply at runtime",
    "default": {},
    "additionalProperties": False,
    "properties": {
        "set": {
            "description": "Environment variables to set to specific values",
            **dictionary_of_strings_or_num,
        },
        "unset": {
            "description": "Environment variables to remove/unset",
            "default": [],
            "type": "array",
            "items": {"type": "string"},
        },
        "prepend_path": {
            "description": "Environment variables to prepend values to (typically PATH-like "
            "variables)",
            **dictionary_of_strings_or_num,
        },
        "append_path": {
            "description": "Environment variables to append values to (typically PATH-like "
            "variables)",
            **dictionary_of_strings_or_num,
        },
        "remove_path": {
            "description": "Values to remove from PATH-like environment variables",
            **dictionary_of_strings_or_num,
        },
        "include": {
            "description": "Only modify these environment variables, also when the "
            "modifications come from elsewhere (e.g. prefix inspections or packages)",
            "type": "array",
            "items": {"type": "string"},
        },
        "exclude": {
            "description": "Do not modify these environment variables, also when the "
            "modifications come from elsewhere (e.g. prefix inspections or packages)",
            "type": "array",
            "items": {"type": "string"},
        },
    },
}

#: $ref pointer for use in merged schema
ref_env_modifications = {"$ref": "#/definitions/env_modifications"}


def parse(config_obj):
    """Returns an EnvironmentModifications object containing the modifications
    parsed from input.

    Args:
        config_obj: a configuration dictionary conforming to the
            schema definition for environment modifications
    """
    import spack.util.environment as ev

    env = ev.EnvironmentModifications()
    for command, variable in config_obj.items():
        if command in ("include", "exclude"):
            continue
        # Distinguish between commands that take only a name as argument
        # (e.g. unset) and commands that take a name and a value.
        if isinstance(variable, collections.abc.Sequence):
            for name in variable:
                getattr(env, command)(name)
        else:
            for name, value in variable.items():
                getattr(env, command)(name, value)

    return env


def filter_modifications(env, config_obj) -> None:
    """Drops the modifications of environment variables that are not allowed by the
    ``include`` and ``exclude`` lists of a configuration dictionary.

    Args:
        env: the environment modifications to filter in place
        config_obj: a configuration dictionary conforming to the
            schema definition for environment modifications
    """
    include = config_obj.get("include")
    exclude = config_obj.get("exclude", [])
    env.env_modifications = [
        x
        for x in env.env_modifications
        if (include is None or x.name in include) and x.name not in exclude
    ]

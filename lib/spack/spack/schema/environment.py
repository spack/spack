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

definition: Dict[str, Any] = {
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
    },
}


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
        # Distinguish between commands that take only a name as argument
        # (e.g. unset) and commands that take a name and a value.
        if isinstance(variable, collections.abc.Sequence):
            for name in variable:
                getattr(env, command)(name)
        else:
            for name, value in variable.items():
                getattr(env, command)(name, value)

    return env

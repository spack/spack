# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module contains jsonschema files for all of Spack's YAML formats."""
import warnings

import llnl.util.lang
import llnl.util.tty


# jsonschema is imported lazily as it is heavy to import
# and increases the start-up time
def _make_validator():
    import jsonschema

    import spack.parser

    def _validate_spec(validator, is_spec, instance, schema):
        """Check if the attributes on instance are valid specs."""
        import jsonschema

        if not validator.is_type(instance, "object"):
            return

        for spec_str in instance:
            try:
                spack.parser.parse(spec_str)
            except spack.parser.SpecSyntaxError as e:
                yield jsonschema.ValidationError(str(e))

    def _deprecated_properties(validator, deprecated, instance, schema):
        if not (validator.is_type(instance, "object") or validator.is_type(instance, "array")):
            return

        # Get a list of the deprecated properties, return if there is none
        deprecated_properties = [x for x in instance if x in deprecated["properties"]]
        if not deprecated_properties:
            return

        # Retrieve the template message
        msg_str_or_func = deprecated["message"]
        if isinstance(msg_str_or_func, str):
            msg = msg_str_or_func.format(properties=deprecated_properties)
        else:
            msg = msg_str_or_func(instance, deprecated_properties)
            if msg is None:
                return

        is_error = deprecated["error"]
        if not is_error:
            warnings.warn(msg)
        else:
            import jsonschema

            yield jsonschema.ValidationError(msg)

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator,
        {"validate_spec": _validate_spec, "deprecatedProperties": _deprecated_properties},
    )


Validator = llnl.util.lang.Singleton(_make_validator)

spec_list_schema = {
    "type": "array",
    "default": [],
    "items": {
        "anyOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "matrix": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                    },
                    "exclude": {"type": "array", "items": {"type": "string"}},
                },
            },
            {"type": "string"},
            {"type": "null"},
        ]
    },
}

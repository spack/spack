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
    import jsonschema  # pylint: disable=import-outside-toplevel

    import spack.parser  # pylint: disable=import-outside-toplevel

    def _validate_spec(validator, is_spec, instance, schema):
        """Check if the attributes on instance are valid specs."""
        # pylint: disable=unused-argument
        if not validator.is_type(instance, "object"):
            return

        for spec_str in instance:
            try:
                spack.parser.parse(spec_str)
            except spack.parser.SpecSyntaxError as exc:
                yield jsonschema.ValidationError(str(exc))

    def _deprecated_properties(validator, deprecated, instance, schema):
        # pylint: disable=unused-argument
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
            yield jsonschema.ValidationError(msg)

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator,
        {"validate_spec": _validate_spec, "deprecatedProperties": _deprecated_properties},
    )


Validator = llnl.util.lang.Singleton(_make_validator)

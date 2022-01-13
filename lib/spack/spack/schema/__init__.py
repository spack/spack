# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module contains jsonschema files for all of Spack's YAML formats."""

import six

import llnl.util.lang
import llnl.util.tty

import spack.spec


# jsonschema is imported lazily as it is heavy to import
# and increases the start-up time
def _make_validator():
    import jsonschema

    def _validate_spec(validator, is_spec, instance, schema):
        """Check if the attributes on instance are valid specs."""
        import jsonschema
        if not validator.is_type(instance, "object"):
            return

        for spec_str in instance:
            try:
                spack.spec.parse(spec_str)
            except spack.spec.SpecParseError as e:
                yield jsonschema.ValidationError(
                    '"{0}" is an invalid spec [{1}]'.format(spec_str, str(e))
                )

    def _deprecated_properties(validator, deprecated, instance, schema):
        if not (validator.is_type(instance, "object") or
                validator.is_type(instance, "array")):
            return

        # Get a list of the deprecated properties, return if there is none
        deprecated_properties = [
            x for x in instance if x in deprecated['properties']
        ]
        if not deprecated_properties:
            return

        # Retrieve the template message
        msg_str_or_func = deprecated['message']
        if isinstance(msg_str_or_func, six.string_types):
            msg = msg_str_or_func.format(properties=deprecated_properties)
        else:
            msg = msg_str_or_func(instance, deprecated_properties)

        is_error = deprecated['error']
        if not is_error:
            llnl.util.tty.warn(msg)
        else:
            import jsonschema
            yield jsonschema.ValidationError(msg)

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator, {
            "validate_spec": _validate_spec,
            "deprecatedProperties": _deprecated_properties
        }
    )


Validator = llnl.util.lang.Singleton(_make_validator)

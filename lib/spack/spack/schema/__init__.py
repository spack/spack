# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains jsonschema files for all of Spack's YAML formats."""

import copy
import re

import six

import llnl.util.lang
import spack.spec


# jsonschema is imported lazily as it is heavy to import
# and increases the start-up time
def _make_validator():
    import jsonschema
    _validate_properties = jsonschema.Draft4Validator.VALIDATORS["properties"]
    _validate_pattern_properties = jsonschema.Draft4Validator.VALIDATORS[
        "patternProperties"
    ]

    def _set_defaults(validator, properties, instance, schema):
        """Adds support for the 'default' attribute in 'properties'.

        ``jsonschema`` does not handle this out of the box -- it only
        validates. This allows us to set default values for configs
        where certain fields are `None` b/c they're deleted or
        commented out.
        """
        for property, subschema in six.iteritems(properties):
            if "default" in subschema:
                instance.setdefault(
                    property, copy.deepcopy(subschema["default"]))
        for err in _validate_properties(
                validator, properties, instance, schema):
            yield err

    def _set_pp_defaults(validator, properties, instance, schema):
        """Adds support for the 'default' attribute in 'patternProperties'.

        ``jsonschema`` does not handle this out of the box -- it only
        validates. This allows us to set default values for configs
        where certain fields are `None` b/c they're deleted or
        commented out.
        """
        for property, subschema in six.iteritems(properties):
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in six.iteritems(instance):
                        if re.match(property, key) and val is None:
                            instance[key] = copy.deepcopy(subschema["default"])

        for err in _validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

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

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator, {
            "validate_spec": _validate_spec,
            "properties": _set_defaults,
            "patternProperties": _set_pp_defaults
        }
    )


Validator = llnl.util.lang.Singleton(_make_validator)

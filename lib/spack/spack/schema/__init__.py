# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains jsonschema files for all of Spack's YAML formats."""

import copy
import re

import jsonschema
import six

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


Validator = jsonschema.validators.extend(
    jsonschema.Draft4Validator, {
        "properties": _set_defaults,
        "patternProperties": _set_pp_defaults
    }
)

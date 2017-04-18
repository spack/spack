##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module contains jsonschema files for all of Spack's YAML formats.
"""
import re
import jsonschema
from jsonschema import Draft4Validator, validators
from six import iteritems

from llnl.util.lang import list_modules

import spack.error


__all__ = ['validate', 'FileFormatError']

# Automatically bring in all sub-modules
for mod in list_modules(__path__[0]):
    __import__('%s.%s' % (__name__, mod))
    __all__.append(mod)


def extend_with_default(validator_class):
    """Add support for the 'default' attr for properties and patternProperties.

       jsonschema does not handle this out of the box -- it only
       validates.  This allows us to set default values for configs
       where certain fields are `None` b/c they're deleted or
       commented out.

    """
    validate_properties = validator_class.VALIDATORS["properties"]
    validate_pattern_properties = validator_class.VALIDATORS[
        "patternProperties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])
        for err in validate_properties(
                validator, properties, instance, schema):
            yield err

    def set_pp_defaults(validator, properties, instance, schema):
        for property, subschema in iteritems(properties):
            if "default" in subschema:
                if isinstance(instance, dict):
                    for key, val in iteritems(instance):
                        if re.match(property, key) and val is None:
                            instance[key] = subschema["default"]

        for err in validate_pattern_properties(
                validator, properties, instance, schema):
            yield err

    return validators.extend(validator_class, {
        "properties": set_defaults,
        "patternProperties": set_pp_defaults
    })


DefaultSettingValidator = extend_with_default(Draft4Validator)


def validate(data, schema):
    """Validate data read in from a Spack YAML file.

    This leverages the line information (start_mark, end_mark) stored on
    Spack YAML structures.
    """
    try:
        DefaultSettingValidator(schema).validate(data)
    except jsonschema.ValidationError as e:
        raise FileFormatError(e, data)


class SchemaError(spack.error.SpackError):
    """Superclass for schema related errors."""


def get_path(path, data):
    if path:
        return get_path(path[1:], data[path[0]])
    else:
        return data


class FileFormatError(SchemaError):
    """Raised when a configuration format does not match its schema."""

    def __init__(self, validation_error, data):
        # Try to get line number from erroneous instance and its parent
        instance_mark = getattr(validation_error.instance, '_start_mark', None)
        parent_mark = getattr(validation_error.parent, '_start_mark', None)
        path = [str(s) for s in getattr(validation_error, 'path', None)]

        # Try really hard to get the parent (which sometimes is not
        # set) This digs it out of the validated structure if it's not
        # on the validation_error.
        if path and not parent_mark:
            parent_path = list(path)[:-1]
            parent = get_path(parent_path, data)
            if path[-1] in parent:
                if isinstance(parent, dict):
                    keylist = list(parent.keys())
                elif isinstance(parent, list):
                    keylist = parent
                idx = keylist.index(path[-1])
                parent_mark = getattr(keylist[idx], '_start_mark', None)

        if instance_mark:
            location = '%s:%d' % (instance_mark.name, instance_mark.line + 1)
        elif parent_mark:
            location = '%s:%d' % (parent_mark.name, parent_mark.line + 1)
        elif path:
            location = 'At ' + ':'.join(path)
        else:
            location = '<unknown line>'

        message = '%s: %s' % (location, validation_error.message)
        super(FileFormatError, self).__init__(message)

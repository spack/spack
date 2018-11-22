# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import jsonschema
import pytest


import spack.schema


@pytest.fixture()
def validate_spec_schema():
    return {
        'type': 'object',
        'validate_spec': True,
        'patternProperties': {
            r'\w[\w-]*': {
                'type': 'string'
            }
        }
    }


@pytest.fixture()
def module_suffixes_schema():
    return {
        'type': 'object',
        'properties': {
            'tcl': {
                'type': 'object',
                'patternProperties': {
                    r'\w[\w-]*': {
                        'type': 'object',
                        'properties': {
                            'suffixes': {
                                'validate_spec': True,
                                'patternProperties': {
                                    r'\w[\w-]*': {
                                        'type': 'string',
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


@pytest.mark.regression('9857')
def test_validate_spec(validate_spec_schema):
    v = spack.schema.Validator(validate_spec_schema)
    data = {'foo@3.7': 'bar'}

    # Validate good data (the key is a spec)
    v.validate(data)

    # Check that invalid data throws
    data['^python@3.7@'] = 'baz'
    with pytest.raises(jsonschema.ValidationError) as exc_err:
        v.validate(data)

    assert 'is an invalid spec' in str(exc_err.value)


@pytest.mark.regression('9857')
def test_module_suffixes(module_suffixes_schema):
    v = spack.schema.Validator(module_suffixes_schema)
    data = {'tcl': {'all': {'suffixes': {'^python@2.7@': 'py2.7'}}}}

    with pytest.raises(jsonschema.ValidationError) as exc_err:
        v.validate(data)

    assert 'is an invalid spec' in str(exc_err.value)

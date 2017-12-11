##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from copy import deepcopy

import pytest
import spack
from spack.config import validate_section, ConfigFormatError
from spack.spec import FlagMap
from spack.util.spack_yaml import syaml_dict, syaml_str, syaml_list


@pytest.fixture()
def minimal_config():
    return syaml_dict({
        'paths': syaml_dict((c, None) for c in ['cc', 'cxx', 'f77', 'fc']),
        'spec': syaml_str(),
        'operating_system': syaml_str(),
        'modules': syaml_list()
    })


optional_with_default = {
    'environment': syaml_dict(),
    'extra_rpaths': syaml_list(),
}

optional_without_default = {
    'alias': None,
    'flags': syaml_dict(),
    'target': syaml_str()
}


def wrap_for_validation(single_compiler_config):
    return syaml_dict(
        {'compilers': [syaml_dict({'compiler': single_compiler_config})]}
    )


def unwrap_after_validation(compilers_config):
    return compilers_config['compilers'][0]['compiler']


def test_minimal_and_defaults(minimal_config):
    """Checks that the minimal configuration is accepted and the optional
    fields are initialized with expected values."""

    config = wrap_for_validation(minimal_config)

    validate_section(config, spack.schema.compilers.schema)

    config = unwrap_after_validation(config)

    for name, value in optional_with_default.items():
        assert name in config
        assert config[name] == value


def test_minimal_is_minimal(minimal_config):
    """Checks that the minimal configuration is really minimal."""

    def deep_copy_without_field(d):
        for field_name, field_value in d.items():
            result = deepcopy(d)
            del result[field_name]
            yield field_name, result
            if isinstance(field_value, dict):
                for sub_name, sub_result in deep_copy_without_field(
                        field_value):
                    result[field_name] = sub_result
                    yield sub_name, result

    for deleted_field, wrong_config in deep_copy_without_field(
            minimal_config):
        with pytest.raises(ConfigFormatError) as e:
            validate_section(wrap_for_validation(wrong_config),
                             spack.schema.compilers.schema)
        expected_message_substring = \
            '\'' + deleted_field + '\' is a required property'
        assert expected_message_substring in str(e.value)


def test_full_accepted(minimal_config):
    """Checks that config with all possible fields is accepted."""
    config = minimal_config
    config.update(dict((n, t) for n, t in optional_with_default.items()))
    config.update(dict((n, t) for n, t in optional_without_default.items()))
    validate_section(wrap_for_validation(config),
                     spack.schema.compilers.schema)


def test_additional_not_allowed(minimal_config):
    """Checks that configs with unexpected fields are not accepted."""

    def deep_copy_with_additional_field(d, add_name, add_value):
        result = deepcopy(d)
        result[add_name] = add_value
        yield result
        for field_name, field_value in d.items():
            if isinstance(field_value, dict):
                for sub_result in deep_copy_with_additional_field(field_value,
                                                                  add_name,
                                                                  add_value):
                    result = deepcopy(d)
                    result[field_name] = sub_result
                    yield result

    config = minimal_config
    config.update(dict((n, t) for n, t in optional_with_default.items()))

    for wrong_config in deep_copy_with_additional_field(
            config, 'ADDITIONAL_FIELD', 'ADDITIONAL_VALUE'):
        with pytest.raises(ConfigFormatError) as e:
            validate_section(wrap_for_validation(wrong_config),
                             spack.schema.compilers.schema)
        expected_message_if_dict = '\'ADDITIONAL_FIELD\' was unexpected'
        assert expected_message_if_dict in str(e.value)


def test_compiler_flags(minimal_config):
    """Checks that the supported set of compiler flags is accepted."""

    config = minimal_config
    config['flags'] = syaml_dict((flag, syaml_str('')) for flag
                                 in FlagMap.valid_compiler_flags())

    validate_section(wrap_for_validation(config),
                     spack.schema.compilers.schema)

    config['flags']['UNSUPPORTED_FLAG'] = syaml_str('')

    with pytest.raises(ConfigFormatError) as e:
        validate_section(wrap_for_validation(config),
                         spack.schema.compilers.schema)
    expected_message_if_dict = '\'UNSUPPORTED_FLAG\' was unexpected'
    assert expected_message_if_dict in str(e.value)

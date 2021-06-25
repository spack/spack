# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.audit
import spack.config


@pytest.mark.parametrize('packages,failing_check', [
    # A non existing variant is used in a conflict directive
    (['wrong-variant-in-conflicts'], 'PKG-DIRECTIVES'),
    # The package declares a non-existing dependency
    (['missing-dependency'], 'PKG-DIRECTIVES'),
    # The package use a non existing variant in a depends_on directive
    (['wrong-variant-in-depends-on'], 'PKG-DIRECTIVES'),
    # This package has no issues
    (['mpileaks'], None)
])
def test_package_audits(packages, failing_check, mock_packages):
    reports = spack.audit.run_group('packages', pkgs=packages)

    for check, errors in reports:
        # Check that we have errors only if there is an expected failure
        # and that the tag matches our expectations
        if bool(failing_check):
            assert check == failing_check
            assert errors
        else:
            assert not errors


# Data used in the test below to audit the double definition of a compiler
_double_compiler_definition = [
    {'compiler': {
        'spec': 'gcc@9.0.1',
        'paths': {
            'cc': '/usr/bin/gcc-9',
            'cxx': '/usr/bin/g++-9',
            'f77': '/usr/bin/gfortran-9',
            'fc': '/usr/bin/gfortran-9'
        },
        'flags': {},
        'operating_system': 'ubuntu18.04',
        'target': 'x86_64',
        'modules': [],
        'environment': {},
        'extra_rpaths': []
    }},
    {'compiler': {
        'spec': 'gcc@9.0.1',
        'paths': {
            'cc': '/usr/bin/gcc-9',
            'cxx': '/usr/bin/g++-9',
            'f77': '/usr/bin/gfortran-9',
            'fc': '/usr/bin/gfortran-9'
        },
        'flags': {"cflags": "-O3"},
        'operating_system': 'ubuntu18.04',
        'target': 'x86_64',
        'modules': [],
        'environment': {},
        'extra_rpaths': []
    }}
]


@pytest.mark.parametrize('config_section,data,failing_check', [
    # Double compiler definitions in compilers.yaml
    ('compilers', _double_compiler_definition, 'CFG-COMPILER'),
    # Multiple definitions of the same external spec in packages.yaml
    ('packages', {
        "mpileaks": {"externals": [
            {"spec": "mpileaks@1.0.0", "prefix": "/"},
            {"spec": "mpileaks@1.0.0", "prefix": "/usr"},
        ]}
    }, 'CFG-PACKAGES')
])
def test_config_audits(config_section, data, failing_check):
    with spack.config.override(config_section, data):
        reports = spack.audit.run_group('configs')
        assert any(
            (check == failing_check) and errors for check, errors in reports
        )

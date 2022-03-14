# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import spack.cmd.info
from spack.main import SpackCommand

info = SpackCommand('info')


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.info.setup_parser(prs)
    return prs


@pytest.fixture()
def info_lines():
    lines = []
    return lines


@pytest.fixture()
def mock_print(monkeypatch, info_lines):

    def _print(*args):
        info_lines.extend(args)

    monkeypatch.setattr(spack.cmd.info.color, 'cprint', _print, raising=False)


@pytest.mark.parametrize('pkg', [
    'openmpi',
    'trilinos',
    'boost',
    'python',
    'dealii',
    'xsdk'  # a BundlePackage
])
def test_it_just_runs(pkg):
    info(pkg)


def test_info_noversion(mock_packages, info_lines, mock_print):
    """Check that a mock package with no versions or variants outputs None."""
    info('noversion')

    line_iter = info_lines.__iter__()
    for line in line_iter:
        if 'version' in line:
            has = [desc in line for desc in ['Preferred', 'Safe', 'Deprecated']]
            if not any(has):
                continue
        elif 'Variants' not in line:
            continue

        assert 'None' in next(line_iter).strip()


@pytest.mark.parametrize('pkg_query,expected', [
    ('zlib', 'False'),
    ('gcc', 'True (version, variants)'),
])
@pytest.mark.usefixtures('mock_print')
def test_is_externally_detectable(pkg_query, expected, parser, info_lines):
    args = parser.parse_args([pkg_query])
    spack.cmd.info.info(parser, args)

    line_iter = info_lines.__iter__()
    for line in line_iter:
        if 'Externally Detectable' in line:
            is_externally_detectable = next(line_iter).strip()
            assert is_externally_detectable == expected


@pytest.mark.parametrize('pkg_query', [
    'hdf5',
    'cloverleaf3d',
    'trilinos'
])
@pytest.mark.usefixtures('mock_print')
def test_info_fields(pkg_query, parser, info_lines):

    expected_fields = (
        'Description:',
        'Homepage:',
        'Externally Detectable:',
        'Safe versions:',
        'Variants:',
        'Installation Phases:',
        'Virtual Packages:',
        'Tags:'
    )

    args = parser.parse_args([pkg_query])
    spack.cmd.info.info(parser, args)

    for text in expected_fields:
        match = [x for x in info_lines if text in x]
        assert match

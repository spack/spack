# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import sys

import pytest

import spack.cmd.info
from spack.main import SpackCommand

info = SpackCommand('info')

pytestmark = pytest.mark.skipif(sys.platform == 'win32',
                                reason="Not yet implemented on Windows")


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.info.setup_parser(prs)
    return prs


@pytest.fixture()
def print_buffer(monkeypatch):
    buffer = []

    def _print(*args):
        buffer.extend(args)

    monkeypatch.setattr(spack.cmd.info.color, 'cprint', _print, raising=False)
    return buffer


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


def test_info_noversion(mock_packages, print_buffer):
    """Check that a mock package with no versions or variants outputs None."""
    info('noversion')

    line_iter = iter(print_buffer)
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
def test_is_externally_detectable(pkg_query, expected, parser, print_buffer):
    args = parser.parse_args(['--detectable', pkg_query])
    spack.cmd.info.info(parser, args)

    line_iter = iter(print_buffer)
    for line in line_iter:
        if 'Externally Detectable' in line:
            is_externally_detectable = next(line_iter).strip()
            assert is_externally_detectable == expected


@pytest.mark.parametrize('pkg_query', [
    'hdf5',
    'cloverleaf3d',
    'trilinos',
    'gcc'    # This should ensure --test's c_names processing loop covered
])
def test_info_fields(pkg_query, parser, print_buffer):
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

    args = parser.parse_args(['--all', pkg_query])
    spack.cmd.info.info(parser, args)

    for text in expected_fields:
        assert any(x for x in print_buffer if text in x)

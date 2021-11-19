# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import llnl.util.tty as tty

import spack.cmd.checksum
import spack.repo
from spack.main import SpackCommand

spack_checksum = SpackCommand('checksum')


@pytest.mark.parametrize('arguments,expected', [
    (['--batch', 'patch'], (True, False, False)),
    (['--latest', 'patch'], (False, True, False)),
    (['--preferred', 'patch'], (False, False, True)),
])
def test_checksum_args(arguments, expected):
    parser = argparse.ArgumentParser()
    spack.cmd.checksum.setup_parser(parser)
    args = parser.parse_args(arguments)
    check = args.batch, args.latest, args.preferred
    assert check == expected


@pytest.mark.parametrize('arguments,expected', [
    (['--batch', 'preferred-test'], 'versions of preferred-test'),
    (['--latest', 'preferred-test'], 'Found 1 version'),
    (['--preferred', 'preferred-test'], 'Found 1 version'),
])
def test_checksum(arguments, expected, mock_packages, mock_stage):
    output = spack_checksum(*arguments)
    assert expected in output
    assert 'version(' in output


def test_checksum_interactive(
        mock_packages, mock_fetch, mock_stage, monkeypatch):
    def _get_number(*args, **kwargs):
        return 1
    monkeypatch.setattr(tty, 'get_number', _get_number)

    output = spack_checksum('preferred-test')
    assert 'versions of preferred-test' in output
    assert 'version(' in output


def test_checksum_versions(mock_packages, mock_fetch, mock_stage):
    pkg = spack.repo.get('preferred-test')

    versions = [str(v) for v in pkg.versions if not v.isdevelop()]
    output = spack_checksum('preferred-test', versions[0])
    assert 'Found 1 version' in output
    assert 'version(' in output

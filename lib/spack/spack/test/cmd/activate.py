# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand

activate = SpackCommand('activate')
deactivate = SpackCommand('deactivate')
install = SpackCommand('install')
extensions = SpackCommand('extensions')


def test_activate(
        mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extension1')
    activate('extension1')
    output = extensions('--show', 'activated', 'extendee')
    assert 'extension1' in output


def test_deactivate(
        mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extension1')
    activate('extension1')
    deactivate('extension1')
    output = extensions('--show', 'activated', 'extendee')
    assert 'extension1' not in output


def test_deactivate_all(
        mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extension1')
    install('extension2')
    activate('extension1')
    activate('extension2')
    deactivate('--all', 'extendee')
    output = extensions('--show', 'activated', 'extendee')
    assert 'extension1' not in output

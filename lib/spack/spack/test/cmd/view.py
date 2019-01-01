# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand
import os.path
import pytest

activate = SpackCommand('activate')
extensions = SpackCommand('extensions')
install = SpackCommand('install')
view = SpackCommand('view')


@pytest.mark.parametrize('cmd', ['hardlink', 'symlink', 'hard', 'add'])
def test_view_link_type(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery, cmd):
    install('libdwarf')
    viewpath = str(tmpdir.mkdir('view_{0}'.format(cmd)))
    view(cmd, viewpath, 'libdwarf')
    package_prefix = os.path.join(viewpath, 'libdwarf')
    assert os.path.exists(package_prefix)
    assert os.path.islink(package_prefix) == (not cmd.startswith('hard'))


def test_view_external(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('externaltool')
    viewpath = str(tmpdir.mkdir('view'))
    output = view('symlink', viewpath, 'externaltool')
    assert 'Skipping external package: externaltool' in output


def test_view_extension(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    assert 'extension1@2.0' in all_installed
    assert 'extension2@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    assert 'extension1@2.0' not in global_activated
    assert 'extension2@1.0' not in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' in view_activated
    assert 'extension1@2.0' not in view_activated
    assert 'extension2@1.0' not in view_activated
    assert os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))


def test_view_extension_remove(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    view('remove', viewpath, 'extension1@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' not in view_activated
    assert not os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))


def test_view_extension_conflict(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    output = view('symlink', viewpath, 'extension1@2.0')
    assert 'Package conflict detected' in output


def test_view_extension_conflict_ignored(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    view('symlink', viewpath, '-i', 'extension1@2.0')
    with open(os.path.join(viewpath, 'bin', 'extension1'), 'r') as fin:
        assert fin.read() == '1.0'


def test_view_extension_global_activation(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    view('symlink', viewpath, 'extension1@1.0')
    activate('extension1@2.0')
    activate('extension2@1.0')
    all_installed = extensions('--show', 'installed', 'extendee')
    assert 'extension1@1.0' in all_installed
    assert 'extension1@2.0' in all_installed
    assert 'extension2@1.0' in all_installed
    global_activated = extensions('--show', 'activated', 'extendee')
    assert 'extension1@1.0' not in global_activated
    assert 'extension1@2.0' in global_activated
    assert 'extension2@1.0' in global_activated
    view_activated = extensions('--show', 'activated',
                                '-v', viewpath,
                                'extendee')
    assert 'extension1@1.0' in view_activated
    assert 'extension1@2.0' not in view_activated
    assert 'extension2@1.0' not in view_activated
    assert os.path.exists(os.path.join(viewpath, 'bin', 'extension1'))
    assert not os.path.exists(os.path.join(viewpath, 'bin', 'extension2'))


def test_view_extendee_with_global_activations(
        tmpdir, mock_packages, mock_archive, mock_fetch, config,
        install_mockery):
    install('extendee')
    install('extension1@1.0')
    install('extension1@2.0')
    install('extension2@1.0')
    viewpath = str(tmpdir.mkdir('view'))
    activate('extension1@2.0')
    output = view('symlink', viewpath, 'extension1@1.0')
    assert 'Error: Globally activated extensions cannot be used' in output

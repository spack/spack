##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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

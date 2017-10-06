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
from spack.main import SpackCommand

activate = SpackCommand('activate')
extensions = SpackCommand('extensions')
install = SpackCommand('install')
view = SpackCommand('view')


def test_view_extension(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
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


def test_view_extension_global_activation(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
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

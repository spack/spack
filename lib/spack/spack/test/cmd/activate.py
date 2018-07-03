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

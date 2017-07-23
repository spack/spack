##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


install = SpackCommand('install')


def _install_package_and_dependency(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
        install_mockery):

    tmpdir.chdir()
    install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


def test_install_package_already_installed(
        tmpdir, builtin_mock, mock_archive, mock_fetch, config,
        install_mockery):

    tmpdir.chdir()
    install('libdwarf')
    install('--log-format=junit', '--log-file=test.xml', 'libdwarf')

    files = tmpdir.listdir()
    filename = tmpdir.join('test.xml')
    assert filename in files

    content = filename.open().read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content

    skipped = [line for line in content.split('\n') if 'skipped' in line]
    assert len(skipped) == 2

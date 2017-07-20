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
import os
import codecs
import collections
import contextlib
import pytest
from six import StringIO

import llnl.util.filesystem
import spack
import spack.cmd
from spack.main import SpackCommand


install = SpackCommand('install')


@pytest.mark.usefixutres('install_mockery', 'builtin_mock', 'config', 'builtin_mock')
def test_install_package_and_dependency(tmpdir):
    tmpdir.chdir()
    install('--log-format=junit', 'libdwarf')

    files = os.listdir()
    assert len(files) == 1
    assert files[0].endswith('xml')

    content = open(files[0]).read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content


@pytest.mark.usefixutres('install_mockery', 'builtin_mock', 'config', 'builtin_mock')
def _install_package_and_dependency(tmpdir):
    tmpdir.chdir()
    install('libelf')
    install('--log-format=junit', 'libdwarf')

    files = os.listdir()
    assert len(files) == 1
    assert files[0].endswith('xml')

    content = open(files[0]).read()
    assert 'tests="2"' in content
    assert 'failures="0"' in content
    assert 'errors="0"' in content

    skipped = [line for line in content.split('\n') if 'skipped' in line]
    assert len(skipped) == 2

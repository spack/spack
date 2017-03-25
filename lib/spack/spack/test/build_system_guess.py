##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import pytest
import spack.cmd.create
import spack.util.executable
import spack.stage


@pytest.fixture(
    scope='function',
    params=[
        ('configure',      'autotools'),
        ('CMakeLists.txt', 'cmake'),
        ('SConstruct',     'scons'),
        ('setup.py',       'python'),
        ('NAMESPACE',      'r'),
        ('WORKSPACE',      'bazel'),
        ('foobar',         'generic')
    ]
)
def url_and_build_system(request, tmpdir):
    """Sets up the resources to be pulled by the stage with
    the appropriate file name and returns their url along with
    the correct build-system guess
    """
    tar = spack.util.executable.which('tar')
    orig_dir = tmpdir.chdir()
    filename, system = request.param
    tmpdir.ensure('archive', filename)
    tar('czf', 'archive.tar.gz', 'archive')
    url = 'file://' + str(tmpdir.join('archive.tar.gz'))
    yield url, system
    orig_dir.chdir()


def test_build_systems(url_and_build_system):
    url, build_system = url_and_build_system
    with spack.stage.Stage(url) as stage:
        stage.fetch()
        guesser = spack.cmd.create.BuildSystemGuesser()
        guesser(stage, url)
        assert build_system == guesser.build_system

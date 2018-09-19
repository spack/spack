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
import glob
import os
import pytest

import spack.repo
from llnl.util.filesystem import working_dir
from spack.build_environment import get_std_cmake_args, setup_package
from spack.spec import Spec
from spack.util.executable import which


DATA_PATH = os.path.join(spack.paths.test_path, 'data')


@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'make', 'affirmative', '*'))
)
def test_affirmative_make_check(directory, config, mock_packages):
    """Tests that Spack correctly detects targets in a Makefile."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with working_dir(directory):
        assert pkg._has_make_target('check')

        pkg._if_make_target_execute('check')


@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'make', 'negative', '*'))
)
@pytest.mark.regression('9067')
def test_negative_make_check(directory, config, mock_packages):
    """Tests that Spack correctly ignores false positives in a Makefile."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with working_dir(directory):
        assert not pkg._has_make_target('check')

        pkg._if_make_target_execute('check')


@pytest.mark.skipif(not which('ninja'), reason='ninja is not installed')
@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'ninja', 'affirmative', '*'))
)
def test_affirmative_ninja_check(directory, config, mock_packages):
    """Tests that Spack correctly detects targets in a Ninja build script."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with working_dir(directory):
        assert pkg._has_ninja_target('check')

        pkg._if_ninja_target_execute('check')

        # Clean up Ninja files
        for filename in glob.iglob('.ninja_*'):
            os.remove(filename)


@pytest.mark.skipif(not which('ninja'), reason='ninja is not installed')
@pytest.mark.parametrize(
    'directory',
    glob.iglob(os.path.join(DATA_PATH, 'ninja', 'negative', '*'))
)
def test_negative_ninja_check(directory, config, mock_packages):
    """Tests that Spack correctly ignores false positives in a Ninja
    build script."""

    # Get a fake package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    setup_package(pkg, False)

    with working_dir(directory):
        assert not pkg._has_ninja_target('check')

        pkg._if_ninja_target_execute('check')


def test_cmake_std_args(config, mock_packages):
    # Call the function on a CMakePackage instance
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    assert pkg.std_cmake_args == get_std_cmake_args(pkg)

    # Call it on another kind of package
    s = Spec('mpich')
    s.concretize()
    pkg = spack.repo.get(s)
    assert get_std_cmake_args(pkg)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestAutotoolsPackage(object):

    def test_with_or_without(self):
        s = Spec('a')
        s.concretize()
        pkg = spack.repo.get(s)

        # Called without parameters
        options = pkg.with_or_without('foo')
        assert '--with-bar' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        def activate(value):
            return 'something'

        options = pkg.with_or_without('foo', activation_value=activate)
        assert '--with-bar=something' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        options = pkg.enable_or_disable('foo')
        assert '--enable-bar' in options
        assert '--disable-baz' in options
        assert '--disable-fee' in options

        options = pkg.with_or_without('bvv')
        assert '--with-bvv' in options

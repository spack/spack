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
import os

import pytest
from spack import spack_root
from spack.environment import EnvironmentModifications
from spack.environment import RemovePath, PrependPath, AppendPath
from spack.environment import SetEnv, UnsetEnv
from spack.util.environment import filter_system_paths, filter_system_bin_paths


@pytest.fixture()
def prepare_environment_for_tests():
    """Sets a few dummy variables in the current environment, that will be
    useful for the tests below.
    """
    os.environ['UNSET_ME'] = 'foo'
    os.environ['EMPTY_PATH_LIST'] = ''
    os.environ['PATH_LIST'] = '/path/second:/path/third'
    os.environ['REMOVE_PATH_LIST'] = '/a/b:/duplicate:/a/c:/remove/this:/a/d:/duplicate/:/f/g'  # NOQA: ignore=E501
    yield
    for x in ('UNSET_ME', 'EMPTY_PATH_LIST', 'PATH_LIST', 'REMOVE_PATH_LIST'):
        if x in os.environ:
            del os.environ[x]


@pytest.fixture
def env(prepare_environment_for_tests):
    """Returns an empty EnvironmentModifications object."""
    return EnvironmentModifications()


@pytest.fixture
def miscellaneous_paths():
    """Returns a list of paths, including system ones."""
    return [
        '/usr/local/Cellar/gcc/5.3.0/lib',
        '/usr/local/lib',
        '/usr/local',
        '/usr/local/include',
        '/usr/local/lib64',
        '/usr/local/opt/some-package/lib',
        '/usr/opt/lib',
        '/lib',
        '/',
        '/usr',
        '/lib64',
        '/include',
        '/opt/some-package/include',
    ]


@pytest.fixture
def bin_paths():
    """Returns a list of bin paths, including system ones."""
    return [
        '/usr/local/Cellar/gcc/5.3.0/bin',
        '/usr/local/bin',
        '/usr/local/opt/some-package/bin',
        '/usr/opt/bin',
        '/bin',
        '/opt/some-package/bin',
    ]


@pytest.fixture
def files_to_be_sourced():
    """Returns a list of files to be sourced"""
    datadir = os.path.join(
        spack_root, 'lib', 'spack', 'spack', 'test', 'data'
    )

    files = [
        os.path.join(datadir, 'sourceme_first.sh'),
        os.path.join(datadir, 'sourceme_second.sh'),
        os.path.join(datadir, 'sourceme_parameters.sh intel64'),
        os.path.join(datadir, 'sourceme_unicode.sh')
    ]

    return files


def test_set(env):
    """Tests setting values in the environment."""

    # Here we are storing the commands to set a couple of variables
    env.set('A', 'dummy value')
    env.set('B', 3)

    # ...and then we are executing them
    env.apply_modifications()

    assert 'dummy value' == os.environ['A']
    assert str(3) == os.environ['B']


def test_unset(env):
    """Tests unsetting values in the environment."""

    # Assert that the target variable is there and unset it
    assert 'foo' == os.environ['UNSET_ME']
    env.unset('UNSET_ME')
    env.apply_modifications()

    # Trying to retrieve is after deletion should cause a KeyError
    with pytest.raises(KeyError):
        os.environ['UNSET_ME']


def test_filter_system_paths(miscellaneous_paths):
    """Tests that the filtering of system paths works as expected."""
    filtered = filter_system_paths(miscellaneous_paths)
    expected = [
        '/usr/local/Cellar/gcc/5.3.0/lib',
        '/usr/local/opt/some-package/lib',
        '/usr/opt/lib',
        '/opt/some-package/include'
    ]
    assert filtered == expected


def test_filter_system_bin_paths(bin_paths):
    """Tests that the filtering of system bin paths works as expected."""
    filtered = filter_system_bin_paths(bin_paths)
    expected = [
        '/usr/local/bin',
        '/bin',
        '/usr/local/Cellar/gcc/5.3.0/bin',
        '/usr/local/opt/some-package/bin',
        '/usr/opt/bin',
        '/opt/some-package/bin'
    ]
    assert filtered == expected


def test_set_path(env):
    """Tests setting paths in an environment variable."""

    # Check setting paths with the default separator
    env.set_path('A', ['foo', 'bar', 'baz'])
    env.apply_modifications()

    assert 'foo:bar:baz' == os.environ['A']

    env.set_path('B', ['foo', 'bar', 'baz'], separator=';')
    env.apply_modifications()

    assert 'foo;bar;baz' == os.environ['B']


def test_path_manipulation(env):
    """Tests manipulating list of paths in the environment."""

    env.append_path('PATH_LIST', '/path/last')
    env.prepend_path('PATH_LIST', '/path/first')

    env.append_path('EMPTY_PATH_LIST', '/path/middle')
    env.append_path('EMPTY_PATH_LIST', '/path/last')
    env.prepend_path('EMPTY_PATH_LIST', '/path/first')

    env.append_path('NEWLY_CREATED_PATH_LIST', '/path/middle')
    env.append_path('NEWLY_CREATED_PATH_LIST', '/path/last')
    env.prepend_path('NEWLY_CREATED_PATH_LIST', '/path/first')

    env.remove_path('REMOVE_PATH_LIST', '/remove/this')
    env.remove_path('REMOVE_PATH_LIST', '/duplicate/')

    env.apply_modifications()

    expected = '/path/first:/path/second:/path/third:/path/last'
    assert os.environ['PATH_LIST'] == expected

    expected = '/path/first:/path/middle:/path/last'
    assert os.environ['EMPTY_PATH_LIST'] == expected

    expected = '/path/first:/path/middle:/path/last'
    assert os.environ['NEWLY_CREATED_PATH_LIST'] == expected

    assert os.environ['REMOVE_PATH_LIST'] == '/a/b:/a/c:/a/d:/f/g'


def test_extra_arguments(env):
    """Tests that we can attach extra arguments to any command."""
    env.set('A', 'dummy value', who='Pkg1')
    for x in env:
        assert 'who' in x.args

    env.apply_modifications()
    assert 'dummy value' == os.environ['A']


def test_extend(env):
    """Tests that we can construct a list of environment modifications
    starting from another list.
    """
    env.set('A', 'dummy value')
    env.set('B', 3)
    copy_construct = EnvironmentModifications(env)

    assert len(copy_construct) == 2

    for x, y in zip(env, copy_construct):
        assert x is y


@pytest.mark.usefixtures('prepare_environment_for_tests')
def test_source_files(files_to_be_sourced):
    """Tests the construction of a list of environment modifications that are
    the result of sourcing a file.
    """
    env = EnvironmentModifications.from_sourcing_files(*files_to_be_sourced)
    modifications = env.group_by_name()

    # This is sensitive to the user's environment; can include
    # spurious entries for things like PS1
    #
    # TODO: figure out how to make a bit more robust.
    assert len(modifications) >= 5

    # Set new variables
    assert len(modifications['NEW_VAR']) == 1
    assert isinstance(modifications['NEW_VAR'][0], SetEnv)
    assert modifications['NEW_VAR'][0].value == 'new'

    assert len(modifications['FOO']) == 1
    assert isinstance(modifications['FOO'][0], SetEnv)
    assert modifications['FOO'][0].value == 'intel64'

    # Unset variables
    assert len(modifications['EMPTY_PATH_LIST']) == 1
    assert isinstance(modifications['EMPTY_PATH_LIST'][0], UnsetEnv)

    # Modified variables
    assert len(modifications['UNSET_ME']) == 1
    assert isinstance(modifications['UNSET_ME'][0], SetEnv)
    assert modifications['UNSET_ME'][0].value == 'overridden'

    assert len(modifications['PATH_LIST']) == 3
    assert isinstance(modifications['PATH_LIST'][0], RemovePath)
    assert modifications['PATH_LIST'][0].value == '/path/third'
    assert isinstance(modifications['PATH_LIST'][1], AppendPath)
    assert modifications['PATH_LIST'][1].value == '/path/fourth'
    assert isinstance(modifications['PATH_LIST'][2], PrependPath)
    assert modifications['PATH_LIST'][2].value == '/path/first'

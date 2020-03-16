# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
def test_affirmative_make_check(directory, config, mock_packages, working_env):
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
def test_negative_make_check(directory, config, mock_packages, working_env):
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
def test_affirmative_ninja_check(
        directory, config, mock_packages, working_env):
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
def test_negative_ninja_check(directory, config, mock_packages, working_env):
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


def test_cmake_bad_generator(config, mock_packages):
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.generator = 'Yellow Sticky Notes'
    with pytest.raises(spack.package.InstallError):
        get_std_cmake_args(pkg)


def test_cmake_secondary_generator(config, mock_packages):
    s = Spec('cmake-client')
    s.concretize()
    pkg = spack.repo.get(s)
    pkg.generator = 'CodeBlocks - Unix Makefiles'
    assert get_std_cmake_args(pkg)


@pytest.mark.usefixtures('config', 'mock_packages')
class TestAutotoolsPackage(object):

    def test_with_or_without(self):
        s = Spec('a')
        s.concretize()
        pkg = spack.repo.get(s)

        options = pkg.with_or_without('foo')

        # Ensure that values that are not representing a feature
        # are not used by with_or_without
        assert '--without-none' not in options
        assert '--with-bar' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        def activate(value):
            return 'something'

        options = pkg.with_or_without('foo', activation_value=activate)
        assert '--without-none' not in options
        assert '--with-bar=something' in options
        assert '--without-baz' in options
        assert '--no-fee' in options

        options = pkg.enable_or_disable('foo')
        assert '--disable-none' not in options
        assert '--enable-bar' in options
        assert '--disable-baz' in options
        assert '--disable-fee' in options

        options = pkg.with_or_without('bvv')
        assert '--with-bvv' in options

    def test_none_is_allowed(self):
        s = Spec('a foo=none')
        s.concretize()
        pkg = spack.repo.get(s)

        options = pkg.with_or_without('foo')

        # Ensure that values that are not representing a feature
        # are not used by with_or_without
        assert '--with-none' not in options
        assert '--without-bar' in options
        assert '--without-baz' in options
        assert '--no-fee' in options


@pytest.mark.usefixtures('config', 'mock_packages')
class TestCMakePackage(object):

    def test_define(self):
        s = Spec('cmake-client')
        s.concretize()
        pkg = spack.repo.get(s)

        for cls in (list, tuple):
            arg = pkg.define('MULTI', cls(['right', 'up']))
            assert arg == '-DMULTI:STRING=right;up'

        arg = pkg.define('ENABLE_TRUTH', False)
        assert arg == '-DENABLE_TRUTH:BOOL=OFF'
        arg = pkg.define('ENABLE_TRUTH', True)
        assert arg == '-DENABLE_TRUTH:BOOL=ON'

        arg = pkg.define('SINGLE', 'red')
        assert arg == '-DSINGLE:STRING=red'

    def test_define_from_variant(self):
        s = Spec('cmake-client multi=up,right ~truthy single=red')
        s.concretize()
        pkg = spack.repo.get(s)

        arg = pkg.define_from_variant('MULTI')
        assert arg == '-DMULTI:STRING=right;up'

        arg = pkg.define_from_variant('ENABLE_TRUTH', 'truthy')
        assert arg == '-DENABLE_TRUTH:BOOL=OFF'

        arg = pkg.define_from_variant('SINGLE')
        assert arg == '-DSINGLE:STRING=red'

        with pytest.raises(KeyError, match="not a variant"):
            pkg.define_from_variant('NONEXISTENT')

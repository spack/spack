# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pytest
from spack.main import SpackCommand, SpackCommandError
import spack.spec
import spack.user_environment as uenv

load = SpackCommand('load')
unload = SpackCommand('unload')
install = SpackCommand('install')
location = SpackCommand('location')


def test_load(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test that the commands generated by load add the specified prefix
    inspections. Also test that Spack records loaded specs by hash in the
    user environment.

    CMAKE_PREFIX_PATH is the only prefix inspection guaranteed for fake
    packages, since it keys on the prefix instead of a subdir."""
    install('mpileaks')
    mpileaks_spec = spack.spec.Spec('mpileaks').concretized()

    sh_out = load('--sh', '--only', 'package', 'mpileaks')
    csh_out = load('--csh', '--only', 'package', 'mpileaks')

    # Test prefix inspections
    sh_out_test = 'export CMAKE_PREFIX_PATH=%s' % mpileaks_spec.prefix
    csh_out_test = 'setenv CMAKE_PREFIX_PATH %s' % mpileaks_spec.prefix
    assert sh_out_test in sh_out
    assert csh_out_test in csh_out

    # Test hashes recorded properly
    hash_test_replacements = (uenv.spack_loaded_hashes_var,
                              mpileaks_spec.dag_hash())
    sh_hash_test = 'export %s=%s' % hash_test_replacements
    csh_hash_test = 'setenv %s %s' % hash_test_replacements
    assert sh_hash_test in sh_out
    assert csh_hash_test in csh_out


def test_load_recursive(install_mockery, mock_fetch, mock_archive,
                        mock_packages):
    """Test that the '-r' option to the load command prepends dependency prefix
    inspections in post-order"""
    install('mpileaks')
    mpileaks_spec = spack.spec.Spec('mpileaks').concretized()

    sh_out = load('--sh', 'mpileaks')
    csh_out = load('--csh', 'mpileaks')

    # Test prefix inspections
    prefix_test_replacement = ':'.join(reversed(
        [s.prefix for s in mpileaks_spec.traverse(order='post')]))

    sh_prefix_test = 'export CMAKE_PREFIX_PATH=%s' % prefix_test_replacement
    csh_prefix_test = 'setenv CMAKE_PREFIX_PATH %s' % prefix_test_replacement
    assert sh_prefix_test in sh_out
    assert csh_prefix_test in csh_out

    # Test spack records loaded hashes properly
    hash_test_replacement = (uenv.spack_loaded_hashes_var, ':'.join(reversed(
        [s.dag_hash() for s in mpileaks_spec.traverse(order='post')])))
    sh_hash_test = 'export %s=%s' % hash_test_replacement
    csh_hash_test = 'setenv %s %s' % hash_test_replacement
    assert sh_hash_test in sh_out
    assert csh_hash_test in csh_out


def test_load_includes_run_env(install_mockery, mock_fetch, mock_archive,
                               mock_packages):
    """Tests that environment changes from the package's
    `setup_run_environment` method are added to the user environment in
    addition to the prefix inspections"""
    install('mpileaks')

    sh_out = load('--sh', 'mpileaks')
    csh_out = load('--csh', 'mpileaks')

    assert 'export FOOBAR=mpileaks' in sh_out
    assert 'setenv FOOBAR mpileaks' in csh_out


def test_load_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install('libelf@0.8.12')
    install('libelf@0.8.13')
    # Now there are two versions of libelf
    with pytest.raises(SpackCommandError):
        # This should cause an error due to multiple versions
        load('--sh', 'libelf')
    # Using --first should avoid the error condition
    load('--sh', '--first', 'libelf')


def test_load_fails_no_shell(install_mockery, mock_fetch, mock_archive,
                             mock_packages):
    """Test that spack load prints an error message without a shell."""
    install('mpileaks')

    out = load('mpileaks', fail_on_error=False)
    assert "To set up shell support" in out


def test_unload(install_mockery, mock_fetch, mock_archive, mock_packages,
                working_env):
    """Tests that any variables set in the user environment are undone by the
    unload command"""
    install('mpileaks')
    mpileaks_spec = spack.spec.Spec('mpileaks').concretized()

    # Set so unload has something to do
    os.environ['FOOBAR'] = 'mpileaks'
    os.environ[uenv.spack_loaded_hashes_var] = '%s:%s' % (
        mpileaks_spec.dag_hash(), 'garbage')

    sh_out = unload('--sh', 'mpileaks')
    csh_out = unload('--csh', 'mpileaks')

    assert 'unset FOOBAR' in sh_out
    assert 'unsetenv FOOBAR' in csh_out

    assert 'export %s=garbage' % uenv.spack_loaded_hashes_var in sh_out
    assert 'setenv %s garbage' % uenv.spack_loaded_hashes_var in csh_out


def test_unload_fails_no_shell(install_mockery, mock_fetch, mock_archive,
                               mock_packages, working_env):
    """Test that spack unload prints an error message without a shell."""
    install('mpileaks')
    mpileaks_spec = spack.spec.Spec('mpileaks').concretized()
    os.environ[uenv.spack_loaded_hashes_var] = mpileaks_spec.dag_hash()

    out = unload('mpileaks', fail_on_error=False)
    assert "To set up shell support" in out

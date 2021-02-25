# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import platform
import os
import re

import pytest

from llnl.util.lang import key_ordering

import spack.config
import spack.compilers
import spack.installer
import spack.main
import spack.binary_distribution
import spack.environment as ev
import spack.spec
import spack.spec_index
from spack.spec_index import (ConcretizedSpec, ConcreteHash, GenericHashedPackageRecord,
                              IndexEntry, IndexLocation)
from spack.spec import Spec

add = spack.main.SpackCommand('add')
buildcache = spack.main.SpackCommand('buildcache')
compiler = spack.main.SpackCommand('compiler')
env = spack.main.SpackCommand('env')
find = spack.main.SpackCommand('find')
gpg = spack.main.SpackCommand('gpg')
install = spack.main.SpackCommand('install')
mirror = spack.main.SpackCommand('mirror')
solve = spack.main.SpackCommand('solve')
spec = spack.main.SpackCommand('spec')
uninstall = spack.main.SpackCommand('uninstall')


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    specs = database.query_local()
    monkeypatch.setattr(
        spack.binary_distribution, 'update_cache_and_get_specs', lambda: specs
    )


@pytest.fixture()
def mock_get_specs_multiarch(database, monkeypatch):
    specs = [spec.copy() for spec in database.query_local()]

    # make one spec that is NOT the test architecture
    for spec in specs:
        if spec.name == "mpileaks":
            spec.architecture = spack.spec.ArchSpec('linux-rhel7-x86_64')
            break

    monkeypatch.setattr(
        spack.binary_distribution, 'update_cache_and_get_specs', lambda: specs
    )


def parse_long_hash(package_instance):
    match = re.match(r'^([^ ]+) [^ ]*$', package_instance)
    assert match is not None
    return ConcreteHash(match.group(1))


def _find_output(with_missing=True):
    missing_args = ('-m',) if with_missing else ()
    all_args = ('--no-groups',) + missing_args + ('--allarch', '-L',)
    return find(*all_args).splitlines()


def all_found_hashes(with_missing=True):
    return frozenset(
        parse_long_hash(line)
        for line in _find_output(with_missing=with_missing))


def _buildcache_list_output(*specs):
    return buildcache('list', '--allarch', '-L', *specs).splitlines()[1:]


def buildcache_hashes(*specs):
    return frozenset(
        parse_long_hash(line) for line in _buildcache_list_output(*specs)
    )


@pytest.mark.skipif(
    platform.system().lower() != 'linux',
    reason='implementation for MacOS still missing'
)
@pytest.mark.db
def test_buildcache_preview_just_runs(database):
    buildcache('preview', 'mpileaks')


@pytest.mark.db
@pytest.mark.regression('13757')
def test_buildcache_list_duplicates(mock_get_specs, capsys):
    with capsys.disabled():
        output = buildcache('list', 'mpileaks', '@2.3')

    assert output.count('mpileaks') == 3


@pytest.fixture(scope='function')
def corge_buildcache(test_mirror, patch_spec_indices, cache_directory, install_mockery,
                     mock_pkg_install):
    cspec = ConcretizedSpec.from_abstract_spec(Spec('corge'))

    patch_spec_indices.location = None

    # Install 'corge' without using a cache
    install('--no-cache', cspec.spec.name)
    # raise Exception(install('--no-cache', cspec.spec.name, fail_on_error=False))
    all_hashes = all_found_hashes()
    assert cspec.into_hash() in all_hashes

    # Matches the concretized 'corge' spec by hash.
    spec_str = cspec.spec_string_name_hash_only

    # Create a buildcache
    mirror_dir = test_mirror
    buildcache('create', '-au', '--rebuild-index', '-d', mirror_dir, spec_str)

    for h in all_hashes:
        entry = spack.spec_index.local_spec_index.lookup_ensuring_single_match(h)
        patch_spec_indices.intern_concretized_spec(entry.concretized_spec, entry.record)

    # Uninstall the package and deps
    uninstall('-a', '-y', '--dependents')
    # assert set() == all_found_hashes(with_missing=False)

    return patch_spec_indices, cspec, all_hashes


@pytest.fixture(scope='function')
def pin_some_dependency_hash(corge_buildcache):
    _, cspec, all_hashes = corge_buildcache

    # Assert that we can pin a *dependency* spec with a hash.
    some_dependency_hash = next(
        h.complete_hash
        for h in all_hashes
        if h != cspec.into_hash()
    )
    merged_spec_str = '{0} ^ /{1}'.format(cspec.spec.name, some_dependency_hash)
    return corge_buildcache + (merged_spec_str,)


@key_ordering
class SpecType(object):
    _known_types = ['TOP_LEVEL_HASH', 'PINNED_DEPENDENCY_HASH']

    def __init__(self, typ):
        assert typ in self._known_types, (typ, self._known_types)
        self.typ = typ

    def _cmp_key(self):
        return (type(self), self.typ)

    @classmethod
    def TOP_LEVEL_HASH(cls):
        return cls('TOP_LEVEL_HASH')

    @classmethod
    def PINNED_DEPENDENCY_HASH(cls):
        return cls('PINNED_DEPENDENCY_HASH')

    @classmethod
    def all_values(cls):
        return [cls(typ) for typ in cls._known_types]

    def __repr__(self):
        return '{0}(typ={1!r})'.format(type(self).__name__, self.typ)


@pytest.fixture(scope='function')
def select_spec_string(pin_some_dependency_hash):
    patch_spec_indices, cspec, all_hashes, merged_spec_str = pin_some_dependency_hash

    def select(arg):
        if arg == SpecType.TOP_LEVEL_HASH():
            return cspec.spec_string_name_hash_only
        return merged_spec_str
    return (patch_spec_indices, cspec, all_hashes, select,)


@pytest.mark.parametrize('spec_type', SpecType.all_values())
@pytest.mark.regression('reference listed binaries by hash')
def test_buildcache_spec_reference_by_hash(spec_type, select_spec_string):
    patch_spec_indices, _, _, select = select_spec_string
    patch_spec_indices.location = spack.spec_index.IndexLocation.REMOTE()
    spec_str = select(spec_type)
    # Would fail if the hashes weren't in the merged db:
    spec(spec_str)


@pytest.mark.maybeslow
@pytest.mark.parametrize('spec_type', SpecType.all_values())
def test_buildcache_solve_reference_by_hash(spec_type, select_spec_string):
    patch_spec_indices, _, _, select = select_spec_string
    patch_spec_indices.location = spack.spec_index.IndexLocation.REMOTE()
    spec_str = select(spec_type)
    # Would fail if the hashes weren't in the merged db:
    solve(spec_str)


@key_ordering
class InstallMethod(object):
    _known_methods = ['INSTALL_CACHE_ONLY', 'BUILDCACHE_INSTALL']

    def __init__(self, method):
        assert method in self._known_methods, (method, self._known_methods)
        self.method = method

    def _cmp_key(self):
        return (type(self), self.method)

    @classmethod
    def INSTALL_CACHE_ONLY(cls):
        return cls('INSTALL_CACHE_ONLY')

    @classmethod
    def BUILDCACHE_INSTALL(cls):
        return cls('BUILDCACHE_INSTALL')

    @classmethod
    def all_values(cls):
        return [cls(meth) for meth in cls._known_methods]

    def __repr__(self):
        return '{0}(method={1!r})'.format(type(self).__name__, self.method)

    def perform_command(self, spec_str):
        if self == type(self).BUILDCACHE_INSTALL():
            return buildcache('install', '-u', spec_str)
        return install('--cache-only', '--verbose', '--no-check-signature', spec_str)


# NB: The InstallMethod.INSTALL_CACHE_ONLY() must go first for this test to pass. It's
# not clear why yet, but likely has to do with some shared state in the pytest fixtures
# used.
@pytest.mark.parametrize('spec_type', SpecType.all_values())
@pytest.mark.parametrize('install_method', InstallMethod.all_values())
def test_buildcache_install_reference_by_hash(
        spec_type,
        install_method,
        select_spec_string,
):
    patch_spec_indices, _, all_hashes, select = select_spec_string
    patch_spec_indices.location = spack.spec_index.IndexLocation.REMOTE()

    spec_str = select(spec_type)

    # Installed again, referencing a hash known only to the remote spec index:
    install_method.perform_command(spec_str)

    patch_spec_indices.location = None
    assert all_hashes == buildcache_hashes()


@pytest.mark.parametrize('spec_type', SpecType.all_values())
def test_buildcache_list_reference_by_hash(
        spec_type,
        select_spec_string,
):
    patch_spec_indices, cspec, all_hashes, select = select_spec_string
    patch_spec_indices.location = spack.spec_index.IndexLocation.REMOTE()
    spec_str = select(spec_type)
    # Assert that the buildcache hashes do not depend on the installed packages!
    assert all_hashes == buildcache_hashes()
    # If we request a single spec by hash, we should get just that spec.
    assert set([cspec.into_hash()]) == buildcache_hashes(spec_str)


@pytest.mark.db
@pytest.mark.regression('17827')
def test_buildcache_list_allarch(database, mock_get_specs_multiarch, capsys):
    with capsys.disabled():
        output = buildcache('list', '--allarch')

    assert output.count('mpileaks') == 3

    with capsys.disabled():
        output = buildcache('list')

    assert output.count('mpileaks') == 2


def test_buildcache_create(
        install_mockery, mock_fetch, monkeypatch, tmpdir):
    """"Ensure that buildcache create creates output files"""
    pkg = 'trivial-install-test-package'
    install(pkg)

    buildcache('create', '-d', str(tmpdir), '--unsigned', pkg)

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, '.spack')
    tarball = spack.binary_distribution.tarball_name(spec, '.spec.yaml')
    assert os.path.exists(
        os.path.join(str(tmpdir), 'build_cache', tarball_path))
    assert os.path.exists(
        os.path.join(str(tmpdir), 'build_cache', tarball))


def test_buildcache_create_env(
        install_mockery, mock_fetch, monkeypatch,
        tmpdir, mutable_mock_env_path):
    """"Ensure that buildcache create creates output files from env"""
    pkg = 'trivial-install-test-package'

    env('create', 'test')
    with ev.read('test'):
        add(pkg)
        install()

        buildcache('create', '-d', str(tmpdir), '--unsigned')

    spec = Spec(pkg).concretized()
    tarball_path = spack.binary_distribution.tarball_path_name(spec, '.spack')
    tarball = spack.binary_distribution.tarball_name(spec, '.spec.yaml')
    assert os.path.exists(
        os.path.join(str(tmpdir), 'build_cache', tarball_path))
    assert os.path.exists(
        os.path.join(str(tmpdir), 'build_cache', tarball))


def test_buildcache_create_fails_on_noargs(tmpdir):
    """Ensure that buildcache create fails when given no args or
    environment."""
    with pytest.raises(spack.main.SpackCommandError):
        buildcache('create', '-d', str(tmpdir), '--unsigned')


@pytest.mark.skipif(
    os.environ.get('SPACK_TEST_SOLVER') == 'clingo',
    reason='Test for Clingo are run in a container with root permissions'
)
def test_buildcache_create_fail_on_perm_denied(
        install_mockery, mock_fetch, monkeypatch, own_tmpdir):
    """Ensure that buildcache create fails on permission denied error."""
    install('trivial-install-test-package')

    own_tmpdir.chmod(0)
    with pytest.raises(OSError) as error:
        buildcache('create', '-d', str(own_tmpdir),
                   '--unsigned', 'trivial-install-test-package')
    assert error.value.errno == errno.EACCES
    own_tmpdir.chmod(0o700)


@pytest.mark.skipif(not spack.util.gpg.has_gpg(),
                    reason='This test requires gpg')
def test_update_key_index(tmpdir, mutable_mock_env_path,
                          install_mockery, mock_packages, mock_fetch,
                          mock_stage, mock_gnupghome):
    """Test the update-index command with the --keys option"""
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    mirror('add', 'test-mirror', mirror_url)

    gpg('create', 'Test Signing Key', 'nobody@nowhere.com')

    s = Spec('libdwarf').concretized()

    # Install a package
    install(s.name)

    # Put installed package in the buildcache, which, because we're signing
    # it, should result in the public key getting pushed to the buildcache
    # as well.
    buildcache('create', '-a', '-d', mirror_dir.strpath, s.name)

    # Now make sure that when we pass the "--keys" argument to update-index
    # it causes the index to get update.
    buildcache('update-index', '--keys', '-d', mirror_dir.strpath)

    key_dir_list = os.listdir(os.path.join(
        mirror_dir.strpath, 'build_cache', '_pgp'))

    uninstall('-y', s.name)
    mirror('rm', 'test-mirror')

    assert 'index.json' in key_dir_list

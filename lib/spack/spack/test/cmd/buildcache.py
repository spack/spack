# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import errno
import platform
import os
import re
from typing import FrozenSet  # novm

import pytest

import spack.config
import spack.compilers
import spack.installer
import spack.main
import spack.binary_distribution
import spack.environment as ev
import spack.repo
import spack.spec
import spack.spec_index
import spack.store
from spack.spec_index import ConcretizedSpec, ConcreteHash, SpecIndex
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


def _parse_long_hash(package_instance):
    match = re.match(r'^([^ ]+) [^ ]*$', package_instance)
    assert match is not None
    return ConcreteHash(match.group(1))


def _find_output(with_missing=True):
    missing_args = ('-m',) if with_missing else ()
    all_args = ('--no-groups',) + missing_args + ('--allarch', '-L',)
    return find(*all_args).splitlines()


def all_found_hashes(with_missing=True):
    # type: (bool) -> FrozenSet[ConcreteHash]
    return frozenset(
        _parse_long_hash(line)
        for line in _find_output(with_missing=with_missing))


def _buildcache_list_output(*specs):
    return buildcache('list', '--allarch', '-L', *specs).splitlines()[1:]


def buildcache_hashes(*specs):
    # type: (Spec) -> FrozenSet[ConcreteHash]
    return frozenset(
        _parse_long_hash(line) for line in _buildcache_list_output(*specs)
    )


@pytest.fixture()
def mock_get_specs(database, monkeypatch):
    spec_index = SpecIndex([database])
    monkeypatch.setattr(
        spack.spec_index.IndexLocation, 'spec_index_for', lambda self: spec_index
    )


@pytest.fixture()
def mock_get_specs_multiarch(database, monkeypatch):
    spec_index = SpecIndex([database])

    # make one spec that is NOT the test architecture
    for spec in database.query_local():
        if spec.name == "mpileaks":
            spec.architecture = spack.spec.ArchSpec('linux-rhel7-x86_64')
            break

    monkeypatch.setattr(
        spack.spec_index.IndexLocation, 'spec_index_for', lambda self: spec_index
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
def corge_buildcache(default_config, mutable_buildcache):
    db, mirror_dir_path, prepare_spec, spec_index_query, _ = mutable_buildcache

    cspec = Spec('corge').concretized()
    prepare_spec(cspec)

    spack.binary_distribution.build_tarball(cspec, str(mirror_dir_path),
                                            regenerate_index=True)

    cspec = ConcretizedSpec(cspec)
    deps = [
        ConcretizedSpec(spec)
        for spec in cspec.spec.traverse()
        if spec.dag_hash() != cspec.spec.dag_hash()
    ]
    all_hashes = frozenset(spec.into_hash() for spec in [cspec] + deps)

    yield cspec, deps, all_hashes, db


@pytest.fixture(scope='function')
def pin_some_dependency_hash(corge_buildcache):
    cspec, deps, _all_hashes, _db = corge_buildcache

    # Assert that we can pin a *dependency* spec with a hash.
    some_dependency_hash = next(iter(deps)).into_hash().complete_hash
    merged_spec_str = '{0} ^ /{1}'.format(cspec.spec.name, some_dependency_hash)
    return merged_spec_str


@pytest.fixture(scope='function')
def select_spec_string(corge_buildcache, pin_some_dependency_hash):
    cspec, deps, all_hashes, _db = corge_buildcache
    merged_spec_str = pin_some_dependency_hash

    def select(arg):
        if arg == 'TOP_LEVEL_HASH':
            return cspec.spec_string_name_hash_only
        return merged_spec_str
    return (cspec, all_hashes, select,)


@pytest.mark.parametrize('spec_type', ['TOP_LEVEL_HASH', 'PINNED_DEPENDENCY_HASH'])
@pytest.mark.regression('reference listed binaries by hash')
def test_buildcache_spec_reference_by_hash(spec_type, select_spec_string):
    _, _, select = select_spec_string
    spec_str = select(spec_type)
    # Would fail if the hashes weren't in the merged db:
    spec(spec_str)


@pytest.mark.maybeslow
@pytest.mark.parametrize('spec_type', ['TOP_LEVEL_HASH', 'PINNED_DEPENDENCY_HASH'])
def test_buildcache_solve_reference_by_hash(spec_type, select_spec_string):
    _, _, select = select_spec_string
    spec_str = select(spec_type)
    # Would fail if the hashes weren't in the merged db:
    solve(spec_str)


# NB: 'INSTALL_CACHE_ONLY' must go first for this test to pass. It's not clear why yet,
# but likely has to do with some shared state in the pytest fixtures used.
@pytest.mark.parametrize('spec_type', ['TOP_LEVEL_HASH', 'PINNED_DEPENDENCY_HASH'])
@pytest.mark.parametrize('install_method', ['INSTALL_CACHE_ONLY', 'BUILDCACHE_INSTALL'])
def test_buildcache_install_reference_by_hash(
        spec_type,
        install_method,
        select_spec_string,
        mutable_buildcache,
):
    _, all_hashes, select = select_spec_string
    db, _, _, spec_index_query, _ = mutable_buildcache

    spec_str = select(spec_type)

    spec_index_query.use_local = False
    assert all_hashes == buildcache_hashes()

    # Installed again, referencing a hash known only to the remote spec index:
    if install_method == 'BUILDCACHE_INSTALL':
        buildcache('install', '-uf', spec_str)
    else:
        install('--cache-only', '--overwrite', '-y', '--verbose',
                '--no-check-signature',
                spec_str)


@pytest.mark.parametrize('spec_type', ['TOP_LEVEL_HASH', 'PINNED_DEPENDENCY_HASH'])
def test_buildcache_list_reference_by_hash(spec_type, select_spec_string):
    cspec, all_hashes, select = select_spec_string
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

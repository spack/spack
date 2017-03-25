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
import collections
import copy
import os
import re
import shutil

import cStringIO
import llnl.util.filesystem
import llnl.util.lang
import ordereddict_backport
import py
import pytest
import spack
import spack.architecture
import spack.database
import spack.directory_layout
import spack.fetch_strategy
import spack.platforms.test
import spack.repository
import spack.stage
import spack.util.executable
import spack.util.pattern


##########
# Monkey-patching that is applied to all tests
##########


@pytest.fixture(autouse=True)
def no_stdin_duplication(monkeypatch):
    """Duplicating stdin (or any other stream) returns an empty
    cStringIO object.
    """
    monkeypatch.setattr(
        llnl.util.lang,
        'duplicate_stream',
        lambda x: cStringIO.StringIO()
    )


@pytest.fixture(autouse=True)
def mock_fetch_cache(monkeypatch):
    """Substitutes spack.fetch_cache with a mock object that does nothing
    and raises on fetch.
    """
    class MockCache(object):
        def store(self, copyCmd, relativeDst):
            pass

        def fetcher(self, targetPath, digest, **kwargs):
            return MockCacheFetcher()

    class MockCacheFetcher(object):
        def set_stage(self, stage):
            pass

        def fetch(self):
            raise spack.fetch_strategy.FetchError(
                'Mock cache always fails for tests'
            )

        def __str__(self):
            return "[mock fetcher]"

    monkeypatch.setattr(spack, 'fetch_cache', MockCache())


# FIXME: The lines below should better be added to a fixture with
# FIXME: session-scope. Anyhow doing it is not easy, as it seems
# FIXME: there's some weird interaction with compilers during concretization.
spack.architecture.real_platform = spack.architecture.platform
spack.architecture.platform = lambda: spack.platforms.test.Test()

##########
# Test-specific fixtures
##########


@pytest.fixture(scope='session')
def repo_path():
    """Session scoped RepoPath object pointing to the mock repository"""
    return spack.repository.RepoPath(spack.mock_packages_path)


@pytest.fixture(scope='module')
def builtin_mock(repo_path):
    """Uses the 'builtin.mock' repository instead of 'builtin'"""
    mock_repo = copy.deepcopy(repo_path)
    spack.repo.swap(mock_repo)
    BuiltinMock = collections.namedtuple('BuiltinMock', ['real', 'mock'])
    # Confusing, but we swapped above
    yield BuiltinMock(real=mock_repo, mock=spack.repo)
    spack.repo.swap(mock_repo)


@pytest.fixture()
def refresh_builtin_mock(builtin_mock, repo_path):
    """Refreshes the state of spack.repo"""
    # Get back the real repository
    mock_repo = copy.deepcopy(repo_path)
    spack.repo.swap(mock_repo)
    return builtin_mock


@pytest.fixture(scope='session')
def linux_os():
    """Returns a named tuple with attributes 'name' and 'version'
    representing the OS.
    """
    platform = spack.architecture.platform()
    name, version = 'debian', '6'
    if platform.name == 'linux':
        platform = spack.architecture.platform()
        current_os = platform.operating_system('default_os')
        name, version = current_os.name, current_os.version
    LinuxOS = collections.namedtuple('LinuxOS', ['name', 'version'])
    return LinuxOS(name=name, version=version)


@pytest.fixture(scope='session')
def configuration_dir(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory. Returns the
    directory path.
    """
    tmpdir = tmpdir_factory.mktemp('configurations')
    # Name of the yaml files in the test/data folder
    test_path = py.path.local(spack.test_path)
    compilers_yaml = test_path.join('data', 'compilers.yaml')
    packages_yaml = test_path.join('data', 'packages.yaml')
    config_yaml = test_path.join('data', 'config.yaml')
    # Create temporary 'site' and 'user' folders
    tmpdir.ensure('site', dir=True)
    tmpdir.ensure('user', dir=True)
    # Copy the configurations that don't need further work
    packages_yaml.copy(tmpdir.join('site', 'packages.yaml'))
    config_yaml.copy(tmpdir.join('site', 'config.yaml'))
    # Write the one that needs modifications
    content = ''.join(compilers_yaml.read()).format(linux_os)
    t = tmpdir.join('site', 'compilers.yaml')
    t.write(content)
    return tmpdir


@pytest.fixture(scope='module')
def config(configuration_dir):
    """Hooks the mock configuration files into spack.config"""
    # Set up a mock config scope
    spack.config.clear_config_caches()
    real_scope = spack.config.config_scopes
    spack.config.config_scopes = ordereddict_backport.OrderedDict()
    spack.config.ConfigScope('site', str(configuration_dir.join('site')))
    spack.config.ConfigScope('user', str(configuration_dir.join('user')))
    Config = collections.namedtuple('Config', ['real', 'mock'])
    yield Config(real=real_scope, mock=spack.config.config_scopes)
    spack.config.config_scopes = real_scope
    spack.config.clear_config_caches()


@pytest.fixture(scope='module')
def database(tmpdir_factory, builtin_mock, config):
    """Creates a mock database with some packages installed note that
    the ref count for dyninst here will be 3, as it's recycled
    across each install.
    """

    # Here is what the mock DB looks like:
    #
    # o  mpileaks     o  mpileaks'    o  mpileaks''
    # |\              |\              |\
    # | o  callpath   | o  callpath'  | o  callpath''
    # |/|             |/|             |/|
    # o |  mpich      o |  mpich2     o |  zmpi
    #   |               |             o |  fake
    #   |               |               |
    #   |               |______________/
    #   | .____________/
    #   |/
    #   o  dyninst
    #   |\
    #   | o  libdwarf
    #   |/
    #   o  libelf

    # Make a fake install directory
    install_path = tmpdir_factory.mktemp('install_for_database')
    spack_install_path = py.path.local(spack.store.root)
    spack.store.root = str(install_path)

    install_layout = spack.directory_layout.YamlDirectoryLayout(
        str(install_path)
    )
    spack_install_layout = spack.store.layout
    spack.store.layout = install_layout

    # Make fake database and fake install directory.
    install_db = spack.database.Database(str(install_path))
    spack_install_db = spack.store.db
    spack.store.db = install_db

    Entry = collections.namedtuple('Entry', ['path', 'layout', 'db'])
    Database = collections.namedtuple(
        'Database', ['real', 'mock', 'install', 'uninstall', 'refresh']
    )

    real = Entry(
        path=spack_install_path,
        layout=spack_install_layout,
        db=spack_install_db
    )
    mock = Entry(path=install_path, layout=install_layout, db=install_db)

    def _install(spec):
        s = spack.spec.Spec(spec)
        s.concretize()
        pkg = spack.repo.get(s)
        pkg.do_install(fake=True)

    def _uninstall(spec):
        spec.package.do_uninstall(spec)

    def _refresh():
        with spack.store.db.write_transaction():
            for spec in spack.store.db.query():
                _uninstall(spec)
            _install('mpileaks ^mpich')
            _install('mpileaks ^mpich2')
            _install('mpileaks ^zmpi')

    t = Database(
        real=real,
        mock=mock,
        install=_install,
        uninstall=_uninstall,
        refresh=_refresh
    )
    # Transaction used to avoid repeated writes.
    with spack.store.db.write_transaction():
        t.install('mpileaks ^mpich')
        t.install('mpileaks ^mpich2')
        t.install('mpileaks ^zmpi')

    yield t

    with spack.store.db.write_transaction():
        for spec in spack.store.db.query():
            t.uninstall(spec)

    install_path.remove(rec=1)
    spack.store.root = str(spack_install_path)
    spack.store.layout = spack_install_layout
    spack.store.db = spack_install_db


@pytest.fixture()
def refresh_db_on_exit(database):
    """"Restores the state of the database after a test."""
    yield
    database.refresh()

##########
# Fake archives and repositories
##########


@pytest.fixture(scope='session')
def mock_archive():
    """Creates a very simple archive directory with a configure script and a
    makefile that installs to a prefix. Tars it up into an archive.
    """
    tar = spack.util.executable.which('tar', required=True)
    stage = spack.stage.Stage('mock-archive-stage')
    tmpdir = py.path.local(stage.path)
    repo_name = 'mock-archive-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)
    # Create the configure script
    configure_path = str(tmpdir.join(repo_name, 'configure'))
    with open(configure_path, 'w') as f:
        f.write(
            "#!/bin/sh\n"
            "prefix=$(echo $1 | sed 's/--prefix=//')\n"
            "cat > Makefile <<EOF\n"
            "all:\n"
            "\techo Building...\n\n"
            "install:\n"
            "\tmkdir -p $prefix\n"
            "\ttouch $prefix/dummy_file\n"
            "EOF\n"
        )
    os.chmod(configure_path, 0755)
    # Archive it
    current = tmpdir.chdir()
    archive_name = '{0}.tar.gz'.format(repo_name)
    tar('-czf', archive_name, repo_name)
    current.chdir()
    Archive = collections.namedtuple('Archive', ['url', 'path'])
    url = 'file://' + str(tmpdir.join(archive_name))
    # Return the url
    yield Archive(url=url, path=str(repodir))
    stage.destroy()


@pytest.fixture(scope='session')
def mock_git_repository():
    """Creates a very simple git repository with two branches and
    two commits.
    """
    git = spack.util.executable.which('git', required=True)
    stage = spack.stage.Stage('mock-git-stage')
    tmpdir = py.path.local(stage.path)
    repo_name = 'mock-git-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)

    # Initialize the repository
    current = repodir.chdir()
    git('init')
    url = 'file://' + str(repodir)

    # r0 is just the first commit
    r0_file = 'r0_file'
    repodir.ensure(r0_file)
    git('add', r0_file)
    git('commit', '-m', 'mock-git-repo r0')

    branch = 'test-branch'
    branch_file = 'branch_file'
    git('branch', branch)

    tag_branch = 'tag-branch'
    tag_file = 'tag_file'
    git('branch', tag_branch)

    # Check out first branch
    git('checkout', branch)
    repodir.ensure(branch_file)
    git('add', branch_file)
    git('commit', '-m' 'r1 test branch')

    # Check out a second branch and tag it
    git('checkout', tag_branch)
    repodir.ensure(tag_file)
    git('add', tag_file)
    git('commit', '-m' 'tag test branch')

    tag = 'test-tag'
    git('tag', tag)

    git('checkout', 'master')

    # R1 test is the same as test for branch
    rev_hash = lambda x: git('rev-parse', x, output=str).strip()
    r1 = rev_hash(branch)
    r1_file = branch_file
    current.chdir()

    Bunch = spack.util.pattern.Bunch

    checks = {
        'master': Bunch(
            revision='master', file=r0_file, args={'git': str(repodir)}
        ),
        'branch': Bunch(
            revision=branch, file=branch_file, args={
                'git': str(repodir), 'branch': branch
            }
        ),
        'tag': Bunch(
            revision=tag, file=tag_file, args={'git': str(repodir), 'tag': tag}
        ),
        'commit': Bunch(
            revision=r1, file=r1_file, args={'git': str(repodir), 'commit': r1}
        )
    }

    t = Bunch(checks=checks, url=url, hash=rev_hash, path=str(repodir))
    yield t
    stage.destroy()


@pytest.fixture(scope='session')
def mock_hg_repository():
    """Creates a very simple hg repository with two commits."""
    hg = spack.util.executable.which('hg', required=True)
    stage = spack.stage.Stage('mock-hg-stage')
    tmpdir = py.path.local(stage.path)
    repo_name = 'mock-hg-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)

    get_rev = lambda: hg('id', '-i', output=str).strip()

    # Initialize the repository
    current = repodir.chdir()
    url = 'file://' + str(repodir)
    hg('init')
    # Commit file r0
    r0_file = 'r0_file'
    repodir.ensure(r0_file)
    hg('add', r0_file)
    hg('commit', '-m', 'revision 0', '-u', 'test')
    r0 = get_rev()
    # Commit file r1
    r1_file = 'r1_file'
    repodir.ensure(r1_file)
    hg('add', r1_file)
    hg('commit', '-m' 'revision 1', '-u', 'test')
    r1 = get_rev()
    current.chdir()

    Bunch = spack.util.pattern.Bunch

    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'hg': str(repodir)}
        ),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'hg': str(repodir), 'revision': r0
            }
        )
    }
    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t
    stage.destroy()


@pytest.fixture(scope='session')
def mock_svn_repository():
    """Creates a very simple svn repository with two commits."""
    svn = spack.util.executable.which('svn', required=True)
    svnadmin = spack.util.executable.which('svnadmin', required=True)
    stage = spack.stage.Stage('mock-svn-stage')
    tmpdir = py.path.local(stage.path)
    repo_name = 'mock-svn-repo'
    tmpdir.ensure(repo_name, dir=True)
    repodir = tmpdir.join(repo_name)
    url = 'file://' + str(repodir)
    # Initialize the repository
    current = repodir.chdir()
    svnadmin('create', str(repodir))

    # Import a structure (first commit)
    r0_file = 'r0_file'
    tmpdir.ensure('tmp-path', r0_file)
    svn(
        'import',
        str(tmpdir.join('tmp-path')),
        url,
        '-m',
        'Initial import r0'
    )
    shutil.rmtree(str(tmpdir.join('tmp-path')))
    # Second commit
    r1_file = 'r1_file'
    svn('checkout', url, str(tmpdir.join('tmp-path')))
    tmpdir.ensure('tmp-path', r1_file)
    tmpdir.join('tmp-path').chdir()
    svn('add', str(tmpdir.ensure('tmp-path', r1_file)))
    svn('ci', '-m', 'second revision r1')
    repodir.chdir()
    shutil.rmtree(str(tmpdir.join('tmp-path')))
    r0 = '1'
    r1 = '2'

    Bunch = spack.util.pattern.Bunch

    checks = {
        'default': Bunch(
            revision=r1, file=r1_file, args={'svn': url}
        ),
        'rev0': Bunch(
            revision=r0, file=r0_file, args={
                'svn': url, 'revision': r0
            }
        )
    }

    def get_rev():
        output = svn('info', output=str)
        assert "Revision" in output
        for line in output.split('\n'):
            match = re.match(r'Revision: (\d+)', line)
            if match:
                return match.group(1)

    t = Bunch(checks=checks, url=url, hash=get_rev, path=str(repodir))
    yield t
    current.chdir()

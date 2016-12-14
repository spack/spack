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
import re
import shutil

import StringIO
import llnl.util.filesystem
import llnl.util.lang
import ordereddict_backport
import py
import pytest
import spack
import spack.architecture
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
    StringIO object.
    """
    monkeypatch.setattr(
        llnl.util.lang,
        'duplicate_stream',
        lambda x: StringIO.StringIO()
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


@pytest.fixture()
def mock_repository():
    """Substitutes the 'builtin' Spack repository with the 'mock' repository
    used for tests.
    """
    db = spack.repository.RepoPath(spack.mock_packages_path)
    spack.repo.swap(db)
    yield
    spack.repo.swap(db)


@pytest.fixture(scope='session')
def linux_os():
    """Returns OS name and OS version as a tuple"""
    platform = spack.architecture.platform()
    os_name, os_version = 'debian', '6'
    if platform.name == 'linux':
        platform = spack.architecture.platform()
        linux_os = platform.operating_system('default_os')
        os_name, os_version = linux_os.name, linux_os_version
    return os_name, os_version


@pytest.fixture(scope='module')
def configuration_files(tmpdir_factory, linux_os):
    """Copies mock configuration files in a temporary directory
    and add hooks them to the current spack instance.
    """
    tmpdir = tmpdir_factory.mktemp('configurations')
    # Name of the yaml files in the test/data folder
    join_path = llnl.util.filesystem.join_path
    compilers_yaml = join_path(spack.test_path, 'data', 'compilers.yaml')
    packages_yaml = join_path(spack.test_path, 'data', 'packages.yaml')
    config_yaml = join_path(spack.test_path, 'data', 'config.yaml')
    # Create temporary 'site' and 'user' folders
    tmpdir.ensure_dir('site')
    tmpdir.ensure_dir('user')
    # Copy the configurations that don't need further work
    shutil.copy(packages_yaml, str(tmpdir.join('site', 'packages.yaml')))
    shutil.copy(config_yaml, str(tmpdir.join('site', 'config.yaml')))
    # Write the one that needs modifications
    os_name, os_version = linux_os
    with open(compilers_yaml) as f:
        content = ''.join(f.readlines()).format(os_name, os_version)
    t = tmpdir.join('site', 'compilers.yaml')
    t.write(content)
    # Set up a mock config scope
    spack.config.clear_config_caches()
    real_scope = spack.config.config_scopes
    spack.config.config_scopes = ordereddict_backport.OrderedDict()
    spack.config.ConfigScope('site', str(tmpdir.join('site')))
    spack.config.ConfigScope('user', str(tmpdir.join('user')))
    yield
    spack.config.config_scopes = real_scope
    spack.config.clear_config_caches()


@pytest.fixture()
def share_path(tmpdir, monkeypatch):
    """Keep tests from interfering with the actual module path."""
    monkeypatch.setattr(spack, 'share_path', str(tmpdir))


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
    Bunch = spack.util.pattern.Bunch
    url = 'file://' + str(tmpdir.join(archive_name))
    t = Bunch(
        url=url, path=str(repodir)
    )
    # Return the url
    yield t
    stage.destroy()


@pytest.fixture(scope='session')
def mock_git_repository():
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
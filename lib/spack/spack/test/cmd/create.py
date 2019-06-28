# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil
import pytest

import llnl.util.tty as tty

import spack.cmd.create
import spack.util.editor

from spack.main import SpackCommand


create = SpackCommand('create')


@pytest.fixture("module")
def cmd_create_repo(tmpdir_factory):
    repo_namespace = 'cmd_create_repo'
    repodir = tmpdir_factory.mktemp(repo_namespace)
    repodir.ensure(spack.repo.packages_dir_name, dir=True)
    yaml = repodir.join('repo.yaml')
    yaml.write("""
repo:
    namespace: cmd_create_repo
""")

    db = spack.repo.RepoPath(str(repodir))
    with spack.repo.swap(db):
        yield repodir

    # shutil.rmtree(str(repodir))


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module"""
    prs = argparse.ArgumentParser()
    spack.cmd.create.setup_parser(prs)
    return prs


@pytest.fixture
def mock_editor(monkeypatch):
    def _editor(*args, **kwargs):
        return

    monkeypatch.setattr(spack.util.editor, 'editor', _editor)
    yield


@pytest.mark.parametrize('options,name,expected', [
    ([], 'test-package', [r'TestPackage(Package)', r'def install(self']),
    (['-t', 'bundle'], 'test-bundle', [r'TestBundle(BundlePackage)']),
])
def test_create_templates(parser, cmd_create_repo, options, name, expected):
    """Test template creation."""
    repodir = cmd_create_repo

    temp_args = options + ['--skip-editor', name]
    args = parser.parse_args(temp_args)
    spack.cmd.create.create(parser, args)

    filename = str(repodir.join(spack.repo.packages_dir_name, name,
                                spack.repo.package_file_name))
    assert os.path.exists(filename)

    with open(filename, 'r') as package_file:
        content = ' '.join(package_file.readlines())
        for entry in expected:
            assert content.find(entry) > -1

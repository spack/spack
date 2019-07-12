# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import pytest

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

    repo = spack.repo.RepoPath(str(repodir))
    with spack.repo.swap(repo):
        yield repo, repodir


@pytest.fixture(scope='module')
def parser():
    """Returns the parser for the module"""
    prs = argparse.ArgumentParser()
    spack.cmd.create.setup_parser(prs)
    return prs


def test_create_template(parser, cmd_create_repo):
    """Test template creation."""
    repo, repodir = cmd_create_repo

    name = 'test-package'
    args = parser.parse_args(['--skip-editor', name])
    spack.cmd.create.create(parser, args)

    filename = repo.filename_for_package_name(name)
    assert os.path.exists(filename)

    with open(filename, 'r') as package_file:
        content = ' '.join(package_file.readlines())
        for entry in [r'TestPackage(Package)', r'def install(self']:
            assert content.find(entry) > -1

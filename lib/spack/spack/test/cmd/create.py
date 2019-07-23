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


@pytest.mark.parametrize('args,name_index,expected', [
    (['test-package'], 0, [r'TestPackage(Package)', r'def install(self']),
    (['-n', 'test-named-package', 'file://example.tar.gz'], 1,
     [r'TestNamedPackage(Package)', r'def install(self']),
    (['-t', 'bundle', 'test-bundle'], 2, [r'TestBundle(BundlePackage)']),
    (['-n', 'test-named-bundle'], 1, [r'TestNamedBundle(BundlePackage)'])
])
def test_create_template(parser, cmd_create_repo, args, name_index, expected):
    """Test template creation."""
    repo, repodir = cmd_create_repo

    constr_args = parser.parse_args(['--skip-editor'] + args)
    spack.cmd.create.create(parser, constr_args)

    filename = repo.filename_for_package_name(args[name_index])
    assert os.path.exists(filename)

    with open(filename, 'r') as package_file:
        content = ' '.join(package_file.readlines())
        for entry in expected:
            assert entry in content

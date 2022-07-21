# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

import pytest

import spack.config
import spack.repo
import spack.util.spack_yaml as syaml
from spack.config import ConfigError, ConfigScope
from spack.spec import Spec
from spack.version import Version
from spack.solver.asp import UnsatisfiableSpecError

# TODO: this is entirely reused from concretize_preferences
@pytest.fixture()
def concretize_scope(mutable_config, tmpdir):
    """Adds a scope for concretization preferences"""
    tmpdir.ensure_dir('concretize')
    mutable_config.push_scope(
        ConfigScope('concretize', str(tmpdir.join('concretize'))))

    yield

    mutable_config.pop_scope()
    spack.repo.path._provider_index = None

def update_packages_config(conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set('packages', conf['packages'], scope='concretize')


_pkgx = ('x', """\
class X(Package):
    version('1.1')
    version('1.0')

    depends_on('y')
""")


_pkgy = ('y', """\
class Y(Package):
    version('2.5')
    version('2.4')
""")


@pytest.fixture
def test_repo(tmpdir, mutable_config):
    repo_path = str(tmpdir)
    repo_yaml = tmpdir.join('repo.yaml')
    with open(repo_yaml, 'w') as f:
        f.write("""\
repo:
  namespace: testcfgrequirements
""")

    packages_dir = tmpdir.join('packages')
    for (pkg_name, pkg_str) in [_pkgx, _pkgy]:
        pkg_dir = packages_dir.ensure(pkg_name, dir=True)
        pkg_file = pkg_dir.join('package.py')
        with open(pkg_file, 'w') as f:
            f.write(pkg_str)

    mock_repo = spack.repo.Repo(repo_path)
    with spack.repo.use_repositories(mock_repo) as mock_repo_path:
        yield mock_repo_path


def test_requirements_arent_optional(concretize_scope, test_repo):
    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    with pytest.raises(UnsatisfiableSpecError):
        Spec('x@1.1').concretize()


def test_basic_requirements_are_respected(concretize_scope, test_repo):
    s1 = Spec('x').concretized()
    # Without any requirements/preferences, the later version is preferred
    assert s1.satisfies('@1.1')

    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    s2 = Spec('x').concretized()
    # The requirement forces choosing the eariler version
    assert s2.satisfies('@1.0')


def test_multi_package_requirements_are_respected(
        concretize_scope, test_repo):
    conf_str = """\
packages:
  x:
    require: "@1.0"
  y:
    require: "@2.4"
"""
    update_packages_config(conf_str)
    spec = Spec('x').concretized()
    assert spec['x'].satisfies('@1.0')
    assert spec['y'].satisfies('@2.4')

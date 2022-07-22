# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

import spack.config
import spack.repo
import spack.util.spack_yaml as syaml
from spack.config import ConfigScope
from spack.solver.asp import UnsatisfiableSpecError
from spack.spec import Spec

pytestmark = pytest.mark.skipif(sys.platform == "win32",
                                reason="Windows uses old concretizer")


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
    version('0.9')

    variant('shared', default=True,
            description='Build shared libraries')

    depends_on('y')
""")


_pkgy = ('y', """\
class Y(Package):
    version('2.5')
    version('2.4')

    variant('shared', default=True,
            description='Build shared libraries')
""")


@pytest.fixture
def test_repo(tmpdir, mutable_config):
    repo_path = str(tmpdir)
    repo_yaml = tmpdir.join('repo.yaml')
    with open(str(repo_yaml), 'w') as f:
        f.write("""\
repo:
  namespace: testcfgrequirements
""")

    packages_dir = tmpdir.join('packages')
    for (pkg_name, pkg_str) in [_pkgx, _pkgy]:
        pkg_dir = packages_dir.ensure(pkg_name, dir=True)
        pkg_file = pkg_dir.join('package.py')
        with open(str(pkg_file), 'w') as f:
            f.write(pkg_str)

    mock_repo = spack.repo.Repo(repo_path)
    with spack.repo.use_repositories(mock_repo) as mock_repo_path:
        yield mock_repo_path


def test_requirement_isnt_optional(concretize_scope, test_repo):
    """If a user spec requests something that directly conflicts
       with a requirement, make sure we get an error.
    """
    if spack.config.get('config:concretizer') == 'original':
        pytest.skip("Original concretizer does not support configuration"
                    " requirements")

    conf_str = """\
packages:
  x:
    require: "@1.0"
"""
    update_packages_config(conf_str)
    with pytest.raises(UnsatisfiableSpecError):
        Spec('x@1.1').concretize()


def test_requirement_is_successfully_applied(concretize_scope, test_repo):
    """If a simple requirement can be satisfied, make sure the
       concretization succeeds and the requirement spec is applied.
    """
    if spack.config.get('config:concretizer') == 'original':
        pytest.skip("Original concretizer does not support configuration"
                    " requirements")

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


def test_multiple_packages_requirements_are_respected(
        concretize_scope, test_repo):
    """Apply requirements to two packages; make sure the concretization
       succeeds and both requirements are respected.
    """
    if spack.config.get('config:concretizer') == 'original':
        pytest.skip("Original concretizer does not support configuration"
                    " requirements")

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


def test_one_of(concretize_scope, test_repo):
    """'one_of' allows forcing the concretizer to satisfy one of
       the specs in the group (but not all have to be satisfied).
    """
    if spack.config.get('config:concretizer') == 'original':
        pytest.skip("Original concretizer does not support configuration"
                    " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4", "~shared"]
"""
    update_packages_config(conf_str)
    spec = Spec('x').concretized()
    # The concretizer only has to satisfy one of @2.4/~shared, and @2.4
    # comes first so it is prioritized
    assert spec['y'].satisfies('@2.4+shared')


def test_one_package_multiple_one_of_groups(concretize_scope, test_repo):
    if spack.config.get('config:concretizer') == 'original':
        pytest.skip("Original concretizer does not support configuration"
                    " requirements")

    conf_str = """\
packages:
  y:
    require:
    - one_of: ["@2.4%gcc", "@2.5%clang"]
    - one_of: ["@2.5~shared", "@2.4+shared"]
"""
    update_packages_config(conf_str)

    s1 = Spec('y@2.5').concretized()
    assert s1.satisfies('%clang~shared')

    s2 = Spec('y@2.4').concretized()
    assert s2.satisfies('%gcc+shared')

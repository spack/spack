# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from six import StringIO

import pytest

import llnl.util.filesystem as fs

import spack.modules
import spack.environment as ev
from spack.cmd.env import _env_create
from spack.spec import Spec
from spack.main import SpackCommand


# everything here uses the mock_env_path
pytestmark = pytest.mark.usefixtures(
    'mutable_mock_env_path', 'config', 'mutable_mock_packages')

env        = SpackCommand('env')
install    = SpackCommand('install')
add        = SpackCommand('add')
remove     = SpackCommand('remove')
concretize = SpackCommand('concretize')
stage      = SpackCommand('stage')
uninstall  = SpackCommand('uninstall')
find       = SpackCommand('find')


def test_add():
    e = ev.create('test')
    e.add('mpileaks')
    assert Spec('mpileaks') in e.user_specs


def test_env_list(mutable_mock_env_path):
    env('create', 'foo')
    env('create', 'bar')
    env('create', 'baz')

    out = env('list')

    assert 'foo' in out
    assert 'bar' in out
    assert 'baz' in out

    # make sure `spack env list` skips invalid things in var/spack/env
    mutable_mock_env_path.join('.DS_Store').ensure(file=True)
    out = env('list')

    assert 'foo' in out
    assert 'bar' in out
    assert 'baz' in out
    assert '.DS_Store' not in out


def test_env_remove(capfd):
    env('create', 'foo')
    env('create', 'bar')

    out = env('list')
    assert 'foo' in out
    assert 'bar' in out

    foo = ev.read('foo')
    with foo:
        with pytest.raises(spack.main.SpackCommandError):
            with capfd.disabled():
                env('remove', '-y', 'foo')
        assert 'foo' in env('list')

    env('remove', '-y', 'foo')
    out = env('list')
    assert 'foo' not in out
    assert 'bar' in out

    env('remove', '-y', 'bar')
    out = env('list')
    assert 'foo' not in out
    assert 'bar' not in out


def test_concretize():
    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()
    env_specs = e._get_environment_specs()
    assert any(x.name == 'mpileaks' for x in env_specs)


def test_env_install_all(install_mockery, mock_fetch):
    e = ev.create('test')
    e.add('cmake-client')
    e.concretize()
    e.install_all()
    env_specs = e._get_environment_specs()
    spec = next(x for x in env_specs if x.name == 'cmake-client')
    assert spec.package.installed


def test_env_install_single_spec(install_mockery, mock_fetch):
    env('create', 'test')
    install = SpackCommand('install')

    e = ev.read('test')
    with e:
        install('cmake-client')

    e = ev.read('test')
    assert e.user_specs[0].name == 'cmake-client'
    assert e.concretized_user_specs[0].name == 'cmake-client'
    assert e.specs_by_hash[e.concretized_order[0]].name == 'cmake-client'


def test_env_install_same_spec_twice(install_mockery, mock_fetch, capfd):
    env('create', 'test')

    e = ev.read('test')
    with capfd.disabled():
        with e:
            install('cmake-client')
            out = install('cmake-client')
            assert 'is already installed in' in out


def test_remove_after_concretize():
    e = ev.create('test')

    e.add('mpileaks')
    e.concretize()

    e.add('python')
    e.concretize()

    e.remove('mpileaks')
    assert Spec('mpileaks') not in e.user_specs
    env_specs = e._get_environment_specs()
    assert any(s.name == 'mpileaks' for s in env_specs)

    e.add('mpileaks')
    assert any(s.name == 'mpileaks' for s in e.user_specs)

    e.remove('mpileaks', force=True)
    assert Spec('mpileaks') not in e.user_specs
    env_specs = e._get_environment_specs()
    assert not any(s.name == 'mpileaks' for s in env_specs)


def test_remove_command():
    env('create', 'test')
    assert 'test' in env('list')

    with ev.read('test'):
        add('mpileaks')
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        remove('mpileaks')
        assert 'mpileaks' not in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        add('mpileaks')
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' not in find('--show-concretized')

    with ev.read('test'):
        concretize()
        assert 'mpileaks' in find()
        assert 'mpileaks@' not in find()
        assert 'mpileaks@' in find('--show-concretized')

    with ev.read('test'):
        remove('mpileaks')
        assert 'mpileaks' not in find()
        # removed but still in last concretized specs
        assert 'mpileaks@' in find('--show-concretized')

    with ev.read('test'):
        concretize()
        assert 'mpileaks' not in find()
        assert 'mpileaks@' not in find()
        # now the lockfile is regenerated and it's gone.
        assert 'mpileaks@' not in find('--show-concretized')


def test_environment_status(capfd, tmpdir):
    with capfd.disabled():
        with tmpdir.as_cwd():
            assert 'No active environment' in env('status')

            with ev.create('test'):
                assert 'In environment test' in env('status')

            with ev.Environment('local_dir'):
                assert os.path.join(os.getcwd(), 'local_dir') in env('status')

                e = ev.Environment('myproject')
                e.write()
                with tmpdir.join('myproject').as_cwd():
                    with e:
                        assert 'in current directory' in env('status')


def test_to_lockfile_dict():
    e = ev.create('test')
    e.add('mpileaks')
    e.concretize()
    context_dict = e._to_lockfile_dict()

    e_copy = ev.create('test_copy')

    e_copy._read_lockfile_dict(context_dict)
    assert e.specs_by_hash == e_copy.specs_by_hash


def test_env_repo():
    e = ev.create('test')
    e.add('mpileaks')
    e.write()

    with ev.read('test'):
        concretize()

    package = e.repo.get('mpileaks')
    assert package.name == 'mpileaks'
    assert package.namespace == 'builtin.mock'


def test_user_removed_spec():
    """Ensure a user can remove from any position in the spack.yaml file."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")

    before = ev.create('test', initial_yaml)
    before.concretize()
    before.write()

    # user modifies yaml externally to spack and removes hypre
    with open(before.manifest_path, 'w') as f:
        f.write("""\
env:
  specs:
  - mpileaks
  - libelf
""")

    after = ev.read('test')
    after.concretize()
    after.write()

    env_specs = after._get_environment_specs()
    read = ev.read('test')
    env_specs = read._get_environment_specs()

    assert not any(x.name == 'hypre' for x in env_specs)


def test_init_from_lockfile(tmpdir):
    """Test that an environment can be instantiated from a lockfile."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")
    e1 = ev.create('test', initial_yaml)
    e1.concretize()
    e1.write()

    e2 = ev.Environment(str(tmpdir), e1.lock_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    for h1, h2 in zip(e1.concretized_order, e2.concretized_order):
        assert h1 == h2
        assert e1.specs_by_hash[h1] == e2.specs_by_hash[h2]

    for s1, s2 in zip(e1.concretized_user_specs, e2.concretized_user_specs):
        assert s1 == s2


def test_init_from_yaml(tmpdir):
    """Test that an environment can be instantiated from a lockfile."""
    initial_yaml = StringIO("""\
env:
  specs:
  - mpileaks
  - hypre
  - libelf
""")
    e1 = ev.create('test', initial_yaml)
    e1.concretize()
    e1.write()

    e2 = ev.Environment(str(tmpdir), e1.manifest_path)

    for s1, s2 in zip(e1.user_specs, e2.user_specs):
        assert s1 == s2

    assert not e2.concretized_order
    assert not e2.concretized_user_specs
    assert not e2.specs_by_hash


def test_init_with_file_and_remove(tmpdir):
    """Ensure a user can remove from any position in the spack.yaml file."""
    path = tmpdir.join('spack.yaml')

    with tmpdir.as_cwd():
        with open(str(path), 'w') as f:
            f.write("""\
env:
  specs:
  - mpileaks
""")

        env('create', 'test', 'spack.yaml')

    out = env('list')
    assert 'test' in out

    with ev.read('test'):
        assert 'mpileaks' in find()

    env('remove', '-y', 'test')

    out = env('list')
    assert 'test' not in out


def test_env_with_config():
    test_config = """\
env:
  specs:
  - mpileaks
  packages:
    mpileaks:
      version: [2.2]
"""
    spack.package_prefs.PackagePrefs.clear_caches()

    _env_create('test', StringIO(test_config))

    e = ev.read('test')
    ev.prepare_config_scope(e)
    e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_with_included_config_file():
    test_config = """\
env:
  include:
  - ./included-config.yaml
  specs:
  - mpileaks
"""
    spack.package_prefs.PackagePrefs.clear_caches()

    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'included-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    ev.prepare_config_scope(e)
    e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_with_included_config_scope():
    config_scope_path = os.path.join(ev.root('test'), 'config')
    test_config = """\
env:
  include:
  - %s
  specs:
  - mpileaks
""" % config_scope_path

    spack.package_prefs.PackagePrefs.clear_caches()
    _env_create('test', StringIO(test_config))

    e = ev.read('test')

    fs.mkdirp(config_scope_path)
    with open(os.path.join(config_scope_path, 'packages.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
""")

    ev.prepare_config_scope(e)
    e.concretize()

    assert any(x.satisfies('mpileaks@2.2')
               for x in e._get_environment_specs())


def test_env_config_precedence():
    test_config = """\
env:
  packages:
    libelf:
      version: [0.8.12]
  include:
  - ./included-config.yaml
  specs:
  - mpileaks
"""

    spack.package_prefs.PackagePrefs.clear_caches()

    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'included-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
  libelf:
    version: [0.8.11]
""")

    ev.prepare_config_scope(e)
    e.concretize()

    # ensure included scope took effect
    assert any(
        x.satisfies('mpileaks@2.2') for x in e._get_environment_specs())

    # ensure env file takes precedence
    assert any(
        x.satisfies('libelf@0.8.12') for x in e._get_environment_specs())


def test_included_config_precedence():
    test_config = """\
env:
  include:
  - ./high-config.yaml  # this one should take precedence
  - ./low-config.yaml
  specs:
  - mpileaks
"""
    spack.package_prefs.PackagePrefs.clear_caches()

    _env_create('test', StringIO(test_config))
    e = ev.read('test')

    with open(os.path.join(e.path, 'high-config.yaml'), 'w') as f:
        f.write("""\
packages:
  libelf:
    version: [0.8.10]  # this should override libelf version below
""")

    with open(os.path.join(e.path, 'low-config.yaml'), 'w') as f:
        f.write("""\
packages:
  mpileaks:
    version: [2.2]
  libelf:
    version: [0.8.12]
""")

    ev.prepare_config_scope(e)
    e.concretize()

    assert any(
        x.satisfies('mpileaks@2.2') for x in e._get_environment_specs())

    assert any(
        [x.satisfies('libelf@0.8.10') for x in e._get_environment_specs()])


def test_bad_env_yaml_format(tmpdir):
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
env:
  spacks:
    - mpileaks
""")

    with tmpdir.as_cwd():
        with pytest.raises(spack.config.ConfigFormatError) as e:
            env('create', 'test', './spack.yaml')
        assert './spack.yaml:2' in str(e)
        assert "'spacks' was unexpected" in str(e)


def test_env_loads(install_mockery, mock_fetch):
    env('create', 'test')

    with ev.read('test'):
        add('mpileaks')
        concretize()
        install('--fake')

    with ev.read('test'):
        env('loads', 'test')

    e = ev.read('test')

    loads_file = os.path.join(e.path, 'loads')
    assert os.path.exists(loads_file)

    with open(loads_file) as f:
        contents = f.read()
        assert 'module load mpileaks' in contents


@pytest.mark.disable_clean_stage_check
def test_stage(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        add('zmpi')
        concretize()
        stage()

    root = str(mock_stage)

    def check_stage(spec):
        spec = Spec(spec).concretized()
        for dep in spec.traverse():
            stage_name = "%s-%s-%s" % (dep.name, dep.version, dep.dag_hash())
            assert os.path.isdir(os.path.join(root, stage_name))

    check_stage('mpileaks')
    check_stage('zmpi')


def test_env_commands_die_with_no_env_arg():
    # these fail in argparse when given no arg
    with pytest.raises(SystemExit):
        env('create')
    with pytest.raises(SystemExit):
        env('remove')

    # these have an optional env arg and raise errors via tty.die
    with pytest.raises(spack.main.SpackCommandError):
        env('loads')

    # This should NOT raise an error with no environment
    # it just tells the user there isn't an environment
    env('status')


def test_env_blocks_uninstall(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        install('--fake')

    out = uninstall('mpileaks', fail_on_error=False)
    assert uninstall.returncode == 1
    assert 'used by the following environments' in out


def test_uninstall_removes_from_env(mock_stage, mock_fetch, install_mockery):
    env('create', 'test')
    with ev.read('test'):
        add('mpileaks')
        add('libelf')
        install('--fake')

    test = ev.read('test')
    assert any(s.name == 'mpileaks' for s in test.specs_by_hash.values())
    assert any(s.name == 'libelf' for s in test.specs_by_hash.values())

    with ev.read('test'):
        uninstall('-ya')

    test = ev.read('test')
    assert not test.specs_by_hash
    assert not test.concretized_order
    assert not test.user_specs

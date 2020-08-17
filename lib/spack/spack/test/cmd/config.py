# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import pytest

import llnl.util.filesystem as fs
import spack.config
import spack.environment as ev
import spack.main
import spack.util.spack_yaml as syaml

config = spack.main.SpackCommand('config')
env = spack.main.SpackCommand('env')


@pytest.fixture()
def packages_yaml_v015(mutable_config):
    """Create a packages.yaml in the old format"""
    def _create(scope=None):
        old_data = {
            'packages': {
                'cmake': {
                    'paths': {'cmake@3.14.0': '/usr'}
                },
                'gcc': {
                    'modules': {'gcc@8.3.0': 'gcc-8'}
                }
            }
        }
        scope = scope or spack.config.default_modify_scope()
        cfg_file = spack.config.config.get_config_filename(scope, 'packages')
        with open(cfg_file, 'w') as f:
            syaml.dump(old_data, stream=f)
        return cfg_file
    return _create


def test_get_config_scope(mock_low_high_config):
    assert config('get', 'compilers').strip() == 'compilers: {}'


def test_get_config_scope_merged(mock_low_high_config):
    low_path = mock_low_high_config.scopes['low'].path
    high_path = mock_low_high_config.scopes['high'].path

    fs.mkdirp(low_path)
    fs.mkdirp(high_path)

    with open(os.path.join(low_path, 'repos.yaml'), 'w') as f:
        f.write('''\
repos:
- repo3
''')

    with open(os.path.join(high_path, 'repos.yaml'), 'w') as f:
        f.write('''\
repos:
- repo1
- repo2
''')

    assert config('get', 'repos').strip() == '''repos:
- repo1
- repo2
- repo3'''


def test_config_edit():
    """Ensure `spack config edit` edits the right paths."""
    dms = spack.config.default_modify_scope('compilers')
    dms_path = spack.config.config.scopes[dms].path
    user_path = spack.config.config.scopes['user'].path

    comp_path = os.path.join(dms_path, 'compilers.yaml')
    repos_path = os.path.join(user_path, 'repos.yaml')

    assert config('edit', '--print-file', 'compilers').strip() == comp_path
    assert config('edit', '--print-file', 'repos').strip() == repos_path


def test_config_get_gets_spack_yaml(mutable_mock_env_path):
    env = ev.create('test')

    config('get', fail_on_error=False)
    assert config.returncode == 1

    with env:
        config('get', fail_on_error=False)
        assert config.returncode == 1

        env.write()

        assert 'mpileaks' not in config('get')

        env.add('mpileaks')
        env.write()

        assert 'mpileaks' in config('get')


def test_config_edit_edits_spack_yaml(mutable_mock_env_path):
    env = ev.create('test')
    with env:
        assert config('edit', '--print-file').strip() == env.manifest_path


def test_config_edit_fails_correctly_with_no_env(mutable_mock_env_path):
    output = config('edit', '--print-file', fail_on_error=False)
    assert "requires a section argument or an active environment" in output


def test_config_get_fails_correctly_with_no_env(mutable_mock_env_path):
    output = config('get', fail_on_error=False)
    assert "requires a section argument or an active environment" in output


def test_config_list():
    output = config('list')
    assert 'compilers' in output
    assert 'packages' in output


def test_config_add(mutable_empty_config):
    config('add', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config:
  dirty: true
"""


def test_config_add_list(mutable_empty_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test3
  - test2
  - test1
"""


def test_config_add_override(mutable_empty_config):
    config('--scope', 'site', 'add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test2
  - test1
"""

    config('add', 'config::template_dirs:[test2]')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test2
"""


def test_config_add_override_leaf(mutable_empty_config):
    config('--scope', 'site', 'add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test2
  - test1
"""

    config('add', 'config:template_dirs::[test2]')
    output = config('get', 'config')

    assert output == """config:
  'template_dirs:':
  - test2
"""


def test_config_add_update_dict(mutable_empty_config):
    config('add', 'packages:all:compiler:[gcc]')
    config('add', 'packages:all:version:1.0.0')
    output = config('get', 'packages')

    expected = """packages:
  all:
    compiler: [gcc]
    version:
    - 1.0.0
"""

    assert output == expected


def test_config_add_ordered_dict(mutable_empty_config):
    config('add', 'mirrors:first:/path/to/first')
    config('add', 'mirrors:second:/path/to/second')
    output = config('get', 'mirrors')

    assert output == """mirrors:
  first: /path/to/first
  second: /path/to/second
"""


def test_config_add_invalid_fails(mutable_empty_config):
    config('add', 'packages:all:variants:+debug')
    with pytest.raises(
        (spack.config.ConfigFormatError, AttributeError)
    ):
        config('add', 'packages:all:True')


def test_config_add_from_file(mutable_empty_config, tmpdir):
    contents = """spack:
  config:
    dirty: true
"""

    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)
    config('add', '-f', file)
    output = config('get', 'config')

    assert output == """config:
  dirty: true
"""


def test_config_add_from_file_multiple(mutable_empty_config, tmpdir):
    contents = """spack:
  config:
    dirty: true
    template_dirs: [test1]
"""

    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)
    config('add', '-f', file)
    output = config('get', 'config')

    assert output == """config:
  dirty: true
  template_dirs: [test1]
"""


def test_config_add_override_from_file(mutable_empty_config, tmpdir):
    config('--scope', 'site', 'add', 'config:template_dirs:test1')
    contents = """spack:
  config::
    template_dirs: [test2]
"""

    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)
    config('add', '-f', file)
    output = config('get', 'config')

    assert output == """config:
  template_dirs: [test2]
"""


def test_config_add_override_leaf_from_file(mutable_empty_config, tmpdir):
    config('--scope', 'site', 'add', 'config:template_dirs:test1')
    contents = """spack:
  config:
    template_dirs:: [test2]
"""

    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)
    config('add', '-f', file)
    output = config('get', 'config')

    assert output == """config:
  'template_dirs:': [test2]
"""


def test_config_add_update_dict_from_file(mutable_empty_config, tmpdir):
    config('add', 'packages:all:compiler:[gcc]')

    # contents to add to file
    contents = """spack:
  packages:
    all:
      version:
      - 1.0.0
"""

    # create temp file and add it to config
    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)
    config('add', '-f', file)

    # get results
    output = config('get', 'packages')

    expected = """packages:
  all:
    compiler: [gcc]
    version:
    - 1.0.0
"""

    assert output == expected


def test_config_add_invalid_file_fails(tmpdir):
    # contents to add to file
    # invalid because version requires a list
    contents = """spack:
  packages:
    all:
      version: 1.0.0
"""

    # create temp file and add it to config
    file = str(tmpdir.join('spack.yaml'))
    with open(file, 'w') as f:
        f.write(contents)

    with pytest.raises(
        (spack.config.ConfigFormatError)
    ):
        config('add', '-f', file)


def test_config_remove_value(mutable_empty_config):
    config('add', 'config:dirty:true')
    config('remove', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_config_remove_alias_rm(mutable_empty_config):
    config('add', 'config:dirty:true')
    config('rm', 'config:dirty:true')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_config_remove_dict(mutable_empty_config):
    config('add', 'config:dirty:true')
    config('rm', 'config:dirty')
    output = config('get', 'config')

    assert output == """config: {}
"""


def test_remove_from_list(mutable_empty_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    config('remove', 'config:template_dirs:test2')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test3
  - test1
"""


def test_remove_list(mutable_empty_config):
    config('add', 'config:template_dirs:test1')
    config('add', 'config:template_dirs:[test2]')
    config('add', 'config:template_dirs:test3')
    config('remove', 'config:template_dirs:[test2]')
    output = config('get', 'config')

    assert output == """config:
  template_dirs:
  - test3
  - test1
"""


def test_config_add_to_env(mutable_empty_config, mutable_mock_env_path):
    env = ev.create('test')
    with env:
        config('add', 'config:dirty:true')
        output = config('get')

    expected = ev.default_manifest_yaml
    expected += """  config:
    dirty: true

"""
    assert output == expected


def test_config_remove_from_env(mutable_empty_config, mutable_mock_env_path):
    env('create', 'test')

    with ev.read('test'):
        config('add', 'config:dirty:true')

    with ev.read('test'):
        config('rm', 'config:dirty')
        output = config('get')

    expected = ev.default_manifest_yaml
    expected += """  config: {}

"""
    assert output == expected


def test_config_update_packages(packages_yaml_v015):
    """Test Spack updating old packages.yaml format for externals
    to new format. Ensure that data is preserved and converted
    properly.
    """
    packages_yaml_v015()
    config('update', '-y', 'packages')

    # Check the entries have been transformed
    data = spack.config.get('packages')
    check_update(data)


def test_config_update_not_needed(mutable_config):
    data_before = spack.config.get('repos')
    config('update', '-y', 'repos')
    data_after = spack.config.get('repos')
    assert data_before == data_after


def test_config_update_fail_on_permission_issue(
        packages_yaml_v015, monkeypatch
):
    # The first time it will update and create the backup file
    packages_yaml_v015()
    # Mock a global scope where we cannot write
    monkeypatch.setattr(
        spack.cmd.config, '_can_update_config_file', lambda x, y: False
    )
    with pytest.raises(spack.main.SpackCommandError):
        config('update', '-y', 'packages')


def test_config_revert(packages_yaml_v015):
    cfg_file = packages_yaml_v015()
    bkp_file = cfg_file + '.bkp'

    config('update', '-y', 'packages')

    # Check that the backup file exists, compute its md5 sum
    assert os.path.exists(bkp_file)
    md5bkp = fs.md5sum(bkp_file)

    config('revert', '-y', 'packages')

    # Check that the backup file does not exist anymore and
    # that the md5 sum of the configuration file is the same
    # as that of the old backup file
    assert not os.path.exists(bkp_file)
    assert md5bkp == fs.md5sum(cfg_file)


def test_config_revert_raise_if_cant_write(packages_yaml_v015, monkeypatch):
    packages_yaml_v015()
    config('update', '-y', 'packages')

    # Mock a global scope where we cannot write
    monkeypatch.setattr(
        spack.cmd.config, '_can_revert_update', lambda x, y, z: False
    )
    # The command raises with an helpful error if a configuration
    # file is to be deleted and we don't have sufficient permissions
    with pytest.raises(spack.main.SpackCommandError):
        config('revert', '-y', 'packages')


def test_updating_config_implicitly_raises(packages_yaml_v015):
    # Trying to write implicitly to a scope with a configuration file
    # in the old format raises an exception
    packages_yaml_v015()
    with pytest.raises(RuntimeError):
        config('add', 'packages:cmake:buildable:false')


def test_updating_multiple_scopes_at_once(packages_yaml_v015):
    # Create 2 config files in the old format
    packages_yaml_v015(scope='user')
    packages_yaml_v015(scope='site')

    # Update both of them at once
    config('update', '-y', 'packages')

    for scope in ('user', 'site'):
        data = spack.config.get('packages', scope=scope)
        check_update(data)


@pytest.mark.regression('18031')
def test_config_update_can_handle_comments(mutable_config):
    # Create an outdated config file with comments
    scope = spack.config.default_modify_scope()
    cfg_file = spack.config.config.get_config_filename(scope, 'packages')
    with open(cfg_file, mode='w') as f:
        f.write("""
packages:
  # system cmake in /usr
  cmake:
    paths:
      cmake@3.14.0:  /usr
    # Another comment after the outdated section
    buildable: False
""")

    # Try to update it, it should not raise errors
    config('update', '-y', 'packages')

    # Check data
    data = spack.config.get('packages', scope=scope)
    assert 'paths' not in data['cmake']
    assert 'externals' in data['cmake']
    externals = data['cmake']['externals']
    assert len(externals) == 1
    assert externals[0]['spec'] == 'cmake@3.14.0'
    assert externals[0]['prefix'] == '/usr'

    # Check the comment is there
    with open(cfg_file) as f:
        text = ''.join(f.readlines())

    assert '# system cmake in /usr' in text
    assert '# Another comment after the outdated section' in text


@pytest.mark.regression('18050')
def test_config_update_works_for_empty_paths(mutable_config):
    # Create an outdated config file with empty "paths" and "modules"
    scope = spack.config.default_modify_scope()
    cfg_file = spack.config.config.get_config_filename(scope, 'packages')
    with open(cfg_file, mode='w') as f:
        f.write("""
packages:
  cmake:
    paths: {}
    modules: {}
    buildable: False
""")

    # Try to update it, it should not raise errors
    output = config('update', '-y', 'packages')

    # This ensures that we updated the configuration
    assert '[backup=' in output


def check_update(data):
    """Check that the data from the packages_yaml_v015
    has been updated.
    """
    assert 'externals' in data['cmake']
    externals = data['cmake']['externals']
    assert {'spec': 'cmake@3.14.0', 'prefix': '/usr'} in externals
    assert 'paths' not in data['cmake']
    assert 'externals' in data['gcc']
    externals = data['gcc']['externals']
    assert {'spec': 'gcc@8.3.0', 'modules': ['gcc-8']} in externals
    assert 'modules' not in data['gcc']

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import sys

import pytest

import spack
import spack.detection
import spack.detection.path
from spack.main import SpackCommand
from spack.spec import Spec

is_windows = sys.platform == 'win32'


@pytest.fixture
def executables_found(monkeypatch):
    def _factory(result):
        def _mock_search(path_hints=None):
            return result

        monkeypatch.setattr(spack.detection.path, 'executables_in_path', _mock_search)
    return _factory


@pytest.fixture
def _platform_executables(monkeypatch):
    def _win_exe_ext():
        return '.bat'

    monkeypatch.setattr(spack.package, 'win_exe_ext', _win_exe_ext)


def define_plat_exe(exe):
    if is_windows:
        exe += '.bat'
    return exe


def test_find_external_single_package(mock_executable, executables_found,
                                      _platform_executables):
    pkgs_to_check = [spack.repo.get('cmake')]
    executables_found({
        mock_executable("cmake", output='echo cmake version 1.foo'):
            define_plat_exe('cmake')
    })

    pkg_to_entries = spack.detection.by_executable(pkgs_to_check)

    pkg, entries = next(iter(pkg_to_entries.items()))
    single_entry = next(iter(entries))

    assert single_entry.spec == Spec('cmake@1.foo')


def test_find_external_two_instances_same_package(mock_executable, executables_found,
                                                  _platform_executables):
    pkgs_to_check = [spack.repo.get('cmake')]

    # Each of these cmake instances is created in a different prefix
    # In Windows, quoted strings are echo'd with quotes includes
    # we need to avoid that for proper regex.
    cmake_path1 = mock_executable(
        "cmake", output='echo cmake version 1.foo', subdir=('base1', 'bin')
    )
    cmake_path2 = mock_executable(
        "cmake", output='echo cmake version 3.17.2', subdir=('base2', 'bin')
    )
    cmake_exe = define_plat_exe('cmake')
    executables_found({
        cmake_path1: cmake_exe,
        cmake_path2: cmake_exe
    })

    pkg_to_entries = spack.detection.by_executable(pkgs_to_check)

    pkg, entries = next(iter(pkg_to_entries.items()))
    spec_to_path = dict((e.spec, e.prefix) for e in entries)
    assert spec_to_path[Spec('cmake@1.foo')] == (
        spack.detection.executable_prefix(os.path.dirname(cmake_path1)))
    assert spec_to_path[Spec('cmake@3.17.2')] == (
        spack.detection.executable_prefix(os.path.dirname(cmake_path2)))


def pkgconfig_do_detection(pkgs_to_check):
    spack.detection.by_pkgconfig(pkgs_to_check)
    pkgs_to_entries = spack.detection.by_pkgconfig(pkgs_to_check)
    return pkgs_to_entries


def test_pkgconfig_executible_not_found(monkeypatch, mock_pkgconfig):
    pkgs_to_check = [spack.repo.get('zlib')]
    pkgfile = mock_pkgconfig(name='zlib', pkgcfg={'version': '1.2.11',
                                                  'prefix': '/x/y1'})
    monkeypatch.delenv('PKG_CONFIG', raising=False)
    monkeypatch.setenv('PATH', ':')
    if pkgfile is not None:
        monkeypatch.setenv('PKG_CONFIG_LIBDIR', os.path.dirname(pkgfile))

    pkgs_to_entries = pkgconfig_do_detection(pkgs_to_check)
    assert 'zlib' not in pkgs_to_entries.keys()


def test_pkgconfig_module_not_found(monkeypatch, mock_pkgconfig):
    pkgs_to_check = [spack.repo.get('zlib')]
    pkgfile = mock_pkgconfig(name='zlib', pkgcfg={'version': '1.2.11',
                                                  'prefix': '/x/y1'})

    def _mock_list_all(path_hints=None):
        return []

    monkeypatch.setattr(spack.detection.path.pkgconfig, 'list_all', _mock_list_all)

    if pkgfile is not None:
        monkeypatch.setenv('PKG_CONFIG_LIBDIR', os.path.dirname(pkgfile))

    pkgs_to_entries = pkgconfig_do_detection(pkgs_to_check)

    assert 'zlib' not in pkgs_to_entries.keys()


def test_find_path_by_pkgconfig(monkeypatch, mock_pkgconfig, capsys):
    pkgs_to_check = [spack.repo.get('zlib'), spack.repo.get('lzma'),
                     spack.repo.get('libpciaccess'), spack.repo.get('libxml2'),
                     spack.repo.get('bzip2'), spack.repo.get('hwloc'),
                     spack.repo.get('cmake')]
    # repo name and pkgconfig name match
    pkgfile = mock_pkgconfig(name='zlib', pkgcfg={'version': '1.2.11',
                                                  'prefix': '/x/y1'})
    # repo name has no 'lib', pkgconfig does
    mock_pkgconfig(name='liblzma', pkgcfg={'version': '5.2.3',
                                           'prefix': '/x/y2'})
    # repo name has 'lib' prepended, pkgconfig does
    mock_pkgconfig(name='pciaccess', pkgcfg={'version': '0.14',
                                             'prefix': '/x/y3'})
    # libxml2 pkgconfig file has a different name specified in package
    mock_pkgconfig(name='libxml-2.0', pkgcfg={'version': '2.0.1',
                                              'prefix': '/x/y4'})
    # no prefix in pkgconfig file: error -> not to be considered
    mock_pkgconfig(name='bzip2', pkgcfg={'version': '1.0.5',
                                         'execprefix': '/x/y5'})
    # invalid character '@' in version: error -> not to be considered
    mock_pkgconfig(name='hwloc', pkgcfg={'version': '2.4@0',
                                         'prefix': '/x/y6'})
    # explicitly fail validation by mocking a validation function
    mock_pkgconfig(name='cmake', pkgcfg={'version': '3.17.0',
                                         'prefix': '/x/y7'})
    errmsg = 'DEAD_BEEF'

    def _detected_spec(*args):
        assert False, errmsg

    monkeypatch.setattr(spack.pkg.builtin.cmake.Cmake,
                        'validate_detected_spec', _detected_spec, raising=False)

    if pkgfile is not None:
        monkeypatch.setenv('PKG_CONFIG_LIBDIR', os.path.dirname(pkgfile))

    pkgs_to_entries = pkgconfig_do_detection(pkgs_to_check)
    captured = capsys.readouterr()

    assert pkgs_to_entries['zlib'][0].spec == Spec('zlib@1.2.11')
    assert pkgs_to_entries['lzma'][0].spec == Spec('lzma@5.2.3')
    assert pkgs_to_entries['libpciaccess'][0].spec == Spec('libpciaccess@0.14')
    assert pkgs_to_entries['libxml2'][0].spec == Spec('libxml2@2.0.1')
    assert pkgs_to_entries['zlib'][0].prefix == '/x/y1'
    assert pkgs_to_entries['lzma'][0].prefix == '/x/y2'
    assert pkgs_to_entries['libpciaccess'][0].prefix == '/x/y3'
    assert pkgs_to_entries['libxml2'][0].prefix == '/x/y4'
    assert 'bzip2' not in pkgs_to_entries.keys()
    assert 'hwloc' not in pkgs_to_entries.keys()
    assert 'cmake' not in pkgs_to_entries.keys()
    assert errmsg in captured[1]


def test_find_external_update_config(mutable_config):
    entries = [
        spack.detection.DetectedPackage(Spec.from_detection('cmake@1.foo'), '/x/y1/'),
        spack.detection.DetectedPackage(Spec.from_detection('cmake@3.17.2'), '/x/y2/'),
    ]
    pkg_to_entries = {'cmake': entries}

    scope = spack.config.default_modify_scope('packages')
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_externals = cmake_cfg['externals']

    assert {'spec': 'cmake@1.foo', 'prefix': '/x/y1/'} in cmake_externals
    assert {'spec': 'cmake@3.17.2', 'prefix': '/x/y2/'} in cmake_externals


def test_get_executables(working_env, mock_executable):
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")

    os.environ['PATH'] = os.pathsep.join([os.path.dirname(cmake_path1)])
    path_to_exe = spack.detection.executables_in_path()
    cmake_exe = define_plat_exe('cmake')
    assert path_to_exe[cmake_path1] == cmake_exe


external = SpackCommand('external')


def test_find_external_cmd(mutable_config, working_env, mock_executable,
                           _platform_executables):
    """Test invoking 'spack external find' with additional package arguments,
    which restricts the set of packages that Spack looks for.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    prefix = os.path.dirname(os.path.dirname(cmake_path1))

    os.environ['PATH'] = os.pathsep.join([os.path.dirname(cmake_path1)])
    external('find', 'cmake')

    pkgs_cfg = spack.config.get('packages')
    cmake_cfg = pkgs_cfg['cmake']
    cmake_externals = cmake_cfg['externals']

    assert {'spec': 'cmake@1.foo', 'prefix': prefix} in cmake_externals


def test_find_external_cmd_pkgconfig(monkeypatch, mutable_config, working_env,
                                     mock_pkgconfig, executables_found):
    """Test invoking 'spack external find' with additional package arguments
    on packages for which pkg_config information, which restricts the set of
    packages that Spack looks for.
    """
    executables_found({})
    pkgfile = mock_pkgconfig(name='zlib', pkgcfg={'version': '1.2.10',
                                                  'prefix': '/x/y1'})
    mock_pkgconfig(name='liblzma', pkgcfg={'version': '5.2.3',
                                           'prefix': '/x/y2'})
    mock_pkgconfig(name='pciaccess', pkgcfg={'version': '0.14',
                                             'prefix': '/x/y3'})
    mock_pkgconfig(name='libxml-2.0', pkgcfg={'version': '2.0.1',
                                              'prefix': '/x/y4'})

    if pkgfile is not None:
        monkeypatch.setenv('PKG_CONFIG_LIBDIR', os.path.dirname(pkgfile))

    external('find', 'zlib', 'lzma', 'libpciaccess', 'libxml2')

    pkgs_cfg = spack.config.get('packages')
    assert {'spec': 'zlib@1.2.10', 'prefix': '/x/y1'} \
        in pkgs_cfg['zlib']['externals']
    assert {'spec': 'lzma@5.2.3', 'prefix': '/x/y2'} \
        in pkgs_cfg['lzma']['externals']
    assert {'spec': 'libpciaccess@0.14', 'prefix': '/x/y3'} \
        in pkgs_cfg['libpciaccess']['externals']
    assert {'spec': 'libxml2@2.0.1', 'prefix': '/x/y4'} \
        in pkgs_cfg['libxml2']['externals']


def test_find_external_cmd_not_buildable(
        mutable_config, working_env, mock_executable):
    """When the user invokes 'spack external find --not-buildable', the config
    for any package where Spack finds an external version should be marked as
    not buildable.
    """
    cmake_path1 = mock_executable("cmake", output="echo cmake version 1.foo")
    os.environ['PATH'] = os.pathsep.join([os.path.dirname(cmake_path1)])
    external('find', '--not-buildable', 'cmake')
    pkgs_cfg = spack.config.get('packages')
    assert not pkgs_cfg['cmake']['buildable']


def test_find_external_cmd_full_repo(
        mutable_config, working_env, mock_executable, mutable_mock_repo,
        _platform_executables):
    """Test invoking 'spack external find' with no additional arguments, which
    iterates through each package in the repository.
    """
    exe_path1 = mock_executable(
        "find-externals1-exe", output="echo find-externals1 version 1.foo"
    )
    prefix = os.path.dirname(os.path.dirname(exe_path1))
    os.environ['PATH'] = os.pathsep.join([os.path.dirname(exe_path1)])
    external('find', '--all')

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_externals = pkg_cfg['externals']

    assert {'spec': 'find-externals1@1.foo', 'prefix': prefix} in pkg_externals


def test_find_external_merge(mutable_config, mutable_mock_repo):
    """Check that 'spack find external' doesn't overwrite an existing spec
    entry in packages.yaml.
    """
    pkgs_cfg_init = {
        'find-externals1': {
            'externals': [{
                'spec': 'find-externals1@1.1',
                'prefix': '/preexisting-prefix/'
            }],
            'buildable': False
        }
    }

    mutable_config.update_config('packages', pkgs_cfg_init)
    entries = [
        spack.detection.DetectedPackage(
            Spec.from_detection('find-externals1@1.1'), '/x/y1/'
        ),
        spack.detection.DetectedPackage(
            Spec.from_detection('find-externals1@1.2'), '/x/y2/'
        )
    ]
    pkg_to_entries = {'find-externals1': entries}
    scope = spack.config.default_modify_scope('packages')
    spack.detection.update_configuration(pkg_to_entries, scope=scope, buildable=True)

    pkgs_cfg = spack.config.get('packages')
    pkg_cfg = pkgs_cfg['find-externals1']
    pkg_externals = pkg_cfg['externals']

    assert {'spec': 'find-externals1@1.1',
            'prefix': '/preexisting-prefix/'} in pkg_externals
    assert {'spec': 'find-externals1@1.2',
            'prefix': '/x/y2/'} in pkg_externals


def test_list_detectable_packages(mutable_config, mutable_mock_repo):
    external("list")
    assert external.returncode == 0


def test_packages_yaml_format(
        mock_executable, mutable_config, monkeypatch, _platform_executables):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    # Find the external spec
    external('find', 'gcc')

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get('packages')
    assert 'gcc' in packages_yaml
    assert 'externals' in packages_yaml['gcc']
    externals = packages_yaml['gcc']['externals']
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc['spec'] == 'gcc@4.2.1 languages=c'
    assert external_gcc['prefix'] == os.path.dirname(prefix)
    assert 'extra_attributes' in external_gcc
    extra_attributes = external_gcc['extra_attributes']
    assert 'prefix' not in extra_attributes
    assert extra_attributes['compilers']['c'] == gcc_exe


def test_overriding_prefix(
        mock_executable, mutable_config, monkeypatch, _platform_executables):
    # Prepare an environment to detect a fake gcc that
    # override its external prefix
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    @classmethod
    def _determine_variants(cls, exes, version_str):
        return 'languages=c', {
            'prefix': '/opt/gcc/bin',
            'compilers': {'c': exes[0]}
        }

    gcc_cls = spack.repo.path.get_pkg_class('gcc')
    monkeypatch.setattr(gcc_cls, 'determine_variants', _determine_variants)

    # Find the external spec
    external('find', 'gcc')

    # Check entries in 'packages.yaml'
    packages_yaml = spack.config.get('packages')
    assert 'gcc' in packages_yaml
    assert 'externals' in packages_yaml['gcc']
    externals = packages_yaml['gcc']['externals']
    assert len(externals) == 1
    assert externals[0]['prefix'] == '/opt/gcc/bin'


def test_new_entries_are_reported_correctly(
        mock_executable, mutable_config, monkeypatch, _platform_executables
):
    # Prepare an environment to detect a fake gcc
    gcc_exe = mock_executable('gcc', output="echo 4.2.1")
    prefix = os.path.dirname(gcc_exe)
    monkeypatch.setenv('PATH', prefix)

    # The first run will find and add the external gcc
    output = external('find', 'gcc')
    assert 'The following specs have been' in output

    # The second run should report that no new external
    # has been found
    output = external('find', 'gcc')
    assert 'No new external packages detected' in output


@pytest.mark.parametrize('command_args', [
    ('-t', 'build-tools'),
    ('-t', 'build-tools', 'cmake'),
])
def test_use_tags_for_detection(
        command_args, mock_executable, mutable_config, monkeypatch
):
    # Prepare an environment to detect a fake cmake
    cmake_exe = mock_executable('cmake', output="echo cmake version 3.19.1")
    prefix = os.path.dirname(cmake_exe)
    monkeypatch.setenv('PATH', prefix)

    openssl_exe = mock_executable('openssl', output="OpenSSL 2.8.3")
    prefix = os.path.dirname(openssl_exe)
    monkeypatch.setenv('PATH', prefix)

    # Test that we detect specs
    output = external('find', *command_args)
    assert 'The following specs have been' in output
    assert 'cmake' in output
    assert 'openssl' not in output

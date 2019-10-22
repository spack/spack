# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest

import spack.build_environment
import spack.spec
from spack.paths import build_env_path
from spack.build_environment import dso_suffix, _static_to_shared_library
from spack.util.executable import Executable
from spack.util.spack_yaml import syaml_dict, syaml_str
from spack.util.environment import EnvironmentModifications

from llnl.util.filesystem import LibraryList


@pytest.fixture
def build_environment(working_env):
    cc = Executable(os.path.join(build_env_path, "cc"))
    cxx = Executable(os.path.join(build_env_path, "c++"))
    fc = Executable(os.path.join(build_env_path, "fc"))

    realcc = "/bin/mycc"
    prefix = "/spack-test-prefix"

    os.environ['SPACK_CC'] = realcc
    os.environ['SPACK_CXX'] = realcc
    os.environ['SPACK_FC'] = realcc

    os.environ['SPACK_PREFIX'] = prefix
    os.environ['SPACK_ENV_PATH'] = "test"
    os.environ['SPACK_DEBUG_LOG_DIR'] = "."
    os.environ['SPACK_DEBUG_LOG_ID'] = "foo-hashabc"
    os.environ['SPACK_COMPILER_SPEC'] = "gcc@4.4.7"
    os.environ['SPACK_SHORT_SPEC'] = (
        "foo@1.2 arch=linux-rhel6-x86_64 /hashabc")

    os.environ['SPACK_CC_RPATH_ARG']  = "-Wl,-rpath,"
    os.environ['SPACK_CXX_RPATH_ARG'] = "-Wl,-rpath,"
    os.environ['SPACK_F77_RPATH_ARG'] = "-Wl,-rpath,"
    os.environ['SPACK_FC_RPATH_ARG']  = "-Wl,-rpath,"
    os.environ['SPACK_SYSTEM_DIRS'] = '/usr/include /usr/lib'
    os.environ['SPACK_TARGET_ARGS'] = ''

    if 'SPACK_DEPENDENCIES' in os.environ:
        del os.environ['SPACK_DEPENDENCIES']

    yield {'cc': cc, 'cxx': cxx, 'fc': fc}

    for name in ('SPACK_CC', 'SPACK_CXX', 'SPACK_FC', 'SPACK_PREFIX',
                 'SPACK_ENV_PATH', 'SPACK_DEBUG_LOG_DIR',
                 'SPACK_COMPILER_SPEC', 'SPACK_SHORT_SPEC',
                 'SPACK_CC_RPATH_ARG', 'SPACK_CXX_RPATH_ARG',
                 'SPACK_F77_RPATH_ARG', 'SPACK_FC_RPATH_ARG',
                 'SPACK_TARGET_ARGS'):
        del os.environ[name]


def test_static_to_shared_library(build_environment):
    os.environ['SPACK_TEST_COMMAND'] = 'dump-args'

    expected = {
        'linux': ('/bin/mycc -shared'
                  ' -Wl,-soname,{2} -Wl,--whole-archive {0}'
                  ' -Wl,--no-whole-archive -o {1}'),
        'darwin': ('/bin/mycc -dynamiclib'
                   ' -install_name {1} -Wl,-force_load,{0} -o {1}')
    }

    static_lib = '/spack/libfoo.a'

    for arch in ('linux', 'darwin'):
        for shared_lib in (None, '/spack/libbar.so'):
            output = _static_to_shared_library(arch, build_environment['cc'],
                                               static_lib, shared_lib,
                                               compiler_output=str).strip()

            if not shared_lib:
                shared_lib = '{0}.{1}'.format(
                    os.path.splitext(static_lib)[0], dso_suffix)

            assert set(output.split()) == set(expected[arch].format(
                static_lib, shared_lib, os.path.basename(shared_lib)).split())


@pytest.mark.regression('8345')
@pytest.mark.usefixtures('config', 'mock_packages')
def test_cc_not_changed_by_modules(monkeypatch, working_env):

    s = spack.spec.Spec('cmake')
    s.concretize()
    pkg = s.package

    def _set_wrong_cc(x):
        os.environ['CC'] = 'NOT_THIS_PLEASE'
        os.environ['ANOTHER_VAR'] = 'THIS_IS_SET'

    monkeypatch.setattr(
        spack.build_environment, 'load_module', _set_wrong_cc
    )
    monkeypatch.setattr(
        pkg.compiler, 'modules', ['some_module']
    )

    spack.build_environment.setup_package(pkg, False)

    assert os.environ['CC'] != 'NOT_THIS_PLEASE'
    assert os.environ['ANOTHER_VAR'] == 'THIS_IS_SET'


@pytest.mark.usefixtures('config', 'mock_packages')
def test_compiler_config_modifications(monkeypatch, working_env):
    s = spack.spec.Spec('cmake')
    s.concretize()
    pkg = s.package

    os.environ['SOME_VAR_STR'] = ''
    os.environ['SOME_VAR_NUM'] = '0'
    os.environ['PATH_LIST'] = '/path/third:/path/forth'
    os.environ['EMPTY_PATH_LIST'] = ''
    os.environ.pop('NEW_PATH_LIST', None)

    env_mod = syaml_dict()
    set_cmd = syaml_dict()
    env_mod[syaml_str('set')] = set_cmd

    set_cmd[syaml_str('SOME_VAR_STR')] = syaml_str('SOME_STR')
    set_cmd[syaml_str('SOME_VAR_NUM')] = 1

    monkeypatch.setattr(pkg.compiler, 'environment', env_mod)
    spack.build_environment.setup_package(pkg, False)
    assert os.environ['SOME_VAR_STR'] == 'SOME_STR'
    assert os.environ['SOME_VAR_NUM'] == str(1)

    env_mod = syaml_dict()
    unset_cmd = syaml_dict()
    env_mod[syaml_str('unset')] = unset_cmd

    unset_cmd[syaml_str('SOME_VAR_STR')] = None

    monkeypatch.setattr(pkg.compiler, 'environment', env_mod)
    assert 'SOME_VAR_STR' in os.environ
    spack.build_environment.setup_package(pkg, False)
    assert 'SOME_VAR_STR' not in os.environ

    env_mod = syaml_dict()
    set_cmd = syaml_dict()
    env_mod[syaml_str('set')] = set_cmd
    append_cmd = syaml_dict()
    env_mod[syaml_str('append-path')] = append_cmd
    unset_cmd = syaml_dict()
    env_mod[syaml_str('unset')] = unset_cmd
    prepend_cmd = syaml_dict()
    env_mod[syaml_str('prepend-path')] = prepend_cmd

    set_cmd[syaml_str('EMPTY_PATH_LIST')] = syaml_str('/path/middle')

    append_cmd[syaml_str('PATH_LIST')] = syaml_str('/path/last')
    append_cmd[syaml_str('EMPTY_PATH_LIST')] = syaml_str('/path/last')
    append_cmd[syaml_str('NEW_PATH_LIST')] = syaml_str('/path/last')

    unset_cmd[syaml_str('SOME_VAR_NUM')] = None

    prepend_cmd[syaml_str('PATH_LIST')] = syaml_str('/path/first:/path/second')
    prepend_cmd[syaml_str('EMPTY_PATH_LIST')] = syaml_str('/path/first')
    prepend_cmd[syaml_str('NEW_PATH_LIST')] = syaml_str('/path/first')
    prepend_cmd[syaml_str('SOME_VAR_NUM')] = syaml_str('/8')

    assert 'SOME_VAR_NUM' in os.environ
    monkeypatch.setattr(pkg.compiler, 'environment', env_mod)
    spack.build_environment.setup_package(pkg, False)
    # Check that the order of modifications is respected and the
    # variable was unset before it was prepended.
    assert os.environ['SOME_VAR_NUM'] == '/8'

    expected = '/path/first:/path/second:/path/third:/path/forth:/path/last'
    assert os.environ['PATH_LIST'] == expected

    expected = '/path/first:/path/middle:/path/last'
    assert os.environ['EMPTY_PATH_LIST'] == expected

    expected = '/path/first:/path/last'
    assert os.environ['NEW_PATH_LIST'] == expected


@pytest.mark.regression('9107')
def test_spack_paths_before_module_paths(
        config, mock_packages, monkeypatch, working_env):
    s = spack.spec.Spec('cmake')
    s.concretize()
    pkg = s.package

    module_path = '/path/to/module'

    def _set_wrong_cc(x):
        os.environ['PATH'] = module_path + ':' + os.environ['PATH']

    monkeypatch.setattr(
        spack.build_environment, 'load_module', _set_wrong_cc
    )
    monkeypatch.setattr(
        pkg.compiler, 'modules', ['some_module']
    )

    spack.build_environment.setup_package(pkg, False)

    spack_path = os.path.join(spack.paths.prefix, 'lib/spack/env')
    paths = os.environ['PATH'].split(':')

    assert paths.index(spack_path) < paths.index(module_path)


def test_package_inheritance_module_setup(config, mock_packages, working_env):
    s = spack.spec.Spec('multimodule-inheritance')
    s.concretize()
    pkg = s.package

    spack.build_environment.setup_package(pkg, False)

    os.environ['TEST_MODULE_VAR'] = 'failed'

    assert pkg.use_module_variable() == 'test_module_variable'
    assert os.environ['TEST_MODULE_VAR'] == 'test_module_variable'


def test_set_build_environment_variables(
        config, mock_packages, working_env, monkeypatch,
        installation_dir_with_headers
):
    """Check that build_environment supplies the needed library/include
    directories via the SPACK_LINK_DIRS and SPACK_INCLUDE_DIRS environment
    variables.
    """

    root = spack.spec.Spec('dt-diamond')
    root.concretize()

    for s in root.traverse():
        s.prefix = '/{0}-prefix/'.format(s.name)

    dep_pkg = root['dt-diamond-left'].package
    dep_lib_paths = ['/test/path/to/ex1.so', '/test/path/to/subdir/ex2.so']
    dep_lib_dirs = ['/test/path/to', '/test/path/to/subdir']
    dep_libs = LibraryList(dep_lib_paths)

    dep2_pkg = root['dt-diamond-right'].package
    dep2_pkg.spec.prefix = str(installation_dir_with_headers)

    setattr(dep_pkg, 'libs', dep_libs)
    try:
        pkg = root.package
        env_mods = EnvironmentModifications()
        spack.build_environment.set_build_environment_variables(
            pkg, env_mods, dirty=False)

        env_mods.apply_modifications()

        def normpaths(paths):
            return list(os.path.normpath(p) for p in paths)

        link_dir_var = os.environ['SPACK_LINK_DIRS']
        assert (
            normpaths(link_dir_var.split(':')) == normpaths(dep_lib_dirs))

        root_libdirs = ['/dt-diamond-prefix/lib', '/dt-diamond-prefix/lib64']
        rpath_dir_var = os.environ['SPACK_RPATH_DIRS']
        # The 'lib' and 'lib64' subdirectories of the root package prefix
        # should always be rpathed and should be the first rpaths
        assert (
            normpaths(rpath_dir_var.split(':')) ==
            normpaths(root_libdirs + dep_lib_dirs))

        header_dir_var = os.environ['SPACK_INCLUDE_DIRS']

        # The default implementation looks for header files only
        # in <prefix>/include and subdirectories
        prefix = str(installation_dir_with_headers)
        include_dirs = normpaths(header_dir_var.split(':'))

        assert os.path.join(prefix, 'include') in include_dirs
        assert os.path.join(prefix, 'include', 'boost') not in include_dirs
        assert os.path.join(prefix, 'path', 'to') not in include_dirs
        assert os.path.join(prefix, 'path', 'to', 'subdir') not in include_dirs

    finally:
        delattr(dep_pkg, 'libs')


def test_parallel_false_is_not_propagating(config, mock_packages):
    class AttributeHolder(object):
        pass

    # Package A has parallel = False and depends on B which instead
    # can be built in parallel
    s = spack.spec.Spec('a foobar=bar')
    s.concretize()

    for spec in s.traverse():
        expected_jobs = spack.config.get('config:build_jobs') \
            if s.package.parallel else 1
        m = AttributeHolder()
        spack.build_environment._set_variables_for_single_module(s.package, m)
        assert m.make_jobs == expected_jobs

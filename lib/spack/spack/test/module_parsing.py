# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import os
import spack

from spack.util.module_cmd import (
    module,
    get_path_from_module,
    get_path_args_from_module_line,
    get_path_from_module_contents
)

test_module_lines = ['prepend-path LD_LIBRARY_PATH /path/to/lib',
                     'setenv MOD_DIR /path/to',
                     'setenv LDFLAGS -Wl,-rpath/path/to/lib',
                     'setenv LDFLAGS -L/path/to/lib',
                     'prepend-path PATH /path/to/bin']


@pytest.fixture
def module_function_test_mode():
    old_mode = spack.util.module_cmd._test_mode
    spack.util.module_cmd._test_mode = True

    yield

    spack.util.module_cmd._test_mode = old_mode


@pytest.fixture
def save_module_func():
    old_func = spack.util.module_cmd.module

    yield

    spack.util.module_cmd.module = old_func


def test_module_function_change_env(tmpdir, working_env,
                                    module_function_test_mode):
    src_file = str(tmpdir.join('src_me'))
    with open(src_file, 'w') as f:
        f.write('export TEST_MODULE_ENV_VAR=TEST_SUCCESS\n')

    os.environ['NOT_AFFECTED'] = "NOT_AFFECTED"
    module('load', src_file)

    assert os.environ['TEST_MODULE_ENV_VAR'] == 'TEST_SUCCESS'
    assert os.environ['NOT_AFFECTED'] == "NOT_AFFECTED"


def test_module_function_no_change(tmpdir, module_function_test_mode):
    src_file = str(tmpdir.join('src_me'))
    with open(src_file, 'w') as f:
        f.write('echo TEST_MODULE_FUNCTION_PRINT')

    old_env = os.environ.copy()
    text = module('show', src_file)

    assert text == 'TEST_MODULE_FUNCTION_PRINT\n'
    assert os.environ == old_env


def test_get_path_from_module_faked(save_module_func):
    for line in test_module_lines:
        def fake_module(*args):
            return line
        spack.util.module_cmd.module = fake_module

        path = get_path_from_module('mod')
        assert path == '/path/to'


def test_get_path_from_module_contents():
    # A line with "MODULEPATH" appears early on, and the test confirms that it
    # is not extracted as the package's path
    module_show_output = """
os.environ["MODULEPATH"] = "/path/to/modules1:/path/to/modules2";
----------------------------------------------------------------------------
   /root/cmake/3.9.2.lua:
----------------------------------------------------------------------------
help([[CMake Version 3.9.2
]])
whatis("Name: CMake")
whatis("Version: 3.9.2")
whatis("Category: Tools")
whatis("URL: https://cmake.org/")
prepend_path("LD_LIBRARY_PATH","/bad/path")
prepend_path("PATH","/path/to/cmake-3.9.2/bin:/other/bad/path")
prepend_path("MANPATH","/path/to/cmake/cmake-3.9.2/share/man")
prepend_path("LD_LIBRARY_PATH","/path/to/cmake-3.9.2/lib64")
"""
    module_show_lines = module_show_output.split('\n')

    # PATH and LD_LIBRARY_PATH outvote MANPATH and the other PATH and
    # LD_LIBRARY_PATH entries
    assert (get_path_from_module_contents(module_show_lines, 'cmake-3.9.2') ==
            '/path/to/cmake-3.9.2')


def test_get_path_from_empty_module():
    assert get_path_from_module_contents('', 'test') is None


def test_pkg_dir_from_module_name():
    module_show_lines = ['setenv FOO_BAR_DIR /path/to/foo-bar']

    assert (get_path_from_module_contents(module_show_lines, 'foo-bar') ==
            '/path/to/foo-bar')

    assert (get_path_from_module_contents(module_show_lines, 'foo-bar/1.0') ==
            '/path/to/foo-bar')


def test_get_argument_from_module_line():
    simple_lines = ['prepend-path LD_LIBRARY_PATH /lib/path',
                    'prepend-path  LD_LIBRARY_PATH  /lib/path',
                    "prepend_path('PATH' , '/lib/path')",
                    'prepend_path( "PATH" , "/lib/path" )',
                    'prepend_path("PATH",' + "'/lib/path')"]

    complex_lines = ['prepend-path LD_LIBRARY_PATH /lib/path:/pkg/path',
                     'prepend-path  LD_LIBRARY_PATH  /lib/path:/pkg/path',
                     "prepend_path('PATH' , '/lib/path:/pkg/path')",
                     'prepend_path( "PATH" , "/lib/path:/pkg/path" )',
                     'prepend_path("PATH",' + "'/lib/path:/pkg/path')"]

    bad_lines = ['prepend_path(PATH,/lib/path)',
                 'prepend-path (LD_LIBRARY_PATH) /lib/path']

    assert all(get_path_args_from_module_line(l) == ['/lib/path']
               for l in simple_lines)
    assert all(get_path_args_from_module_line(l) == ['/lib/path', '/pkg/path']
               for l in complex_lines)
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_path_args_from_module_line(bl)

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest
import subprocess
import os
from spack.util.module_cmd import (
    get_path_from_module,
    get_path_from_module_contents,
    get_path_arg_from_module_line,
    get_module_cmd_from_bash,
    get_module_cmd,
    ModuleError)


env = os.environ.copy()
env['LC_ALL'] = 'C'
typeset_func = subprocess.Popen('module avail',
                                env=env,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
typeset_func.wait()
typeset = typeset_func.stderr.read()
MODULE_NOT_DEFINED = b'not found' in typeset


@pytest.fixture
def save_env():
    old_path = os.environ.get('PATH', None)
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)

    yield

    if old_path:
        os.environ['PATH'] = old_path
    if old_bash_func:
        os.environ['BASH_FUNC_module()'] = old_bash_func


def test_get_path_from_module(save_env):
    lines = ['prepend-path LD_LIBRARY_PATH /path/to/lib',
             'prepend-path CRAY_LD_LIBRARY_PATH /path/to/lib',
             'setenv MOD_DIR /path/to',
             'setenv LDFLAGS -Wl,-rpath/path/to/lib',
             'setenv LDFLAGS -L/path/to/lib',
             'prepend-path PATH /path/to/bin']

    for line in lines:
        module_func = '() { eval `echo ' + line + ' bash filler`\n}'
        os.environ['BASH_FUNC_module()'] = module_func
        path = get_path_from_module('mod')
        assert path == '/path/to'

    os.environ['BASH_FUNC_module()'] = '() { eval $(echo fill bash $*)\n}'
    path = get_path_from_module('mod')

    assert path is None


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
prepend_path("PATH","/path/to/cmake-3.9.2/bin")
prepend_path("MANPATH","/path/to/cmake/cmake-3.9.2/share/man")
"""
    module_show_lines = module_show_output.split('\n')
    assert (get_path_from_module_contents(module_show_lines, 'cmake-3.9.2') ==
            '/path/to/cmake-3.9.2')


def test_pkg_dir_from_module_name():
    module_show_lines = ['setenv FOO_BAR_DIR /path/to/foo-bar']

    assert (get_path_from_module_contents(module_show_lines, 'foo-bar') ==
            '/path/to/foo-bar')

    assert (get_path_from_module_contents(module_show_lines, 'foo-bar/1.0') ==
            '/path/to/foo-bar')


def test_get_argument_from_module_line():
    lines = ['prepend-path LD_LIBRARY_PATH /lib/path',
             'prepend-path  LD_LIBRARY_PATH  /lib/path',
             "prepend_path('PATH' , '/lib/path')",
             'prepend_path( "PATH" , "/lib/path" )',
             'prepend_path("PATH",' + "'/lib/path')"]

    bad_lines = ['prepend_path(PATH,/lib/path)',
                 'prepend-path (LD_LIBRARY_PATH) /lib/path']

    assert all(get_path_arg_from_module_line(l) == '/lib/path' for l in lines)
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_path_arg_from_module_line(bl)


@pytest.mark.skipif(MODULE_NOT_DEFINED, reason='Depends on defined module fn')
def test_get_module_cmd_from_bash_using_modules():
    module_list_proc = subprocess.Popen(['module list'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        executable='/bin/bash',
                                        shell=True)
    module_list_proc.wait()
    module_list = module_list_proc.stdout.read()

    module_cmd = get_module_cmd_from_bash()
    module_cmd_list = module_cmd('list', output=str, error=str)

    # Lmod command reprints some env variables on every invocation.
    # Test containment to avoid false failures on lmod systems.
    assert module_list in module_cmd_list


def test_get_module_cmd_from_bash_ticks(save_env):
    os.environ['BASH_FUNC_module()'] = '() { eval `echo bash $*`\n}'

    module_cmd = get_module_cmd()
    module_cmd_list = module_cmd('list', output=str, error=str)

    assert module_cmd_list == 'python list\n'


def test_get_module_cmd_from_bash_parens(save_env):
    os.environ['BASH_FUNC_module()'] = '() { eval $(echo fill sh $*)\n}'

    module_cmd = get_module_cmd()
    module_cmd_list = module_cmd('list', output=str, error=str)

    assert module_cmd_list == 'fill python list\n'


def test_get_module_cmd_fails(save_env):
    os.environ.pop('BASH_FUNC_module()')
    os.environ.pop('PATH')
    with pytest.raises(ModuleError):
        module_cmd = get_module_cmd(b'--norc')
        module_cmd()  # Here to avoid Flake F841 on previous line


def test_get_module_cmd_from_which(tmpdir, save_env):
    f = tmpdir.mkdir('bin').join('modulecmd')
    f.write('#!/bin/bash\n'
            'echo $*')
    f.chmod(0o770)

    os.environ['PATH'] = str(tmpdir.join('bin')) + ':' + os.environ['PATH']
    os.environ.pop('BASH_FUNC_module()')

    module_cmd = get_module_cmd(b'--norc')
    module_cmd_list = module_cmd('list', output=str, error=str)

    assert module_cmd_list == 'python list\n'

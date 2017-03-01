##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import pytest
import subprocess
import os
from spack.util.module_cmd import *

typeset_func = subprocess.Popen('module avail',
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)
typeset_func.wait()
typeset = typeset_func.stdout.read()
MODULE_DEFINED = False if 'Command not found' in typeset else True

def test_get_argument_from_module_line():
    lines = ['prepend-path LD_LIBRARY_PATH /lib/path',
             'prepend-path  LD_LIBRARY_PATH  /lib/path',
             "prepend_path('PATH' , '/lib/path')",
             'prepend_path( "PATH" , "/lib/path" )',
             'prepend_path("PATH",' + "'/lib/path')"]

    bad_lines = ['prepend_path(PATH,/lib/path)',
                 'prepend-path (LD_LIBRARY_PATH) /lib/path']

    assert all(get_argument_from_module_line(l) == '/lib/path' for l in lines)
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_argument_from_module_line(bl)

@pytest.mark.skipif(not MODULE_DEFINED, reason='Depends on defined module cmd')
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

@pytest.mark.skipif(MODULE_DEFINED, reason='Depends on redefining module cmd')
def test_get_module_cmd_from_bash_ticks():
    module_func = os.environ.get('BASH_FUNC_module()', None)
    os.environ['BASH_FUNC_module()'] = '() { `echo bash $*` \n }'
    module_cmd = get_module_cmd_from_bash()
    module_cmd_list = module_cmd('list', output=str, error=str)

    assert module_cmd_list == 'python list\n'

    if module_func:
        os.environ['BASH_FUNC_module()'] = module_func

@pytest.mark.skipif(MODULE_DEFINED, reason='Depends on redefining module cmd')
def test_get_module_cmd_from_bash_parens():
    module_func = os.environ.get('BASH_FUNC_module()', None)
    os.environ['BASH_FUNC_module()'] = '() { eval $(cat arg bash $*) \n }'
    module_cmd = get_module_cmd_from_bash()
    module_cmd_list = module_cmd('list', output=str, error=str)

    # Check directory for spack, python, and list
    # Parse output appropriately
    dir_list = os.listdir(os.getcwd())
    if 'arg' in dir_list:
        with open('arg', 'r') as f:
            assert f.read() in module_cmd_list
    else:
        assert 'cat: arg: No such file or directory' in module_cmd_list
    if 'python' in dir_list:
        with open('python', 'r') as f:
            assert f.read() in module_cmd_list
    else:
        assert 'cat: python: No such file or directory' in module_cmd_list
    if 'list' in dir_list:
        with open('list', 'r') as f:
            assert f.read() in module_cmd_list
    else:
        assert 'cat: list: No such file or directory' in module_cmd_list

    if module_func:
        os.environ['BASH_FUNC_module()'] = module_func

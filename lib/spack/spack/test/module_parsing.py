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
                                stderr=subprocess.PIPE,
                                shell=True)
typeset_func.wait()
typeset = typeset_func.stderr.read()
MODULE_NOT_DEFINED = b'not found' in typeset


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


def test_get_module_cmd_from_bash_ticks():
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)

    try:
        os.environ['BASH_FUNC_module()'] = '() { eval `echo bash $*`\n}'

        module_cmd = get_module_cmd()
        module_cmd_list = module_cmd('list', output=str, error=str)

        assert module_cmd_list == 'python list\n'

    finally:
        if old_bash_func:
            os.environ['BASH_FUNC_module()'] = old_bash_func


def test_get_module_cmd_from_bash_parens():
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)

    try:
        os.environ['BASH_FUNC_module()'] = '() { eval $(echo fill bash $*)\n}'

        module_cmd = get_module_cmd()
        module_cmd_list = module_cmd('list', output=str, error=str)

        assert module_cmd_list == 'fill python list\n'

    finally:
        if old_bash_func:
            os.environ['BASH_FUNC_module()'] = old_bash_func


def test_get_module_cmd_fails():
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)
    old_PATH = os.environ.get('PATH', None)
    try:
        os.environ.pop('BASH_FUNC_module()')
        os.environ.pop('PATH')
        with pytest.raises(ModuleError):
            module_cmd = get_module_cmd('--norc')
            print module_cmd

    finally:
        if old_PATH:
            os.environ['PATH'] = old_PATH
        if old_bash_func:
            os.environ['BASH_FUNC_module()'] = old_bash_func


def test_get_module_cmd_from_which(tmpdir):
    old_PATH = os.environ.get('PATH', None)
    old_bash_func = os.environ.get('BASH_FUNC_module()', None)

    f = tmpdir.mkdir('bin').join('modulecmd')
    f.write('#!/bin/bash\n'
            'echo $*')
    f.chmod(0o770)

    try:
        os.environ['PATH'] = str(tmpdir.join('bin')) + ':' + old_PATH
        os.environ.pop('BASH_FUNC_module()')

        module_cmd = get_module_cmd('--norc')
        module_cmd_list = module_cmd('list', output=str, error=str)

        assert module_cmd_list == 'python list\n'

    finally:
        if old_PATH:
            os.environ['PATH'] = old_PATH
        if old_bash_func:
            os.environ['BASH_FUNC_module()'] = old_bash_func

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from spack.main import print_setup_info


def test_print_shell_vars_sh(capsys):
    print_setup_info('sh')
    out, _ = capsys.readouterr()

    assert "_sp_sys_type=" in out
    assert "_sp_tcl_root=" in out
    assert "_sp_lmod_root=" in out
    assert "_sp_module_prefix" not in out


def test_print_shell_vars_csh(capsys):
    print_setup_info('csh')
    out, _ = capsys.readouterr()

    assert "set _sp_sys_type = " in out
    assert "set _sp_tcl_root = " in out
    assert "set _sp_lmod_root = " in out
    assert "set _sp_module_prefix = " not in out


def test_print_shell_vars_sh_modules(capsys):
    print_setup_info('sh', 'modules')
    out, _ = capsys.readouterr()

    assert "_sp_sys_type=" in out
    assert "_sp_tcl_root=" in out
    assert "_sp_lmod_root=" in out
    assert "_sp_module_prefix=" in out


def test_print_shell_vars_csh_modules(capsys):
    print_setup_info('csh', 'modules')
    out, _ = capsys.readouterr()

    assert "set _sp_sys_type = " in out
    assert "set _sp_tcl_root = " in out
    assert "set _sp_lmod_root = " in out
    assert "set _sp_module_prefix = " in out

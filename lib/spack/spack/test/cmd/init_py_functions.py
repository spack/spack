# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
from spack.cmd import require_python_name, python_name, PythonNameError, \
    require_cmd_name, cmd_name, CommandNameError


def test_require_python_name():
    require_python_name("okey_dokey")
    with pytest.raises(PythonNameError):
        require_python_name("okey-dokey")
    require_python_name(python_name("okey-dokey"))


def test_require_cmd_name():
    require_cmd_name("okey-dokey")
    with pytest.raises(CommandNameError):
        require_cmd_name("okey_dokey")
    require_cmd_name(cmd_name("okey_dokey"))

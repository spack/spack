# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
import spack.cmd


def test_require_python_name():
    spack.cmd.require_python_name("okey_dokey")
    with pytest.raises(spack.cmd.PythonNameError):
        spack.cmd.require_python_name("okey-dokey")
    spack.cmd.require_python_name(spack.cmd.python_name("okey-dokey"))


def test_require_cmd_name():
    spack.cmd.require_cmd_name("okey-dokey")
    with pytest.raises(spack.cmd.CommandNameError):
        spack.cmd.require_cmd_name("okey_dokey")
    spack.cmd.require_cmd_name(spack.cmd.cmd_name("okey_dokey"))

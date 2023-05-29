# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

import pytest

import spack
from spack.main import SpackCommand

python = SpackCommand("python")


def test_python(capsys):
    with capsys.disabled():
        out = python("-c", "import spack; print(spack.spack_version)")
        assert out.strip() == spack.spack_version


def test_python_interpreter_path():
    out = python("--path")
    assert out.strip() == sys.executable


def test_python_version():
    out = python("-V")
    assert platform.python_version() in out


def test_python_with_module(capsys):
    with capsys.disabled():
        out = python("-m", "sys", fail_on_error=False)
        assert "No code object" in out


def test_python_raises_on_bad_arg():
    with pytest.raises(spack.util.executable.ProcessError):
        python("--foobar")

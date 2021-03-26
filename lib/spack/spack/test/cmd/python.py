# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

import pytest

import spack
from spack.main import SpackCommand

python = SpackCommand('python')


def test_python(capsys):
    out = python('-c', 'import spack; print(spack.spack_version)', out=capsys)
    assert out.strip() == spack.spack_version


def test_python_interpreter_path(capsys):
    out = python('--path', out=capsys)
    assert out.strip() == sys.executable


def test_python_version(capsys):
    out = python('-V', out=capsys)
    assert platform.python_version() in out


def test_python_with_module():
    # pytest rewrites a lot of modules, which interferes with runpy, so
    # it's hard to test this.  Trying to import a module like sys, that
    # has no code associated with it, raises an error reliably in python
    # 2 and 3, which indicates we successfully ran runpy.run_module.
    with pytest.raises(ImportError, match="No code object"):
        python('-m', 'sys')


def test_python_raises(capsys):
    out = python('--foobar', fail_on_error=False, out=capsys)
    assert "Error: Unknown arguments" in out

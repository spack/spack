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

try:
    import IPython  # noqa: F401

    have_ipython = True
except ImportError:
    have_ipython = False


def test_python(capfd):
    python("-c", "import spack; print(spack.spack_version)")
    out, _ = capfd.readouterr()
    assert out.strip() == spack.spack_version


@pytest.mark.skipif(not have_ipython, reason="requires IPython to be installed")
def test_ipython(capfd):
    with capfd.disabled():
        out = python("-I", "-c", "import spack; print(spack.spack_version)")
    assert out.strip() == spack.spack_version


def test_python_interpreter_path(capfd):
    with capfd.disabled():
        out = python("--path")
    assert out.strip() == sys.executable


def test_python_version(capfd):
    with capfd.disabled():
        out = python("-V")
    assert platform.python_version() in out


def test_python_with_module(capfd):
    python("-m", "sys", fail_on_error=False)
    _, err = capfd.readouterr()
    assert "No code object" in err


def test_python_raises_on_bad_arg():
    with pytest.raises(spack.util.executable.ProcessError):
        python("--foobar")

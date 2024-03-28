# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPtrace(PythonPackage):
    """python-ptrace is a debugger using ptrace (Linux, BSD and Darwin system
    call to trace processes) written in Python."""

    pypi = "python-ptrace/python-ptrace-0.9.8.tar.gz"

    license("GPL-2.0-only")

    version(
        "0.9.8",
        sha256="440c58a47423eb6eeea419854b9c6c28bfd9fd6ab9ae6630a7ea8be4600b1369",
        url="https://pypi.org/packages/8c/e9/5ca5369bcba01fed6c9c52f7d25e012b42aadeb7b79e2d02401cf8a74081/python_ptrace-0.9.8-py2.py3-none-any.whl",
    )

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDbfread(PythonPackage):
    """DBF is a file format used by databases such dBase, Visual FoxPro, and
    FoxBase+. This library reads DBF files and returns the data as native
    Python data types for further processing. It is primarily intended for
    batch jobs and one-off scripts."""

    homepage = "https://dbfread.readthedocs.io/en/latest/"
    pypi = "dbfread/dbfread-2.0.7.tar.gz"

    license("MIT")

    version(
        "2.0.7",
        sha256="f604def58c59694fa0160d7be5d0b8d594467278d2bb6a47d46daf7162c84cec",
        url="https://pypi.org/packages/4c/94/51349e43503e30ed7b4ecfe68a8809cdb58f722c0feb79d18b1f1e36fe74/dbfread-2.0.7-py2.py3-none-any.whl",
    )

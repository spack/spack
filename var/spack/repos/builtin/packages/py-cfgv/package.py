# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv/"
    pypi = "cfgv/cfgv-2.0.1.tar.gz"

    license("MIT")

    version(
        "3.4.0",
        sha256="b7265b1f29fd3316bfcd2b330d63d024f2bfd8bcb8b0272f8e19a504856c48f9",
        url="https://pypi.org/packages/c5/55/51844dd50c4fc7a33b653bfaba4c2456f06955289ca770a5dbd5fd267374/cfgv-3.4.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.1",
        sha256="c6a0883f3917a037485059700b9e75da2464e6c27051014ad85ba6aaa5884426",
        url="https://pypi.org/packages/6d/82/0a0ebd35bae9981dea55c06f8e6aaf44a49171ad798795c72c6f64cba4c2/cfgv-3.3.1-py2.py3-none-any.whl",
    )
    version(
        "2.0.1",
        sha256="fbd93c9ab0a523bf7daec408f3be2ed99a980e20b2d19b50fc184ca6b820d289",
        url="https://pypi.org/packages/6e/ff/2e6bcaff26058200717c469a0910da96c89bb00e9cc31b68aa0bfc9b1b0d/cfgv-2.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3.4:")
        depends_on("py-six", when="@:2")

    # Historical dependencies

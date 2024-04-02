# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyperf(PythonPackage):
    """The Python perf module is a toolkit to write, run and
    analyze benchmarks.
    """

    homepage = "https://github.com/vstinner/pyperf"
    url = "https://github.com/vstinner/pyperf/archive/1.5.1.tar.gz"

    license("MIT")

    version(
        "1.6.1",
        sha256="b9074a5e16e526ebe260922005ee96b67621ce804efd3e8dd49de49b513397a8",
        url="https://pypi.org/packages/7f/34/12f4f27e43ed9d2269162fbb07005a08b45b6ed275a0e50cc3afda84af76/pyperf-1.6.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@:1")

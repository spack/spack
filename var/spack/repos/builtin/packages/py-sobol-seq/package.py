# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySobolSeq(PythonPackage):
    """Sobol sequence implementation in python"""

    homepage = "https://github.com/naught101/sobol_seq"
    pypi = "sobol_seq/sobol_seq-0.2.0.tar.gz"

    license("MIT")

    version(
        "0.2.0",
        sha256="277ab767250a20b440fc74df8b6f4d79773949d5770927e1cee83e8de026b704",
        url="https://pypi.org/packages/e4/df/6c4ad25c0b48545a537b631030f7de7e4abb939e6d2964ac2169d4379c85/sobol_seq-0.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy", when="@0.2:")
        depends_on("py-scipy", when="@0.2:")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOpencensus(PythonPackage):
    """A stats collection and distributed tracing framework."""

    homepage = "https://github.com/census-instrumentation/opencensus-python"
    pypi = "opencensus/opencensus-0.7.10.tar.gz"

    license("Apache-2.0")

    version(
        "0.7.10",
        sha256="41fbba4f26e4f66bf7e6a8761b1a61346cf46e2f6a2d82073c11a35576c2d9eb",
        url="https://pypi.org/packages/8a/9c/d40e3408e72d02612acf247d829e3fa9ff15c59f7ad81418ed79962f8681/opencensus-0.7.10-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-google-api-core@1", when="@:0.7")
        depends_on("py-opencensus-context@0.1.1", when="@:0.7.10")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydevtool(PythonPackage):
    """CLI dev tools powered by pydoit."""

    homepage = "https://github.com/pydoit/pydevtool"
    pypi = "pydevtool/pydevtool-0.3.0.tar.gz"

    license("MIT")

    version(
        "0.3.0",
        sha256="da7876254f0bbedc6fffcd2a75cd1c624e3a2864ff13b2dff73e785056f7a643",
        url="https://pypi.org/packages/d8/bf/3807d5876ed8ac2ef4515774c0b7ad977296eea084d5fafaccbefb9f1c7a/pydevtool-0.3.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:")
        depends_on("py-doit@0.36:", when="@0.3:")

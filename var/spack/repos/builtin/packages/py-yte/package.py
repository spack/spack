# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYte(PythonPackage):
    """A YAML template engine with Python expressions."""

    homepage = "https://yte-template-engine.github.io"
    pypi = "yte/yte-1.5.1.tar.gz"

    maintainers("charmoniumQ")

    license("MIT")

    version(
        "1.5.1",
        sha256="fd646bc47c355f202f14b7476996de4a31501cf1e107ac7ad8e19edcd786d30b",
        url="https://pypi.org/packages/27/a2/638c528c6b35582b1de094de2ff2e8d0ac87c426ed04a375281356857bc7/yte-1.5.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.2:")
        depends_on("py-dpath@2:", when="@1.3:1.5.1")
        depends_on("py-plac@1.3.4:")
        depends_on("py-pyyaml@6.0:")

    # https://github.com/yte-template-engine/yte/blob/v1.5.1/pyproject.toml#L12

    # https://github.com/yte-template-engine/yte/blob/v1.5.1/pyproject.toml#L41

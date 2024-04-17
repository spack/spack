# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterTelemetry(PythonPackage):
    """Jupyter Telemetry enables Jupyter Applications to record events and transmit"""

    """ them to destinations as structured data"""

    pypi = "jupyter-telemetry/jupyter_telemetry-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.0",
        sha256="1de3e423b23aa40ca4a4238d65c56dda544061ff5aedc3f7647220ed7e3b9589",
        url="https://pypi.org/packages/90/ab/8d565a0797dacf82dea161ba5c40bd1f3ddbf365e3f7f8fd63007f03b19f/jupyter_telemetry-0.1.0-py3-none-any.whl",
    )
    version(
        "0.0.5",
        sha256="f6546c6da6ca589fe6d4ce314bd4a05e4136b54b1f69e8856c7c0eb5764e8227",
        url="https://pypi.org/packages/a7/8a/c1302cdbcc1b045b25fc6f6988b74fab4cc077ec2aa9c1dcd8c7a6be4404/jupyter_telemetry-0.0.5-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-jsonschema", when="@0.0.4:")
        depends_on("py-python-json-logger", when="@0.0.4:")
        depends_on("py-ruamel-yaml", when="@0.0.4:")
        depends_on("py-traitlets", when="@0.0.4:")

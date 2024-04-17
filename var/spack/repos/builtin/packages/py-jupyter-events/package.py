# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterEvents(PythonPackage):
    """Jupyter Event System library."""

    homepage = "https://github.com/jupyter/jupyter_events"
    pypi = "jupyter_events/jupyter_events-0.6.3.tar.gz"

    version(
        "0.6.3",
        sha256="57a2749f87ba387cd1bfd9b22a0875b889237dbf2edc2121ebb22bde47036c17",
        url="https://pypi.org/packages/ee/14/e11a93c1b47a69432ee7898f1b55f1da27f2f93b009a34dbdafb9b903f81/jupyter_events-0.6.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@:0.6")
        depends_on("py-jsonschema@3.2:+format-nongpl", when="@0.6.1:0.6")
        depends_on("py-python-json-logger@2.0.4:", when="@0.6:")
        depends_on("py-pyyaml@5.3:", when="@0.6.2:")
        depends_on("py-rfc3339-validator", when="@0.6.1:")
        depends_on("py-rfc3986-validator@0.1.1:", when="@0.6.1:")
        depends_on("py-traitlets@5.3:5.3.0.0,5.4:", when="@0.6:")

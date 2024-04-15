# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJupyterlabServer(PythonPackage):
    """A set of server components for JupyterLab and JupyterLab
    like applications"""

    homepage = "https://github.com/jupyterlab/jupyterlab_server"
    pypi = "jupyterlab_server/jupyterlab_server-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.22.1",
        sha256="1c8eb55c7cd70a50a51fef42a7b4e26ef2f7fc48728f0290604bd89b1dd156e6",
        url="https://pypi.org/packages/ad/31/cfb84feb3803c1e0e69dbe6928ab9251b9a1548b9092a5013413c0dd49f8/jupyterlab_server-2.22.1-py3-none-any.whl",
    )
    version(
        "2.10.3",
        sha256="62f3c598f1d48dfb9b27729ed17772e38115cbe61e7d60fe68a853791bdf1038",
        url="https://pypi.org/packages/cb/22/308fdf317ed12c7f8e6081797bcccc53de3c7a34d89cbf975069194f7c41/jupyterlab_server-2.10.3-py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="10ca364e764a6ca1e387530dfe5a09dc8fd563f1739b2b7b5a49e8cf5c4140ee",
        url="https://pypi.org/packages/01/c4/461a38d71c5c9c756d8adf2e3acd6fd133512fae2bc22779c09e5b287149/jupyterlab_server-2.6.0-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="55d256077bf13e5bc9e8fbd5aac51bef82f6315111cec6b712b9a5ededbba924",
        url="https://pypi.org/packages/b4/eb/560043dcd8376328f8b98869efed66ef68307278406ab99c7f63a34d4ae2/jupyterlab_server-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="6aeaa1133069ec8d109f474b628059da2ec2e73f4e448c89e56821e6cfc26c0f",
        url="https://pypi.org/packages/74/bc/e87bb9dc5d20b6af9efa9551e5cb4e02bbd5bd100484e35acfa60a9bbba0/jupyterlab_server-1.1.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2.11:2.24")
        depends_on("py-babel@2.10:", when="@2.16.4:")
        depends_on("py-babel", when="@1.3:2.16.3")
        depends_on("py-entrypoints@0.2.2:", when="@2.7:2.12")
        depends_on("py-importlib-metadata@4.8.3:", when="@2.16.0: ^python@:3.9")
        depends_on("py-jinja2@3.0.3:", when="@2.11:")
        depends_on("py-jinja2@2.10:", when="@1.0.5:2.10")
        depends_on("py-json5@0.9:", when="@2.16.4:")
        depends_on("py-json5", when="@1.0.0:2.16.3")
        depends_on("py-jsonschema@4.17.3:", when="@2.17:2.24")
        depends_on("py-jsonschema@3.0.1:", when="@:2.16")
        depends_on("py-jupyter-server@1.21:", when="@2.16.5:")
        depends_on("py-jupyter-server@1.4:1", when="@2.3:2.10")
        depends_on("py-notebook@4.2.0:", when="@:2.0.0-alpha0")
        depends_on("py-packaging@21.3:", when="@2.16.4:")
        depends_on("py-packaging", when="@1.3:2.16.3")
        depends_on("py-requests@2.28:", when="@2.16.4:2.24")
        depends_on("py-requests", when="@1.1:2.16.3")

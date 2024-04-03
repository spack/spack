# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParsl(PythonPackage):
    """
    Simple data dependent workflows in Python
    """

    homepage = "https://github.com/Parsl/parsl"
    url = "https://github.com/Parsl/parsl/archive/refs/tags/1.1.0.tar.gz"

    maintainers("hategan")

    license("Apache-2.0")

    version(
        "2023.8.21",
        sha256="e3d47c4c6f13fc3c107211b98dcdcd8f9bf2d57a1b0938b9adcd46fb3ae9c8a8",
        url="https://pypi.org/packages/2e/26/3ed3a3a0f8bfc7d9e43141a7f66d0f30c49e78e3975084d5cf5c8bd82f22/parsl-2023.8.21-py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="28c4cfb3d7a8f2abb0d055bc858f6fd930486231db846ebe7d6489292f7ddc68",
        url="https://pypi.org/packages/ab/98/efdcd068060eb4c913b17c385ae8dd6ce36d22de26d9a65377781af1f29c/parsl-1.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="1762ed04f4a5b83f075f77ede148e60b8ca96513bd6927d28c0c69abc2bba42b",
        url="https://pypi.org/packages/01/75/886d1402c1bfa0aacadae611f875f7e7cc57d9d108a6659143474cf8aa3f/parsl-1.1.0.post1-py3-none-any.whl",
    )

    variant("monitoring", default=False, description="enable live monitoring")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2023.6.26:")
        depends_on("py-dill")
        depends_on("py-flask@1.0.2:", when="@0.9:2023.10.16+monitoring")
        depends_on("py-flask-sqlalchemy", when="@0.9:2023.10.16+monitoring")
        depends_on("py-globus-sdk")
        depends_on("py-networkx@2.5", when="@1.3:2023.10.16+monitoring")
        depends_on("py-networkx", when="@0.9:1.2+monitoring")
        depends_on("py-pandas@:1", when="@2023.3.27:2023.10.16+monitoring")
        depends_on("py-pandas", when="@0.9:1.2+monitoring")
        depends_on("py-paramiko")
        depends_on("py-plotly", when="@0.9:2023.10.16+monitoring")
        depends_on("py-psutil@5.5.1:", when="@0.9:")
        depends_on("py-pydot", when="@0.9:2023.10.16+monitoring")
        depends_on("py-python-daemon", when="@0.9:2023.10.16+monitoring")
        depends_on("py-pyzmq@17.1.2:")
        depends_on("py-requests")
        depends_on("py-setproctitle", when="@1.3:")
        depends_on("py-six", when="@2023.1.23:2024.1.22")
        depends_on("py-sqlalchemy@1.4.0:1", when="@2023.4.24:+monitoring")
        depends_on("py-sqlalchemy@1.3.0:1.3.3,1.3.5:1.3", when="@1.1.0:1.2+monitoring")
        depends_on("py-sqlalchemy-utils", when="@:0.7,0.9:1.2+monitoring")
        depends_on("py-tblib")
        depends_on("py-typeguard@2.10:2", when="@2023.3.20:2024.1")
        depends_on("py-typeguard@2.10:", when="@1.1:2023.3.13")
        depends_on("py-typing-extensions@4.6:", when="@2023.6:")
        depends_on("py-typing-extensions", when="@1.1.0:2023.5")

    # See https://parsl.readthedocs.io/en/stable/userguide/monitoring.html

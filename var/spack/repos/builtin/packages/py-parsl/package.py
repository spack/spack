# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("1.1.0", sha256="6a623d3550329f028775950d23a2cafcb0f82b199f15940180410604aa5d102c")

    variant("monitoring", default=False, description="enable live monitoring")
    # See https://parsl.readthedocs.io/en/stable/userguide/monitoring.html

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyzmq@17.1.2:", type=("build", "run"))
    depends_on("py-typeguard@2.10:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-globus-sdk", type=("build", "run"))
    depends_on("py-dill", type=("build", "run"))
    depends_on("py-tblib", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-paramiko", type=("build", "run"))
    depends_on("py-psutil@5.5.1:", type=("build", "run"))

    with when("+monitoring"):
        depends_on("py-sqlalchemy@1.3", type=("build", "run"))
        conflicts("^py-sqlalchemy@1.3.4")
        depends_on("py-sqlalchemy-utils", type=("build", "run"))
        depends_on("py-pydot", type=("build", "run"))
        depends_on("py-networkx", type=("build", "run"))
        depends_on("py-flask@1.0.2:", type=("build", "run"))
        depends_on("py-flask-sqlalchemy", type=("build", "run"))
        depends_on("py-pandas", type=("build", "run"))
        depends_on("py-plotly", type=("build", "run"))
        depends_on("py-python-daemon", type=("build", "run"))

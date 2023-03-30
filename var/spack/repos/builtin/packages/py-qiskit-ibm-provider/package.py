# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQiskitIbmProvider(PythonPackage):
    """This project contains a provider that allows accessing the IBM Quantum
    systems and simulators."""

    homepage = "https://github.com/Qiskit/qiskit-ibm-provider"
    url = "https://github.com/Qiskit/qiskit-ibm-provider/archive/refs/tags/0.4.0.tar.gz"

    version("0.4.0", sha256="69e9582a42ec5a9b9977ab0d6ea75da68cff5c09420763cd91813b46ff7bbb9e")

    variant("visualization", description="visualization extra requirements", default=False)

    depends_on("python@3.7:",                   type=("build", "run"))
    depends_on("py-setuptools",                 type="build")
    depends_on("py-qiskit-terra@0.23.1:",       type=("build", "run"))
    depends_on("py-requests@2.19:",             type=("build", "run"))
    depends_on("py-requests-ntlm@1.1.0:",       type=("build", "run"))
    depends_on("py-numpy@1.13:",                type=("build", "run"))
    depends_on("py-urllib3@1.21.1:",            type=("build", "run"))
    depends_on("py-python-dateutil@2.8.0:",     type=("build", "run"))
    depends_on("py-websocket-client@1.5.1:",    type=("build", "run"))
    depends_on("py-websockets@10.0:",           type=("build", "run"))
    depends_on("py-typing-extensions@4.3:",     type=("build", "run"))

    # visualization requirements
    with when("+visualization"):
        depends_on("py-matplotlib@2.1:",            type=("build", "run"))
        depends_on("py-ipywidgets@:7",              type=("build", "run"))
        depends_on("py-seaborn@0.9:",               type=("build", "run"))
        depends_on("py-plotly@4.4:",                type=("build", "run"))
        depends_on("py-ipyvuetify@1.1:",            type=("build", "run"))
        depends_on("py-pyperclip@1.7:",             type=("build", "run"))
        depends_on("py-ipython@5.0.0:",             type=("build", "run"))
        depends_on("py-traitlets@:5.0.4,5.0.6:",    type=("build", "run"))
        depends_on("py-ipyvue@1.4.1:",              type=("build", "run"))

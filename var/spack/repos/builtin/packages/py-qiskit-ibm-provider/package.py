# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQiskitIbmProvider(PythonPackage):
    """Qiskit IBM Quantum Provider for accessing the quantum devices and simulators
    at IBM"""

    homepage = "https://github.com/Qiskit/qiskit-ibm-provider"
    pypi = "qiskit-ibm-provider/qiskit-ibm-provider-0.5.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.5.1",
        sha256="70b099b6e9b65b15ba52dfd0a9364a7a7be8272fc5ac90dc14b4107b3a750731",
        url="https://pypi.org/packages/68/a6/469da0fb7d959778ec31ed61251d444241d6b28e71d9b7008824ec52e027/qiskit_ibm_provider-0.5.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@:0.5.2")
        depends_on("py-numpy@1.13.0:")
        depends_on("py-python-dateutil@2.8:")
        depends_on("py-qiskit-terra@0.23.1:", when="@0.3:0.5.2")
        depends_on("py-requests@2.19:")
        depends_on("py-requests-ntlm@1.1:")
        depends_on("py-typing-extensions@4.3:")
        depends_on("py-urllib3@1.21.1:")
        depends_on("py-websocket-client@1.5.1:", when="@0.4:")
        depends_on("py-websockets@10:")

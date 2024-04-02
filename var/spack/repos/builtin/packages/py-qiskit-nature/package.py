# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQiskitNature(PythonPackage):
    """Qiskit Nature is an open-source framework which supports
    solving quantum mechanical natural science problems using
    quantum computing algorithms"""

    homepage = "https://github.com/Qiskit/qiskit-nature"
    pypi = "qiskit-nature/qiskit-nature-0.2.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.2",
        sha256="d99b4beedc9f86d19cef0405c16d63395ae97c6ff0d128f0fe0dadeeb174988f",
        url="https://pypi.org/packages/11/a0/3ead7a1b1979a797f3c3d14277dc0caa0140972f96f7e57874719c0ef0ce/qiskit_nature-0.2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses", when="@0.2:0.3.1 ^python@:3.6")
        depends_on("py-h5py@:3.2", when="@0.1.4:0.2")
        depends_on("py-numpy@1.17.0:")
        depends_on("py-psutil@5:")
        depends_on("py-qiskit-terra@0.18:", when="@0.1.4:0.2")
        depends_on("py-scikit-learn@0.20.0:", when="@:0.6")
        depends_on("py-scipy@1.4.0:")
        depends_on("py-setuptools@40.1:")

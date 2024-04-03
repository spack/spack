# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRseqc(PythonPackage):
    """RSeQC package provides a number of useful modules that can
    comprehensively evaluate high throughput sequence data especially RNA-seq
    data."""

    homepage = "http://rseqc.sourceforge.net"
    pypi = "RSeQC/RSeQC-2.6.4.tar.gz"

    version(
        "5.0.1",
        sha256="5e2de2280ab511d584f210ef1b513f6de00cd22c55dc1e08de5d90f5517b0ea5",
        url="https://pypi.org/packages/88/21/be047be1b5f8c8e1fd828a17969066d9c80fc5c60c2c4b7d42448d57e349/RSeQC-5.0.1-py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="4939c07ce2fd873aae4f3611e3c27fd42bb5035e7f77998958b26d7ba3dbb475",
        url="https://pypi.org/packages/7f/2e/6ba1d89159b09500c0f450971e614228531b9a4bc51e92638148c7e58742/RSeQC-4.0.1-py3-none-any.whl",
    )
    version(
        "3.0.1",
        sha256="d34d4bd4979f9c567b5c81a399bdf56d094d7000617f1e7c84bbfa8df9ab7ad7",
        url="https://pypi.org/packages/a8/ee/932ddc178619a5381fb1a11dfe849bed7852ee981dac5ac26fb14b407ac0/RSeQC-3.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bx-python", when="@2.6.5:")
        depends_on("py-cython@0.17:", when="@2.6.5:")
        depends_on("py-numpy", when="@2.6.5:")
        depends_on("py-pybigwig", when="@3:")
        depends_on("py-pysam", when="@2.6.5:")

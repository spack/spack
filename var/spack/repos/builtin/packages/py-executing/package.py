# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExecuting(PythonPackage):
    """Get the currently executing AST node of a frame, and other information."""

    homepage = "https://github.com/alexmojaki/executing"
    pypi = "executing/executing-0.8.2.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="0314a69e37426e3608aada02473b4161d4caf5a4b244d1d0c48072b8fee7bacc",
        url="https://pypi.org/packages/28/3c/bc3819dd8b1a1588c9215a87271b6178cc5498acaa83885211f5d4d9e693/executing-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="4a6d96ba89eb3dcc11483471061b42b9006d8c9f81c584dd04246944cd022530",
        url="https://pypi.org/packages/00/de/9222dd64c07608cfe7b43e0ced0c6317b003c8ebef8043a6938ea22d9796/executing-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="550d581b497228b572235e633599133eeee67073c65914ca346100ad56775349",
        url="https://pypi.org/packages/7b/54/66caf1028fd51396996019100225da71c000220dc05bda1fb39adb458f43/executing-1.0.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.2",
        sha256="32fc6077b103bd19e6494a72682d66d5763cf20a106d5aa7c5ccbea4e47b0df7",
        url="https://pypi.org/packages/ba/64/59e024b685666514cb20ffc2463a8b062df8e6c36efc5199cb422b728b78/executing-0.8.2-py2.py3-none-any.whl",
    )

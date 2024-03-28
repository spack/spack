# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonJenkins(PythonPackage):
    """Python bindings for the remote Jenkins API"""

    homepage = "https://opendev.org/jjb/python-jenkins/"
    pypi = "python-jenkins/python-jenkins-1.5.0.tar.gz"

    version(
        "1.5.0",
        sha256="0b57097456839a3901562cd67582e3672b5e39c200c0653e477450534c80c9d3",
        url="https://pypi.org/packages/ab/22/7099a997bdbaa1105758b577c7c35705a68bda40226e8c0df2415245a081/python_jenkins-1.5.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="07d0cf392c8fdf6cab9339c63cf661a63b973845503e6c3e7676a06209312e6f",
        url="https://pypi.org/packages/76/4a/4bc451a898e67f92b627115c2e0c4cdcc2a9e61e4da560923884ab3e9e7b/python_jenkins-1.0.2-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-multi-key-dict", when="@0.4.9:")
        depends_on("py-pbr@0.8.2:", when="@0.4.14:")
        depends_on("py-requests", when="@1:")
        depends_on("py-six@1.3:", when="@0.4.9:")

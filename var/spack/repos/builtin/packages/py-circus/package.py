# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCircus(PythonPackage):
    """Circus is a program that will let you run and watch
    multiple processes and sockets.
    """

    homepage = "https://github.com/circus-tent/circus"
    pypi = "circus/circus-0.18.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.18.0",
        sha256="f3ee4167bea16d34b42bab61440284f3936d2548f5546e70cf79f66daec867b0",
        url="https://pypi.org/packages/7b/fd/254a8a04ae1b57af59917bcd2670b31d42ce0da94d0aa257c80096c9089e/circus-0.18.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@0.18:")
        depends_on("py-psutil", when="@0.16:")
        depends_on("py-pyzmq@17.0.0:", when="@0.16:")
        depends_on("py-tornado@5.0.2:", when="@0.17:")

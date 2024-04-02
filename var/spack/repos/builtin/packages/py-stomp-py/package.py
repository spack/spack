# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStompPy(PythonPackage):
    """Python client library for accessing messaging servers
    (such as ActiveMQ, Artemis or RabbitMQ) using the STOMP
    protocol (STOMP v1.0, STOMP v1.1 and STOMP v1.2)"""

    homepage = "https://github.com/jasonrbriggs/stomp.py"
    pypi = "stomp.py/stomp.py-8.0.0.tar.gz"

    maintainers("haralmha")

    license("Apache-2.0")

    version(
        "8.0.0",
        sha256="7e4d8d864ecd608f306d238ba951bd76e30bbfb2a4ba0b804b0333de6d75dfc4",
        url="https://pypi.org/packages/8e/2e/5ebcdfbf76c5aee13fdff1b3903706e2c5181296b845644c5c116ebeedb7/stomp.py-8.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@6:")
        depends_on("py-docopt@0.6.2:", when="@6:")
        depends_on("py-pyopenssl@20.0.1:20", when="@8:8.0.0")

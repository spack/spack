# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPahoMqtt(PythonPackage):
    """paho-mqtt is the Eclipse Paho MQTT Python client library, which
    implements versions 5.0, 3.1.1, and 3.1 of the MQTT protocol.

    This library provides a client class which enables applications to connect
    to an MQTT broker to publish messages, and to subscribe to topics and
    receive published messages. It also provides some helper functions to make
    publishing one off messages to an MQTT server very straightforward.
    """

    homepage = "https://eclipse.dev/paho/"
    pypi = "paho-mqtt/paho_mqtt-2.1.0.tar.gz"

    version("2.1.0", sha256="12d6e7511d4137555a3f6ea167ae846af2c7357b10bc6fa4f7c3968fc1723834")
    version("2.0.0", sha256="13b205f29251e4f2c66a6c923c31fc4fd780561e03b2d775cff8e4f2915cf947")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("py-hatchling", type="build")

    variant("proxy", default=False, description="Enable socket proxy support")

    with when("+proxy"):
        depends_on("py-pysocks", type=("build", "run"))

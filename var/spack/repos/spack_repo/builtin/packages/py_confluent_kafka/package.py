# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyConfluentKafka(PythonPackage):
    """Confluent's Kafka Python Client."""

    homepage = "https://docs.confluent.io/kafka-clients/python"
    pypi = "confluent-kafka/confluent-kafka-2.6.0.tar.gz"

    license("Apache-2.0", checked_by="github_user1")

    version("2.6.0", sha256="f7afe69639bd2ab15404dd46a76e06213342a23cb5642d873342847cb2198c87")

    depends_on("c", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("librdkafka@2.6.0:")

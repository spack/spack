# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloSerialization(PythonPackage):
    """
    The oslo.serialization library provides support for representing objects in
    transmittable and storable formats, such as Base64, JSON and MessagePack.
    """

    homepage = "https://docs.openstack.org/oslo.serialization/"
    pypi = "oslo.serialization/oslo.serialization-4.1.0.tar.gz"

    maintainers("haampie")

    version(
        "4.1.0",
        sha256="a0acf0ff7ca88b3ee6514713571f614b5c20870005ed0eb90408fa7f9f3edb60",
        url="https://pypi.org/packages/a4/99/d02844a4ddd063dab89b8b9cfd176081ef9e60a5b57fa89cd3a62a406195/oslo.serialization-4.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-msgpack@0.5.2:")
        depends_on("py-oslo-utils@3.33:")
        depends_on("py-pbr@2:2.0,3:")
        depends_on("py-pytz@2013.6:", when="@:5.3")

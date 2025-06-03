# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPykwalify(PythonPackage):
    """
    Python lib/cli for JSON/YAML schema validation
    """

    homepage = "https://github.com/grokzen/pykwalify"
    pypi = "pykwalify/pykwalify-1.7.0.tar.gz"

    license("MIT")

    version("1.8.0", sha256="796b2ad3ed4cb99b88308b533fb2f559c30fa6efb4fa9fda11347f483d245884")
    version("1.7.0", sha256="7e8b39c5a3a10bc176682b3bd9a7422c39ca247482df198b402e8015defcceb2")
    version("1.6.1", sha256="191fd3f457f23c0aa8538c3a5c0249f70eeb1046e88d0eaaef928e09c44dff8d")

    depends_on("py-setuptools", type="build")

    with default_args(type=("build", "run")):
        # Uses deprecated imp module
        depends_on("python@:3.11", when="@:1.7")
        depends_on("py-docopt@0.6.2:")
        depends_on("py-ruamel-yaml@0.16:", when="@1.8:")
        depends_on("py-ruamel-yaml@0.11:")
        depends_on("py-python-dateutil@2.8:", when="@1.8:")
        depends_on("py-python-dateutil@2.4.2:")
        depends_on("py-pyyaml@3.11:", when="@1.6.1")

    conflicts("^py-ruamel-yaml@0.16.0:", when="@1.6.1")

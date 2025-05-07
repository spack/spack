# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPyvizComms(PythonPackage):
    """Bidirectional communication for the HoloViz ecosystem."""

    homepage = "https://holoviz.org/"
    pypi = "pyviz_comms/pyviz_comms-2.2.1.tar.gz"

    license("BSD-3-Clause")

    version("3.0.4", sha256="d70e17555f7262c4884a6b7bc9ca19cb816507a032a334d9cb411b4546caff4c")
    version("2.2.1", sha256="a26145b8ce43d2d934b3c6826d77b913ce105c528eb2e494c890b3e3525ddf33")

    depends_on("py-setuptools@40.8:60", type="build", when="@2.2.1")

    depends_on("py-hatchling@1.5.0:", type="build", when="@3.0.4:")
    depends_on("py-hatch-nodejs-version", type="build", when="@3.0.4:")
    depends_on("py-jupyterlab@4.0.0:4", type="build", when="@3.0.4:")

    depends_on("py-param", type=("build", "run"))

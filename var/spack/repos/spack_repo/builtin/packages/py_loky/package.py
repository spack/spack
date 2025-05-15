# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLoky(PythonPackage):
    """Reusable Process Pool Executor"""

    homepage = "https://loky.readthedocs.io"
    pypi = "loky/loky-3.5.1.tar.gz"

    license("BSD-3-Clause", checked_by="RobertMaaskant")

    version("3.5.1", sha256="bcd1d718f005d06b099da856305cb337be36f552d49794f0b86df628a885eefe")

    depends_on("py-setuptools", type="build")
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"))

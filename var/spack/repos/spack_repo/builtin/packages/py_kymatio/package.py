# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyKymatio(PythonPackage):
    """Wavelet scattering transforms in Python with GPU acceleration."""

    homepage = "https://www.kymat.io"
    url = "https://files.pythonhosted.org/packages/py3/k/kymatio/kymatio-0.3.0-py3-none-any.whl"

    maintainers("LydDeb")

    license("BSD-3-Clause", checked_by="LydDeb")

    version("0.3.0", sha256="e517113bc98a52795144eb80549f0686ee8a57dbbd9839b935f10dbceba0ec6b")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-appdirs", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))

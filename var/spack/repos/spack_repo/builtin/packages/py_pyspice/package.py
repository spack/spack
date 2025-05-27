# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspice(PythonPackage):
    """Simulate electronic circuit using Python and the Ngspice / Xyce simulators"""

    homepage = "https://github.com/PySpice-org/PySpice"
    pypi = "PySpice/PySpice-1.5.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0", checked_by="LydDeb")

    version("1.5", sha256="d28448accad98959e0f5932af8736e90a1f3f9ff965121c6881d24cdfca23d22")

    depends_on("c", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@5.3:", type=("build", "run"))
    depends_on("py-cffi@1.14:", type=("build", "run"))
    depends_on("py-matplotlib@3.2:", type=("build", "run"))
    depends_on("py-numpy@1.18:", type=("build", "run"))
    depends_on("py-ply@3.11:", type=("build", "run"))
    depends_on("py-scipy@1.4:", type=("build", "run"))
    depends_on("py-requests@2.23:", type=("build", "run"))

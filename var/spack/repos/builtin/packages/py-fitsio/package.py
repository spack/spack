# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFitsio(PythonPackage):
    """A python package for FITS input/output wrapping cfitsio"""

    homepage = "https://github.com/esheldon/fitsio"
    pypi = "fitsio/fitsio-1.2.5.tar.gz"

    license("GPL-2.0-or-later", checked_by="lgarrison")

    version("1.2.5", sha256="001e8689cf82229e19bc20e62494b1eba777aaca7471723ba67a4bac24fdd0d6")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("cfitsio@4.4.1:", type=("build", "link", "run"))

    def setup_build_environment(self, env):
        env.set("FITSIO_USE_SYSTEM_FITSIO", "1")

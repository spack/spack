# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdfAstropy(PythonPackage):
    """ASDF serialization support for astropy"""

    homepage = "https://asdf-astropy.readthedocs.io/"
    pypi = "asdf_astropy/asdf_astropy-0.7.1.tar.gz"

    license("BSD-3-Clause", checked_by="lgarrison")

    version("0.7.1", sha256="5aa5a448ee0945bd834a9ba8fb86cf43b39e85d24260e1339b734173ab6024c7")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-setuptools@60:", type="build")
    depends_on("py-setuptools-scm@3.4: +toml", type="build")

    depends_on("py-asdf@2.14.4:", type=("build", "run"))
    depends_on("py-asdf-coordinates-schemas@0.3:", type=("build", "run"))
    depends_on("py-asdf-transform-schemas@0.5:", type=("build", "run"))
    depends_on("py-asdf-standard@1.1.0:", type=("build", "run"))
    # depends_on("py-astropy@5.2.0:", type=("build", "run"))
    conflicts("py-astropy@:5.1")
    depends_on("py-numpy@1.24:", type=("build", "run"))
    depends_on("py-packaging@19:", type=("build", "run"))

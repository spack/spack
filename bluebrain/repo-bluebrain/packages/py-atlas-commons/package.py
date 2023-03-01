# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasCommons(PythonPackage):
    """Library containing common functions to build atlases"""

    homepage = "https://github.com/BlueBrain/atlas-commons"
    git = "https://github.com/BlueBrain/atlas-commons.git"
    pypi = "atlas-commons/atlas-commons-0.1.4.tar.gz"

    version("develop", branch="main")
    version("0.1.4", sha256="ceff16f6dbad374dfde40b11f3ce59200e484710aa0e17d05d1f45c2167cf2cb")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:", type=("build", "run"))
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))

    depends_on("py-pytest", type="test")

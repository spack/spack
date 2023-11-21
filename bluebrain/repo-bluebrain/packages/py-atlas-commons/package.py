# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasCommons(PythonPackage):
    """Library containing common functions to build atlases"""

    homepage = "https://github.com/BlueBrain/atlas-commons"
    git = "https://github.com/BlueBrain/atlas-commons.git"
    pypi = "atlas-commons/atlas-commons-0.1.4.tar.gz"

    version("develop", branch="main")
    version("0.1.5", sha256="52c4ac8a86122b7a0d3783ffe971b0cc91ed98b7e79faee1ab3b6287f58a9183")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:", type=("build", "run"))
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))

    depends_on("py-pytest", type="test")

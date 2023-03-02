# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasPlacementHints(PythonPackage):
    """Library containing command lines and tools to compute placement hints"""

    homepage = "https://github.com/BlueBrain/atlas-placement-hints"
    git = "https://github.com/BlueBrain/atlas-placement-hints.git"
    pypi = "atlas-placement-hints/atlas-placement-hints-0.1.1.tar.gz"

    version("develop", branch="main")
    version("0.1.1", sha256="81d5dcaf5dec607f7a81f730f9e6b9b9567e1e23dabe78d5b397e46564676fb1")

    depends_on("py-atlas-commons@0.1.4:", type=("build", "run"))
    depends_on("py-cached-property@1.5.2", type=("build", "run"))
    depends_on("py-cgal-pybind@0.1.4:", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-networkx@2.4:", type=("build", "run"))
    depends_on("py-numpy@1.15.0:", type=("build", "run"))
    depends_on("py-pytest", type="test")
    depends_on("py-rtree@0.8.3:", type=("build", "run"))
    depends_on("py-scipy@1.4.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-tqdm@4.44.1:", type=("build", "run"))
    depends_on("py-trimesh@2.38.10:", type=("build", "run"))
    depends_on("py-voxcell@3.0.0:", type=("build", "run"))
    depends_on("ultraliser@0.2.0:", type="run")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests/app/test_placement_hints.py")

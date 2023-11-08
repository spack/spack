# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtlasAnalysis(PythonPackage):
    """Python library to analyze atlases."""

    homepage = "https://bbpgitlab.epfl.ch/nse/atlas-analysis"
    git = "ssh://git@bbpgitlab.epfl.ch/nse/atlas-analysis.git"

    version("develop", branch="main")
    version("0.0.6", tag="atlas-analysis-v0.0.6")

    depends_on("nlohmann-json", type=("build", "run"))
    depends_on("py-click@7.0:", type=("build", "run"))
    depends_on("py-geomdl@5.2.8:", type=("build", "run"))
    depends_on("py-numpy@1.16.3:", type=("build", "run"))
    depends_on("py-networkx@2.3:", type=("build", "run"))
    depends_on("py-pathos@0.2.3:", type=("build", "run"))
    depends_on("py-plotly-helper@0.0.2:", type=("build", "run"))
    depends_on("py-pyquaternion@0.9.5:", type=("build", "run"))
    depends_on("py-scikit-image@0.16.1:", type=("build", "run"))
    depends_on("py-scipy@1.2.1:", type=("build", "run"))
    depends_on("py-voxcell@2.6.2:", type=("build", "run"))
    depends_on("vtk+python@8.1.2:", type=("build", "run"))

# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbaDataPush(PythonPackage):
    """CLIs that take in input atlas pipeline datasets and push them into Nexus"""

    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push"
    git = "ssh://git@bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push.git"

    version("1.0.4", tag="v1.0.4")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-nexusforge", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-pynrrd", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))

    depends_on("py-pytest", type=("test", "build", "run"))
    depends_on("py-pytest-cov", type=("test", "build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")

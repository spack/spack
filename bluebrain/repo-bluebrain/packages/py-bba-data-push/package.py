# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBbaDataPush(PythonPackage):
    """CLIs that take in input atlas pipeline datasets and push them into Nexus"""

    homepage = "https://bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push"
    git = "ssh://git@bbpgitlab.epfl.ch/dke/apps/blue_brain_atlas_nexus_push.git"

    version("3.0.0", tag="v3.0.0")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-nexusforge@0.8.1", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-pynrrd", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-voxcell", type=("build", "run"))

    depends_on("py-pytest", type=("test", "build", "run"))
    depends_on("py-pytest-cov", type=("test", "build", "run"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")

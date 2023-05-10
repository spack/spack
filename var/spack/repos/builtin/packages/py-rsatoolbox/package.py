# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRsatoolbox(PythonPackage):
    """Representational Similarity Analysis (RSA) in Python."""

    homepage = "https://github.com/rsagroup/rsatoolbox"
    pypi = "rsatoolbox/rsatoolbox-0.0.3.tar.gz"
    git = "https://github.com/rsagroup/rsatoolbox.git"

    rsatoolbox_sha256 = {
        # rsatoolbox version - python version: sha256sum
        # 0.1.2
        "0.1.2-cp310": "ab37201de70f82b9ac85c42e036ca82acf38db301c2cbd8b793a236854b146ce",
        "0.1.2-cp39": "2f63b204628d2935f4c2e2f739335ac0c75565ac524e7d03c41064f1fe7192b2",
        "0.1.2-cp38": "69384a81ac4801b446afafe4a178633953ea4123b568f15afcabd5a2dce00e71",
        "0.1.2-cp37": "41058a58c4e39bf2ed3fa948d7c4b450fcee9f18185a5e64d6ebeed02df0035b",
        # 0.1.0
        "0.1.0-cp310": "516807da721cdc06e09e2d2e419c87106bb456d7e79d07701ee7bc47908e3e45",
        "0.1.0-cp39": "e7e67633d4b0f274387ef5fdc168b08d59f17f0d4e673df3b5583e5eb6313a77",
        "0.1.0-cp38": "f0d996d834d9b763fc278cbfbf662c1b9b2d298585a93528cacb6973c31c90ec",
        "0.1.0-cp37": "6380386f903d68888a8f238833a203a78b83315bef402e36e4cde2aa74239cab",
        # 0.0.5
        "0.0.5-cp310": "07623d15ca124243a592a35113d05486620555356012d3040ffb78eb03701915",
        "0.0.5-cp39": "2239762b9d9a419098dafd1e79079beb91d572f832c2f34edb64f8c9a7b45017",
        "0.0.5-cp38": "e858f3ccb1e5439f82aba66676251dfc3a884437a488e0c2dfc24e20a7792b99",
        "0.0.5-cp37": "db31c08fb4b448d229d3b0e682cb15f595f543fca26506bf5abc810fd1e89573",
    }

    version("main", branch="main")
    for pkg_version, sha in rsatoolbox_sha256.items():
        version(pkg_version, sha256=sha, expand=False)
    version("0.0.4", sha256="84153fa4c686c95f3e83f2cb668b97b82b53dc2a565856db80aa5f8c96d09359")
    version("0.0.3", sha256="9bf6e16d9feadc081f9daaaaab7ef38fc1cd64dd8ef0ccd9f74adb5fe6166649")

    for ver in ["0.0.5", "0.1.0", "0.1.2"]:
        conflicts("^python@:3.9,3.11:", when="@{0}-cp310".format(ver))
        conflicts("^python@:3.8,3.10:", when="@{0}-cp39".format(ver))
        conflicts("^python@:3.7,3.9:", when="@{0}-cp38".format(ver))
        conflicts("^python@:3.6,3.8:", when="@{0}-cp37".format(ver))

    @when("@0.0.5:")
    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/r/rsatoolbox/rsatoolbox-{1}-{0}-{0}-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"

        if self.spec["python"].satisfies("@3.10"):
            python_tag = "cp310"
        elif self.spec["python"].satisfies("@3.9"):
            python_tag = "cp39"
        elif self.spec["python"].satisfies("@3.8"):
            python_tag = "cp38"
        elif self.spec["python"].satisfies("@3.7"):
            python_tag = "cp37"

        return url.format(python_tag, str(version).split("-")[0])

    depends_on("python@:3.10", when="@0.0.5:", type=("build", "run"))

    # build dependencies for versions @0.0.5: can not be concretized with
    # the current concretizer
    # depends_on("py-setuptools@65.3:65", when="@0.0.5:", type="build")
    depends_on("py-setuptools", type="build")
    # depends_on("py-setuptools-scm+toml@7.0.0:7.0", when="@0.0.5:", type="build")
    # depends_on("py-cython@3.0.0:3.0", when="@0.0.5:", type="build")
    # depends_on("py-twine@4.0.1:4.0", when="@0.0.5:", type="build")

    depends_on("py-numpy@1.21.2:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-scikit-learn", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-pandas", when="@0.0.4:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))

    # old dependcies
    depends_on("py-coverage", when="@:0.1.1", type=("build", "run"))
    depends_on("py-petname@2.2", when="@0.0.4", type=("build", "run"))

    @when("@:0.0.3")
    def patch(self):
        # tests are looking for a not existing requirements.txt file
        with working_dir("tests"):
            open("requirements.txt", "a").close()

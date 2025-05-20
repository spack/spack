# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyMultiprocess(PythonPackage):
    """Better multiprocessing and multithreading in Python"""

    homepage = "https://github.com/uqfoundation/multiprocess"
    pypi = "multiprocess/multiprocess-0.70.17.tar.gz"

    license("BSD-3-Clause")

    version("0.70.17", sha256="4ae2f11a3416809ebc9a48abfc8b14ecce0652a0944731a1493a3c1ba44ff57a")
    version("0.70.16", sha256="161af703d4652a0e1410be6abccecde4a7ddffd19341be0a7011b94aeb171ac1")
    version("0.70.15", sha256="f20eed3036c0ef477b07a4177cf7c1ba520d9a2677870a4f47fe026f0cd6787e")
    version("0.70.14", sha256="3eddafc12f2260d27ae03fe6069b12570ab4764ab59a75e81624fac453fbf46a")
    version("0.70.13", sha256="2e096dd618a84d15aa369a9cf6695815e5539f853dc8fa4f4b9153b11b1d0b32")
    version("0.70.12.2", sha256="206bb9b97b73f87fec1ed15a19f8762950256aa84225450abc7150d02855a083")
    version("0.70.9", sha256="9fd5bd990132da77e73dec6e9613408602a4612e1d73caf2e2b813d2b61508e5")
    version("0.70.7", sha256="46479a327388df8e77ad268892f2e73eac06d6271189b868ce9d4f95474e58e3")
    version(
        "0.70.5",
        sha256="c4c196f3c4561dc1d78139c3e73709906a222d2fc166ef3eef895d8623df7267",
        url="https://files.pythonhosted.org/packages/multiprocess/multiprocess-0.70.5.zip",
    )
    version(
        "0.70.4",
        sha256="a692c6dc8392c25b29391abb58a9fbdc1ac38bca73c6f27d787774201e68e12c",
        url="https://files.pythonhosted.org/packages/multiprocess/multiprocess-0.70.4.zip",
    )

    depends_on("python@2.5:2.8,3.1:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", when="@0.70.12.2:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.7:", when="@0.70.13:", type=("build", "run"))
    depends_on("python@3.7:", when="@0.70.14:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.70.16:", type=("build", "run"))

    depends_on("py-setuptools@0.6:", type="build")
    depends_on("py-dill@0.2.6:", type=("build", "run"))
    depends_on("py-dill@0.2.9:", type=("build", "run"), when="@0.70.7:")
    depends_on("py-dill@0.3.1:", type=("build", "run"), when="@0.70.9:")
    depends_on("py-dill@0.3.4:", type=("build", "run"), when="@0.70.12.2:")
    depends_on("py-dill@0.3.5.1:", type=("build", "run"), when="@0.70.13:")
    depends_on("py-dill@0.3.6:", type=("build", "run"), when="@0.70.14:")
    depends_on("py-dill@0.3.7:", type=("build", "run"), when="@0.70.15:")
    depends_on("py-dill@0.3.8:", type=("build", "run"), when="@0.70.16:")
    depends_on("py-dill@0.3.9:", type=("build", "run"), when="@0.70.17:")

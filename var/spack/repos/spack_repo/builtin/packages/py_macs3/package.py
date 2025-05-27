# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyMacs3(PythonPackage):
    """MACS: Model-based Analysis for ChIP-Seq"""

    homepage = "https://github.com/macs3-project/MACS/"
    pypi = "MACS3/macs3-3.0.2.tar.gz"

    maintainers("snehring")

    license("BSD-3-Clause")

    version("3.0.3", sha256="ee1c892901c4010ff9e201b433c0623cbd747a3058300322386a7185623b1684")
    version("3.0.0b3", sha256="caa794d4cfcd7368447eae15878505315dac44c21546e8fecebb3561e9cee362")

    def url_for_version(self, version):
        if version < Version("3.0.2"):
            url_fmt = "https://files.pythonhosted.org/packages/b1/88/df5436ec1510d635e7c41f2aee185da35d6d98ccde9bf1ec5a67ad2bbd62/MACS3-{}.tar.gz"
            return url_fmt.format(version)
        return super().url_for_version(version)

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@68.0:", when="@3.0.2:", type="build")
    depends_on("py-setuptools@60.0:", when="@:3.0.1", type="build")
    depends_on("py-cython@3.0", when="@3.0.2:", type=("build", "run"))
    depends_on("py-cython@0.29:0", when="@:3.0.1", type=("build", "run"))

    depends_on("py-numpy@1.25:", when="@3.0.3:", type=("build", "run"))
    depends_on("py-numpy@1.24.2:", when="@3.0.1:3.0.2", type=("build", "run"))
    depends_on("py-numpy@1.19:", when="@:3.0.0", type=("build", "run"))
    depends_on("py-scipy@1.12:", when="@3.0.3:", type=("build", "run"))
    depends_on("py-scipy@1.11.4:", when="@3.0.1:3.0.2", type=("build", "run"))
    depends_on("py-cykhash@2", type=("build", "run"))
    depends_on("py-scikit-learn@1.3:", when="@3.0.2:", type=("build", "run"))
    depends_on("py-scikit-learn@1.2.1:", when="@3.0.1", type=("build", "run"))
    depends_on("py-hmmlearn@0.3.2:", when="@3.0.2:", type=("build", "run"))
    depends_on("py-hmmlearn@0.3:", when="@:3.0.1", type=("build", "run"))

    depends_on("zlib-api")
    depends_on("c", type="build")  # generated

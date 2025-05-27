# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPpft(PythonPackage):
    """Distributed and parallel python"""

    homepage = "https://github.com/uqfoundation/ppft"
    pypi = "ppft/ppft-1.6.4.9.tar.gz"

    license("BSD-3-Clause")

    version("1.7.6.9", sha256="73161c67474ea9d81d04bcdad166d399cff3f084d5d2dc21ebdd46c075bbc265")
    version("1.7.6.8", sha256="76a429a7d7b74c4d743f6dba8351e58d62b6432ed65df9fe204790160dab996d")
    version("1.7.6.7", sha256="ab34436814e2f18238f35688fd869b2641b2d2d8dca22b8d246f6701dfc954c8")
    version("1.7.6.6", sha256="f933f0404f3e808bc860745acb3b79cd4fe31ea19a20889a645f900415be60f1")
    version("1.7.6.5", sha256="47e0dab87a516c0b9992cd5b0c908348e4c7d964304d106b227fad28ae03219e")
    version("1.6.6.4", sha256="473442cc6731856990bd25bd6b454bb98720007de4523a73c560bdd0060463d2")
    version("1.6.4.9", sha256="5537b00afb7b247da0f59cc57ee5680178be61c8b2e21b5a0672b70a3d247791")
    version("1.6.4.7.1", sha256="f94b26491b4a36adc975fc51dba7568089a24756007a3a4ef3414a98d7337651")
    version("1.6.4.6", sha256="92d09061f5425634c43dbf99c5558f2cf2a2e1e351929f8da7e85f4649c11095")
    version("1.6.4.5", sha256="d47da9d2e553848b75727ce7c510f9e149965d5c68f9fc56c774a7c6a3d18214")

    depends_on("python@2.5:2.8,3.1:", type=("build", "run"))
    depends_on("python@2.7:2.8,3.6:", when="@1.6.6.4:", type=("build", "run"))

    depends_on("py-setuptools@0.6:", type="build")
    depends_on("py-six@1.7.3:", type=("build", "run"), when="@:1.7.6.5")
    depends_on("py-dill@0.2.6:", type=("build", "run"))
    depends_on("py-dill@0.3.4:", type=("build", "run"), when="@1.6.6.4:")
    depends_on("py-dill@0.3.5:", type=("build", "run"), when="@1.7.6.5")
    depends_on("py-dill@0.3.6:", type=("build", "run"), when="@1.7.6.6")
    depends_on("py-dill@0.3.7:", type=("build", "run"), when="@1.7.6.7")
    depends_on("py-dill@0.3.8:", type=("build", "run"), when="@1.7.6.8")
    depends_on("py-dill@0.3.9:", type=("build", "run"), when="@1.7.6.9")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/p/ppft/"
        if version >= Version("1.6.4.8"):
            url += "ppft-{0}.tar.gz"
        else:
            url += "ppft-{0}.zip"

        url = url.format(version)
        return url

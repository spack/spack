# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCharsetNormalizer(PythonPackage):
    """The Real First Universal Charset Detector. Open, modern and actively
    maintained alternative to Chardet."""

    homepage = "https://github.com/jawah/charset_normalizer"
    pypi = "charset-normalizer/charset-normalizer-2.0.7.tar.gz"

    license("MIT")

    version("3.4.2", sha256="5baececa9ecba31eff645232d59845c07aa030f0c81ee70184a90d35099a0e63")
    version("3.3.0", sha256="63563193aec44bce707e0c5ca64ff69fa72ed7cf34ce6e11d5127555756fd2f6")
    version("3.1.0", sha256="34e0a2f9c370eb95597aae63bf85eb5e96826d81e3dcf88b8886012906f509b5")
    version("2.1.1", sha256="5a3d016c7c547f69d6f81fb0db9449ce888b418b5b9952cc5e6e66843e9dd845")
    version("2.0.12", sha256="2857e29ff0d34db842cd7ca3230549d1a697f96ee6d3fb071cfa6c7393832597")
    version("2.0.7", sha256="e019de665e2bcf9c2b64e2e5aa025fa991da8720daa3c1138cadd2fd1856aed0")

    with default_args(type="build"):
        depends_on("py-setuptools")
        depends_on("py-setuptools-scm", when="@3.4.2:")
        depends_on("py-mypy@1.4.1:1.15.0", when="@3.4.2:")

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3.13", when="@3.4:")
        depends_on("python@3.7:3.12", when="@3.2:3.3")
        depends_on("python@3.7:3.11", when="@3.1")
        depends_on("python@3.6:3.11", when="@2.1:3.0")
        depends_on("python@3.5:3.11", when="@2.0.11:2.0.12")
        depends_on("python@3.5:3.10", when="@1.3.5:2.0.10")

    def url_for_version(self, version):
        if version >= Version("3.4.0"):
            url = "https://files.pythonhosted.org/packages/source/c/charset_normalizer/charset_normalizer-{0}.tar.gz"
        else:
            url = "https://files.pythonhosted.org/packages/source/c/charset-normalizer/charset-normalizer-{0}.tar.gz"
        return url.format(version)

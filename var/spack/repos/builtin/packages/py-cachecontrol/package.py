# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCachecontrol(PythonPackage):
    """CacheControl is a port of the caching algorithms in httplib2
    for use with requests session object."""

    homepage = "https://github.com/ionrock/cachecontrol"
    pypi = "CacheControl/CacheControl-0.12.10.tar.gz"

    version("0.13.1", sha256="f012366b79d2243a6118309ce73151bf52a38d4a5dac8ea57f09bd29087e506b")
    version("0.12.11", sha256="a5b9fcc986b184db101aa280b42ecdcdfc524892596f606858e0b7a8b4d9e144")
    version("0.12.10", sha256="d8aca75b82eec92d84b5d6eb8c8f66ea16f09d2adb09dbca27fe2d5fc8d3732d")

    variant("filecache", default=False, description="Add lockfile dependency")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.13.0", type="build")
    depends_on("py-flit-core@3.2:3", when="@0.13.1:", type="build")
    depends_on("py-requests@2.16.0:", when="@0.13.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-msgpack@0.5.2:", type=("build", "run"))
    depends_on("py-filelock@3.8.0:", when="@0.13.1: +filecache", type="run")
    depends_on("py-lockfile@0.9:", when="@:0.13.0 +filecache", type="run")

    def url_for_version(self, version):
        if version <= Version("0.13.0"):
            url = "https://files.pythonhosted.org/packages/source/c/cachecontrol/CacheControl-{}.tar.gz"
        elif version > Version("0.13.0"):
            url = "https://files.pythonhosted.org/packages/source/c/cachecontrol/cachecontrol-{}.tar.gz"
        return url.format(version)

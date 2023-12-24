# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApacheLibcloud(PythonPackage):
    """Python library for multiple cloud provider APIs"""

    homepage = "https://libcloud.apache.org"
    pypi = "apache-libcloud/apache-libcloud-1.2.1.tar.gz"

    version("3.8.0", sha256="75bf4c0b123bc225e24ca95fca1c35be30b19e6bb85feea781404d43c4276c91")
    version("3.7.0", sha256="148a9e50069654432a7d34997954e91434dd38ebf68832eb9c75d442b3e62fad")
    version("1.2.1", sha256="b26b542c6c9785dd4e34892d87421ffa4c043335c1cba301a97a8d9748c423f2")

    depends_on("py-setuptools", type="build")

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingExtensions(PythonPackage):
    """The typing_extensions module contains both backports of these
    changes as well as experimental types that will eventually be
    added to the typing module, such as Protocol (see PEP 544 for
    details about protocols and static duck typing)."""

    homepage = "https://github.com/python/typing/tree/master/typing_extensions"
    pypi = "typing_extensions/typing_extensions-3.7.4.tar.gz"

    version("4.3.0", sha256="e6d2677a32f47fc7eb2795db1dd15c1f34eff616bcaf2cfb5e997f854fa1c4a6")
    version("4.2.0", sha256="f1c24655a0da0d1b67f07e17a5e6b2a105894e6824b92096378bb3668ef02376")
    version("4.1.1", sha256="1a9462dcc3347a79b1f1c0271fbe79e844580bb598bafa1ed208b94da3cdcd42")
    version("3.10.0.2", sha256="49f75d16ff11f1cd258e1b988ccff82a3ca5570217d7ad8c5f48205dd99a677e")
    version("3.10.0.0", sha256="50b6f157849174217d0656f99dc82fe932884fb250826c18350e159ec6cdf342")
    version("3.7.4.3", sha256="99d4073b617d30288f569d3f13d2bd7548c3a7e4c8de87db09a9d29bb3a4a60c")
    version("3.7.4", sha256="2ed632b30bb54fc3941c382decfd0ee4148f5c591651c9272473fea2c6397d95")
    version("3.7.2", sha256="fb2cd053238d33a8ec939190f30cfd736c00653a85a2919415cecf7dc3d9da71")
    version("3.6.6", sha256="51e7b7f3dcabf9ad22eed61490f3b8d23d9922af400fe6656cb08e66656b701f")

    # typing-extensions 4+ uses flit
    depends_on("python@3.7:", when="@4.2:", type=("build", "run"))
    depends_on("python@3.6:", when="@4:", type=("build", "run"))
    depends_on("py-flit-core@3.4:3", when="@4:", type="build")

    # typing-extensions 3 uses setuptools
    depends_on("python@2.7:2.8,3.4:", when="@:3", type=("build", "run"))
    depends_on("py-setuptools", when="@:3", type="build")

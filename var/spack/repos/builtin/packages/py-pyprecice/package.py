# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyprecice(PythonPackage):
    """
    This package provides python language bindings for the
    C++ library preCICE.
    """

    homepage = "https://precice.org"
    git = "https://github.com/precice/python-bindings.git"
    url = "https://github.com/precice/python-bindings/archive/v2.4.0.0.tar.gz"
    maintainers("ajaust", "BenjaminRodenberg", "IshaanDesai")

    # Always prefer final version of release candidate
    version("develop", branch="develop")
    version("2.5.0.2", sha256="6d7b78da830db6c5133b44617196ee90be8c7d6c8e14c8994a4800b3d4856416")
    version("2.5.0.1", sha256="e2602f828d4f907ea93e34f7d4adb8db086044a75a446592a4099423d56ed62c")
    version("2.5.0.0", sha256="9f55a22594bb602cde8a5987217728569f16d9576ea53ed00497e9046a2e1794")
    version("2.4.0.0", sha256="e80d16417b8ce1fdac80c988cb18ae1e16f785c5eb1035934d8b37ac18945242")
    version("2.3.0.1", sha256="ed4e48729b662680beaa4ee2a9aff724a79e760534c6c58181be739988da2789")
    version("2.2.1.1", sha256="139bac5077c3807e1b7b83d8d0da5ca0fc8c17393fd0df4bc5999cd63a351b78")
    version("2.2.0.2", sha256="2287185f9ad7500dced53459543d27bb66bd2438c2e4bf81ee3317e6a00513d5")
    version("2.2.0.1", sha256="229625e2e6df03987ababce5abe2021b0974cbe5a588b936a9cba653f4908d4b")
    version("2.1.1.2", sha256="363eb3eeccf964fd5ee87012c1032353dd1518662868f2b51f04a6d8a7154045")
    version("2.1.1.1", sha256="972f574549344b6155a8dd415b6d82512e00fa154ca25ae7e36b68d4d2ed2cf4")
    version("2.1.0.1", sha256="ac5cb7412c6b96b08a04fa86ea38e52d91ea739a3bd1c209baa93a8275e4e01a")
    version("2.0.2.1", sha256="c6fca26332316de041f559aecbf23122a85d6348baa5d3252be4ddcd5e94c09a")
    version("2.0.1.1", sha256="2791e7c7e2b04bc918f09f3dfca2d3371e6f8cbb7e57c82bd674703f4fa00be7")
    version("2.0.0.2", sha256="5f055d809d65ec2e81f4d001812a250f50418de59990b47d6bcb12b88da5f5d7")
    version("2.0.0.1", sha256="96eafdf421ec61ad6fcf0ab1d3cf210831a815272984c470b2aea57d4d0c9e0e")

    for ver in [
        "develop",
        "2.5.0",
        "2.4.0",
        "2.3.0",
        "2.2.1",
        "2.2.0",
        "2.1.1",
        "2.1.0",
        "2.0.2",
        "2.0.1",
        "2.0.0",
    ]:
        depends_on("precice@" + ver, when="@" + ver)

    depends_on("python@3:", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "link", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-cython@0.29:", type="build")
    depends_on("py-packaging", type="build")
    depends_on("py-pip@19.0.0:", type="build")
    depends_on("py-pkgconfig", type="build", when="@2.5:")

    @when("@:2.1")
    def patch(self):
        filter_file("distutils.command.install", "setuptools.command.install", "setup.py")

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQutipQip(PythonPackage):
    """The QuTiP quantum information processing package"""

    homepage = "https://github.com/qutip/qutip-qip"
    pypi = "qutip-qip/qutip-qip-0.2.2.tar.gz"

    version("0.2.3", sha256="b883e91e723b7d192e704d3280ecac222b961e2fc565e966ad140113e535309b")
    version("0.2.2", sha256="c3cd49022684e5b929690c11d15118ab79cb2cd1073a8b6c9cbd2fefcc3ae73e")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-packaging", type="build")

    depends_on("py-numpy@1.12:", type=("build", "run"))
    depends_on("py-scipy@1.0:", type=("build", "run"))

    depends_on("py-qutip@4.5:", type=("build", "run"))

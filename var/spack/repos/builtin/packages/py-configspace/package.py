# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigspace(PythonPackage):
    """Creation and manipulation of parameter configuration spaces for
    automated algorithm configuration and hyperparameter tuning."""

    maintainers("Kerilk")

    homepage = "https://automl.github.io/ConfigSpace/master/"
    pypi = "ConfigSpace/ConfigSpace-0.4.20.tar.gz"

    license("BSD-3-Clause")

    version("0.7.1", sha256="57b5b8e28ed6ee14ecf6206fdca43ca698ef63bc1531f081d482b26acf4edf1a")
    version("0.6.1", sha256="b0a9487c7997481a041feee46f2c8fc9fb9787e1ff553250838d62624dfb0d5a")
    version("0.6.0", sha256="9b6c95d8839fcab220372673214b3129b45dcd8b1179829eb2c65746cacb72a9")
    version("0.5.0", sha256="c8b61fe119829c29c47fc8719bb5f5740ae3034c793040f7bff67dbc9eb9c754")
    version("0.4.21", sha256="09c5ee343f2850865609cc91f2ab27da0a6182f7f196354f9550f6da578ea827")
    version("0.4.20", sha256="2e4ca06f5a6a61e5322a73dd7545468c79f2a3e8385cab92fdada317af41d9e9")

    depends_on("c", type="build")  # generated

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-scipy", when="@0.4.21:")
    depends_on("py-typing-extensions", when="@0.6.0:")
    depends_on("py-more-itertools", when="@0.6.1:")

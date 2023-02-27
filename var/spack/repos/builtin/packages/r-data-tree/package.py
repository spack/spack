# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDataTree(RPackage):
    """Create tree structures from hierarchical data, and traverse the
tree in various orders. Aggregate, cumulate, print, plot, convert to
and from data.frame and more. Useful for decision trees, machine
learning, finance, conversion from and to JSON, and many other
applications."""

    cran="data.tree"

    maintainers = ["viniciusvgp"]

    version("1.0.0", sha256="40674c90a5bd00f5185db9adbd221c6f1114043e69095249f5fa8b3044af3f5e")
    version("0.7.11", sha256="b8b57f9376c2d447f4a55001a780bd8f7d65d3d0b8809e313f876331c73da2d6")
    version("0.7.8", sha256="0b326682946ae60780329f34725a05a343b631964df0a66a14c9367060685b17")
    version("0.7.7", sha256="88f59cf781775165888ae97741a1f9cd9fa6dcc3d6d55db6993b5ee52a954d72")
    version("0.7.6", sha256="b6e3d24d0caee4640d8d41c81c25cf10c78323638ccee1a274ab6642b1e6073b")
    version("0.7.5", sha256="5c1439f071711c8441f7d6a8d439c2cec42cc107d216dec240f3e10b86dcaa1e")
    version("0.7.4", sha256="0eae269988a7039a336a7a15d41355d9b629a6d4773775ce3c28c503982ed37b")
    version("0.7.3", sha256="57f030d78c226b2c345d5045ca14449e8971c95f339983503f3bd755831284e4")
    version("0.7.0", sha256="2b393fe3fb1bed019acf25f7e8bce80922695620777ceb22937f59acfb55f765")
    version("0.6.2", sha256="afe2af6282519f8119bc377d4885cc33d21f8bf4c83a58efc840805644bdecb2")
    version("0.4.0", sha256="dd3a96104d81e29ad78744fc8415cb06c1dc075d78d7137041eed8989c68623a")
    version("0.3.5", sha256="229bd1f2a5db9fad5a634cb9794f8960f1cfb42cd12958e22adec1de81608d6a")
    version("0.3.0", sha256="91ff3b2d8e167fbe0a4631b50df8d6e32c36f156a9e13abe4ee424b86788b246")
    version("0.2.4", sha256="3321a3d1540467bd4aa1f380c2ec962cf0509e561d0e0f77e3f67dfe26a0b61a")
    version("0.2.1", sha256="e9df1b569710659810ca64f5791b12ed0ef008ecf7acfdc9baa3f755a133afc8")
    version("0.2.0-3", sha256="f57b899018fb69c57aea2d7a01963d9b3ae9658b13076168cd533be905691dcb")
    version("0.1.6", sha256="0ce62da1105b92155377e2f094ced399f00079d0eb0ad5b5a9c9c8290b23f326")

    depends_on("r-stringi", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))


# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RArrow(RPackage):
    """'Apache' 'Arrow' <https://arrow.apache.org/> is a cross-language
development platform for in-memory data. It specifies a standardized
language-independent columnar memory format for flat and hierarchical
data, organized for efficient analytic operations on modern
hardware. This package provides an interface to the 'Arrow C++'
library."""

    cran = "arrow"

    maintainers = ["viniciusvgp"]

    version("11.0.0.2", sha256="6b179a2fceb62b676a032d19f9b880a1b6aecb92a5b39669f397385d82201a74")
    version("10.0.0", sha256="e855b5ea913e93935d20be11b342f45193437404945c9fc39e9c61fd91911a13")
    version("9.0.0", sha256="669fd46c700a69e351fa529f967a35c1f305654c1245e5573597e318f2856934")
    version("8.0.0", sha256="6c9aa08c68b7b39cb7d6b9394c0b94a566c0fe9a85cea61f5ed19e460bdb05ad")
    version("7.0.0", sha256="d49ca7f9dba9b2e450d1d864c298e9cd6370171e61ba2cbe2de4c568b81230e9")
    version("6.0.1", sha256="17d49e80d7c2be8ccfabfc2ab192ff0ffad7a2db9915c3c06499c9d8d387cf91")
    version("6.0.0.2", sha256="76808692851eca33ff7ea9532b143db4698689081ce2f8cfe53c3e9e0aee1184")
    version("5.0.0.2", sha256="7204ffce8e917c043facd6282f8b6c17a79743f3f1e85ac22c5208a9556553aa")
    version("5.0.0", sha256="5df61776ebe44a72809aa7d2318a0411220b5bc4a468b7098858db7cb23c3ff5")
    version("4.0.1", sha256="8cae1528a7abf8158f1fe791dc9fb215db54baab23e5d16f88cb8374bb747fa6")
    version("4.0.0.1", sha256="3df039acc986bec6fc4bf7580cb0be1280f7d336b6801922a77a5f842d3526a7")
    version("4.0.0", sha256="81f103825d649bf75f9d450c57822c8ca1982d2e20602a71f259e652813e5fa3")
    version("3.0.0", sha256="d8e18381915066110299ef27c7ddf8e81a83c5f6dc3d7374487f6d929d91ed71")
    version("2.0.0", sha256="28a7e093a1c97ca2b113c6bb534b13d0bab3ab690f3116857aeae8b88e442f59")
    version("1.0.1", sha256="fb92a3fc92a9423aeb0c08e1851de347705a2b424dea56c14cf79c658ba5d6fc")
    version("1.0.0", sha256="736c306e6ab68f3129bda0b05054084de74ff84bbee54d264635f277952e16c8")
    version("0.17.1", sha256="c6de688f1a3282d89c1b4f8f1ebd70c2addbfa7a67e3d41184017d20a7d23aa3")
    version("0.17.0", sha256="e85f0b6cf4b193f5ce0f6bdb1657233568c7207332e7989c3ee920f357bf4c69")
    version("0.16.0.2", sha256="bb8af54298117b6e37089a114d7a69441eb1b732da4134546e257c95b121ecc0")
    version("0.16.0.1", sha256="320a2f68eef7843ab33852ca8056c2d70052b53964bb2fd6cf87f9a2079c9841")
    version("0.16.0", sha256="b5d9c76d1c63931c1242c4c3132b3ccf5b586c3eb8a2b369f5a272bc2f8a7b19")
    version("0.15.1.1", sha256="016e4ed1d2428402353c61023d663e08d7355138340ba392e20eb3d185c0bf61")
    version("0.15.1", sha256="d9eb26f4f20bbb7867bb99e2df22bb0a2f131f6d5430374f5a276a866ddae3f9")
    version("0.15.0", sha256="845a928e9edaa8c2b8689406a386b9ec2e5f3dc15767dd62e63de02b609a7b4e")
    version("0.14.1.1", sha256="2da7962b7c32ec1f108b27ca614764c3bde6fd88519520a5ba6eff0327ce59d4")
    version("0.14.1", sha256="612255f149a79f58cf464599faea6e42dbb65886d3565aa2ea5f08b90e689a33")

    variant('notcran', description="Enable full-featured build.", default=False)

    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))    
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))    
    depends_on("r-assertthat", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"))


    def setup_build_environment(self, env):
        if self.spec.satisfies('+notcran'):
            env.set('NOT_CRAN', True)

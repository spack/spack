# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yafyaml(CMakePackage):
    """
    yet another Fortran (implementation of) YAML

    There is at least one other open source Fortran-based YAML parser.

    The rationale for this one is simply to be compatible with the
    containers in gFTL.  It is not intended to be a complete YAML
    parser, just the subset needed by my own projects.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml"
    url = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml/archive/refs/tags/v1.0.4.tar.gz"
    git = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml.git"

    maintainers("mathomp4", "tclune")

    version("main", branch="main")

    version("1.0.5", sha256="84abad01cdcfe387240844c35e5fb36d5099f657b57a50d5d5909cc567e72200")
    version("1.0.4", sha256="93ba67c87cf96be7ebe479907ca5343251aa48072b2671b8630bd244540096d3")
    version("1.0.3", sha256="cfbc6b6db660c5688e37da56f9f0091e5cafeeaec395c2a038469066c83b0c65")
    version("1.0.2", sha256="1d08d093d0f4331e4019306a3b6cb0b230aed18998692b57931555d6805f3d94")
    version("1.0.1", sha256="706d77c43a9c3d2cbd1030c4bbf6b196ea2e0d84df72b3704035d1b52c408baf")
    version("1.0.0", sha256="19334e924d031445f159602a27a1e6778e8a1bd2ead219accdb397c25706f88e")
    version("1.0-beta8", sha256="0a2ae37f45abaca2e4d8dbc317117eeb08c5652d5d2524f51852d957fd719855")
    version("1.0-beta7", sha256="cf7992818cc2caa86346f6f24c251bcfd96bc68eaacc17da89d997260d9db867")
    version("1.0-beta6", sha256="9d90ffd78ae70e477ed58afa474e214822a3c1a0a86c067ba3e245550108a028")
    version("1.0-beta5", sha256="509487c544f199503b3724c170a6d6cd35c237e8ee23a34e94ee3c056b9e39ee")
    version("1.0-beta4", sha256="42bf9c8517d7867614cc24cc4267c70bbe6f8d62474e22d3552d9cc5aa4fc195")
    version("0.5.1", sha256="7019460314e388b2d556db75d5eb734237a18494f79b921613addb96b7b7ce2f")
    version("0.5.0", sha256="8ac5d41b1020e9311ac87f50dbd61b9f3e3188f3599ce463ad59650208fdb8ad")

    depends_on("gftl-shared")
    depends_on("gftl")
    depends_on("cmake@3.12:", type="build")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

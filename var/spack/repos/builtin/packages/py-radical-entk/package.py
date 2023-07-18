# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalEntk(PythonPackage):
    """RADICAL Ensemble Toolkit is used for developing and executing
    large-scale ensemble-based workflows."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.entk.git"
    pypi = "radical.entk/radical.entk-1.20.0.tar.gz"

    maintainers("andre-merzky")

    version("develop", branch="devel")
    version("1.20.0", sha256="1b9fc470b926a93528fd2a898636bdcd1c565bd58ba47608f9bead811d8a46d7")
    version("1.18.0", sha256="049f70ec7e95819ec0ea706ee6275db04799ceff119dd7b675ef0d36d814de6f")
    version("1.17.0", sha256="695e162b8b6209384660400920f4a2e613d01f0b904e44cfe5b5d012dcc35af9")
    version("1.16.0", sha256="6611b4634ad554651601d9aed3a6d8b8273073da6218112bb472ce51f771ac8e")
    version("1.14.0", sha256="beb6de5625b52b3aeeace52f7b4ac608e9f1bb761d8e9cdfe85d3e36931ce9f3")
    version("1.13.0", sha256="5489338173409777d69885fd5fdb296552937d5a539a8182321bebe273647e1c")
    version("1.12.0", sha256="1ea4814c8324e28cc2b86e6f44d26aaa09c8257ed58f50d1d2eada99adaa17da")
    version("1.11.0", sha256="a912ae3aee4c1a323910dbbb33c87a65f02bb30da94e64d81bb3203c2109fb83")
    version("1.9.0", sha256="918c716ac5eecb012a57452f45f5a064af7ea72f70765c7b0c60be4322b23557")
    version("1.8.0", sha256="47a3f7f1409612d015a3e6633853d31ec4e4b0681aecb7554be16ebf39c7f756")
    version("1.6.7", sha256="9384568279d29b9619a565c075f287a08bca8365e2af55e520af0c2f3595f8a2")

    depends_on("py-radical-utils", type=("build", "run"))
    depends_on("py-radical-pilot", type=("build", "run"))

    depends_on("py-radical-pilot@1.18:", type=("build", "run"), when="@1.20:")

    depends_on("py-radical-utils@1.12:", type=("build", "run"), when="@1.12:")
    depends_on("py-radical-pilot@1.12:1.17", type=("build", "run"), when="@1.12:1.19")

    depends_on("py-radical-utils@:1.11", type=("build", "run"), when="@:1.11")
    depends_on("py-radical-pilot@:1.11", type=("build", "run"), when="@:1.11")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-pika@0.13.0", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-setuptools", type="build")

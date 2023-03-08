# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMypy(PythonPackage):
    """Optional static typing for Python."""

    homepage = "http://www.mypy-lang.org/"
    pypi = "mypy/mypy-0.740.tar.gz"

    maintainers("adamjstewart")

    version("1.1.1", sha256="ae9ceae0f5b9059f33dbc62dea087e942c0ccab4b7a003719cb70f9b8abfa32f")
    version("1.0.1", sha256="28cea5a6392bb43d266782983b5a4216c25544cd7d80be681a155ddcdafd152d")
    version("1.0.0", sha256="f34495079c8d9da05b183f9f7daec2878280c2ad7cc81da686ef0b484cea2ecf")
    version("0.991", sha256="3c0165ba8f354a6d9881809ef29f1a9318a236a6d81c690094c5df32107bde06")
    version("0.990", sha256="72382cb609142dba3f04140d016c94b4092bc7b4d98ca718740dc989e5271b8d")
    version("0.982", sha256="85f7a343542dc8b1ed0a888cdd34dca56462654ef23aa673907305b260b3d746")
    version("0.981", sha256="ad77c13037d3402fbeffda07d51e3f228ba078d1c7096a73759c9419ea031bf4")
    version("0.971", sha256="40b0f21484238269ae6a57200c807d80debc6459d444c0489a102d7c6a75fa56")
    version("0.961", sha256="f730d56cb924d371c26b8eaddeea3cc07d78ff51c521c6d04899ac6904b75492")
    version("0.960", sha256="d4fccf04c1acf750babd74252e0f2db6bd2ac3aa8fe960797d9f3ef41cf2bfd4")
    version("0.950", sha256="1b333cfbca1762ff15808a0ef4f71b5d3eed8528b23ea1c3fb50543c867d68de")
    version("0.942", sha256="17e44649fec92e9f82102b48a3bf7b4a5510ad0cd22fa21a104826b5db4903e2")
    version("0.941", sha256="cbcc691d8b507d54cb2b8521f0a2a3d4daa477f62fe77f0abba41e5febb377b7")
    version("0.940", sha256="71bec3d2782d0b1fecef7b1c436253544d81c1c0e9ca58190aed9befd8f081c5")
    version("0.931", sha256="0038b21890867793581e4cb0d810829f5fd4441aa75796b53033af3aa30430ce")
    version("0.930", sha256="51426262ae4714cc7dd5439814676e0992b55bcc0f6514eccb4cf8e0678962c2")
    version("0.921", sha256="eca089d7053dff45d6dcd5bf67f1cabc311591e85d378917d97363e7c13da088")
    version("0.920", sha256="a55438627f5f546192f13255a994d6d1cf2659df48adcf966132b4379fd9c86b")
    version("0.910", sha256="704098302473cb31a218f1775a873b376b30b4c18229421e9e9dc8916fd16150")
    version("0.900", sha256="65c78570329c54fb40f956f7645e2359af5da9d8c54baa44f461cdc7f4984108")
    version("0.800", sha256="e0202e37756ed09daf4b0ba64ad2c245d357659e014c3f51d8cd0681ba66940a")
    version("0.790", sha256="2b21ba45ad9ef2e2eb88ce4aeadd0112d0f5026418324176fd494a6824b74975")
    version("0.740", sha256="48c8bc99380575deb39f5d3400ebb6a8a1cb5cc669bbba4d3bb30f904e0a0e7d")
    version("0.670", sha256="e80fd6af34614a0e898a57f14296d0dacb584648f0339c2e000ddbf0f4cc2f8d")

    # pyproject.toml
    depends_on("py-setuptools@40.6.2:", when="@0.790:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-wheel@0.30:", when="@0.790:", type="build")
    depends_on("py-typing-extensions@3.10:", when="@0.930:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", when="@0.700:", type=("build", "run"))
    depends_on("py-mypy-extensions@1:", when="@1.1:", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3:", when="@0.930:1.0", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3:0.4", when="@0.700:0.929", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.0:0.4", when="@:0.699", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1", when="@0.920: ^python@:3.7", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1.4", when="@0.900:0.910 ^python@:3.7", type=("build", "run"))
    depends_on("py-typed-ast@1.4.0:1.4", when="@0.700:0.899", type=("build", "run"))
    depends_on("py-typed-ast@1.3.1:1.3", when="@:0.699", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@0.950: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@0.930:0.949", type=("build", "run"))
    depends_on("py-tomli@1.1:2", when="@0.920:0.929", type=("build", "run"))
    depends_on("py-types-psutil", when="@0.981:", type="build")
    depends_on("py-types-setuptools", when="@0.981:", type="build")
    depends_on("py-types-typed-ast@1.5.8:1.5", when="@0.981:", type="build")

    # setup.py
    depends_on("python@3.7:", when="@0.981:", type=("build", "run"))

    # Historical dependencies
    depends_on("py-toml", when="@0.900:0.910", type=("build", "run"))

    # https://github.com/python/mypy/issues/13627
    conflicts("^python@3.10.7:", when="@:0.971")

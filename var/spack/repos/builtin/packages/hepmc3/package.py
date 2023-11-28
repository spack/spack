# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hepmc3(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
    High Energy Physics Monte Carlo generators and simulation."""

    homepage = "https://cern.ch/hepmc"
    url = "https://gitlab.cern.ch/hepmc/HepMC3/-/archive/3.2.1/HepMC3-3.2.1.tar.gz"
    git = "https://gitlab.cern.ch/hepmc/HepMC3.git"

    tags = ["hep"]

    maintainers("vvolkl")

    version("3.2.6", sha256="248f3b5b36dd773844cbe73d51f60891458334b986b259754c59dbf4bbf1d525")
    version("3.2.5", sha256="cd0f75c80f75549c59cc2a829ece7601c77de97cb2a5ab75790cac8e1d585032")
    version("3.2.4", sha256="e088fccfd1a6c2f8e1089f457101bee1e5c7a9777e9d51c6419c8a288a49e1bb")
    version("3.2.3", sha256="8caadacc2c969883cd1f994b622795fc885fb4b15dad8c8ae64bcbdbf0cbd47d")
    version("3.2.2", sha256="0e8cb4f78f804e38f7d29875db66f65e4c77896749d723548cc70fb7965e2d41")
    version("3.2.1", sha256="6e4e4bb5708af105d4bf74efc2745e6efe704e942d46a8042f7dcae37a4739fe")
    version("3.2.0", sha256="f132387763d170f25a7cc9f0bd586b83373c09acf0c3daa5504063ba460f89fc")
    version("3.1.2", sha256="4133074b3928252877982f3d4b4c6c750bb7a324eb6c7bb2afc6fa256da3ecc7")
    version("3.1.1", sha256="2fcbc9964d6f9f7776289d65f9c73033f85c15bf5f0df00c429a6a1d8b8248bb")
    version("3.1.0", sha256="cd37eed619d58369041018b8627274ad790020a4714b54ac05ad1ebc1a6e7f8a")
    # note that version 3.0.0 is not supported
    # conflicts with cmake configuration

    variant("protobuf", default=False, description="Enable Protobuf I/O")
    variant("python", default=False, description="Enable Python bindings")
    variant("rootio", default=False, description="Enable ROOT I/O")
    variant(
        "interfaces",
        default=False,
        description="Install interfaces for some Monte-Carlo Event Gens",
    )

    depends_on("cmake@2.8.9:", type="build")
    depends_on("root", when="+rootio")
    depends_on("protobuf", when="+protobuf")
    depends_on("python", when="+python")

    conflicts("%gcc@9.3.0", when="@:3.1.1")
    patch("ba38f14d8f56c16cc4105d98f6d4540c928c6150.patch", when="@3.1.2:3.2.1 %gcc@9.3.0")

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant
        args = [
            from_variant("HEPMC3_ENABLE_PROTOBUF", "protobuf"),
            from_variant("HEPMC3_ENABLE_PYTHON", "python"),
            from_variant("HEPMC3_ENABLE_ROOTIO", "rootio"),
            from_variant("HEPMC3_INSTALL_INTERFACES", "interfaces"),
            self.define("HEPMC3_ENABLE_TEST", self.run_tests),
        ]

        if "+python" in spec:
            py_ver = spec["python"].version.up_to(2)
            args.extend(
                [
                    from_variant("HEPMC3_PYTHON_VERSIONS", str(py_ver)),
                    from_variant("HEPMC3_Python_SITEARCH" + py_ver.joined, python_platlib),
                ]
            )

        if "+rootio" in spec:
            args.append(self.define("ROOT_DIR", spec["root"].prefix))

        return args

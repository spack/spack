# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# Maintainer comments:
# 18/12/2018: fix python detection
class Tfel(CMakePackage):
    """
    The TFEL project is a collaborative development of CEA
    (French Alternative Energies and Atomic Energy Commission) and
    EDF (Electricite de France).

    It mostly contains the MFront code generator which translates
    a set of closely related domain specific languages into plain C++
    on top of the TFEL libraries. MFront handles material properties,
    mechanical behaviours and simple point-wise models. Interfaces
    are provided for several finite element solvers, such as:
    Abaqus/Standard, Abaqus/Explicit, Ansys APDL, Cast3M,
    Europlexus, Code_Aster, CalculiX and a few others.

    MFront comes with an handy easy-to-use tool called MTest that can
    test the local behaviour of a material, by imposing independent
    constraints on each component of the strain or the stress.
    """

    homepage = "http://tfel.sourceforge.net"
    url = "https://github.com/thelfer/tfel/archive/TFEL-4.0.tar.gz"
    git = "https://github.com/thelfer/tfel.git"
    maintainers("thelfer")

    # development branches
    version("master", branch="master")
    version("rliv-4.0", branch="rliv-4.0")
    version("rliv-3.4", branch="rliv-3.4")
    version("rliv-3.3", branch="rliv-3.3")
    version("rliv-3.2", branch="rliv-3.2")
    version("rliv-3.1", branch="rliv-3.1")
    version("rliv-3.0", branch="rliv-3.0")
    version("rliv-2.0", branch="rliv-2.0")
    version("rliv-1.2", branch="rliv-1.2")

    # released version
    version(
        "4.0.0",
        sha256="7a0c32c8a9cd2fd65cbcb54fff802f303665d7cba5d46f92ff3d55f057c92845",
        preferred=True,
    )
    version("3.4.3", sha256="e58515effe57d473385fe0b592d9e1d1286c0901496c61268d9efd92a2550849")
    version("3.4.2", sha256="f39e65b2282fd3b108081388f161ba662407b192fed68fafe324c7528026a202")
    version("3.4.1", sha256="04cd4257e39e1b05e02b12ad941106fff4d439934bdfe6e950c08bab23e2a4ba")
    version("3.4.0", sha256="176feb4c1726d0f21f4c656b20620dce6f99ab7f5f09a66905aeb643a316bbc1")
    version("3.3.3", sha256="5a1fb43a8086e594e0a7234c1f227e6e005d384fd84affe3acadccb68fe2bbf6")
    version("3.3.2", sha256="17127ffdf92367c10041258f70a88ac3dcb0a7d89c1766a6aa1ebaeb4d03d55d")
    version("3.3.1", sha256="ad07329c25874832fbacc999b5f88d9b9ab84415bc897a6f3cae5b4afcd7661f")
    version("3.3.0", sha256="884ad68b0fbbededc3a602d559433c24114ae4534dc9f0a759d31ca3589dace0")
    version("3.2.6", sha256="ae80c76d92aeae207e307436aed32bbaed913a437ae57b5ee128ce4f543f20a9")
    version("3.2.5", sha256="194e799ca8d2f7ffea25aa3842c48cfc12850c252d851ce03941b5e3ae533b21")
    version("3.2.4", sha256="e7ac7e61fb3e02301285885bb3dc81ca1b09bd6e2929d15c755555d66088fe33")
    version("3.2.3", sha256="ac429c50ad1901d9d6e518a1cf6505d7a404c21d8ad3c6e5b0acecc77f20e3f7")
    version("3.2.2", sha256="69b01ae0d1f9140b619aaa9135948284ff40d4654672c335e55ab4934c02eb43")
    version("3.2.1", sha256="12786480524a7fe86889120fb334fa00211dfd44ad5ec71e2279e7adf1ddc807")
    version("3.2.0", sha256="089d79745e9f267a2bd03dcd8841d484e668bd27f5cc2ff7453634cb39016848")
    version("3.1.10", sha256="635a2507f139bb6d893e0a7bb223cd1d9ddab5dfddee179a3b2e9f8b0b63e065")
    version("3.1.9", sha256="8aeb020beddd125c207271e01d3e7d3985a91268dbf0bbc6132d217cc72b12a8")
    version("3.1.8", sha256="8c99ef80a27b3e791d78de2ceb1111396989942424697eccbc886edc3983163f")
    version("3.1.7", sha256="9cd8beab96c8f9cc5647a3452e61b06968a172f5875a72db227e6148fdbf294c")
    version("3.1.6", sha256="27684884cff441a6c548ffe5d88e35e2b532ed100c97e3125e89c82985a08c50")
    version("3.1.5", sha256="e22cf2110f19666f004b8acda32e87beae74721f82e7f83fd0c4fafb86812763")
    version("3.1.4", sha256="8dc2904fc930636976baaf7e91ac89c0377afb1629c336343dfad8ab651cf87d")
    version("3.1.3", sha256="2022fa183d2c2902ada982ec6550ebe15befafcb748fd988fc9accdde7976a42")
    version("3.1.2", sha256="2eaa191f0699031786d8845ac769320a42c7e035991d82b3738289886006bfba")
    version("3.1.1", sha256="a4c0c21c6c22752cc90c82295a6bafe637b3395736c66fcdfcfe4aeccb5be7af")
    version("3.1.0", sha256="dd67b400b5f157aef503aa3615b9bf6b52333876a29e75966f94ee3f79ab37ad")
    version("3.0.10", sha256="1604f22948b4af6ef84839d97909f7011ce614254e1a6de092ddc61832f7d343")
    version("3.0.9", sha256="461dbb9e78fb6de9eaff21e387f5441020a077bba51d47b6510f11312e5ee333")
    version("3.0.8", sha256="3639f11d14278e20814e8673e097d26161e26117128289516be5b1b1e1387e57")
    version("3.0.7", sha256="4f4e04a1c1f360f27bbd4f72268dd31b46e2cef676ea8d36c35f21569540c76f")
    version("3.0.6", sha256="3359e928dbde0f9ddbc9cd62bd2c2dbafe38543aad68fda9f3768fcc5c219f66")
    version("3.0.5", sha256="abf58f87962cf98b6129e873a841819a2a751f2ebd4e08490eb89fb933cd7887")
    version("3.0.4", sha256="e832d421a0dc9f315c60c5ea23f958dcaa299913c50a4eb73bde0e053067a3cc")
    version("3.0.3", sha256="3ff1c14bcc27e9b615aab5748eaf3afac349050b27b55a2b57648aba28b801ac")
    version("3.0.2", sha256="edd54ac652e99621410137ea2f7f90f133067615a17840440690365e2c3906f5")
    version("3.0.1", sha256="fa239ddd353431954f2ab7443cf85d86c862433e72f7685c1b933ae12dbde435")
    version("3.0.0", sha256="b2cfaa3d7900b4f32f327565448bf9cb8e4242763f651bff8f231f378a278f9e")
    version("2.0.4", sha256="cac078435aad73d9a795516f161b320d204d2099d6a286e786359f484355a43a")

    # solvers interfaces
    variant("castem", default=True, description="Enables Cast3M interface")
    variant("aster", default=True, description="Enables Code_Aster interface")
    variant(
        "abaqus",
        default=True,
        description="Enables Abaqus/Standard and " + "Abaqus/Explicit interfaces",
    )
    variant("calculix", default=True, description="Enables CalculiX interfaces")
    variant("ansys", default=True, description="Enables Ansys APDL interface")
    variant("europlexus", default=True, description="Enables Europlexus interface")
    variant("cyrano", default=True, description="Enables Cyrano interface")
    variant("lsdyna", default=True, description="Enables LS-DYNA interface")
    variant("fortran", default=True, description="Enables fortran interface")
    variant("python", default=True, description="Enables python interface")
    variant("python_bindings", default=True, description="Enables python bindings")
    variant("java", default=False, description="Enables java interface")

    # only since TFEL-3.3, no effect on version below
    variant("comsol", default=True, description="Enables comsol interface")
    variant("diana-fea", default=True, description="Enables DIANA-FEA interface")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    depends_on("java", when="+java")
    depends_on("python", when="+python", type=("build", "link", "run"))
    depends_on("python", when="+python_bindings", type=("build", "link", "run"))
    depends_on("py-numpy", when="+python_bindings", type=("build", "link", "run"))
    # As boost+py has py runtime dependency, boost+py needs types link and run as well:
    depends_on(
        "boost+python+numpy+exception+container",
        when="+python_bindings",
        type=("build", "link", "run"),
    )

    extends("python", when="+python_bindings")

    conflicts("%gcc@:7", when="@4:")

    def cmake_args(self):
        args = []

        args.append("-DUSE_EXTERNAL_COMPILER_FLAGS=ON")

        for i in [
            "fortran",
            "java",
            "aster",
            "abaqus",
            "calculix",
            "ansys",
            "europlexus",
            "cyrano",
            "lsdyna",
            "python",
            "comsol",
            "diana-fea",
        ]:
            if "+" + i in self.spec:
                args.append("-Denable-{0}=ON".format(i))
            else:
                args.append("-Denable-{0}=OFF".format(i))

        if "+castem" in self.spec:
            args.append("-Dlocal-castem-header=ON")
        else:
            args.append("-Dlocal-castem-header=OFF")

        if "+python_bindings" in self.spec:
            args.append("-Denable-python-bindings=ON")
        else:
            args.append("-Denable-python-bindings=OFF")

        if ("+python" in self.spec) or ("+python_bindings" in self.spec):
            python = self.spec["python"]
            args.append("-DPYTHON_LIBRARY={0}".format(python.libs[0]))
            args.append("-DPYTHON_INCLUDE_DIR={0}".format(python.headers.directories[0]))
            args.append("-DPython_ADDITIONAL_VERSIONS={0}".format(python.version.up_to(2)))

        if "+python_bindings" in self.spec:
            args.append("-DBOOST_ROOT={0}".format(self.spec["boost"].prefix))
            args.append("-DBoost_NO_SYSTEM_PATHS=ON")
            args.append("-DBoost_NO_BOOST_CMAKE=ON")

        return args

    def check(self):
        """Skip the target 'test' which doesn't build all test programs used by tests"""
        with working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                self._if_make_target_execute("check")
            elif self.generator == "Ninja":
                self._if_ninja_target_execute("check")

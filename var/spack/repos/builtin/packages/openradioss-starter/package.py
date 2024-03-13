# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class OpenradiossStarter(CMakePackage):
    """
    OpenRadioss is the publicly available open-source code base that a worldwide
    community of researchers, software developers, and industry leaders are
    enhancing every day. OpenRadioss is changing the game by empowering users to
    make rapid contributions that tackle the latest challenges brought on by rapidly
    evolving technologies like battery development, lightweight materials and composites,
    human body models and biomaterials, autonomous driving and flight,
    as well as the desire to give passengers the safest environment possible via virtual testing.
    OpenRadioss Starter is a component of the OpenRadioss that checks the model and
    splits the mesh.
    """

    homepage = "https://www.openradioss.org/"
    git = "https://github.com/OpenRadioss/OpenRadioss.git"

    license("AGPL-3.0-only")

    maintainers("kjrstory")
    version("main", branch="main")

    variant("sp", default=False, description="Using single precision option")
    variant("debug", default=False, description="Debug Option")
    variant("static_link", default=False, description="Static_link Option")

    depends_on("cmake@2.8:", type="build")
    depends_on("perl", type="build")
    depends_on("python", type="build")

    requires(
        "%gcc",
        "%intel",
        "%oneapi",
        "%aocc",
        "%arm",
        policy="one_of",
        msg="Openradioss-starter can be built using GNU Fortran, Intel Fortran, AOCC, \
             or Armflang compilers only.",
    )

    build_directory = "starter"
    root_cmakelists_dir = "starter"

    @property
    def compiler_name(self):
        compiler_mapping = {
            "aocc": "64_AOCC",
            "intel": "64_intel",
            "oneapi": "64_intel",
            "gcc": "64_gf",
            "arm": "a64_gf",
        }
        compiler_name = compiler_mapping[self.spec.compiler.name]
        return compiler_name

    def cmake_args(self):
        args = [
            "-DCMAKE_Fortran_COMPILER={0}".format(spack_fc),
            "-DCMAKE_C_COMPILER={0}".format(spack_cc),
            "-DCMAKE_CPP_COMPILER={0}".format(spack_cxx),
            "-DCMAKE_CXX_COMPILER={0}".format(spack_cxx),
            "-Dsanitize=0",
        ]

        args.append("-Darch=linux" + self.compiler_name)

        if "+sp" in self.spec:
            args.append("-Dprecision=sp")
        else:
            args.append("-Dprecision=dp")

        if "+debug" in self.spec:
            args.append("-Ddebug=1")
        else:
            args.append("-Ddebug=0")

        if "+static_link" in self.spec:
            args.append("-Dstatic_link=1")
        else:
            args.append("-Dstatic_link=0")

        return args

    def install(self, spec, prefix):
        mkdirp(join_path(prefix, "exec"))

        exec_file = "starter_linux" + self.compiler_name

        install(
            join_path(self.stage.source_path, "starter", exec_file),
            join_path(prefix, "exec", exec_file),
        )
        install_tree(
            join_path(self.stage.source_path, "hm_cfg_files"), join_path(prefix, "hm_cfg_files")
        ),
        install_tree(
            join_path(self.stage.source_path, "extlib", "h3d"), join_path(prefix, "extlib", "h3d")
        ),
        install_tree(
            join_path(self.stage.source_path, "extlib", "hm_reader"),
            join_path(prefix, "extlib", "hm_reader"),
        )

    def setup_run_environment(self, env):
        env.set("OPENRADIOSS_PATH", self.prefix)
        env.set("RAD_CFG_PATH", join_path(self.prefix, "hm_cfg_files"))
        env.set("RAD_H3D_PATH", join_path(self.prefix, "extlib", "h3d", "lib", "linux64"))
        env.set("OMP_STACKSIZE", "400m")
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "extlib", "h3d", "linux64"))
        env.prepend_path(
            "LD_LIBRARY_PATH", join_path(self.prefix, "extlib", "hm_reader", "linux64")
        )
        env.prepend_path("PATH", join_path(self.prefix, "exec"))

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AlgebraPlugins(CMakePackage, CudaPackage):
    """Algebra Plugins provides different algebra plugins with minimal
    functionality for the R&D projects detray and traccc."""

    homepage = "https://github.com/acts-project/algebra-plugins"
    url = "https://github.com/acts-project/algebra-plugins/archive/refs/tags/v0.24.0.tar.gz"

    maintainers("HadrienG2", "stephenswat", "wdconinc")

    license("MPL-2.0", checked_by="wdconinc")

    version("0.24.0", sha256="f44753e62b1ba29c28ab86b282ab67ac6028a0f9fe41e599b7fc6fc50b586b62")

    variant("eigen", default=False, description="Include Eigen types in Algebra Plugins")
    variant("fastor", default=False, description="Include Fastor types in Algebra Plugins")
    variant("smatrix", default=False, description="Include Smatrix types in Algebra Plugins")
    variant("vc", default=False, description="Include Vc types in Algebra Plugins")
    variant("vecmem", default=True, description="Include VecMem types in Algebra Plugins")

    depends_on("cmake@3.14:", type="build")

    depends_on("eigen", when="+eigen")
    depends_on("fastor@0.6.3:", when="+fastor")
    depends_on("root", when="+smatrix")
    depends_on("vc@1.4.2:", when="+vc")
    depends_on("vecmem@0.7.0:", when="+vecmem")

    # FIXME: due to #29447, googletest is not available to cmake when building with --test
    # depends_on("googletest", type="test")

    def cmake_args(self):
        def plugin_arg(argtype, plugin, variant):
            arg = f"ALGEBRA_PLUGINS_{argtype}_{plugin.upper()}"
            return self.define_from_variant(arg, variant if variant is not None else plugin)

        def plugin_include(plugin, variant=None):
            return plugin_arg("INCLUDE", plugin, variant)

        def plugin_setup(plugin, variant=None):
            return plugin_arg("SETUP", plugin, variant)

        args = [
            self.define("ALGEBRA_PLUGINS_USE_SYSTEM_LIBS", True),
            self.define("ALGEBRA_PLUGINS_FAIL_ON_WARNINGS", False),
            self.define("ALGEBRA_PLUGINS_BUILD_TESTING", self.run_tests),
            self.define("BUILD_TESTING", self.run_tests),
            self.define("ALGEBRA_PLUGINS_SETUP_BENCHMARK", False),
            self.define("ALGEBRA_PLUGINS_USE_SYSTEM_GOOGLETEST", False),  # see FIXME above
        ]

        for plugin in ["eigen", "fastor", "smatrix", "vc", "vecmem"]:
            args.append(plugin_include(plugin))
            args.append(plugin_setup(plugin))
        # also add misnamed setup flag for eigen
        args.append(plugin_setup("eigen3", "eigen"))

        return args

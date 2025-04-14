# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.builtin.pdi import Pdi


class PdipluginDeclNetcdf(CMakePackage):
    """The trace plugin is intended to generate a trace of  what happens in PDI
    "data store"."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"
    url = "https://github.com/pdidev/pdi/archive/refs/tags/1.8.0.tar.gz"

    license("BSD-3-Clause")

    maintainers("jbigot")

    for v in Pdi.versions:
        version(str(v), **Pdi.versions[v])

    variant("tests", default=False, description="Build tests")
    variant("mpi", default=True, description="Enable parallel NetCDF")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.16.3:", type=("build"))
    depends_on("netcdf-c@4.7.3:4", type=("link"))
    depends_on("netcdf-c+mpi", type=("link"), when="+mpi")
    for v in Pdi.versions:
        depends_on("pdi@" + str(v), type=("link", "run"), when="@" + str(v))
    depends_on("pkgconfig", type=("build"))

    root_cmakelists_dir = "plugins/decl_netcdf"

    def url_for_version(self, version):
        return Pdi.version_url(version)

    def cmake_args(self):
        return [
            "-DINSTALL_PDIPLUGINDIR:PATH={:s}".format(self.prefix.lib),
            self.define_from_variant("BUILD_HDF5_PARALLEL", "mpi"),
            self.define_from_variant("BUILD_NETCDF_PARALLEL", "mpi"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]

    def setup_run_environment(self, env):
        env.prepend_path("PDI_PLUGIN_PATH", self.prefix.lib)

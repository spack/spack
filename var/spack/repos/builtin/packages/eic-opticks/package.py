from spack.package import *


class EicOpticks(CMakePackage, CudaPackage):
    """EIC Opticks package for GPU simulation"""

    homepage = "https://github.com/bnlnpps/eic-opticks"
    url      = "https://github.com/bnlnpps/eic-opticks/archive/tags/1.0.0-rc1.tar.gz"
    git      = "https://github.com/bnlnpps/eic-opticks.git"

    maintainers = ["plexoos"]

    version("1.0.0-rc1", sha256="6c6d13d996bde8e0658f2804a9fe6ea17bb15ca0d40707d64e2afff70da4d294")
    version("esi", branch="esi")

    depends_on("cmake@3.10:", type="build")
    depends_on("geant4")
    depends_on("glew")
    depends_on("glfw")
    depends_on("glm")
    depends_on("glu")
    depends_on("nlohmann-json")
    depends_on("mesa~llvm")
    depends_on("plog")

    # External resource (e.g., an additional dataset, model, or patch file)
    resource(
        name="OptiX",
        url="https://developer.download.nvidia.com/redist/optix/v8.0/OptiX-8.0-Include.zip",
        sha256="ba617fbb61587bac99106dbd6cda5a27c9d178308cc423878ed72b220b8b951c",
        destination="resources",
        placement="optix/include"
    )

    def cmake_args(self):
        args = []
        # Pass the resource path to CMake
        resource_path = self.stage.source_path + "/resources/optix"
        args.append("-DOptiX_INSTALL_DIR={0}".format(resource_path))
        return args

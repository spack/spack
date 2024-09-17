from spack.package import *


class Feelpp(CMakePackage):
    """
    Feel++ is an Open-Source C++ library designed to solve a wide range of
    partial differential equations (PDEs) using advanced Galerkin methods.
    These methods include the finite element method (FEM), spectral element
    method, discontinuous Galerkin methods, and reduced basis methods.

    Feel++ is optimized for high-performance computing, enabling seamless
    parallel computing on large-scale systems, ranging from desktop machines
    to supercomputers with tens of thousands of cores. The library supports
    multi-physics simulations and provides a modular structure to simplify
    the development of applications.
    """

    homepage = "https://docs.feelpp.org"
    url = "https://github.com/feelpp/feelpp/archive/v0.110.2.tar.gz"
    git = "https://github.com/feelpp/feelpp.git"

    license = "LGPL-3.0-or-later AND GPL-3.0-or-later"
    maintainers = ["prudhomm", "vincentchabannes"]

    version("develop", branch="develop")
    version("preset", branch="2284-add-spack-environment-to-the-main-ci")

    # Define variants
    variant("toolboxes", default=False, description="Enable the Feel++ toolboxes")
    variant("mor", default=False, description="Enable Model Order Reduction (MOR)")
    variant("python", default=False, description="Enable Python wrappers")
    variant("quickstart", default=False, description="Enable the quickstart examples")
    variant("tests", default=False, description="Enable the tests")
    
    # MPI Variants
    variant("mpi", default="openmpi4", description="Choose MPI version", values=("openmpi4", "openmpi5", "cray-mpich8", "mpich3", "mpich4"), multi=False)

    # Add variants for C++ standards
    variant("cpp17", default=False, description="Use C++17 standard")
    variant("cpp20", default=True, description="Use C++20 standard")
    variant("cpp23", default=False, description="Use C++23 standard")

    # Conflicts between C++ standard variants
    conflicts("+cpp17", when="+cpp20", msg="Cannot enable both C++17 and C++20")
    conflicts("+cpp17", when="+cpp23", msg="Cannot enable both C++17 and C++23")
    conflicts("+cpp20", when="+cpp23", msg="Cannot enable both C++20 and C++23")

    # Specify dependencies with required versions
    depends_on("cmake@3.21:", type="build")
    depends_on("boost@1.74: +filesystem+iostreams+mpi+multithreaded+shared")
    depends_on("petsc@3.20 +mumps+hwloc+ptscotch +suite-sparse+hdf5 +hypre+kokkos")
    depends_on("llvm@18:", type="build")
    depends_on("slepc")
    depends_on("cln@1.3.6")
    depends_on("fftw")
    depends_on("libunwind")
    depends_on("libzip")
    depends_on("bison")
    depends_on("flex")
    depends_on("pugixml")
    depends_on("gsl")
    depends_on("glpk")
    depends_on("gl2ps")
    depends_on("ruby")
    depends_on("gmsh +opencascade+mmg+fltk")
    depends_on("curl")
    
    # MPI dependencies
    depends_on("openmpi@4.0.0:4.999", when="mpi=openmpi4")
    depends_on("openmpi@5.0.0:5.999", when="mpi=openmpi5")
    depends_on("cray-mpich@8.0.0:8.999", when="mpi=cray-mpich8")
    depends_on("mpich@3.0.0:3.999", when="mpi=mpich3")
    depends_on("mpich@4.0.0:4.999", when="mpi=mpich4")

    # Python dependencies if +python variant is enabled
    depends_on("py-pytest", when="+python")
    depends_on("py-pandas", when="+python")
    depends_on("py-petsc4py", when="+python")
    depends_on("py-slepc4py", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-pybind11", when="+python")
    depends_on("py-sympy", when="+python")
    depends_on("py-plotly", when="+python")
    depends_on("py-scipy", when="+python")
    depends_on("py-tabulate", when="+python")
    depends_on("py-ipykernel", when="+python")
    depends_on("py-mpi4py", when="+python")
    depends_on("python@3.7:", when="+python", type=("build", "run"))

    def get_cpp_version(self):
        """Helper function to determine the C++ standard preset."""
        if "+cpp17" in self.spec:
            return "cpp17"
        elif "+cpp20" in self.spec:
            return "cpp20"
        elif "+cpp23" in self.spec:
            return "cpp23"
        else:
            return "cpp20"  # default

    def get_preset_name(self):
        cpp_version = self.get_cpp_version()
        preset_name = f"feelpp-clang-{cpp_version}-default-release"
        return preset_name

    def cmake_args(self):
        """Define the CMake preset and CMake options based on variants."""
        args = [
            f"--preset={self.get_preset_name()}",
            "-DFEELPP_ENABLE_VTK=OFF",
            "-DFEELPP_ENABLE_OPENTURNS=OFF",
            "-DFEELPP_ENABLE_OMC=OFF",
            "-DFEELPP_ENABLE_ANN=OFF",
            "-DFEELPP_USE_EXTERNAL_CLN=ON",
            self.define_from_variant("FEELPP_ENABLE_QUICKSTART", "quickstart"),
            self.define_from_variant("FEELPP_ENABLE_TESTS", "tests"),
            self.define_from_variant("FEELPP_ENABLE_TOOLBOXES", "toolboxes"),
            self.define_from_variant("FEELPP_ENABLE_MOR", "mor"),
            self.define_from_variant("FEELPP_ENABLE_FEELPP_PYTHON", "python"),
        ]
        return args

    def build(self, spec, prefix):
        cmake = which("cmake")
        cmake("--build", "--preset", self.get_preset_name())

    def install(self, spec, prefix):
        cmake = which("cmake")
        cmake("--build", "--preset", self.get_preset_name(), "-t", "install")

    def test(self, spec, prefix):
        ctest = which("ctest")
        ctest("--preset", self.get_preset_name(), "-R", "qs_laplacian")
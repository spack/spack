# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-shamrock
#
# You can edit this file again by typing:
#
#     spack edit py-shamrock
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Shamrock(CMakePackage):
    """The Shamrock exascale framework for astrophysics"""

    homepage = "https://shamrock-code.github.io/"
    url = "https://github.com/Shamrock-code/Shamrock/releases/download/v2025.05.0/shamrock-2025.05.0.tar"
    git = "https://github.com/Shamrock-code/Shamrock.git"

    maintainers("tdavidcl")

    license("CeCILL Free Software License Agreement v2.1", checked_by="tdavidcl")

    version("main", branch="main", submodules=True)

    version("2025.05.0", sha256="d5d8d13ffdf80ca5245d091ffc793f3bdeb51ec7")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("testing", default=True, description="Enables the build of shared libraries")
    variant("pybindings", default=True, description="Install python bindings")

    depends_on("sycl")
    depends_on("mpi")
    depends_on("python")
    extends("python", when="+pybindings")

    depends_on("ninja", type="build", when="generator=ninja")

    conflicts("^intel-oneapi-runtime", msg="Shamrock supports it but this package does not yet.")

    def cmake_args(self):
        """Main configure step"""

        spec = self.spec

        args = [
            "-DSHAMROCK_ENABLE_BACKEND=SYCL",
        ]

        # switch based on SYCL provider
        sycl_spec = self.spec["sycl"]
        if sycl_spec.satisfies("intel-oneapi"):
            raise ValueError("Unsupported SYCL provider")
        elif sycl_spec.satisfies("hipsycl"):
            
            args+=[
                "-DSYCL_IMPLEMENTATION=ACPPDirect",
            ]

            if sycl_spec.satisfies("hipsycl@:0.9.4"):
                args+=[
                    "-DCMAKE_CXX_COMPILER=syclcc",
                ]
            else:
                args+=[
                    "-DCMAKE_CXX_COMPILER=acpp",
                ]

            hipsycl_root = self.spec["hipsycl"].prefix

            args+=[
                f"-DACPP_PATH={hipsycl_root}",
            ]
        else:
            raise ValueError("Unsupported SYCL provider")

        if "+testing" in spec:
            args+=[
                "-DBUILD_TEST=yes",
            ]

        args+=[
            "-DPYTHON_EXECUTABLE={}".format(spec["python"].command.path),
        ]

        return args

    @run_after("install")
    def install_python_bindigs(self):
        """Copy the .so files to the python site-packages directory"""

        spec = self.spec
        define = self.define
        libdir = spec.prefix.lib

        if self.spec.satisfies("+pybindings"):
            # move shamrock python bindings into expected place
            site_packages = join_path(python_platlib, "shamrock")
            mkdirp(site_packages)

            # Find all .so files in the build directory
            import glob
            so_files = glob.glob(join_path(libdir, "*.so"))

            # Install each .so file to the install directory
            for _f in so_files:
                install(_f, site_packages)

            # Python need a __init__.py file to import properly the .so
            raw_string = "from .shamrock import *\n"
            filename = "__init__.py"
            filepath = join_path(site_packages, filename)
            with open(filepath, 'w') as f:
                f.write(raw_string)

    def test_install(self):
        """Test the install (executable, python bindings)"""

        shamrock = Executable(self.prefix.bin.shamrock)

        shamrock("--help")
        shamrock("--smi")
        shamrock("--smi", "--sycl-cfg", "0:0")

        python("-c", 
            "import shamrock;"
            "shamrock.change_loglevel(125);"
            "shamrock.sys.init('0:0');"
            "shamrock.sys.close()")

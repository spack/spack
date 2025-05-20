# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyGpaw(PythonPackage):
    """GPAW is a density-functional theory (DFT) Python code based on the
    projector-augmented wave (PAW) method and the atomic simulation environment
    (ASE)."""

    homepage = "https://gpaw.readthedocs.io/index.html"
    pypi = "gpaw/gpaw-25.1.0.tar.gz"

    maintainers("alikhamze", "Chronum94")

    license("GPL-3.0-or-later", checked_by="alikhamze")

    version("25.1.0", sha256="80236e779784df3317e7da395dc59ea403bc0213bb3a68d02c17957162e972ea")
    version("24.6.0", sha256="fb48ef0db48c0e321ce5967126a47900bba20c7efb420d6e7b5459983bd8f6f6")
    version("23.9.1", sha256="19a24840b876003528864b7a0b38fc0d456800b83b8666b1f724273660745b47")
    version("23.6.1", sha256="ff56d323a499972c8991770a6ab0334a6dd18df36e9c94360e0aa1ddf8867dfd")
    version("21.1.0", sha256="96843b68e04bd1c12606036c9f99b0ddfa5e6ee08ce46835e6bb347a6bd560a3")
    version("20.10.0", sha256="77c3d3918f5cc118e448f8063af4807d163b31d502067f5cbe31fc756eb3971d")
    version("20.1.0", sha256="c84307eb9943852d78d966c0c8856fcefdefa68621139906909908fb641b8421")
    version("19.8.1", sha256="79dee367d695d68409c4d69edcbad5c8679137d6715da403f6c2500cb2178c2a")
    version("1.3.0", sha256="cf601c69ac496421e36111682bcc1d23da2dba2aabc96be51accf73dea30655c")

    variant("mpi", default=True, description="Build with MPI support")
    variant("scalapack", default=True, description="Build with ScaLAPACK support")
    variant("fftw", default=True, description="Build with FFTW support")
    variant("libvdwxc", default=True, description="Build with libvdwxc support")
    variant("elpa", default=True, description="Build with ELPA support")

    # Build dependencies
    depends_on("c", type="build")
    depends_on("py-setuptools", type="build")

    # Version-agnostic required dependencies
    depends_on("blas")
    depends_on("lapack")

    # Version-specific required dependencies

    with when("@25.1.0:"):
        depends_on("libxc")
        depends_on("python@3.9:", type=("build", "run"))
        depends_on("py-ase@3.23.0:", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy@1.6.0:", type=("build", "run"))

    with when("@24.1.0:24.6.0"):
        depends_on("libxc@:6.2.2")
        depends_on("python@3.8:", type=("build", "run"))
        depends_on("py-ase@3.23.0:", type=("build", "run"))
        depends_on("py-numpy@1.17:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.6.0:", type=("build", "run"))

    with when("@23.6.1:23.9.1"):
        depends_on("libxc@:6.2.2")
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("py-ase@3.22.1:", type=("build", "run"))
        depends_on("py-numpy@1.17:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.6.0:", type=("build", "run"))

    with when("@21.1.0"):
        depends_on("libxc@3:4.3.4")
        depends_on("python@3.6:3.11", type=("build", "run"))
        depends_on("py-ase@3.21.0:", type=("build", "run"))
        depends_on("py-numpy@:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.2.0:", type=("build", "run"))

    with when("@20.10.0"):
        depends_on("libxc@3:4.3.4")
        depends_on("python@3.6:3.11", type=("build", "run"))
        depends_on("py-ase@3.20.1:", type=("build", "run"))
        depends_on("py-numpy@:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.2.0:", type=("build", "run"))

    with when("@20.1.0"):
        depends_on("libxc@3:4.3.4")
        depends_on("python@3.6:3.11", type=("build", "run"))
        depends_on("py-ase@3.19.0:", type=("build", "run"))
        depends_on("py-numpy@:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.2.0:", type=("build", "run"))

    with when("@19.8.1"):
        depends_on("libxc@3:4.3.4")
        depends_on("python@3.5:3.11", type=("build", "run"))
        depends_on("py-ase@3.18.0:", type=("build", "run"))
        depends_on("py-numpy@:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.2.0:", type=("build", "run"))

    with when("@:1.3.0"):
        depends_on("libxc@3:4.3.4")
        depends_on("python@2.6:2.9", type=("build", "run"))
        depends_on("py-ase@3.13.0:", type=("build", "run"))
        depends_on("py-numpy@:1.26.4", type=("build", "run"))
        depends_on("py-scipy@1.2.0:", type=("build", "run"))
        patch("libxc.patch")

    # Variant dependencies
    depends_on("mpi", when="+mpi", type=("build", "link", "run"))
    depends_on("fftw-api", when="+fftw")
    depends_on("scalapack", when="+scalapack")
    depends_on("libvdwxc", when="+libvdwxc")
    # Fixed elpa version due to compilation/linking errors on older and newer versions.
    # Tested for versions @23.6.1:25.1.0
    depends_on("elpa@2022.11.001", when="+elpa")

    def patch(self):
        spec = self.spec
        # For build notes see https://wiki.fysik.dtu.dk/gpaw/install.html

        libxc = spec["libxc"]
        blas = spec["blas"]
        lapack = spec["lapack"]

        # These aren't necessary for newer versions, test if we can remove them compeletely.
        python_include = spec["python"].headers.directories[0]
        numpy_include = join_path(
            self["py-numpy"].module.python_platlib, "numpy", "core", "include"
        )

        libs = blas.libs + lapack.libs + libxc.libs
        include_dirs = [
            python_include,
            numpy_include,
            blas.prefix.include,
            lapack.prefix.include,
            libxc.prefix.include,
        ]
        runtime_library_dirs = []

        bools = ""

        if "+mpi" in spec:
            libs += spec["mpi"].libs
            mpi_include_dirs = repr([spec["mpi"].prefix.include])
            mpi_library_dirs = repr(list(spec["mpi"].libs.directories))
            include_dirs.append(spec["mpi"].prefix.include)

        if "+scalapack" in spec:
            libs += spec["scalapack"].libs
            include_dirs.append(spec["scalapack"].prefix.include)
            # Are these necessary?
            scalapack_macros = repr(
                [("GPAW_NO_UNDERSCORE_CBLACS", "1"), 
                 ("GPAW_NO_UNDERSCORE_CSCALAPACK", "1")]
            )
            bools += "scalapack = True\n"

        if "+fftw" in spec:
            libs += spec["fftw"].libs
            include_dirs.append(spec["fftw"].prefix.include)
            bools += "fftw = True\n"

        if "+libvdwxc" in spec:
            libs += spec["libvdwxc"].libs
            include_dirs.append(spec["libvdwxc"].prefix.include)
            bools += "libvdwxc = True\n"

        if "+elpa" in spec:
            libs += spec["elpa"].libs
            include_dirs.append(spec["elpa"].prefix.include)
            bools += "elpa = True\n"
            runtime_library_dirs += [spec["elpa"].libs.directories]

        lib_dirs = list(libs.directories)
        libs = list(libs.names)
        rpath_str = ":".join(self.rpath)

        if spec.satisfies("@:19.8.1"):
            cfgfile = "customize.py"
        else:
            cfgfile = "siteconfig.py"

        with open(cfgfile, "w") as f:
            f.write(bools)
            f.write(f"libraries = {repr(libs)}\n")
            f.write(f"include_dirs = {repr(include_dirs)}\n")
            f.write(f"library_dirs = {repr(lib_dirs)}\n")
            f.write(f"extra_link_args += ['-Wl,-rpath={rpath_str}']\n")
            if "+mpi" in spec:
                # Do we need this macro for older versions? Newer versions don't seem to.
                f.write("define_macros += [('PARALLEL', '1')]\n")
                f.write(f"compiler='{spec["mpi"].mpicc}'\n")
                f.write(f"mpicompiler = '{spec["mpi"].mpicc}'\n")
                # These may not be needed for versions @23.6.0:
                # We can add logic to only apply them for older versions, but they don't cause problems even when not needed.
                f.write(f"mpi_include_dirs = {mpi_include_dirs}\n")
                f.write(f"mpi_library_dirs = {mpi_library_dirs}\n")
            else:
                f.write(f"compiler='{self.compiler.cc}'\n")
                f.write("mpicompiler = None\n")
            if "+scalapack" in spec:
                f.write(f"define_macros += {scalapack_macros}\n")
            if "+elpa" in spec:
                f.write(f"runtime_library_dirs = {repr(runtime_library_dirs)}")

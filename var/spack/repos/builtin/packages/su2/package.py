# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Su2(MesonPackage):
    """SU2 is a suite of open-source software tools written in C++ for
    the numerical solution of partial differential equations (PDE) and
    performing PDE constrained optimization."""

    maintainers("kjrstory")
    homepage = "https://su2code.github.io"
    url = "https://github.com/su2code/SU2/archive/v7.0.3.tar.gz"
    git = "https://github.com/su2code/SU2.git"

    license("BSD-3-Clause")

    version("7.5.1", commit="09ba9e3a9605c02d38290e34f42aa6982cb4dd05", submodules=True)
    version("7.5.0", commit="8e8ea59fe6225c8ec4e94d0e0a4b6690ea4294e5", submodules=True)
    version("7.4.0", commit="745e5d922c63c8ec6963b31808c20df2e3bfd075", submodules=True)
    version("7.3.1", commit="328a1b747a4785d13b749e7fb6cc4589fd1b9529", submodules=True)
    version("7.2.0", sha256="e929f25dcafc93684df2fe0827e456118d24b8b12b0fb74444bffa9b3d0baca8")
    version("7.1.1", sha256="6ed3d791209317d5916fd8bae54c288f02d6fe765062a4e3c73a1e1c7ea43542")
    version("7.1.0", sha256="deb0abcb10e23a6a41a46c1a2117c4331d68cf97c2fa9c02e10e918973e1c0e7")
    version("7.0.8", sha256="53b6d417e17ff4290a871257b2739a3d9bcd701d37c69e85397efedac93ba17f")
    version("7.0.7", sha256="123c42f097c583a3d7b53123d79bf470f67a6481851fddb010ff590837da61d4")
    version("7.0.6", sha256="5be22a992952b08f16bb80658f6cbe29c62a27e20236eccd175ca58dbc4ed27d")
    version("7.0.5", sha256="3cb2b87ef6ad3d31011756ca1da068fc8172c0d2d1be902fbbd4800b50da28bd")
    version("7.0.4", sha256="abeba82ff922e3b5980944d98eb3ee3fef51ce663c39224a52105798542ef29b")
    version("7.0.3", sha256="7fc01deaad9baabbe0ccd162a4b565172d49e573e79abcb65433b51ff29bda06")
    version("7.0.2", sha256="69e51d52c5a84fb572bd6a83faf8f9fd04471fbf7d5b70d967c7306c1d4e17d9")
    version("7.0.1", sha256="eb0550c82ccaef8cb71e4a8775aa71d2020ef085ec3dd19dfafff5d301034f6f")
    version("7.0.0", sha256="6207dcca15eaebc11ce12b2866c937b4ad9b93274edf6f23d0487948ac3963b8")
    version("6.2.0", sha256="ffc953326e8432a1a6534556a5f6cf086046d3149cfcec6b4e7390eebe30ce2e")

    variant("mpi", default=False, description="enable MPI support")
    variant("openmp", default=False, description="enable OpenMP support")
    variant("tecio", default=True, description="enable TECIO support")
    variant("cgns", default=True, description="enable CGNS support")
    variant("autodiff", default=False, description="enable AD(reverse) support")
    variant("directdiff", default=False, description="enable AD(forward) support")
    variant("pywrapper", default=False, description="enable Python wrapper support")
    variant("mkl", default=False, description="enable Intel MKL support")
    variant("openblas", default=False, description="enable OpenBLAS support")
    variant("mpp", default=False, description="enable Mutation++ support")
    variant(
        "mixedprec",
        default=False,
        description="use single precision floating point arithmetic for sparse algebra",
    )

    depends_on("meson@0.61.1:", type=("build"))
    depends_on("python@3:", type=("build", "run"))
    depends_on("zlib-api")
    depends_on("pkgconfig")
    depends_on("mpi", when="+mpi")
    depends_on("swig", type="build", when="+pywrapper")
    depends_on("py-mpi4py", when="+pywrapper")
    depends_on("intel-oneapi-mkl", when="+mkl")
    depends_on("openblas", when="+openblas ~mkl")
    depends_on("cmake", type="build", when="+mpp")

    # Remove the part that fixes the meson version to 0.61.1.
    # This fix is considered meaningless and will be removed in the next version(@7.6:) of SU2.
    patch("meson_version.patch", when="@7.4.0:7.5.1")

    def meson_args(self):
        args = [
            "-Dwith-omp={}".format("+openmp" in self.spec),
            "-Denable-tecio={}".format("+tecio" in self.spec),
            "-Denable-cgns={}".format("+cgns" in self.spec),
            "-Denable-autodiff={}".format("+autodiff" in self.spec),
            "-Denable-directdiff={}".format("+direcdiff" in self.spec),
            "-Denable-pywrapper={}".format("+pywrapper" in self.spec),
            "-Denable-mkl={}".format("+mkl" in self.spec),
            "-Denable-openblas={}".format("+openblas" in self.spec),
            "-Denable-mpp={}".format("+mpp" in self.spec),
            "-Denable-mixedprec={}".format("+midexprec" in self.spec),
        ]

        if "+mkl" in self.spec:
            args.append("-Dmkl_root=" + self.spec["intel-oneapi-mkl"].prefix)

        if "+mpi" in self.spec:
            args.append("-Dwith-mpi=enabled")
        else:
            args.append("-Dwith-mpi=disabled")

        return args

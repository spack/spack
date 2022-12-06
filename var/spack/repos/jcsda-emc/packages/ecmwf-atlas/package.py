# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EcmwfAtlas(CMakePackage):
    """A library for numerical weather prediction and climate modelling."""

    homepage = "https://software.ecmwf.int/wiki/display/atlas"
    git = "https://github.com/ecmwf/atlas.git"
    url = "https://github.com/ecmwf/atlas/archive/0.22.1.tar.gz"

    maintainers = ["climbfuji", "srherbener"]

    version("master", branch="master")
    version("develop", branch="develop")
    version("0.31.1", sha256="fa9274c74c40c2115b9c6120a7040e357b0c7f37b20b601b684d2a83a479cdfb")
    version("0.31.0", sha256="fa4ff8665544b8e19f79d171c540a9ca8bfc4127f52a3c4d4d618a2fe23354d7")
    version("0.30.0", commit="d81887206fc49c83fd5eb2e0e17457bdcd04731a")
    version("0.29.0", commit="b2558897fa22b18164d4481089423e7b443436f9")
    version("0.27.0", commit="d825fad7ab415558a81415914a0fc60da1d0295a")
    version("0.26.0", commit="3ae6184a598a00fbc6b1a77c3c9d5d808f1c65ea")
    version("0.25.0", commit="3c74adda4960723f237db936132888e3fd380154")
    version("0.24.1", commit="36772b5a72f91e99b30756808d8cff6edb415b8f")
    version("0.24.0", commit="071bbb18c1fe3eac9d19557cc4490995e0af5184")
    version("0.23.0", commit="7e0a1251685e07a5dcccc84f4d9251d5a066e2ee")
    version("0.22.1", commit="e55e9c72883d24e3ed4d4eaaae330825a2d77dd3")
    version("0.22.0", commit="a70030278541d4c4e18ebf92b683951749d60049")
    version("0.21.0", commit="b7728bb798b9891ce62e1034fa21c0bc33a30cab")

    depends_on("ecbuild", type=("build"))
    depends_on("eckit")
    depends_on("boost cxxstd=14 visibility=hidden", when="@0.26.0:", type=("build", "run"))
    variant("fckit", default=True)
    depends_on("fckit", when="+fckit")
    depends_on("python")

    patch("clang_include_array.patch", when="%apple-clang")
    patch("clang_include_array.patch", when="%clang")

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant('openmp', default=True, description='Use OpenMP?')
    depends_on("llvm-openmp", when="+openmp %apple-clang", type=("build", "run"))
    variant("shared", default=True)

    variant("trans", default=False)
    depends_on("ectrans@:1.0.0", when="@:0.30.0 +trans")
    depends_on("ectrans@1.1.0:", when="@0.31.0: +trans")
    # variant('cgal', default=False)
    # depends_on('cgal', when='+cgal')
    variant("eigen", default=True)
    depends_on("eigen", when="+eigen")
    variant("fftw", default=True)
    depends_on("fftw-api", when="+fftw")

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_OMP', 'openmp'),
            self.define_from_variant("ENABLE_FCKIT", "fckit"),
            self.define_from_variant("ENABLE_TRANS", "trans"),
            self.define_from_variant("ENABLE_EIGEN", "eigen"),
            self.define_from_variant("ENABLE_FFTW", "fftw"),
            "-DPYTHON_EXECUTABLE:FILEPATH=" + self.spec["python"].command.path,
        ]
        if "~shared" in self.spec:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        return args

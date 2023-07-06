# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vecgeom(CMakePackage, CudaPackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
    url = "https://gitlab.cern.ch/VecGeom/VecGeom/-/archive/v1.1.6/VecGeom-v1.1.6.tar.gz"
    git = "https://gitlab.cern.ch/VecGeom/VecGeom.git"

    tags = ["hep"]

    maintainers("drbenmorgan", "sethrj")

    version("master", branch="master")
    version("1.2.3", sha256="703e52d78b5b78e9f595bc76771659ab0cb09898ea32c50cfbde07d6d09ef1e1")
    version(
        "1.2.2",
        sha256="887134d40fc9731138189299f0bd5e73485fbb95a96eb4124ce0854e4672291f",
        deprecated=True,
    )
    version(
        "1.2.1",
        sha256="2b47f0d23f6d25ca4fc0601b93a98167bbfb4b8aa6a1bba16d0391569e99e6f0",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="3448606fceb98ceb72d687d2d3b7ad44c67793d799def4ece9601b8e39c2868a",
        deprecated=True,
    )
    version(
        "1.1.20",
        sha256="e1c75e480fc72bca8f8072ea00320878a9ae375eed7401628b15cddd097ed7fd",
        deprecated=True,
    )
    version(
        "1.1.19",
        sha256="4c586b57fd4e30be044366c9be983249c7fa8bec629624523f5f69fd9caaa05b",
        deprecated=True,
    )
    version(
        "1.1.18",
        sha256="2780640233a36e0d3c767140417015be1893c1ad695ccc0bd3ee0767bc9fbed8",
        deprecated=True,
    )
    version(
        "1.1.17",
        sha256="2e95429b795311a6986320d785bedcd9dace9f8e7b7f6bd778d23a4ff23e0424",
        deprecated=True,
    )
    version(
        "1.1.16",
        sha256="2fa636993156d9d06750586e8a1ac1701ae2be62dea07964e2369698ae521d02",
        deprecated=True,
    )
    version(
        "1.1.15",
        sha256="0ee9897eb12d8d560dc0c9e56e8fdb78d0111f651a984df24e983da035bd1c70",
        deprecated=True,
    )
    version(
        "1.1.13",
        sha256="6bb364cc74bdab2e64e2fe132debd7f1e192da0a103f5149df7ab25b7c19a205",
        deprecated=True,
    )
    version(
        "1.1.12",
        sha256="fec4495aac4a9d583f076551da61a68b956bba1dd1ebe1cd48c00ef95c962049",
        deprecated=True,
    )
    version(
        "1.1.9",
        sha256="a90e11bf83724300d1d7206e5fe89a7915c4ec6aae881587f18e282ac0f6ee8e",
        deprecated=True,
    )
    version(
        "1.1.8",
        sha256="9c42206d788ec4b791571882f5ea8d2c591c938abe61c21cc5ec37bfea6bf768",
        deprecated=True,
    )
    version(
        "1.1.7",
        sha256="cc79a0baa783b21ecc399c4e7cca925ca340e6aeb96e3b2cad45c141557519bf",
        deprecated=True,
    )
    version(
        "1.1.6",
        sha256="c4806a6b67d01b40074b8cc6865d78574a6a1c573be51696f2ecdf98b9cb954a",
        deprecated=True,
    )
    version(
        "1.1.5",
        sha256="da674f3bbc75c30f56c1a2d251fa8930c899f27fa64b03a36569924030d87b95",
        deprecated=True,
    )
    version(
        "1.1.3",
        sha256="ada09e8b6b2fa6c058290302b2cb5a6c2e644192aab1623c31d18c6a2f4c01c8",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="e9d1ef83ff591fe4f9ef744a4d3155a3dc7e90ddb6735b24f3afe4c2dc3f7064",
        deprecated=True,
    )
    version(
        "1.0.1",
        sha256="1eae7ac9014c608e8d8db5568058b8c0fea1a1dc7a8f54157a3a1c997b6fd9eb",
        deprecated=True,
    )
    version(
        "0.5.2",
        tag="v00.05.02",
        commit="a7e0828c915ff936a79e672d1dd84b087a323b51",
        deprecated=True,
    )
    version(
        "0.3.rc",
        sha256="a87a9ea4ab126b59ff9c79182bc0911ead3d76dd197194742e2a35ccd341299d",
        deprecated=True,
    )

    _cxxstd_values = ("11", "14", "17")
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building",
    )
    variant("gdml", default=True, description="Support native GDML geometry descriptions")
    variant("geant4", default=False, description="Support Geant4 geometry construction")
    variant("root", default=False, description="Support ROOT geometry construction")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("veccore")
    depends_on("veccore@0.8.1:", when="+cuda")
    depends_on("veccore@0.8.0:0.8", when="@1.1.18:")
    depends_on("veccore@0.5.2:", when="@1.1.0:")
    depends_on("veccore@0.4.2", when="@:1.0")

    conflicts("+cuda", when="@:1.1.5")
    conflicts("cxxstd=14", when="@1.2:")
    conflicts("cxxstd=11", when="@1.2:")

    # Fix missing CMAKE_CUDA_STANDARD
    patch(
        "https://gitlab.cern.ch/VecGeom/VecGeom/-/commit/7094dd180ef694f2abb7463cafcedfb8b8ed30a1.diff",
        sha256="34f1a6899616e40bce33d80a38a9b409f819cbaab07b2e3be7f4ec4bedb52b29",
        when="@1.1.7 +cuda",
    )
    # Fix installed target properties to not propagate flags to nvcc
    patch(
        "https://gitlab.cern.ch/VecGeom/VecGeom/-/commit/ac398bd109dd9175e4a898cd4b62571a3cc88252.diff",
        sha256="a9ba136d3ed4282ec950069da2199f22beadea27d89a4264d8773ba329e253df",
        when="@1.1.18 +cuda ^cuda@:11.4",
    )

    for std in _cxxstd_values:
        depends_on("geant4 cxxstd=" + std, when="+geant4 cxxstd=" + std)
        depends_on("root cxxstd=" + std, when="+root cxxstd=" + std)
        depends_on("xerces-c cxxstd=" + std, when="+gdml cxxstd=" + std)

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        target_instructions = "empty"
        if "~cuda" in spec:
            # Only add vectorization if CUDA is disabled due to nvcc flag
            # forwarding issues
            vecgeom_arch = "sse2 sse3 ssse3 sse4.1 sse4.2 avx avx2".split()
            for feature in reversed(vecgeom_arch):
                if feature.replace(".", "_") in spec.target:
                    target_instructions = feature
                    break

        prefix = "VECGEOM_" if spec.satisfies("@1.2:") else ""
        args = [
            define(prefix + "BACKEND", "Scalar"),
            define(prefix + "BUILTIN_VECCORE", False),
            define(prefix + "NO_SPECIALIZATION", True),
            define("VECGEOM_VECTOR", target_instructions),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            from_variant(prefix + "GDML", "gdml"),
            from_variant(prefix + "GEANT4", "geant4"),
            from_variant(prefix + "ROOT", "root"),
        ]

        if spec.satisfies("@1.1.19:"):
            args.append(from_variant("VECGEOM_ENABLE_CUDA", "cuda"))
            if "+cuda" in spec:
                # This will add an (ignored) empty string if no values are
                # selected, otherwise will add a CMake list of arch values
                args.append(define("CMAKE_CUDA_ARCHITECTURES", spec.variants["cuda_arch"].value))
        else:
            args.append(from_variant("CUDA"))
            if "+cuda" in spec:
                arch = spec.variants["cuda_arch"].value
                if len(arch) != 1:
                    raise InstallError("Exactly one cuda_arch must be specified")
                args.append(define("CUDA_ARCH", arch[0]))

        # Set testing flags
        build_tests = self.run_tests
        args.append(define("BUILD_TESTING", build_tests))
        if spec.satisfies("@:1.1"):
            args.extend(
                [
                    define("CTEST", build_tests),
                    define("GDMLTESTING", build_tests and "+gdml" in spec),
                ]
            )

        if spec.satisfies("@:0.5.2"):
            args.extend([define("USOLIDS", True), define("USOLIDS_VECGEOM", True)])

        return args

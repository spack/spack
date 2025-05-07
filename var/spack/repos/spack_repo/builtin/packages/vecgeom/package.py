# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.variant import ConditionalVariantValues


def _std_when(values):
    for v in values:
        if isinstance(v, ConditionalVariantValues):
            for c in v:
                yield (c.value, c.when)
        else:
            yield (v, "")


class Vecgeom(CMakePackage, CudaPackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
    url = "https://gitlab.cern.ch/VecGeom/VecGeom/-/archive/v1.1.6/VecGeom-v1.1.6.tar.gz"
    git = "https://gitlab.cern.ch/VecGeom/VecGeom.git"

    tags = ["hep"]

    maintainers("drbenmorgan", "sethrj")

    version("master", branch="master", get_full_repo=True)
    # NOTE: the surfacedev branches are not stable or official and will be
    # deleted when the next 2.0 RC comes out
    version(
        "2.0.0-surfacedev.2",
        tag="v2.0.0-surfacedev.2",
        commit="91f5ee554e012ffa3baecd2b30e6f5e6905e5ffb",
        deprecated=True,
    )
    version(
        "2.0.0-surfacedev.1",
        tag="v2.0.0-surfacedev.1",
        commit="1d9797ea47e3b35ab0114e72ce5925ecbd59cbf4",
        deprecated=True,
    )
    version(
        "1.2.10",
        url="https://gitlab.cern.ch/-/project/981/uploads/8e0a94013efdd1b2d4f44c3fbb10bcdf/VecGeom-v1.2.10.tar.gz",
        sha256="3e0934842694452e4cb4a265428cb99af1ecc45f0e2d28a32dfeaa0634c21e2a",
        preferred=True,
    )
    version(
        "1.2.9",
        url="https://gitlab.cern.ch/-/project/981/uploads/55a89cafbf48a418bec68be42867d4bf/VecGeom-v1.2.9.tar.gz",
        sha256="93ee9ce6f7b2d704e9b9db22fad68f81b8eaf17453452969fc47e93dba4bfaf4",
        deprecated=True,
    )
    version(
        "1.2.8",
        url="https://gitlab.cern.ch/VecGeom/VecGeom/uploads/db11697eb81d6f369e9ded1078de946b/VecGeom-v1.2.8.tar.gz",
        sha256="769f59e8377f8268e253a9b2a3eee86868a9ebc1fa66c968b96e19c31440c12b",
        deprecated=True,
    )
    version(
        "1.2.7",
        url="https://gitlab.cern.ch/VecGeom/VecGeom/uploads/e4172cca4f6f731ef15e2780ecbb1645/VecGeom-v1.2.7.tar.gz",
        sha256="d264c69b78bf431b9542be1f1af087517eac629da03cf2da62eb1e433fe06021",
        deprecated=True,
    )
    version(
        "1.2.6",
        url="https://gitlab.cern.ch/VecGeom/VecGeom/uploads/0b16aed9907cea62aa5f5914bec99a90/VecGeom-v1.2.6.tar.gz",
        sha256="337f8846491930f3d8bfa4b45a1589d46e5d1d87f2d38c8f7006645c3aa90df8",
        deprecated=True,
    )
    version(
        "1.2.5",
        url="https://gitlab.cern.ch/VecGeom/VecGeom/uploads/33b93e656c5bc49d81cfcba291f5be51/VecGeom-v1.2.5.tar.gz",
        sha256="d79ea05125e4d03c5605e5ea232994c500841d207b4543ac3d84758adddc15a9",
        deprecated=True,
    )
    version("1.1.20", sha256="e1c75e480fc72bca8f8072ea00320878a9ae375eed7401628b15cddd097ed7fd")
    version(
        "1.1.5",
        sha256="da674f3bbc75c30f56c1a2d251fa8930c899f27fa64b03a36569924030d87b95",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="e9d1ef83ff591fe4f9ef744a4d3155a3dc7e90ddb6735b24f3afe4c2dc3f7064",
        deprecated=True,
    )
    version(
        "0.5.2",
        tag="v00.05.02",
        commit="a7e0828c915ff936a79e672d1dd84b087a323b51",
        deprecated=True,
    )

    _cxxstd_values = (conditional("11", "14", when="@:1.1"), "17", conditional("20", when="@1.2:"))
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="Use the specified C++ standard when building",
    )
    variant("gdml", default=True, description="Support native GDML geometry descriptions")
    # TODO: delete geant4/root variants since they don't affect the build
    variant("geant4", default=False, description="Support Geant4 geometry construction")
    variant("root", default=False, description="Support ROOT geometry construction")
    variant("shared", default=True, description="Build shared libraries")
    variant("surface", default=False, when="@2:", description="Use surface frame representation")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("veccore")
    depends_on("veccore@0.8.1:", when="+cuda")
    depends_on("veccore@0.8.0:0.8", when="@1.1.18:")
    depends_on("veccore@0.5.2:", when="@1.1.0:")
    depends_on("veccore@0.4.2", when="@:1.0")

    conflicts("+cuda", when="@:1.1.5")

    # NOTE: surface branch doesn't yet compile with volume
    conflicts("~surface", when="@=2.0.0-surfacedev.1")

    # Fix empty -Xcompiler= with nvcc
    patch(
        "https://gitlab.cern.ch/VecGeom/VecGeom/-/commit/0bf9b675ab70eb5cb9409ff73c1152fd1326dbf4.diff",
        sha256="f172b0a9ee1de4931b106d8500d1a60d5688c9bce324cf12ca107ec866a16c56",
        when="@1.2.7:1.2.10 +cuda ^cuda@:11",
    )
    # Fix -Wmissing-template-arg-list-after-template-kw
    patch(
        "https://gitlab.cern.ch/VecGeom/VecGeom/-/merge_requests/1251.diff",
        sha256="b9419c6666389b69ee2c9125d10f25b423fce339495413ac4762ae6f32bdea63",
        when="@:1.2.10 ^apple-clang@17:",
    )

    for _std, _when in _std_when(_cxxstd_values):
        depends_on(f"geant4 cxxstd={_std}", when=f"{_when} +geant4 cxxstd={_std}")
        depends_on(f"root cxxstd={_std}", when=f"{_when} +root cxxstd={_std}")
        depends_on(f"xerces-c cxxstd={_std}", when=f"{_when} +gdml cxxstd={_std}")

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

        args.append(from_variant("VECGEOM_USE_SURF", "surface"))

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

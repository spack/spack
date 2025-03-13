# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Simdjson(CMakePackage):
    """
    simdjson is a SIMD-accelerated JSON parsing library for C++ that can parse gigabytes of JSON
    per second.
    """

    homepage = "https://simdjson.org"
    url = "https://github.com/simdjson/simdjson/archive/v3.12.2.tar.gz"

    license("Apache-2.0 OR MIT")

    version("3.12.2", sha256="8ac7c97073d5079f54ad66d04381ec75e1169c2e20bfe9b6500bc81304da3faf")
    version("3.12.1", sha256="b73e21f78eabdaf89bf026d8ef0d65d2f1a9bfdc1cb26659c4ec88959989bf70")
    version("3.12.0", sha256="1e5e82f0a34c331c1b0d0c21609791bfe6d6849edfc24983fc241626b433e1c3")
    version("3.11.6", sha256="7176a2feb98e1b36b6b9fa56d64151068865f505a0ce24203f3ddbb3f985103b")
    version("3.11.5", sha256="509bf4880978666f5a6db1eb3d747681e0cc6e0b5bddd94ab0f14a4199d93e18")
    version("3.11.4", sha256="1029aff6bcca7811fb7b6d5421c5c9024b8e74e84cd268680265723f42e23cf2")
    version("3.11.3", sha256="eeb10661047e476aa3b535d14a32af95690691778d7afe0630a344654ff9759a")
    version("3.11.2", sha256="47a6d78a70c25764386a01b55819af386b98fc421da79ae8de3ae0242cf66d93")
    version("3.11.1", sha256="18f7dfd267b90d177851623747598e45fbe4d91fc485f2b57ff0e3ae1b0fdde3")
    version("3.11.0", sha256="f3469e776ca704cfda47f0a43331690c882f82c9c0c6f185452387c1e222a63e")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # variants by library linkage type
    variant("shared", default=False, description="Build a dynamically linked library")
    variant(
        "simdjson_static",
        default=False,
        description="Build the simdjson_static library along with the dynamically linked simdjson",
        when="+shared",
    )

    # variants by sanitizers
    variant("ubsan", default=False, description="Enable UndefinedBehaviorSanitizer")
    variant("asan", default=False, description="Enable AddressSanitizer")
    variant("msan", default=False, description="Enable MemorySanitizer")
    variant("tsan", default=False, description="Enable ThreadSanitizer", when="+ubsan")

    # variants by features
    variant("deprecated", default=True, description="Enable deprecated APIs")
    variant("exceptions", default=False, description="Enable exception-throwing interface")
    variant("threads", default=True, description="Link with thread support")
    variant("utf8-validation", default=True, description="Enable UTF-8 validation")

    def cmake_args(self):
        args = [
            "-DSIMDJSON_DEVELOPER_MODE:BOOL=OFF",
            "-DSIMDJSON_VERBOSE_LOGGING:BOOL=OFF",
            self.define(
                "SIMDJSON_DEVELOPMENT_CHECKS",
                self.spec.satisfies("build_type=Debug")
                or self.spec.satisfies("build_type=RelWithDebInfo"),
            ),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("SIMDJSON_BUILD_STATIC_LIB", "simdjson_static"),
            self.define_from_variant("SIMDJSON_SANITIZE_UNDEFINED", "ubsan"),
            self.define_from_variant("SIMDJSON_SANITIZE", "asan"),
            self.define_from_variant("SIMDJSON_SANITIZE_MEMORY", "msan"),
            self.define_from_variant("SIMDJSON_SANITIZE_THREADS", "tsan"),
            self.define("SIMDJSON_DISABLE_DEPRECATED_API", self.spec.satisfies("-deprecated")),
            self.define_from_variant("SIMDJSON_EXCEPTIONS", "exceptions"),
            self.define_from_variant("SIMDJSON_ENABLE_THREADS", "threads"),
            self.define_from_variant("SIMDJSON_SKIPUTF8VALIDATION", "utf8-validation"),
        ]

        return args

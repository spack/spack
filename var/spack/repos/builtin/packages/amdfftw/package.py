# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.fftw import FftwBase


class Amdfftw(FftwBase):
    """FFTW (AMD Optimized version) is a comprehensive collection of
    fast C routines for computing the Discrete Fourier Transform (DFT)
    and various special cases thereof.

    It is an open-source implementation of the Fast Fourier transform
    algorithm. It can compute transforms of real and complex-values
    arrays of arbitrary size and dimension.
    AMD Optimized FFTW is the optimized FFTW implementation targeted
    for AMD CPUs.

    For single precision build, please use precision value as float.
    Example : spack install amdfftw precision=float

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-FFTW license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/fftw/fftw-libraries-4-0-eula.html
    https://www.amd.com/en/developer/aocl/fftw/fftw-libraries-eula.html
    """

    _name = "amdfftw"
    homepage = "https://www.amd.com/en/developer/aocl/fftw.html"
    url = "https://github.com/amd/amd-fftw/archive/3.0.tar.gz"
    git = "https://github.com/amd/amd-fftw.git"

    maintainers("amd-toolchain-support")

    version("4.0", sha256="5f02cb05f224bd86bd88ec6272b294c26dba3b1d22c7fb298745fd7b9d2271c0")
    version("3.2", sha256="31cab17a93e03b5b606e88dd6116a1055b8f49542d7d0890dbfcca057087b8d0")
    version("3.1", sha256="3e777f3acef13fa1910db097e818b1d0d03a6a36ef41186247c6ab1ab0afc132")
    version("3.0.1", sha256="87030c6bbb9c710f0a64f4f306ba6aa91dc4b182bb804c9022b35aef274d1a4c")
    version("3.0", sha256="a69deaf45478a59a69f77c4f7e9872967f1cfe996592dd12beb6318f18ea0bcd")
    version("2.2", sha256="de9d777236fb290c335860b458131678f75aa0799c641490c644c843f0e246f8")

    variant("shared", default=True, description="Builds a shared version of the library")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("threads", default=False, description="Enable SMP threads support")
    variant("debug", default=False, description="Builds a debug version of the library")
    variant(
        "amd-fast-planner",
        default=False,
        description="Option to reduce the planning time without much "
        "tradeoff in the performance. It is supported for "
        "float and double precisions only.",
    )
    variant("amd-top-n-planner", default=False, description="Build with amd-top-n-planner support")
    variant(
        "amd-mpi-vader-limit", default=False, description="Build with amd-mpi-vader-limit support"
    )
    variant("static", default=False, description="Build with static suppport")
    variant("amd-trans", default=False, description="Build with amd-trans suppport")
    variant("amd-app-opt", default=False, description="Build with amd-app-opt suppport")
    variant(
        "amd-dynamic-dispatcher",
        default=False,
        when="@3.2:",
        description="Single portable optimized library"
        " to execute on different x86 CPU architectures",
    )

    depends_on("texinfo")

    provides("fftw-api@3", when="@2:")

    conflicts(
        "precision=quad",
        when="@2.2 %aocc",
        msg="Quad precision is not supported by AOCC clang version 2.2",
    )
    conflicts(
        "+debug", when="@2.2 %aocc", msg="debug mode is not supported by AOCC clang version 2.2"
    )
    conflicts("%gcc@:7.2", when="@2.2:", msg="GCC version above 7.2 is required for AMDFFTW")
    conflicts(
        "+amd-fast-planner", when="@2.2", msg="amd-fast-planner is supported from 3.0 onwards"
    )
    conflicts(
        "+amd-fast-planner",
        when="precision=quad",
        msg="Quad precision is not supported with amd-fast-planner",
    )
    conflicts(
        "+amd-fast-planner",
        when="precision=long_double",
        msg="long_double precision is not supported with amd-fast-planner",
    )
    conflicts(
        "+amd-top-n-planner",
        when="@:3.0.0",
        msg="amd-top-n-planner is supported from 3.0.1 onwards",
    )
    conflicts(
        "+amd-top-n-planner",
        when="precision=long_double",
        msg="long_double precision is not supported with amd-top-n-planner",
    )
    conflicts(
        "+amd-top-n-planner",
        when="precision=quad",
        msg="Quad precision is not supported with amd-top-n-planner",
    )
    conflicts(
        "+amd-top-n-planner",
        when="+amd-fast-planner",
        msg="amd-top-n-planner cannot be used with amd-fast-planner",
    )
    conflicts(
        "+amd-top-n-planner", when="+threads", msg="amd-top-n-planner works only for single thread"
    )
    conflicts(
        "+amd-top-n-planner", when="+mpi", msg="mpi thread is not supported with amd-top-n-planner"
    )
    conflicts(
        "+amd-top-n-planner",
        when="+openmp",
        msg="openmp thread is not supported with amd-top-n-planner",
    )
    conflicts(
        "+amd-mpi-vader-limit",
        when="@:3.0.0",
        msg="amd-mpi-vader-limit is supported from 3.0.1 onwards",
    )
    conflicts(
        "+amd-mpi-vader-limit",
        when="precision=quad",
        msg="Quad precision is not supported with amd-mpi-vader-limit",
    )
    conflicts("+amd-trans", when="+threads", msg="amd-trans works only for single thread")
    conflicts("+amd-trans", when="+mpi", msg="mpi thread is not supported with amd-trans")
    conflicts("+amd-trans", when="+openmp", msg="openmp thread is not supported with amd-trans")
    conflicts(
        "+amd-trans",
        when="precision=long_double",
        msg="long_double precision is not supported with amd-trans",
    )
    conflicts(
        "+amd-trans", when="precision=quad", msg="Quad precision is not supported with amd-trans"
    )
    conflicts("+amd-app-opt", when="@:3.0.1", msg="amd-app-opt is supported from 3.1 onwards")
    conflicts("+amd-app-opt", when="+mpi", msg="mpi thread is not supported with amd-app-opt")
    conflicts(
        "+amd-app-opt",
        when="precision=long_double",
        msg="long_double precision is not supported with amd-app-opt",
    )
    conflicts(
        "+amd-app-opt",
        when="precision=quad",
        msg="Quad precision is not supported with amd-app-opt",
    )
    conflicts(
        "+amd-dynamic-dispatcher",
        when="%aocc",
        msg="dynamic-dispatcher is not supported by AOCC clang compiler",
    )

    def configure(self, spec, prefix):
        """Configure function"""
        # Base options
        options = ["--prefix={0}".format(prefix), "--enable-amd-opt"]

        # Dynamic dispatcher builds a single portable optimized library
        # that can execute on different x86 CPU architectures.
        # It is supported for GCC compiler and Linux based systems only.
        if "+amd-dynamic-dispatcher" in self.spec:
            options.append("--enable-dynamic-dispatcher")

        # Check if compiler is AOCC
        if "%aocc" in spec:
            options.append("CC={0}".format(os.path.basename(spack_cc)))
            options.append("FC={0}".format(os.path.basename(spack_fc)))
            options.append("F77={0}".format(os.path.basename(spack_fc)))

        if "+debug" in spec:
            options.append("--enable-debug")

        if "+mpi" in spec:
            options.append("--enable-mpi")
            options.append("--enable-amd-mpifft")
        else:
            options.append("--disable-mpi")
            options.append("--disable-amd-mpifft")

        options.extend(self.enable_or_disable("shared"))
        options.extend(self.enable_or_disable("openmp"))
        options.extend(self.enable_or_disable("threads"))
        options.extend(self.enable_or_disable("amd-fast-planner"))
        options.extend(self.enable_or_disable("amd-top-n-planner"))
        options.extend(self.enable_or_disable("amd-mpi-vader-limit"))
        options.extend(self.enable_or_disable("static"))
        options.extend(self.enable_or_disable("amd-trans"))
        options.extend(self.enable_or_disable("amd-app-opt"))

        if not self.compiler.f77 or not self.compiler.fc:
            options.append("--disable-fortran")

        # Cross compilation is supported in amd-fftw by making use of target
        # variable to set AMD_ARCH configure option.
        # Spack user can not directly use AMD_ARCH for this purpose but should
        # use target variable to set appropriate -march option in AMD_ARCH.
        arch = spec.architecture
        options.append(
            "AMD_ARCH={0}".format(arch.target.optimization_flags(spec.compiler).split("=")[-1])
        )

        # Specific SIMD support.
        # float and double precisions are supported
        simd_features = ["sse2", "avx", "avx2", "avx512"]

        simd_options = []
        for feature in simd_features:
            msg = "--enable-{0}" if feature in spec.target else "--disable-{0}"
            simd_options.append(msg.format(feature))

        # When enabling configure option "--enable-amd-opt", do not use the
        # configure option "--enable-generic-simd128" or
        # "--enable-generic-simd256"

        # Double is the default precision, for all the others we need
        # to enable the corresponding option.
        enable_precision = {
            "float": ["--enable-float"],
            "double": None,
            "long_double": ["--enable-long-double"],
            "quad": ["--enable-quad-precision"],
        }

        # Different precisions must be configured and compiled one at a time
        configure = Executable("../configure")
        for precision in self.selected_precisions:
            opts = (enable_precision[precision] or []) + options[:]

            # SIMD optimizations are available only for float and double
            if precision in ("float", "double"):
                opts += simd_options

            with working_dir(precision, create=True):
                configure(*opts)

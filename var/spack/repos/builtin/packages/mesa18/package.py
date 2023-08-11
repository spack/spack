# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Mesa18(AutotoolsPackage):
    """Mesa is an open-source implementation of the OpenGL specification
    - a system for rendering interactive 3D graphics."""

    homepage = "https://www.mesa3d.org"
    maintainers("v-dobrev", "ChristianTackeGSI")

    # Note that we always want to build from the git repo instead of a
    # tarball since the tarball has pre-generated files for certain versions
    # of LLVM while the git repo doesn't so it can adapt at build time to
    # whatever version of LLVM you're using.
    git = "https://gitlab.freedesktop.org/mesa/mesa.git"

    version("18.3.6", tag="mesa-18.3.6")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("binutils+plugins", when=(sys.platform != "darwin"), type="build")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("gettext", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python@:3.8", type="build")  # https://github.com/spack/spack/issues/28219
    depends_on("py-mako@0.8.0:", type="build")
    depends_on("libxml2")
    depends_on("zlib-api")
    depends_on("expat")
    depends_on("ncurses+termlib")

    # Internal options
    variant("llvm", default=True, description="Enable LLVM.")
    variant(
        "swr",
        values=spack.variant.DisjointSetsOfValues(
            ("none",), ("auto",), ("avx", "avx2", "knl", "skx")
        )
        .with_non_feature_values("auto")
        .with_non_feature_values("none")
        .with_default("auto"),
        when="+llvm",
        description="Enable the SWR driver.",
    )

    # Front ends
    variant("osmesa", default=True, description="Enable the OSMesa frontend.")

    is_linux = sys.platform.startswith("linux")
    variant("glx", default=is_linux, description="Enable the GLX frontend.")

    # Additional backends
    variant("opengles", default=False, description="Enable OpenGL ES support.")

    # Provides
    provides("libglx", when="+glx")
    provides("libosmesa", when="+osmesa")

    # Variant dependencies
    depends_on("libllvm@6:10", when="+llvm")
    depends_on("libx11", when="+glx")
    depends_on("libxcb", when="+glx")
    depends_on("libxext", when="+glx")
    depends_on("glproto@1.4.14:", when="+glx")

    # Require at least 1 front-end
    conflicts("~osmesa ~glx")

    # Prevent an unnecessary xcb-dri dependency
    patch("autotools-x11-nodri.patch")

    # Backport Mesa MR#6053 to prevent multiply-defined symbols
    patch("multiple-symbols_hash.patch", when="@:20.1.4%gcc@10:")

    def setup_build_environment(self, env):
        env.set("PYTHON", self.spec["python"].command.path)

    def autoreconf(self, spec, prefix):
        which("autoreconf")("--force", "--verbose", "--install")

    def configure_args(self):
        spec = self.spec
        args = [
            "LDFLAGS={0}".format(self.spec["ncurses"].libs.search_flags),
            "--enable-shared",
            "--disable-static",
            "--disable-libglvnd",
            "--disable-nine",
            "--disable-omx-bellagio",
            "--disable-omx-tizonia",
            "--disable-opencl",
            "--disable-opencl-icd",
            "--disable-va",
            "--disable-vdpau",
            "--disable-xa",
            "--disable-xvmc",
            "--disable-osmesa",
            "--with-vulkan-drivers=",
            "--disable-egl",
            "--disable-gbm",
            "--disable-dri",
            "--enable-opengl",
        ]

        args_platforms = []
        args_gallium_drivers = ["swrast"]
        args_dri_drivers = []

        if spec.target.family == "arm" or spec.target.family == "aarch64":
            args.append("--disable-libunwind")

        num_frontends = 0
        if "+osmesa" in spec:
            num_frontends += 1
            args.append("--enable-gallium-osmesa")
        else:
            args.append("--disable-gallium-osmesa")

        if "+glx" in spec:
            num_frontends += 1
            args.append("--enable-glx=gallium-xlib")
            args_platforms.append("x11")
        else:
            args.append("--disable-glx")

        if "+opengles" in spec:
            args.extend(["--enable-gles1", "--enable-gles2"])
        else:
            args.extend(["--disable-gles1", "--disable-gles2"])

        if num_frontends > 1:
            args.append("--enable-shared-glapi")
        else:
            args.append("--disable-shared-glapi")

        if "+llvm" in spec:
            args.append("--enable-llvm")
            args.append("--with-llvm-prefix=%s" % spec["libllvm"].prefix)
            if "+llvm_dylib" in spec["libllvm"]:
                args.append("--enable-llvm-shared-libs")
            else:
                args.append("--disable-llvm-shared-libs")
        else:
            args.append("--disable-llvm")

        args_swr_arches = []
        if "swr=auto" in spec:
            if "avx" in spec.target:
                args_swr_arches.append("avx")
            if "avx2" in spec.target:
                args_swr_arches.append("avx2")
            if "avx512f" in spec.target:
                if "avx512er" in spec.target:
                    args_swr_arches.append("knl")
                if "avx512bw" in spec.target:
                    args_swr_arches.append("skx")
        else:
            if "swr=avx" in spec:
                args_swr_arches.append("avx")
            if "swr=avx2" in spec:
                args_swr_arches.append("avx2")
            if "swr=knl" in spec:
                args_swr_arches.append("knl")
            if "swr=skx" in spec:
                args_swr_arches.append("skx")
        if args_swr_arches:
            args_gallium_drivers.append("swr")
            args.append("--with-swr-archs=" + ",".join(args_swr_arches))

        # Add the remaining list args
        args.append("--with-platforms=" + ",".join(args_platforms))
        args.append("--with-gallium-drivers=" + ",".join(args_gallium_drivers))
        args.append("--with-dri-drivers=" + ",".join(args_dri_drivers))

        return args

    @property
    def libs(self):
        spec = self.spec
        libs_to_seek = set()
        if "platform=windows" in spec:
            libs_to_seek.add("opengl32")
            if "+osmesa" in spec:
                libs_to_seek.add("osmesa")
        else:
            libs_to_seek.add("libGL")
            if "+osmesa" in spec:
                libs_to_seek.add("libOSMesa")
            if "+glx" in spec:
                libs_to_seek.add("libGL")
        if "+opengles" in spec:
            libs_to_seek.add("libGLESv1_CM")
            libs_to_seek.add("libGLESv2")

        return find_libraries(
            list(libs_to_seek), root=self.spec.prefix, shared=True, recursive=True
        )

    @property
    def libglx_headers(self):
        return find_headers("GL/glx", root=self.spec.prefix.include, recursive=False)

    @property
    def libglx_libs(self):
        return find_libraries("libGL", root=self.spec.prefix, recursive=True)

    @property
    def libosmesa_headers(self):
        return find_headers("GL/osmesa", root=self.spec.prefix.include, recursive=False)

    @property
    def libosmesa_libs(self):
        if "platform=windows" in self.spec:
            lib_name = "osmesa"
        else:
            lib_name = "libOSMesa"
        return find_libraries(lib_name, root=self.spec.prefix, recursive=True)

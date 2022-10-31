# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ftgl(CMakePackage):
    """Library to use arbitrary fonts in OpenGL applications."""

    homepage = "https://github.com/frankheckenbach/ftgl"
    git = "https://github.com/frankheckenbach/ftgl.git"

    version("master", branch="master")
    version("2.4.0", commit="483639219095ad080538e07ceb5996de901d4e74")
    version("2.3.1", commit="3c0fdf367824b6381f29df3d8b4590240db62ab7")

    variant(
        "cxxstd",
        when="@2.3:",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    # FIXME: Doc generation is broken in upstream build system
    # variant('doc', default=False, description='Build the documentation')
    variant("shared", default=True, description="Build as a shared library")

    depends_on("cmake@2.8:", type="build")
    # depends_on('doxygen', type='build', when='+doc')  -- FIXME, see above
    depends_on("pkgconfig", type="build")
    depends_on("gl")
    depends_on("glu")
    depends_on("freetype@2.0.9:")

    # Fix oversight in CMakeLists
    patch("remove-ftlibrary-from-sources.diff", when="@:2.4.0")

    # ftgl (at least up to 2.4.0) uses `cmake_minimum_version(2.8)`,
    # which doesn't honor CMAKE_CXX_STANDARD.
    def flag_handler(self, name, flags):
        with when("@2.3:"):
            if name == "cxxflags":
                flag_func_name = "self.compiler.cxx{0}_flag".format(
                    self.spec.variants["cxxstd"].value
                )
                flags.append(eval(flag_func_name, {}, {"self": self}))
        return (None, None, flags)

    def cmake_flags(self):
        flags = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        if "darwin" in self.spec.architecture:
            flags.append(self.define("CMAKE_MACOSX_RPATH", True))
        return flags

    # FIXME: See doc variant comment
    # @run_after('build')
    # def build_docs(self):
    #     if '+doc' in self.spec:
    #         cmake = self.spec['cmake'].command
    #         cmake('--build', '../spack-build', '--target', 'doc')
    #
    # @run_after('install')
    # def install_docs(self):
    #     if '+doc' in self.spec:
    #         cmake = self.spec['cmake'].command
    #         cmake('--install', '../spack-build', '--target', 'doc')

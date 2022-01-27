# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Poco(CMakePackage):
    """
    A collection of C++ class libraries, conceptually similar to
    the Java Class Library or the .NET Framework.
    """

    homepage = "https://pocoproject.org/"
    git = "https://github.com/pocoproject/poco.git"
    generator = "Ninja"

    version("1.11.1", tag="poco-1.11.1-release")

    depends_on("cmake@3.5:", type="build")
    depends_on("ninja", type="build")

    def cmake_args(self):
        return [
            "-DENABLE_REDIS=OFF",
            "-DENABLE_ENCODINGS=OFF",
            "-DENABLE_APACHECONNECTOR=OFF",
            "-DENABLE_MONGODB=OFF",
            "-DENABLE_DATA_POSTGRESQL=OFF",
            "-DENABLE_DATA_MYSQL=OFF",
            "-DENABLE_DATA_ODBC=OFF",
            "-DENABLE_DATA_SQLITE=OFF",
            "-DENABLE_ZIP=OFF",
            "-DENABLE_PAGECOMPILER=OFF",
            "-DENABLE_PAGECOMPILER_FILE2PAGE=OFF",
            "-DBUILD_SHARED_LIBS=ON"
        ]

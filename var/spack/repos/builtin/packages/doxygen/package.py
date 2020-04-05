# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Doxygen(CMakePackage):
    """Doxygen is the de facto standard tool for generating documentation
    from annotated C++ sources, but it also supports other popular programming
    languages such as C, Objective-C, C#, PHP, Java, Python, IDL (Corba,
    Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, Tcl, and to some
    extent D.."""

    homepage  = "https://github.com/doxygen/doxygen/"
    git       = "https://github.com/doxygen/doxygen.git"

    # Doxygen versions on GitHub
    version('1.8.15', commit='dc89ac01407c24142698c1374610f2cee1fbf200')
    version('1.8.14', commit='2f4139de014bf03898320a45fe52c92872c1e0f4')
    version('1.8.12', commit='4951df8d0d0acf843b4147136f945504b96536e7')
    version('1.8.11', commit='a6d4f4df45febe588c38de37641513fd576b998f')
    version('1.8.10', commit='fdae7519a2e29f94e65c0e718513343f07302ddb')

    # graphviz appears to be a run-time optional dependency
    variant('graphviz', default=False,
            description='Build with dot command support from Graphviz.')

    depends_on("cmake@2.8.12:", type='build')
    depends_on("python", type='build')  # 2 or 3 OK; used in CMake build
    depends_on("iconv")
    depends_on("flex", type='build')
    # code.l just checks subminor version <=2.5.4 or >=2.5.33
    # but does not recognize 2.6.x as newer...could be patched if needed
    depends_on("flex@2.5.39", type='build', when='@1.8.10')
    depends_on("bison", type='build')

    # optional dependencies
    depends_on("graphviz", when="+graphviz", type='run')

    # Support C++14's std::shared_ptr. For details about this patch, see
    # https://github.com/Sleepyowl/doxygen/commit/6c380ba91ae41c6d5c409a5163119318932ae2a3?diff=unified
    # Also - https://github.com/doxygen/doxygen/pull/6588
    patch('shared_ptr.patch', when='@1.8.14')

    def patch(self):
        if self.spec['iconv'].name == 'libc':
            return
        # On Linux systems, iconv is provided by libc. Since CMake finds the
        # symbol in libc, it does not look for libiconv, which leads to linker
        # errors. This makes sure that CMake always looks for the external
        # libconv instead.
        filter_file('check_function_exists(iconv_open ICONV_IN_GLIBC)',
                    'set(ICONV_IN_GLIBC FALSE)',
                    join_path('cmake', 'FindIconv.cmake'),
                    string=True)

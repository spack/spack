# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Plotutils(AutotoolsPackage, GNUMirrorPackage):
    """The GNU plotutils package contains software for both programmers and technical
    users. Its centerpiece is libplot, a powerful C/C++ function library for exporting
    2-D vector graphics in many file formats, both vector and bitmap. On the X Window
    System, it can also do 2-D vector graphics animations."""

    homepage = "https://www.gnu.org/software/plotutils"
    gnu_mirror_path = "plotutils/plotutils-2.6.tar.gz"

    version('2.6', sha256='4f4222820f97ca08c7ea707e4c53e5a3556af4d8f1ab51e0da6ff1627ff433ab')

    depends_on('libxt')
    depends_on('libxaw')
    # libpng@1.5: introduces an error relating to the incomplete type png_struct which
    # appears to be a result of this codebase using types that later become opaque in
    # 1.5.0 onwards; see discussion at https://github.com/glennrp/libpng/issues/191.
    depends_on('libpng@:1.4')
    depends_on('zlib')

    def configure_args(self):
        xt = self.spec['libxt']
        xaw = self.spec['libxaw']
        configure_args = [
            '--x-includes={}:{}'.format(xt.prefix.include, xaw.prefix.include),
            '--x-libraries={}:{}'.format(xt.prefix.lib, xaw.prefix.lib),
        ]
        return configure_args

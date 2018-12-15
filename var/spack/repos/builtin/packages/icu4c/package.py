# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Icu4c(AutotoolsPackage):
    """ICU is a mature, widely used set of C/C++ and Java libraries providing
    Unicode and Globalization support for software applications. ICU4C is the
    C/C++ interface."""

    homepage = "http://site.icu-project.org/"
    url      = "http://download.icu-project.org/files/icu4c/57.1/icu4c-57_1-src.tgz"
    list_url = "http://download.icu-project.org/files/icu4c"
    list_depth = 2

    version('60.1', '3d164a2d1bcebd1464c6160ebb8315ef')
    version('58.2', 'fac212b32b7ec7ab007a12dff1f3aea1')
    version('57.1', '976734806026a4ef8bdd17937c8898b9')

    configure_directory = 'source'

    def url_for_version(self, version):
        url = "http://download.icu-project.org/files/icu4c/{0}/icu4c-{1}-src.tgz"
        return url.format(version.dotted, version.underscored)

    def configure_args(self):
        args = []

        # The --enable-rpath option is only needed on MacOS, and it
        # breaks the build for xerces-c on Linux.
        if 'platform=darwin' in self.spec:
            args.append('--enable-rpath')

        return args

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    version('64.1', 'f150be2231c13bb45206d79e0242372b')
    version('60.1', '3d164a2d1bcebd1464c6160ebb8315ef')
    version('58.2', 'fac212b32b7ec7ab007a12dff1f3aea1')
    version('57.1', '976734806026a4ef8bdd17937c8898b9')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building')

    depends_on('python', type='build', when='@64.1:')

    configure_directory = 'source'

    def url_for_version(self, version):
        url = "http://download.icu-project.org/files/icu4c/{0}/icu4c-{1}-src.tgz"
        return url.format(version.dotted, version.underscored)

    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            # Control of the C++ Standard is via adding the required "-std"
            # flag to CXXFLAGS in env
            flags.append(getattr(self.compiler,
                         'cxx{0}_flag'.format(
                             self.spec.variants['cxxstd'].value)))
        return (None, flags, None)

    def configure_args(self):
        args = []

        if 'python' in self.spec:
            # Make sure configure uses Spack's python package
            # Without this, configure could pick a broken global installation
            args.append('PYTHON={0}'.format(self.spec['python'].command))

        # The --enable-rpath option is only needed on MacOS, and it
        # breaks the build for xerces-c on Linux.
        if 'platform=darwin' in self.spec:
            args.append('--enable-rpath')

        return args

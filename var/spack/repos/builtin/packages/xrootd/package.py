# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
       tolerant access to data repositories of many kinds."""
    homepage = "http://xrootd.org"
    url      = "http://xrootd.org/download/v4.6.0/xrootd-4.6.0.tar.gz"

    version('4.8.5',
            sha256='42e4d2cc6f8b442135f09bcc12c7be38b1a0c623a005cb5e69ff3d27997bdf73')
    version('4.8.4',
            sha256='f148d55b16525567c0f893edf9bb2975f7c09f87f0599463e19e1b456a9d95ba')
    version('4.8.3', 'bb6302703ffc123f7f9141ddb589435e')
    version('4.8.2', '531b632191b59c2cf76ab8d31af4a866')
    version('4.8.1', 'a307973f7f43b0cc2688dfe502e17709')
    version('4.8.0', '4349e7f664e686b72855e894b49063ad')
    version('4.7.1', '4006422bcf99e0a19996ace4ebb99175')
    version('4.7.0', '2a92ba483f574c6ba6a9ff061878af22')
    version('4.6.1', '70c6f6e1f5f2b4eeb3c7d2c41a36bb2c')
    version('4.6.0', '5d60aade2d995b68fe0c46896bc4a5d1')
    version('4.5.0', 'd485df3d4a991e1c35efa4bf9ef663d7')
    version('4.4.1', '72b0842f802ccc94dede4ac5ab2a589e')
    version('4.4.0', '58f55e56801d3661d753ff5fd33dbcc9')
    version('4.3.0', '39c2fab9f632f35e12ff607ccaf9e16c')

    variant('http', default=True,
            description='Build with HTTP support')

    variant('python', default=False,
            description='Build pyxroot Python extension')

    variant('readline', default=True,
            description='Use readline')

    variant('cxxstd',
            default='11',
            values=('98', '11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    conflicts('cxxstd=98', when='@4.7.0:')

    depends_on('bzip2')
    depends_on('cmake@2.6:', type='build')
    depends_on('libxml2', when='+http')
    depends_on('openssl')
    depends_on('python', when='+python')
    depends_on('readline', when='+readline')
    depends_on('xz')
    depends_on('zlib')

    extends('python', when='+python')
    patch('python-support.patch', level=1, when='@:4.8.99+python')

    def patch(self):
        """Remove hardcoded -std=c++0x flag
        """
        if self.spec.satisfies('@4.7.0:'):
            filter_file(r'\-std=c\+\+0x', r'', 'cmake/XRootDOSDefs.cmake')

    def cmake_args(self):
        spec = self.spec
        options = [
            '-DENABLE_HTTP:BOOL={0}'.
            format('ON' if '+http' in spec else 'OFF'),
            '-DENABLE_PYTHON:BOOL={0}'.
            format('ON' if '+python' in spec else 'OFF'),
            '-DENABLE_READLINE:BOOL={0}'.
            format('ON' if '+readline' in spec else 'OFF'),
            '-DENABLE_CEPH:BOOL=OFF'
        ]
        return options

    def setup_environment(self, spack_env, run_env):
        cxxstdflag = ''
        if self.spec.variants['cxxstd'].value == '98':
            cxxstdflag = self.compiler.cxx98_flag
        elif self.spec.variants['cxxstd'].value == '11':
            cxxstdflag = self.compiler.cxx11_flag
        elif self.spec.variants['cxxstd'].value == '14':
            cxxstdflag = self.compiler.cxx14_flag
        elif self.spec.variants['cxxstd'].value == '17':
            cxxstdflag = self.compiler.cxx17_flag
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(self.spec.variants['cxxstd'].value))

        if cxxstdflag:
            spack_env.append_flags('CXXFLAGS', cxxstdflag)

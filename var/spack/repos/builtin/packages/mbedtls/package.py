# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mbedtls(MakefilePackage):
    """mbed TLS (formerly known as PolarSSL) makes it trivially easy for
       developers to include cryptographic and SSL/TLS capabilities in
       their (embedded) products, facilitating this functionality with a
       minimal coding footprint.
    """

    homepage = "https://tls.mbed.org"
    url      = "https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.2.1.tar.gz"
    maintainers = ['mwkrentel']

    version('3.0.0', sha256='377d376919be19f07c7e7adeeded088a525be40353f6d938a78e4f986bce2ae0')
    version('2.27.0', sha256='4f6a43f06ded62aa20ef582436a39b65902e1126cbbe2fb17f394e9e9a552767')
    version('2.16.11', sha256='51bb9685c4f4ff9255da5659ff346b89dcaf129e3ba0f3b2b0c48a1a7495e701')
    version('2.16.9', sha256='b7ca99ee10551b5b13242b7effebefd2a5cc38c287e5f5be1267d51ee45effe3', deprecated=True)
    version('2.16.7', sha256='4786b7d1676f5e4d248f3a7f2d28446876d64962634f060ff21b92c690cfbe86', deprecated=True)
    version('2.16.1', sha256='daf0d40f3016c34eb42d1e4b3b52be047e976d566aba8668977723c829af72f3', deprecated=True)
    version('2.7.19',  sha256='3da12b1cebe1a25da8365d5349f67db514aefcaa75e26082d7cb2fa3ce9608aa')
    version('2.7.10', sha256='42b19b30b86a798bdb69c5da2f8bbd7d72ffede9a35b888ab986a29480f9dc3e', deprecated=True)
    version('2.3.0', sha256='1614ee70be99a18ca8298148308fb725aad4ad31c569438bb51655a4999b14f9', deprecated=True)
    version('2.2.1', sha256='32819c62c20e8740a11b49daa5d09ac6f179edf120a87ac559cd63120b66b699', deprecated=True)
    version('2.2.0', sha256='75494361e412444b38ebb9c908b7e17a5fb582eb9c3fadb2fe9b21e96f1bf8cb', deprecated=True)
    version('2.1.4', sha256='a0ee4d3dd135baf67a3cf5ad9e70d67575561704325d6c93d8f087181f4db338', deprecated=True)
    version('2.1.3', sha256='94da4618d5a518b99f7914a5e348be436e3571113d9a9978d130725a1fc7bfac', deprecated=True)
    version('1.3.16', sha256='0c2666222b66cf09c4630fa60a715aafd7decb1a09933b75c0c540b0625ac5df', deprecated=True)

    variant('pic', default=False, description='Compile with position independent code.')
    variant('build_type', default='Release', description='Build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))
    variant('libs', default='static', values=('shared', 'static'),
            multi=True, description='What libraries to build')

    depends_on('perl', type='test')
    depends_on('python@3:', type='test', when='@3:')
    depends_on('python@:2', type='test', when='@:2')

    build_type_to_flags = {
        'Debug': '-O0 -g',
        'Release': '-O3',
        'RelWithDebInfo': '-O2 -g',
        'MinSizeRel': '-Os',
    }

    # TODO: Can't express this in spack right now; but we can live with
    # libs=shared building both shared and static libs.
    # conflicts('libs=shared', msg='Makefile build cannot build shared libs only now')

    def flag_handler(self, name, flags):
        # Compile with PIC, if requested.
        if name == 'cflags':
            build_type = self.spec.variants['build_type'].value
            flags.append(self.build_type_to_flags[build_type])
            if self.spec.variants['pic'].value:
                flags.append(self.compiler.cc_pic_flag)

        return (None, flags, None)

    def setup_build_environment(self, env):
        if 'shared' in self.spec.variants['libs'].value:
            env.set('SHARED', 'yes')

    def build(self, spec, prefix):
        make('no_test')

    def install(self, spec, prefix):
        make('install', 'DESTDIR={0}'.format(prefix))

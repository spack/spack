# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gtkplus(Package):
    """GTK+, or the GIMP Toolkit, is a multi-platform toolkit for creating
    graphical user interfaces."""

    homepage = "https://www.gtk.org"
    url      = "https://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.94/gtk+-3.94.0.tar.xz"
    list_url = "https://ftp.acc.umu.se/pub/gnome/sources/gtk+/"
    list_depth = 1

    version('3.94.0',  sha256='a947caa5296610b0f1d7a03b58df34765c227c577c78e683e75eea3251a67035')
    version('3.20.10', sha256='e81da1af1c5c1fee87ba439770e17272fa5c06e64572939814da406859e56b70')
    version('2.99.3',  sha256='b456ab2b90c550cca9596bc5a939eb87dc4d0af3d502c180ec2fa4718a0ced61')
    version('2.24.32', sha256='b6c8a93ddda5eabe3bfee1eb39636c9a03d2a56c7b62828b359bf197943c582e')
    version('2.24.31', sha256='68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658')
    version('2.24.25', sha256='38af1020cb8ff3d10dda2c8807f11e92af9d2fa4045de61c62eedb7fbc7ea5b3')

    # TODO: Add a backend variant to choose between X11 and Wayland

    # Build dependencies
    depends_on('python@3:', type='build', when='@3.92:')
    depends_on('meson@0.43.0:', type='build', when='@3.94:')
    depends_on('meson@0.42.1:', type='build', when='@3.92:')
    depends_on('meson@0.40.0:', type='build', when='@3.91:')
    depends_on('ninja', type='build', when='@3.91:')
    depends_on('gmake', type='build', when='@:3.90')
    depends_on('pkgconfig@0.16:', type='build')

    ##########
    # GTK+ 3 #
    ##########

    # https://developer.gnome.org/gtk3/stable/gtk-building.html

    # Required dependencies
    depends_on('glib@2.55.0:', when='@3:')
    depends_on('gdk-pixbuf@2.30.0:', when='@3:')
    depends_on('gobject-introspection@1.39.0:', when='@3:')
    depends_on('cairo@1.14.0:+X+pdf', when='@3:')
    depends_on('pango@1.41.0:+X', when='@3:')
    depends_on('libepoxy@1.4:', when='@3:')
    # graphene-gobject@1.5.1:
    depends_on('atk@2.15.1:', when='@3:')
    depends_on('libxkbcommon@0.2.0:', when='@3:')
    # depends_on('freetype@2.7.1:')
    # depends_on('harfbuzz@0.9:')
    # cloudproviders_req = '>= 0.2.5'
    depends_on('shared-mime-info', when='@3:')

    # X11 dependencies
    depends_on('libx11', when='@3:')
    depends_on('libxrandr@1.2.99:', when='@3:')
    depends_on('libxrender', when='@3:')
    depends_on('libxi', when='@3:')
    depends_on('libxext', when='@3:')
    depends_on('libxfixes', when='@3:')
    depends_on('libxcursor', when='@3:')
    depends_on('libxdamage', when='@3:')
    depends_on('libxcomposite', when='@3:')
    depends_on('fontconfig', when='@3:')
    depends_on('at-spi2-atk', when='@3:')
    depends_on('gettext', when='@3:')

    ##########
    # GTK+ 2 #
    ##########

    # https://developer.gnome.org/gtk2/stable/gtk-building.html

    depends_on('glib@2.27.5:', when='@:2')
    depends_on('pango@1.20:+X', when='@:2')
    depends_on('gdk-pixbuf@2.21.0:', when='@:2')
    depends_on('atk@1.29.2:', when='@:2')
    depends_on('cairo@1.10.0:+X+pdf', when='@:2')
    depends_on('gobject-introspection@0.9.3:', when='@:2')

    patch('no-demos.patch', when='@2:2.98')

    def url_for_version(self, version):
        url = 'http://ftp.gnome.org/pub/gnome/sources/gtk+'
        ext = 'tar.gz' if version == Version('2.99.3') else 'tar.xz'
        return url + '/%s/gtk+-%s.%s' % (version.up_to(2), version, ext)

    @when('@:3.90')
    def patch(self):
        # remove disable deprecated flag.
        filter_file(r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"',
                    '', 'configure', string=True)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            meson('..', *std_meson_args)
            ninja('-v')
            if self.run_tests:
                meson('test')
            ninja('install')

    def configure_args(self):
        args = []
        # disable building of gtk-doc files following #9771
        args.append('--disable-gtk-doc-html')
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))
        return args

    @when('@:3.90')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix), *self.configure_args())
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')

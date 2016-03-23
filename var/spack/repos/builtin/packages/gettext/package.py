from spack import *

class Gettext(Package):
    """GNU internationalization (i18n) and localization (l10n) library."""
    homepage = "https://www.gnu.org/software/gettext/"
    url      = "http://ftpmirror.gnu.org/gettext/gettext-0.19.7.tar.xz"

    version('0.19.7', 'f81e50556da41b44c1d59ac93474dca5')

    def install(self, spec, prefix):
        options = ['--disable-dependency-tracking',
                   '--disable-silent-rules',
                   '--disable-debug',
                   '--prefix=%s' % prefix,
                   '--with-included-gettext',
                   '--with-included-glib',
                   '--with-included-libcroco',
                   '--with-included-libunistring',
                   '--with-emacs',
                   '--with-lispdir=%s/emacs/site-lisp/gettext' % prefix.share,
                   '--disable-java',
                   '--disable-csharp',
                   '--without-git', # Don't use VCS systems to create these archives
                   '--without-cvs',
                   '--without-xz']

        configure(*options)

        make()
        make("install")

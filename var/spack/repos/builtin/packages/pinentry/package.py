# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Pinentry(AutotoolsPackage):
    """pinentry is a small collection of dialog programs that allow GnuPG to
    read passphrases and PIN numbers in a secure manner.

    There are versions for the common GTK and Qt toolkits as well as for
    the text terminal (Curses).
    """

    homepage = "https://gnupg.org/related_software/pinentry/index.html"
    url      = "https://gnupg.org/ftp/gcrypt/pinentry/pinentry-1.1.0.tar.bz2"

    maintainers = ['alalazo']

    version('1.1.1', sha256='cd12a064013ed18e2ee8475e669b9f58db1b225a0144debdb85a68cecddba57f')
    version('1.1.0', sha256='68076686fa724a290ea49cdf0d1c0c1500907d1b759a3bcbfbec0293e8f56570')

    depends_on('libgpg-error@1.16:')
    depends_on('libassuan@2.1.0:')

    def configure_args(self):
        return [
            '--enable-static',
            '--enable-shared',
            # Autotools automatically enables these if dependencies found
            # TODO: add variants for these
            '--disable-pinentry-curses',
            '--disable-pinentry-emacs',
            '--disable-pinentry-gtk2',
            '--disable-pinentry-gnome3',
            '--disable-pinentry-qt',
            '--disable-pinentry-qt5',
            '--disable-pinentry-tqt',
            '--disable-pinentry-fltk',

            # No dependencies, simplest installation
            '--enable-pinentry-tty',

            # Disable extra features
            '--disable-fallback-curses',
            '--disable-inside-emacs',
            '--disable-libsecret',

            # Required dependencies
            '--with-gpg-error-prefix=' + self.spec['libgpg-error'].prefix,
            '--with-libassuan-prefix=' + self.spec['libassuan'].prefix,
        ]

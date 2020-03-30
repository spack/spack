# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install libnotify
#
# You can edit this file again by typing:
#
#     spack edit libnotify
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Libnotify(MesonPackage):
    """libnotify is a library for sending desktop notifications"""

    homepage = "https://github.com/GNOME/libnotify"
    url      = "https://github.com/GNOME/libnotify/archive/0.7.9.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('0.7.9', sha256='9bd4f5fa911d27567e7cc2d2d09d69356c16703c4e8d22c0b49a5c45651f3af0')

    variant('docbook', default=False, description='Build docbook docs. Currently broken')
    variant('tests', default=False, description='Build with tests. Currenlty broken')
    variant('gtkdoc', default=False, description='Build with gtkdoc. Currently broken')

    depends_on('pkgconfig')
    depends_on('glib@2.26.0:')
    depends_on('gtkplus@2.90:')
    depends_on('gobject-introspection')
    depends_on('gtk-doc', when='+gtkdoc', type='build')
    depends_on('libxslt', type='build')
    depends_on('docbook-xsl', type='build')
    depends_on('xmlto', when='+docbook', type='build')

    patch('docbook-location.patch')

    def meson_args(self):
        spec = self.spec
        args = []

        if '+docbook' in spec:
            args.append('-Ddocbook_docs=enabled')
        else:
            args.append('-Ddocbook_docs=disabled')

        if '+tests' in spec:
            args.append('-Dtests=true')
        else:
            args.append('-Dtests=false')

        if '+gtkdoc' in spec:
            args.append('-Dgtk_doc=true')
        else:
            args.append('-Dgtk_doc=false')


        return args

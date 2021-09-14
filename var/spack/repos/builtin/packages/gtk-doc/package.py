# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GtkDoc(AutotoolsPackage):
    """GtkDoc is a tool used to extract API documentation from
    C-code like Doxygen, but handles documentation of GObject
    (including signals and properties) that makes it very
    suitable for GTK+ apps and libraries. It uses docbook for
    intermediate files and can produce html by default and
    pdf/man-pages with some extra work."""

    homepage = "https://wiki.gnome.org/DocumentationProject/GtkDoc"
    url = 'https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/GTK_DOC_1_32/gtk-doc-GTK_DOC_1_32.tar.gz'

    version('1.32', sha256='0890c1f00d4817279be51602e67c4805daf264092adc58f9c04338566e8225ba')

    # Commented out until package dblatex has been created
    # variant('pdf', default=False, description='Adds PDF support')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('pkgconfig', type='build')

    depends_on('python@3.2:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-anytree',       type=('test'))
    depends_on('py-lxml',          type=('test'))
    depends_on('py-parameterized', type=('test'))
    depends_on('py-six',           type=('test'))
    depends_on('libxslt')
    depends_on('libxml2')
    depends_on('docbook-xsl@1.78.1')
    depends_on('docbook-xml@4.3')
    # depends_on('dblatex', when='+pdf')

    patch('build.patch')

    def setup_build_environment(self, env):
        """ If test/tools.sh does not find gtkdocize it starts a sh which blocks"""
        env.prepend_path('PATH',
                         join_path(self.stage.source_path, 'buildsystems', 'autotools'))

    def install(self, spec, prefix):
        make('install', 'V=1')
        install(join_path('buildsystems', 'autotools', 'gtkdocize'), prefix.bin)

    def installcheck(self):
        """gtk-doc does not support installcheck properly, skip it"""
        pass

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/GTK_DOC_{0}/gtk-doc-GTK_DOC_{0}.tar.gz'
        return url.format(version.underscored)

    def configure_args(self):
        args = [
            '--with-xml-catalog={0}'.format(self.spec['docbook-xml'].package.catalog)
        ]
        return args

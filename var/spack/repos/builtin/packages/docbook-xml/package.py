# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DocbookXml(Package):
    """Docbook DTD XML files."""

    homepage = "https://www.oasis-open.org/docbook"
    url      = "https://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"
    list_url = "https://www.oasis-open.org/docbook/xml/"
    list_depth = 1

    version('4.5', sha256='4e4e037a2b83c98c6c94818390d4bdd3f6e10f6ec62dd79188594e26190dc7b4')
    version('4.4', sha256='02f159eb88c4254d95e831c51c144b1863b216d909b5ff45743a1ce6f5273090')
    version('4.3', sha256='23068a94ea6fd484b004c5a73ec36a66aa47ea8f0d6b62cc1695931f5c143464')
    version('4.2', sha256='acc4601e4f97a196076b7e64b368d9248b07c7abf26b34a02cca40eeebe60fa2')

    depends_on('libxml2', type='build')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    @property
    def catalog(self):
        return join_path(self.prefix, 'catalog')

    @run_after('install')
    def config_docbook(self):
        catalog = self.catalog
        version = self.version
        docbook = join_path(prefix, 'docbook')
        ent_dir = join_path(prefix, 'ent')
        xmlcatalog = which('xmlcatalog')

        # create docbook
        xmlcatalog('--noout', '--create', docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//DTD DocBook XML CALS Table Model '
                   'V{0}//EN'.format(version),
                   'file://{0}/calstblx.dtd'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//DTD DocBook XML V{0}//EN'.format(version),
                   'file://{0}/docbookx.dtd'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//DTD XML Exchange Table Model 19990315//EN',
                   'file://{0}/soextblx.dtd'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ENTITIES DocBook XML Character Entities '
                   'V{0}//EN'.format(version),
                   'file://{0}/dbcentx.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ENTITIES DocBook XML Additional General Entities '
                   'V{0}//EN'.format(version),
                   'file://{0}/dbgenent.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ELEMENTS DocBook XML Document Hierarchy '
                   'V{0}//EN'.format(version),
                   'file://{0}/dbhierx.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ENTITIES DocBook XML Notations '
                   'V{0}//EN'.format(version),
                   'file://{0}/dbnotnx.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ELEMENTS DocBook XML Information Pool '
                   'V{0}//EN'.format(version),
                   'file://{0}/dbpoolx.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   '-//OASIS//ELEMENTS DocBook XML HTML Tables '
                   'V{0}//EN'.format(version),
                   'file://{0}/htmltblx.mod'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: Arrow '
                   'Relations//EN',
                   'file://{0}/isoamsa.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: Binary '
                   'Operators//EN',
                   'file://{0}/isoamsb.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN',
                   'file://{0}/isoamsc.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: '
                   'Negated Relations//EN',
                   'file://{0}/isoamsn.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN',
                   'file://{0}/isoamso.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN',
                   'file://{0}/isoamsr.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Box and Line Drawing//EN',
                   'file://{0}/isobox.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Russian Cyrillic//EN',
                   'file://{0}/isocyr1.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN',
                   'file://{0}/isocyr2.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Diacritical Marks//EN',
                   'file://{0}/isodia.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Greek Letters//EN',
                   'file://{0}/isogrk1.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Monotoniko Greek//EN',
                   'file://{0}/isogrk2.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Greek Symbols//EN',
                   'file://{0}/isogrk3.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN',
                   'file://{0}/isogrk4.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Latin 1//EN',
                   'file://{0}/isolat1.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Added Latin 2//EN',
                   'file://{0}/isolat2.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN',
                   'file://{0}/isonum.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES Publishing//EN',
                   'file://{0}/isopub.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'public',
                   'ISO 8879:1986//ENTITIES General Technical//EN',
                   'file://{0}/isotech.ent'.format(ent_dir),
                   docbook)
        xmlcatalog('--noout', '--add', 'rewriteSystem',
                   'https://www.oasis-open.org/docbook/xml/{0}'.format(version),
                   'file://{0}'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'rewriteURI',
                   'https://www.oasis-open.org/docbook/xml/{0}'.format(version),
                   'file://{0}'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'rewriteSystem',
                   'https://www.oasis-open.org/docbook/xml/current',
                   'file://{0}'.format(prefix),
                   docbook)
        xmlcatalog('--noout', '--add', 'rewriteURI',
                   'https://www.oasis-open.org/docbook/xml/current',
                   'file://{0}'.format(prefix),
                   docbook)

        # create catalog
        xmlcatalog('--noout', '--create', catalog)
        xmlcatalog('--noout', '--add', 'delegatePublic',
                   '-//OASIS//ENTITIES DocBook XML',
                   'file://{0}'.format(docbook),
                   catalog)
        xmlcatalog('--noout', '--add', 'delegatePublic',
                   '-//OASIS//DTD DocBook XML',
                   'file://{0}'.format(docbook),
                   catalog)
        xmlcatalog('--noout', '--add', 'delegatePublic',
                   'ISO 8879:1986',
                   'file://{0}'.format(docbook),
                   catalog)
        xmlcatalog('--noout', '--add', 'delegateSystem',
                   'https://www.oasis-open.org/docbook/',
                   'file://{0}'.format(docbook),
                   catalog)
        xmlcatalog('--noout', '--add', 'delegateURI',
                   'https://www.oasis-open.org/docbook/',
                   'file://{0}'.format(docbook),
                   catalog)

    def setup_run_environment(self, env):
        catalog = self.catalog
        env.prepend_path('XML_CATALOG_FILES', catalog, separator=' ')

    def setup_dependent_build_environment(self, env, dependent_spec):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=' ')

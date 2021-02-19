# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Asciidoc(AutotoolsPackage):
    """A presentable text document format for writing articles, UNIX man
    pages and other small to medium sized documents."""

    homepage = "http://asciidoc.org"
    # Always working URL but strangely with another checksum
    url      = "https://github.com/asciidoc-py/asciidoc-py/archive/8.6.10.tar.gz"
    git      = "https://github.com/asciidoc-py/asciidoc-py.git"

    version('master', branch='master')
    version('9.1.0', sha256='fd499fcf51317b1aaf27336fb5e919c44c1f867f1ae6681ee197365d3065238b')
    version('8.6.9', sha256='78db9d0567c8ab6570a6eff7ffdf84eadd91f2dfc0a92a2d0105d323cab4e1f0')

    depends_on('libxml2')
    depends_on('libxslt')
    depends_on('docbook-xml')
    depends_on('docbook-xsl')
    depends_on('python@2.7.0:2.7.99', when='@:8.6.9')

    def url_for_version(self, version):
        if version > Version('8.6.9'):
            url = "https://github.com/asciidoc-py/asciidoc-py/releases/download/{0}/asciidoc-{0}.tar.gz"
        else:
            url = "http://downloads.sourceforge.net/project/asciidoc/asciidoc/{0}/asciidoc-{0}.tar.gz"

        return url.format(version)

    @when('@:8.6.9')
    def install(self, spec, prefix):
        # Old release demands python2
        python = which('python2.7')
        if os.path.isfile(str(python)):
            exes = ['asciidoc', 'a2x']
            for exe in exes:
                fthfile = FileFilter(exe + '.py')
                fthfile.filter('#!/usr/bin/env python', '#!/usr/bin/env python2.7')
        make('install')

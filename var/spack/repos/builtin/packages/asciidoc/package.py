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
    version('9.0.5', sha256='edc8328c3682a8568172656f6fc309b189f65219a49517966c7ea144cb25f8b2')
    version('9.0.4', sha256='400368a43f3eee656d7f197382cd3554b50fb370ef2aea6534f431692a356c66')
    version('9.0.3', sha256='d99c8be8e8a9232742253c2d87c547b2efd4bbd3f0c1e23ef14898ad0fff77c4')
    version('9.0.2', sha256='185fd68e47034c4dd892e1d4ae64c81152bc049e9bdc7d1ad63f927d35810a3b')
    version('8.6.9', sha256='78db9d0567c8ab6570a6eff7ffdf84eadd91f2dfc0a92a2d0105d323cab4e1f0')

    depends_on('libxml2',     type=('build', 'run'))
    depends_on('libxslt',     type=('build', 'run'))
    depends_on('docbook-xml', type=('build', 'run'))
    depends_on('docbook-xsl', type=('build', 'run'))
    depends_on('python@2.3.0:2.7.99', when='@:8.6.9')
    depends_on('python@3.5:',         when='@9.0.2:')

    def url_for_version(self, version):
        if version > Version('8.6.9'):
            url = "https://github.com/asciidoc-py/asciidoc-py/releases/download/{0}/asciidoc-{0}.tar.gz"
        else:
            url = "http://downloads.sourceforge.net/project/asciidoc/asciidoc/{0}/asciidoc-{0}.tar.gz"

        return url.format(version)

    @when('@:8.6.9')
    def install(self, spec, prefix):
        # Old release demands python2
        mpythpath = spec['python'].command.path
        if os.path.isfile(mpythpath):
            exes = ['asciidoc', 'a2x']
            for exe in exes:
                fthfile = FileFilter(exe + '.py')
                fthfile.filter('#!/usr/bin/env python', '#!' + mpythpath)

            make('install')

##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Pdftk(MakefilePackage):
    """PDFtk Server is a command-line tool for working with PDFs. It is
    commonly used for client-side scripting or server-side processing
    of PDFs."""

    homepage = "https://www.pdflabs.com/tools/pdftk-server"
    url      = "https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk-2.02-src.zip"
    # Alternative download locations:
    # https://sources.debian.org/src/pdftk/
    # http://archive.ubuntu.com/ubuntu/pool/universe/p/pdftk/pdftk_2.02.orig.tar.gz

    maintainers = ['citibeth']

    version('2.02', '6534365fd6727724f288a556ede33faa')

    depends_on('eclipse-gcj-parser', type='build')

    # Only takes effect in phases not overridden here
    build_directory = 'pdftk'

    # https://www.pdflabs.com/docs/install-pdftk-on-redhat-or-centos/
    def edit(self, spec, prefix):

        # ------ Fix install directory in main Makefile
        makefile = FileFilter(join_path('pdftk', 'Makefile.Base'))
        makefile.filter('/usr/local/bin', spec.prefix.bin)

        # ------ Create new config file
        compiler = self.compiler
        gcc_base = os.path.split(os.path.split(compiler.cxx)[0])[0]
        gcc_version = compiler.version

        cppflags = (
            '-DPATH_DELIM=0x2f',
            '-DASK_ABOUT_WARNINGS=false',
            '-DUNBLOCK_SIGNALS',
            '-fdollars-in-identifiers')
        cxxflags = ('-Wall', '-Wextra', '-Weffc++', '-O2')
        gcjflags = ('-Wall', '-Wextra', '-O2')
        vars = [
            ('VERSUFF', '-%s' % gcc_version),
            ('CXX', compiler.cxx),
            ('GCJ', spec['eclipse-gcj-parser'].package.gcj),
            ('GCJH', join_path(gcc_base, 'bin', 'gcjh')),
            ('GJAR', join_path(gcc_base, 'bin', 'gjar')),
            ('LIBGCJ', join_path(
                gcc_base, 'share', 'java',
                'libgcj-{0}.jar'.format(gcc_version))),
            ('AR', 'ar'),
            ('RM', 'rm'),
            ('ARFLAGS', 'rs'),
            ('RMFLAGS', '-vf'),
            ('CPPFLAGS', ' '.join(cppflags)),
            ('CXXFLAGS', ' '.join(cxxflags)),
            ('GCJFLAGS', ' '.join(gcjflags)),
            ('GCJHFLAGS', '-force'),
            ('LDLIBS', '-lgcj')
        ]
        with open(join_path('pdftk', 'Makefile.Spack'), 'w') as mk:
            for var, val in vars:
                mk.write("export {0}={1}\n".format(var, str(val)))
            mk.write('include Makefile.Base\n')

    def build(self, spec, prefix):
        compiler = self.compiler
        gcc_base = os.path.split(os.path.split(compiler.cxx)[0])[0]
        env['PATH'] = join_path(gcc_base, 'bin') + ':' + env['PATH']
        with working_dir(self.build_directory):
            make('-f', 'Makefile.Spack', parallel=False)

    def install(self, spec, prefix):
        mkdirp(self.spec.prefix.bin)
        with working_dir(self.build_directory):
            make('-f', 'Makefile.Spack', 'install', parallel=False)

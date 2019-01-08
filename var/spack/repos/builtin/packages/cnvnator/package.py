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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install cnvnator
#
# You can edit this file again by typing:
#
#     spack edit cnvnator
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Cnvnator(MakefilePackage):
    """A tool for CNV discovery and genotyping from depth-of-coverage by mapped reads."""

    homepage = "https://github.com/abyzovlab/CNVnator"
    url      = "https://github.com/abyzovlab/CNVnator/archive/v0.3.3.tar.gz"

    version('0.3.3', 'f9fc0c2e79abe85decab00d3748d8904')

    depends_on('samtools')
    depends_on('htslib')
    depends_on('root')
    depends_on('bzip2')
    depends_on('curl')
    depends_on('lzma')
    depends_on('zlib')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        # Replace CXX with CXXFLAGS
        makefile.filter('CXX.*=.*', 'CXXFLAGS = -O3 -std=c++11 -DCNVNATOR_VERSION=\\"$(VERSION)\\" $(OMPFLAGS)')
        makefile.filter('$(CXX)', '$(CXX) $(CXXFLAGS)', string=True)
        # Replace -I$(SAMDIR) with -I$(SAMINC)
        makefile.filter('-I$(SAMDIR)', '-I$(SAMINC)', string=True)
        # Link more libs
        makefile.filter('^override LIBS.*', 'override LIBS += -lz -lbz2 -lcurl -llzma')

    def build(self, spec, prefix):
        make('ROOTSYS={0}'.format(spec['root'].prefix),
             'SAMINC={0}'.format(spec['samtools'].prefix.include),
             'SAMDIR={0}'.format(spec['samtools'].prefix.lib),
             'HTSDIR={0}'.format(spec['htslib'].prefix.lib))

    def install(self, spec, prefix):
        mkdir = which('mkdir')
        mkdir(prefix.bin)
        install('cnvnator', prefix.bin)

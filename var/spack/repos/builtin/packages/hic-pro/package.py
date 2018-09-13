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


class HicPro(MakefilePackage):
    """HiC-Pro is a package designed to process Hi-C data,
    from raw fastq files (paired-end Illumina data)
    to the normalized contact maps"""

    homepage = "https://github.com/nservant/HiC-Pro"
    url      = "https://github.com/nservant/HiC-Pro/archive/v2.10.0.tar.gz"

    version('2.10.0', '6ae2213dcc984b722d1a1f65fcbb21a2')

    depends_on('bowtie2')
    depends_on('samtools')
    depends_on('python+ucs4@2.7:2.8')
    depends_on('r')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-bx-python', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))

    def edit(self, spec, prefix):
        config = FileFilter('config-install.txt')
        config.filter('PREFIX =.*', 'PREFIX = {0}'.format(prefix))
        config.filter('BOWTIE2 PATH =.*',
                      'BOWTIE2_PATH = {0}'.format(spec['bowtie2'].prefix))
        config.filter('SAMTOOLS_PATH =.*',
                      'SAMTOOLS_PATH = {0}'.format(spec['samtools'].prefix))
        config.filter('R_PATH =.*',
                      'R_RPTH ={0}'.format(spec['r'].prefix))
        config.filter('PYTHON_PATH =.*',
                      'PYTHON_RPTH ={0}'.format(spec['python'].prefix))

    def build(self, spec, preifx):
        make('-f', './scripts/install/Makefile',
             'CONFIG_SYS=./config-install.txt')
        make('mapbuilder')
        make('readstrimming')
        make('iced')

    def install(self, spec, prefix):
        # Patch INSTALLPATH in config-system.txt
        config = FileFilter('config-system.txt')
        config.filter('/HiC-Pro_%s' % self.version, '')
        # Install
        install('config-hicpro.txt', prefix)
        install('config-install.txt', prefix)
        install('config-system.txt', prefix)
        install_tree('bin', prefix.bin)
        install_tree('annotation', prefix.annotation)
        install_tree('doc', prefix.doc)
        install_tree('scripts', prefix.scripts)
        install_tree('test-op', join_path(prefix, 'test-op'))

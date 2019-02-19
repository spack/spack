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


class PyUnicycler(PythonPackage):
    """Unicycler is an assembly pipeline for bacterial genomes. It can
    assemble Illumina-only read sets where it functions as a SPAdes-optimiser.
    It can also assembly long-read-only sets (PacBio or Nanopore) where it
    runs a miniasm+Racon pipeline. For the best possible assemblies, give it
    both Illumina reads and long reads, and it will conduct a hybrid assembly.
    """

    homepage = "https://github.com/rrwick/Unicycler"
    url      = "https://github.com/rrwick/Unicycler/archive/v0.4.5.tar.gz"

    version('0.4.7', '10ee4fef4bd9a46702de83537a902164')
    version('0.4.6', '78633a5f557af23e62d6b37d1caedf53')
    version('0.4.5', 'f7b4f6b712fee6a4fa86a046a6781768')

    depends_on('python@3.4:', type=('build', 'link', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('spades', type='run')
    depends_on('pilon', type='run')
    depends_on('jdk', type=('build', 'run'))
    depends_on('bowtie2', type='run')
    depends_on('samtools@1.0:', type=('build', 'link', 'run'))
    depends_on('racon', type=('build', 'link', 'run'))
    depends_on('blast-plus', type='run')

    conflicts('%gcc@:4.9.0')
    conflicts('%clang@:3.4.2')

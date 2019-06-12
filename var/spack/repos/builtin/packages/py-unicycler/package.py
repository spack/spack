# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

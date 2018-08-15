##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Trinity(MakefilePackage):
    """Trinity, developed at the Broad Institute and the Hebrew University of
       Jerusalem, represents a novel method for the efficient and robust de
       novo reconstruction of transcriptomes from RNA-seq data. Trinity
       combines three independent software modules: Inchworm, Chrysalis, and
       Butterfly, applied sequentially to process large volumes of RNA-seq
       reads. Trinity partitions the sequence data into many individual de
       Bruijn graphs, each representing the transcriptional complexity at a
       given gene or locus, and then processes each graph independently to
       extract full-length splicing isoforms and to tease apart transcripts
       derived from paralogous genes.
    """

    homepage = "http://trinityrnaseq.github.io/"
    url      = "https://github.com/trinityrnaseq/trinityrnaseq/archive/Trinity-v2.6.6.tar.gz"

    version('2.6.6', 'b7472e98ab36655a6d9296d965471a56')

    depends_on("java@8:", type=("build", "run"))
    depends_on("bowtie2")
    depends_on("jellyfish")
    depends_on("salmon")
    depends_on("perl+threads", type=("build", "run"))
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def build(self, spec, prefix):
        make()
        make("trinity_essentials")
        make("plugins")

    def install(self, spec, prefix):
        install_tree('.', prefix.bin)
        force_remove(join_path(prefix.bin, '.gitmodules'))
        force_remove(join_path(prefix.bin, 'Butterfly', '.err'))
        force_remove(join_path(prefix.bin, 'Butterfly', 'src', '.classpath'))
        force_remove(join_path(prefix.bin, 'Butterfly', 'src', '.err'))
        force_remove(join_path(prefix.bin, 'Butterfly', 'src', '.project'))
        remove_linked_tree(join_path(prefix.bin, 'Butterfly', 'src',
                                     '.settings'))
        remove_linked_tree(join_path(prefix.bin, 'Inchworm', 'src', '.deps'))
        remove_linked_tree(join_path(prefix.bin, 'trinity-plugins',
                                     'ParaFly-0.1.0', 'src', '.deps'))
        force_remove(join_path(prefix.bin, 'trinity-plugins',
                               'seqtk-trinity-0.0.2', '.gitignore'))
        force_remove(join_path(prefix.bin, 'trinity-plugins', 'slclust', 'bin',
                               '.hidden'))

    def setup_environment(self, spack_env, run_env):
        run_env.set('TRINITY_HOME', self.prefix.bin)
        spack_env.append_flags('CXXFLAGS', self.compiler.openmp_flag)

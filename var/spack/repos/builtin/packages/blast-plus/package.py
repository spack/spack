##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os
from spack import *


class BlastPlus(Package):
    """BLAST (Basic Local Alignment Search Tool) finds regions of similarity
    between biological sequences. The program compares nucleotide or protein sequences
    to sequence databases and calculates the statistical significance"""

    homepage = "http://ncbi.nlm.nih.gov/Blast.cgi"

    variant("static", default=True, description="build static libraries and executables")
    variant("freetype", default=False, description="build with freetype")
    variant("gnutls", default=False, description="enable gnutls")
    variant("hdf5", default=False, description="enable hdf5")
    variant("jpeg", default=True, description="enable jpeg")
    variant("libpng", default=True, description="enable libpng")
    variant("pcre", default=True, description="enable pcre")
    variant("python", default=True, description="build with python support")
    variant("debug", default=True, description="Enable debug")

    version('2.6.0', 'c8ce8055b10c4d774d995f88c7cc6225', url="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.6.0+-src.tar.gz")
    version('2.5.0', '54ad4f2ea15715487b3de712a9d27be8',  url="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.5.0/ncbi-blast-2.5.0+-src.tar.gz")

    depends_on("freetype", when="+freetype")
    depends_on("gnutls", when="+gnutls")
    depends_on("python", when="+python")
    depends_on("hdf5", when="+hdf5")
    depends_on("jpeg", when="+jpeg")
    depends_on("pcre", when="+pcre")
    depends_on("libpng", when="+libpng")


    # Run patch to prevent make install from failing. 
    # Patch and problem were solved in this thread:
    # https://github.com/Homebrew/homebrew-science/pull/4740
    patch('blast-plus-make-fix.patch', when="@2.5.0:")

    def install(self, spec, prefix):
        config_args = ["--prefix=" + prefix,
                       "--with-bin-release",
                       "--with-mt",
                       "--with-64",
                       "--without-debug",
                       "--with-optimization"]

        if "+static" in spec:
            config_args.append("--with-static")
            config_args.append("LDFLAGS=-static")
            if not spec.satisfies("platform=linux"):
                config_args.append("--with-static-exe")
        else:
            config_args.extend(["--without-static", "--without-static-exe"])

        if "+freetype" in spec:
            config_args.append("--with-freetype=%s" % self.spec['freetype'].prefix)
        if "+gnutls" in spec:
            config_args.append("--with-gnutls=%s" % self.spec['gnutls'].prefix)
        if "+jpeg" in spec:
            config_args.append("--with-jpeg=%s" % self.spec['jpeg'].prefix)
        if "+libpng" in spec:
            config_args.append("--with-png=%s" % self.spec['libpng'].prefix)
        if "+pcre" in spec:
            config_args.append("--with-pcre=%s" % self.spec['pcre'].prefix)
        if "+hdf5" in spec:
            config_args.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
        if "+python" in spec:
            config_args.append("--with-python=%s" % spec['python'].prefix)


        with working_dir("c++"):
            configure(*config_args)
            make()
            make("install")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gor(MakefilePackage):
    """The GOR (Garnier–Osguthorpe–Robson) method is an information theory-based method
    for the prediction of secondary structures in proteins"""

    homepage = (
        "https://npsa-prabi.ibcp.fr/cgi-bin/npsa_automat.pl?page=/NPSAHLP/npsahlp_secpredgor4.html"
    )
    # This mirror is the only extant download of GOR that I can find, as per
    #   https://github.com/cbcrg/tcoffee/blob/master/lib/data_headers/tclinkdb.txt
    url = "https://s3.eu-central-1.amazonaws.com/tcoffee-packages/mirrors/source/GOR_IV.tar.gz"

    version("4", sha256="3c2707195e39bc682d8fb9d7d1ee39d07a43588209fff54487ff2a2d0bf2f18e")

    build_directory = "SOURCE"

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file("cc", spack_cc, "Makefile")
            filter_file("DATABASE", prefix.DATABASE, "gor.c")

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            make("gor")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install("gorIV", prefix.bin)
        install_tree("DATABASE", prefix.DATABASE)

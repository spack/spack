# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Paraver(Package):
    """"A very powerful performance visualization and analysis tool
        based on traces that can be used to analyse any information that
        is expressed on its input trace format.  Traces for parallel MPI,
        OpenMP and other programs can be genereated with Extrae."""
    homepage = "https://tools.bsc.es/paraver"
    url = "https://ftp.tools.bsc.es/paraver/wxparaver-4.6.3-src.tar.bz2"

    # NOTE: Paraver provides only latest version for download.
    #       Don't keep/add older versions.
    version('4.6.3', '7940a2651f56712c4e8a21138b4bf16c')
    version('4.6.2', '3f5b3e207d98b2c44101f1ff5685aa55')

    depends_on("boost")
    # depends_on("extrae")
    depends_on("wxwidgets")
    depends_on("wxpropgrid")

    def install(self, spec, prefix):
        os.chdir("ptools_common_files")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../paraver-kernel")
        # "--with-extrae=%s" % spec['extrae'].prefix,
        configure("--prefix=%s" % prefix,
                  "--with-ptools-common-files=%s" % prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--with-boost-serialization=boost_serialization")
        make()
        make("install")

        os.chdir("../paraver-toolset")
        configure("--prefix=%s" % prefix)
        make()
        make("install")

        os.chdir("../wxparaver")
        # "--with-extrae=%s" % spec['extrae'].prefix,
        configure("--prefix=%s" % prefix,
                  "--with-paraver=%s" % prefix,
                  "--with-boost=%s" % spec['boost'].prefix,
                  "--with-boost-serialization=boost_serialization",
                  "--with-wxdir=%s" % spec['wx'].prefix.bin)
        make()
        make("install")

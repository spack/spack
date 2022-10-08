# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pilercr(Package):
    """Identification and analysis of CRISPR repeats."""

    homepage = "http://www.drive5.com/pilercr/"
    url = "http://www.drive5.com/pilercr/pilercr1.06.tar.gz"

    version("1.06", sha256="50175f7aa171674cda5ba255631f340f9cc7f80e8cc25135a4cb857147d91068")

    def install(self, spec, prefix):
        make()
        make("install")

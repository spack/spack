# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Qthreads(AutotoolsPackage):
    """The qthreads API is designed to make using large numbers of
       threads convenient and easy, and to allow portable access to
       threading constructs used in massively parallel shared memory
       environments. The API maps well to both MTA-style threading and
       PIM-style threading, and we provide an implementation of this
       interface in both a standard SMP context as well as the SST
       context. The qthreads API provides access to full/empty-bit
       (FEB) semantics, where every word of memory can be marked
       either full or empty, and a thread can wait for any word to
       attain either state."""
    homepage = "http://www.cs.sandia.gov/qthreads/"

    url = "https://github.com/Qthreads/qthreads/releases/download/1.10/qthread-1.10.tar.bz2"
    version("1.14", sha256="16f15e5b2e35b6329a857d24c283a1e43cd49921ee49a1446d4f31bf9c6f5cf9")
    version("1.12", sha256="2c13a5f6f45bc2f22038d272be2e748e027649d3343a9f824da9e86a88b594c9")
    version("1.11", sha256="dbde6c7cb7de7e89921e47363d09cecaebf775c9d090496c2be8350355055571")
    version("1.10", sha256="29fbc2e54bcbc814c1be13049790ee98c505f22f22ccee34b7c29a4295475656")

    patch("restrict.patch", when="@:1.10")
    patch("trap.patch", when="@:1.10")

    variant(
        'hwloc',
        default=True,
        description='hwloc support'
    )

    depends_on("hwloc@1.0:1.99", when="+hwloc")

    def configure_args(self):
        spec = self.spec
        if "+hwloc" in self.spec:
            args = [
                "--enable-guard-pages",
                "--with-topology=hwloc",
                "--with-hwloc=%s" % spec["hwloc"].prefix]
        else:
            args = ["--with-topology=no"]
        return args

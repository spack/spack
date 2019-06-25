# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version("1.14", "3e6eb58baf78dc961b19a37b2dc4f9a5")
    version("1.12", "c857d175f8135eaa669f3f8fa0fb0c09")
    version("1.11", "68b5f9a41cfd1a2ac112cc4db0612326")
    version("1.10", "d1cf3cf3f30586921359f7840171e551")

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

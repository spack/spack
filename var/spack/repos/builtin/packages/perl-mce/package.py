# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMce(PerlPackage):
    """MCE - Many-Core Engine for Perl providing parallel processing
    capabilities.

    MCE spawns a pool of workers and therefore does not fork a new process per
    each element of data. Instead, MCE follows a bank queuing model. Imagine
    the line being the data and bank-tellers the parallel workers. MCE enhances
    that model by adding the ability to chunk the next n elements from the
    input stream to the next available worker."""

    homepage = "https://github.com/marioroy/mce-perl"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MARIOROY/MCE-1.874.tar.gz"

    version("1.879", sha256="9c4cf39838b5c113448799af451b3d64b54e0de39d635536d7e85e8bdc5888dc")
    version("1.878", sha256="bb5713197cc5ab91302aec746b5cc7204bf84556c30d6af67ce34a6fd38444ad")
    version("1.877", sha256="e2a05061b88e909e90b01320b8381d7e2f8f3840d0f0b35c2f816daf7edcf2ea")
    version("1.876", sha256="dfee4b9ea91c89acb58c0defefdd46633a9d4f04b01e43ec16515fd5c675e510")
    version("1.875", sha256="d01b5454bba594352525bb485c08c499c802d75504e3a2fec9e3b6c3542205f9")
    version("1.874", sha256="d809e3018475115ad7eccb8bef49bde3bf3e75abbbcd80564728bbcfab86d3d0")
    provides("perl-mce-candy")  # AUTO-CPAN2Spack
    provides("perl-mce-channel")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-mutex")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-mutexfast")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-simple")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-simplefast")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-threads")  # AUTO-CPAN2Spack
    provides("perl-mce-channel-threadsfast")  # AUTO-CPAN2Spack
    provides("perl-mce-child")  # AUTO-CPAN2Spack
    provides("perl-mce-core-input-generator")  # AUTO-CPAN2Spack
    provides("perl-mce-core-input-handle")  # AUTO-CPAN2Spack
    provides("perl-mce-core-input-iterator")  # AUTO-CPAN2Spack
    provides("perl-mce-core-input-request")  # AUTO-CPAN2Spack
    provides("perl-mce-core-input-sequence")  # AUTO-CPAN2Spack
    provides("perl-mce-core-manager")  # AUTO-CPAN2Spack
    provides("perl-mce-core-validation")  # AUTO-CPAN2Spack
    provides("perl-mce-core-worker")  # AUTO-CPAN2Spack
    provides("perl-mce-flow")  # AUTO-CPAN2Spack
    provides("perl-mce-grep")  # AUTO-CPAN2Spack
    provides("perl-mce-loop")  # AUTO-CPAN2Spack
    provides("perl-mce-map")  # AUTO-CPAN2Spack
    provides("perl-mce-mutex")  # AUTO-CPAN2Spack
    provides("perl-mce-mutex-channel")  # AUTO-CPAN2Spack
    provides("perl-mce-mutex-channel2")  # AUTO-CPAN2Spack
    provides("perl-mce-mutex-flock")  # AUTO-CPAN2Spack
    provides("perl-mce-queue")  # AUTO-CPAN2Spack
    provides("perl-mce-relay")  # AUTO-CPAN2Spack
    provides("perl-mce-signal")  # AUTO-CPAN2Spack
    provides("perl-mce-step")  # AUTO-CPAN2Spack
    provides("perl-mce-stream")  # AUTO-CPAN2Spack
    provides("perl-mce-subs")  # AUTO-CPAN2Spack
    provides("perl-mce-util")  # AUTO-CPAN2Spack
    depends_on("perl@5.8.1:", type=("build", "run"))  # AUTO-CPAN2Spack
    depends_on("perl-sereal-decoder@3.15:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-time-hires", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-scalar-util", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-sereal-encoder@3.15:", type="run")  # AUTO-CPAN2Spack

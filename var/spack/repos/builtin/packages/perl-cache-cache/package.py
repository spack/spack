# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCacheCache(PerlPackage):
    """Extends Cache::SizeAwareMemoryCache."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Cache-Cache-1.08.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.08", sha256="d2c7fd5dba5dd010b7d8923516890bb6ccf6b5f188ccb69f35cb0fd6c031d1e8")
    version("1.07", sha256="c1afe8fff07f05385468f78f3fdbf1dbb5fd2bb70b50c25163d5be540bdc8d12")

    provides("perl-cache-basecache")  # AUTO-CPAN2Spack
    provides("perl-cache-basecachetester")  # AUTO-CPAN2Spack
    provides("perl-cache-cachemetadata")  # AUTO-CPAN2Spack
    provides("perl-cache-cachesizer")  # AUTO-CPAN2Spack
    provides("perl-cache-cachetester")  # AUTO-CPAN2Spack
    provides("perl-cache-cacheutils")  # AUTO-CPAN2Spack
    provides("perl-cache-filebackend")  # AUTO-CPAN2Spack
    provides("perl-cache-filecache")  # AUTO-CPAN2Spack
    provides("perl-cache-memorybackend")  # AUTO-CPAN2Spack
    provides("perl-cache-memorycache")  # AUTO-CPAN2Spack
    provides("perl-cache-nullcache")  # AUTO-CPAN2Spack
    provides("perl-cache-object")  # AUTO-CPAN2Spack
    provides("perl-cache-sharedmemorybackend")  # AUTO-CPAN2Spack
    provides("perl-cache-sharedmemorycache")  # AUTO-CPAN2Spack
    provides("perl-cache-sizeawarecache")  # AUTO-CPAN2Spack
    provides("perl-cache-sizeawarecachetester")  # AUTO-CPAN2Spack
    provides("perl-cache-sizeawarefilecache")  # AUTO-CPAN2Spack
    provides("perl-cache-sizeawarememorycache")  # AUTO-CPAN2Spack
    provides("perl-cache-sizeawaresharedmemorycache")  # AUTO-CPAN2Spack
    depends_on("perl-error@0.15:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-ipc-sharelite@0.9:", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack
    depends_on("perl-digest-sha1@2.2:", type="run")  # AUTO-CPAN2Spack

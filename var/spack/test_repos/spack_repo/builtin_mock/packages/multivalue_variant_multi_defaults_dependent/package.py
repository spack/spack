# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class MultivalueVariantMultiDefaultsDependent(Package):
    homepage = "http://www.spack.llnl.gov"
    url = "http://www.spack.llnl.gov/mpileaks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    # includes a subset of the default values `bar,baz`; we expect the request for myvariant=bar
    # not to override the default myvariant=bar,baz
    depends_on("multivalue-variant-multi-defaults myvariant=bar")

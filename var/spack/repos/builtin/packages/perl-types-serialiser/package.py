# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTypesSerialiser(PerlPackage):
    """Simple data types for common serialisation formats."""  # AUTO-CPAN2Spack

    homepage = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN"  # AUTO-CPAN2Spack
    url = "https://cpan.metacpan.org/authors/id/M/ML/MLEHMANN/Types-Serialiser-1.01.tar.gz"

    maintainers = ["chissg", "gartung", "marcmengel", "vitodb"]  # AUTO-CPAN2Spack

    version("1.01", sha256="f8c7173b0914d0e3d957282077b366f0c8c70256715eaef3298ff32b92388a80")
    version("1.0", sha256="7ad3347849d8a3da6470135018d6af5fd8e58b4057cd568c3813695f2a04730d")

    provides("perl-json-pp-boolean")  # AUTO-CPAN2Spack
    provides("perl-types-serialiser-booleanbase")  # AUTO-CPAN2Spack
    provides("perl-types-serialiser-error")  # AUTO-CPAN2Spack
    depends_on("perl-common-sense", type="run")  # AUTO-CPAN2Spack
    depends_on("perl-extutils-makemaker", type="build")  # AUTO-CPAN2Spack

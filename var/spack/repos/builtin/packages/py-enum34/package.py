# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEnum34(PythonPackage):
    """Python 3.4 Enum backported to 3.3, 3.2, 3.1, 2.7, 2.6, 2.5, and 2.4.

    An enumeration is a set of symbolic names (members) bound to unique,
    constant values. Within an enumeration, the members can be compared by
    identity, and the enumeration itself can be iterated over."""

    homepage = "https://pypi.org/project/enum34/"
    pypi = "enum34/enum34-1.1.10.tar.gz"

    # NOTE: This project no longer appears to be maintained.

    version("1.1.10", sha256="cce6a7477ed816bd2542d03d53db9f0db935dd013b70f336a95c73979289f248")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")

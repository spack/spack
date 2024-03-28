# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProfilehooks(PythonPackage):
    """Python decorators for profiling/tracing/timing a single function"""

    homepage = "https://mg.pov.lt/profilehooks/"
    pypi = "profilehooks/profilehooks-1.11.2.tar.gz"

    git = "https://github.com/mgedmin/profilehooks.git"

    license("MIT")

    version(
        "1.11.2",
        sha256="29627b3e9938d77e1237089278d22f103b8373b82f841651a4f322b0ae101665",
        url="https://pypi.org/packages/26/25/5b748479b609ed0b134b013f6fff9a708ddf5194fa3f90edacfc738fa3f9/profilehooks-1.11.2-py2.py3-none-any.whl",
    )

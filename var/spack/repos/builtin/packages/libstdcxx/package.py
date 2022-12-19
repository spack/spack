# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libstdcxx(Package):
    homepage = "https://gcc.gnu.org"
    has_code = False

    version("3.4.31")
    version("3.4.30")
    version("3.4.29")
    version("3.4.28")
    version("3.4.28")
    version("3.4.27")
    version("3.4.26")
    version("3.4.25")
    version("3.4.24")
    version("3.4.23")
    version("3.4.22")
    version("3.4.21")
    version("3.4.20")
    version("3.4.19")
    version("3.4.18")
    version("3.4.17")
    version("3.4.16")
    version("3.4.15")
    version("3.4.14")
    version("3.4.13")
    version("3.4.12")
    version("3.4.11")
    version("3.4.10")
    version("3.4.9")
    version("3.4.8")
    version("3.4.7")
    version("3.4.6")
    version("3.4.5")
    version("3.4.4")
    version("3.4.3")
    version("3.4.2")

    depends_on("gcc@13.1.0", when="@3.4.31", type="compiler")
    depends_on("gcc@12.1.0:12", when="@3.4.30", type="compiler")
    depends_on("gcc@11.1.0:11", when="@3.4.29", type="compiler")
    # not a typo, no symbol version change between 9.3 / 10.1
    depends_on("gcc@9.3.0:10", when="@3.4.28", type="compiler")
    depends_on("gcc@9.2.0", when="@3.4.27", type="compiler")
    depends_on("gcc@9.1.0", when="@3.4.26", type="compiler")
    depends_on("gcc@8.1.0:8", when="@3.4.25", type="compiler")
    depends_on("gcc@7.2.0:7", when="@3.4.24", type="compiler")
    depends_on("gcc@7.1.0", when="@3.4.23", type="compiler")
    depends_on("gcc@6.1.0:6", when="@3.4.22", type="compiler")
    depends_on("gcc@5.1.0:5", when="@3.4.21", type="compiler")
    depends_on("gcc@4.9.0:4", when="@3.4.20", type="compiler")
    depends_on("gcc@4.8.3", when="@3.4.19", type="compiler")
    depends_on("gcc@4.8.0", when="@3.4.18", type="compiler")
    depends_on("gcc@4.7.0", when="@3.4.17", type="compiler")
    depends_on("gcc@4.6.1", when="@3.4.16", type="compiler")
    depends_on("gcc@4.6.0", when="@3.4.15", type="compiler")
    depends_on("gcc@4.5.0", when="@3.4.14", type="compiler")

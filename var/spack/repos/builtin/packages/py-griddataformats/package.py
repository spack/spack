# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGriddataformats(PythonPackage):
    """The gridDataFormats package provides classes to unify reading
    and writing n-dimensional datasets. One can read grid data from
    files, make them available as a Grid object, and write out the
    data again."""

    homepage = "http://www.mdanalysis.org/GridDataFormats"
    pypi = "GridDataFormats/GridDataFormats-0.5.0.tar.gz"

    maintainers("RMeli")

    version("1.0.1", sha256="ad2c9ab7d672a6d8c426de7d083eee4f3e2b0bd59391675d30683c768ab83cc4")
    version(
        "0.5.0",
        sha256="f317ed60708de22d1b2a76ce89a00f722d903291b1055ff1018d441870c39d69",
        deprecated=True,
    )
    version(
        "0.4.1",
        sha256="b362662c2dc475e2a3895fe044eaaa9a707bd660fd109a63dac84a47236690a3",
        deprecated=True,
    )
    version(
        "0.4.0",
        sha256="f81d6b75aa7ebd9e8b64e14558c2d2583a0589829382beb4ef69860110261512",
        deprecated=True,
    )
    version(
        "0.3.3",
        sha256="938f0efcb3bc2f58ec85048b933942da8a52c134170acc97cb095f09d3698fbd",
        deprecated=True,
    )

    depends_on("py-setuptools", type="build")

    depends_on("python@3.8:", when="@1:", type=("build", "run"))

    depends_on("py-numpy@1.19:", when="@1:", type=("build", "run"))
    depends_on("py-scipy", when="@1:", type=("build", "run"))
    depends_on("py-mrcfile", when="@1:", type=("build", "run"))

    # Deprecated
    depends_on("python@2.7:", when="@0", type=("build", "run"))
    depends_on("py-numpy@1.0.3:", when="@0", type=("build", "run"))
    depends_on("py-six", when="@0", type=("build", "run"))

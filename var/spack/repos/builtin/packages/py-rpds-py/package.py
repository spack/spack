# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRpdsPy(PythonPackage):
    """Python bindings to the Rust rpds crate for persistent data structures."""

    homepage = "https://rpds.readthedocs.io/"
    pypi = "rpds_py/rpds_py-0.20.0.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.20.0", sha256="d72a210824facfdaf8768cf2d7ca25a042c30320b3020de2fa04640920d4e121")

    depends_on("py-maturin@1.2:1", type="build")

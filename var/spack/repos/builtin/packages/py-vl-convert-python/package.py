# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVlConvertPython(PythonPackage):
    """Convert Vega-Lite chart specifications to SVG, PNG, or Vega"""

    homepage = "https://github.com/jonmmease/vl-convert"
    pypi = "vl_convert_python/vl_convert_python-0.13.1.tar.gz"

    version("0.13.1", sha256="d70a608257dd6b5b782d96cccebfe7289992e522e47a8bebb7d928253ca8b396")

    depends_on("python@3.7:", type=("build", "run"))

    # TODO: This package currently requires internet access to install.
    depends_on("py-maturin@1.1:1", type="build")

    depends_on("cmake", type="build")  # some rust dependencies need this

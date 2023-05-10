# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPanedr(PythonPackage):
    """Panedr uses the Pyedr library to read a Gromacs EDR binary energy XDR file and returns
    its contents as a pandas dataframe"""

    homepage = "https://github.com/MDAnalysis/panedr"
    pypi = "panedr/panedr-0.7.1.tar.gz"

    maintainers("RMeli")

    version("0.7.1", sha256="64c74863f72d51729ac5cb1e2dbb18747f7137588990c308ef8ca120fbf2ddd4")

    # PyEDR is released together with PanEDR, therefore versions should match
    depends_on("py-pyedr@0.7.1", type=("build", "run"), when="@0.7.1")

    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pbr", type=("build", "run"))

    depends_on("py-setuptools", type="build")

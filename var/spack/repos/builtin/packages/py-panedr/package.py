# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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

    license("LGPL-2.1-or-later")

    version(
        "0.7.2",
        sha256="fe8ba7071eae60db38b1d6307866baaf4f8ccd1b18d38708659b05ff078fe89b",
        url="https://pypi.org/packages/c1/e9/3f7a09dc2ceb866e143c47f32486913eded2013525a0e3c2798a7aaa136c/panedr-0.7.2-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="61704feaed3feb47189a719e3e37d3b61f75f92c4f701d6490be5925519a1ba3",
        url="https://pypi.org/packages/70/fa/f725a900f77401699fb60862395610b5d93d3d396ec9571fe8fda97a6c57/panedr-0.7.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pandas")
        depends_on("py-pbr", when="@:0.7")
        depends_on("py-pyedr", when="@0.6:")

    # PyEDR is released together with PanEDR, therefore versions should match

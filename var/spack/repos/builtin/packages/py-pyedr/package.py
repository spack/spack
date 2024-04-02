# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyedr(PythonPackage):
    """Pyedr provides a means of reading a Gromacs EDR binary XDR file and return
    its contents as a dictionary of NumPy arrays"""

    homepage = "https://github.com/MDAnalysis/panedr"
    pypi = "pyedr/pyedr-0.7.1.tar.gz"

    maintainers("RMeli")

    license("LGPL-2.1-or-later")

    version(
        "0.7.2",
        sha256="c5f024973f69ec32a3234eb4033b69044dbd3a73a9c96ed59f2b0f9962fb63ed",
        url="https://pypi.org/packages/35/63/02ea8cef64bdead4c65d6e80f1f92f82b6db7438d285fa30ee4484102485/pyedr-0.7.2-py3-none-any.whl",
    )
    version(
        "0.7.1",
        sha256="7914ec210abb17a72684b4a8f042c5cfcf19042d3afa3bce2b3f0a2c9d22affa",
        url="https://pypi.org/packages/64/76/5b1a485afba2cbaa5634a49eed716d12dcf92fcc548c2ea531f4bc2f4fc6/pyedr-0.7.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-mda-xdrlib", when="@0.7.2:")
        depends_on("py-numpy@1.19.0:", when="@:0.7")
        depends_on("py-pbr", when="@:0.7")
        depends_on("py-tqdm", when="@0.7.1:")

    # Minimal NumPy version only specified in requirements.txt

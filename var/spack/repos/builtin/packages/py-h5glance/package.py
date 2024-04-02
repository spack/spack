# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyH5glance(PythonPackage):
    """H5Glance lets you explore HDF5 files in the terminal or
    an HTML interface.
    """

    homepage = "https://github.com/European-XFEL/h5glance"
    pypi = "h5glance/h5glance-0.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.6",
        sha256="ddb5a71604c06619dca1d895603fda2057c999376751e48f52c3ec4b1721e829",
        url="https://pypi.org/packages/fe/71/c5acb6ec531ebf431ae6f2fd34e17b729ddbe9a7d5038ac88a5175f88f34/h5glance-0.6-py3-none-any.whl",
    )
    version(
        "0.5",
        sha256="3b4bc11cb8c0b3316cf16c888d094ccda6a69a2e9dcbcebb898cce07db42c473",
        url="https://pypi.org/packages/e2/7f/f3d2a4477d14ff082c328d534b047dbad399af028c33819683594e61c59e/h5glance-0.5-py3-none-any.whl",
    )
    version(
        "0.4",
        sha256="e4c06ca1ed3ba3aed44ba8f5b3e00fc70425988a1da0cccb62de5d1b8f11813a",
        url="https://pypi.org/packages/f6/a8/3ee16ab4e4f9ad6989c1502408885b128ecb2e750f5156c607f3720303ab/h5glance-0.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py", when="@:0.6")
        depends_on("py-htmlgen")

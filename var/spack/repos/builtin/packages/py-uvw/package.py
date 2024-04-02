# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUvw(PythonPackage):
    """
    UVW is a small utility library to write VTK files
    from data contained in Numpy arrays.
    """

    homepage = "https://github.com/prs513rosewood/uvw"
    git = "https://github.com/prs513rosewood/uvw.git"
    pypi = "uvw/uvw-0.3.1.tar.gz"

    maintainers("prs513rosewood")

    license("MIT")

    version(
        "0.5.0",
        sha256="f929e3260385dbd607cdaab77f0562b6757e4230e2d2f8c6c9737a8e379a4821",
        url="https://pypi.org/packages/1b/aa/e718b4a2eefa6937b7514744f3dc639ae2d006a6440c3542008f37cef927/uvw-0.5.0-py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="c21cd66483b2d947f5cb6778d6f700b7dae81106cd49284434bedb395be31d73",
        url="https://pypi.org/packages/63/3a/40590dea2b1452f000a29286debd538c5f709e09d045fa71fee4b58f7f8c/uvw-0.4.0-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="940aaf7fa7ce86216442d74df261e56a854484458333850d7818e7b041670399",
        url="https://pypi.org/packages/1b/a9/197f8137d43c84bc85deeb821e756806d335fdacddbaf21fb1b0f7e97a0f/uvw-0.3.2-py3-none-any.whl",
    )
    version(
        "0.3.1",
        sha256="1e14c4f4381bb506c1d7de7fa3d85098a50abb38aced88220b8eae58275879fb",
        url="https://pypi.org/packages/c2/d8/6c5aa064b8664a15c6aaca69549d52f4d91c20f97283cc8430297621fc4a/uvw-0.3.1-py3-none-any.whl",
    )
    version(
        "0.0.7",
        sha256="0a38ad38dce1ddb7013599316012bfbaa895c99cb055ac76735696770c8c95b8",
        url="https://pypi.org/packages/13/c0/d19ec69d75af026299478a858ab41fc7a084f4b79f165db18e53ad1b39c0/uvw-0.0.7-py3-none-any.whl",
    )

    variant("mpi", description="Use parallel writers", default=False)

    with default_args(type="run"):
        depends_on("py-mpi4py", when="@0.1:+mpi")
        depends_on("py-numpy")

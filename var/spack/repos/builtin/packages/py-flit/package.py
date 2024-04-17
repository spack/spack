# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlit(PythonPackage):
    """Flit is a simple way to put Python packages and modules on PyPI."""

    homepage = "https://github.com/pypa/flit"
    pypi = "flit/flit-3.9.0.tar.gz"
    maintainers("takluyver")

    license("BSD-3-Clause")

    version(
        "3.9.0",
        sha256="076c3aaba5ac24cf0ad3251f910900d95a08218e6bcb26f21fef1036cc4679ca",
        url="https://pypi.org/packages/68/0e/b1d1a1201215bf54adea518e79d0f0e84e376bec896c3a6ed437e5201471/flit-3.9.0-py3-none-any.whl",
    )
    version(
        "3.8.0",
        sha256="5ee0f88fd1cfa4160d1a8fa01237e96d06d677ae0403a0bbabbb277cb37c5e9c",
        url="https://pypi.org/packages/2c/05/73a5dc4ac52bba54a79ba1389aea11aa8220e877f777023dbd73ef470c54/flit-3.8.0-py3-none-any.whl",
    )
    version(
        "3.7.1",
        sha256="06a93a6737fa9380ba85fe8d7f28efb6c93c4f4ee9c7d00cc3375a81f33b91a4",
        url="https://pypi.org/packages/f8/81/5281e3f50a238d1169cc5c4c3acec91c631da79962d387ea843083bd151e/flit-3.7.1-py3-none-any.whl",
    )
    version(
        "3.6.0",
        sha256="03b9812856c7e4368dfa419a87f406e49414e871de02c43c4f754d35dfd70f87",
        url="https://pypi.org/packages/4a/2c/76c650ccf913781aa9e654c39296d2eb2caeca9ffa7b3108ebd475441158/flit-3.6.0-py3-none-any.whl",
    )
    version(
        "3.3.0",
        sha256="a286b9699e6a9f8537bbc21639cc3aaecf5e4e1daf0e0d236ea32b82c5b49404",
        url="https://pypi.org/packages/d0/d7/6e2d6c1f79b27a0fb47b3e51124c06341ed30e3a688655254248b6fa2809/flit-3.3.0-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-docutils")
        depends_on("py-flit-core@3.9:", when="@3.9:")
        depends_on("py-flit-core@3.8:", when="@3.8")
        depends_on("py-flit-core@3.7.1:", when="@3.7.1:3.7")
        depends_on("py-flit-core@3.6:", when="@3.6")
        depends_on("py-flit-core@3.3:", when="@3.3")
        depends_on("py-requests")
        depends_on("py-toml", when="@3.1:3.3")
        depends_on("py-tomli", when="@3.4:3.7")
        depends_on("py-tomli-w", when="@3.4:")

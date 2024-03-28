# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyQutipQip(PythonPackage):
    """The QuTiP quantum information processing package"""

    homepage = "https://github.com/qutip/qutip-qip"
    url = "https://github.com/qutip/qutip-qip/archive/refs/tags/v0.2.2.tar.gz"
    # using github for now, because pypi tarball is missing the VERSION file
    # pypi = "qutip-qip/qutip-qip-0.2.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.2.3",
        sha256="625a08c00cc8a045bca9c25088f683c74196603990a82a8c29c7bfaa9cabcb24",
        url="https://pypi.org/packages/8d/9b/5fa095406ffabfb1e16a37b0e94b753922d4e2f720b325d676e2fd615c0c/qutip_qip-0.2.3-py3-none-any.whl",
    )
    version(
        "0.2.2",
        sha256="e9af0088bfe661d286f0902fee4942d9ca581a6a7496c1a47d96a05e03f131b4",
        url="https://pypi.org/packages/c4/f5/7faeeeb2e2d12482962460616213968106cbcb0abbd00d730399ed79090b/qutip_qip-0.2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.16.6:", when="@:0.2.0,0.2.2:")
        depends_on("py-packaging", when="@0.2.2:")
        depends_on("py-qutip@4.6:", when="@0.2.2:")
        depends_on("py-scipy@1.0.0:")

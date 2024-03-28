# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBreathe(PythonPackage):
    """This is an extension to reStructuredText and Sphinx to be able to read
    and render the Doxygen xml output."""

    homepage = "https://github.com/michaeljones/breathe"
    url = "https://github.com/michaeljones/breathe/archive/v4.11.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "4.35.0",
        sha256="52c581f42ca4310737f9e435e3851c3d1f15446205a85fbc272f1f97ed74f5be",
        url="https://pypi.org/packages/eb/61/faddc25913de74e60e175bcfd962ec83532653c5895c0a06a83a6b5bbf3d/breathe-4.35.0-py3-none-any.whl",
    )
    version(
        "4.34.0",
        sha256="48804dcf0e607a89fb6ad88c729ef12743a42db03ae9489be4ef8f7c4011774a",
        url="https://pypi.org/packages/e8/6b/1385608a27653b6f02047d23f365f5dde7a54a266a0b3358b578c9a747b9/breathe-4.34.0-py3-none-any.whl",
    )
    version(
        "4.33.1",
        sha256="553aeffb00efc2cf96c4c9ed388d6ee8036ecd6d1bd9bd0c656fc25ca271bd3c",
        url="https://pypi.org/packages/04/e2/9d835c6f7fa0a575a005fa920506f07085fbf71651d1d1b1e8dd4f75b7af/breathe-4.33.1-py3-none-any.whl",
    )
    version(
        "4.21.0",
        sha256="d21ccaf5e655fe489c7e34fd8ae4e791fd66b2b556fd91b786146240b5696f34",
        url="https://pypi.org/packages/78/14/ced4c33680df1301ee56f1dbdb43fe4d2810a56b299fd232e4db875763d1/breathe-4.21.0-py3-none-any.whl",
    )
    version(
        "4.11.1",
        sha256="da13ebcb17951e606a869a745a36f9c6837a9a7c12ceec81c15a115495127451",
        url="https://pypi.org/packages/c3/60/b45d6797ddb2d013187dedb074dac9bc9bc4ffe1abc6d9bce8eabfcd5ba3/breathe-4.11.1-py2.py3-none-any.whl",
    )
    version(
        "4.11.0",
        sha256="fe8437d8de2d7a382d397ad106d5cf6045e3ea8699adab50b0e17db4bfe3167e",
        url="https://pypi.org/packages/e3/f2/b9e00a7dfc091be1906b99cd1b38ee7d4e5625a91e97ebdd19ede6ef0aee/breathe-4.11.0-py2.py3-none-any.whl",
    )
    version(
        "4.10.0",
        sha256="17b0aa0569ede04e04d45d27bd4e2353bfaddbee9a28cb01781c8493ef9971d0",
        url="https://pypi.org/packages/a4/14/8b6689dc331becb41a782f90e7d9d6eba407652bc3a4b18f5a1b5afaee9b/breathe-4.10.0-py2.py3-none-any.whl",
    )
    version(
        "4.9.1",
        sha256="df5d2edd1cee0045082e550d68bca5ee6bd3a8da009d51212bd0b2fa201ab808",
        url="https://pypi.org/packages/2c/a5/040234179dc9140be4a1cb4350af362327d001d0ca7e5bba4d580916ceb4/breathe-4.9.1-py2.py3-none-any.whl",
    )
    version(
        "4.9.0",
        sha256="8f8e51646711a66779e9bef74930fc7222399cbe7b1d2e75cdd4bedf431f0add",
        url="https://pypi.org/packages/4a/5d/324d2d3b4ea1ec4dbb123319883c1bd450be928383a8a56f3263a6d61dac/breathe-4.9.0-py2.py3-none-any.whl",
    )
    version(
        "4.8.0",
        sha256="7bbea23c8533b7ceced496d4ac6524d5a3dd9c3b78038ab49482a0ddfdd84d3d",
        url="https://pypi.org/packages/c0/dd/24cd6d978a179a8df2a6408bfc57c24b144a4ec4b22bddff7072403c6209/breathe-4.8.0-py2.py3-none-any.whl",
    )
    version(
        "4.7.3",
        sha256="9aa7927c0dcecdbc1663f5d5ce0c83e2e538021267b56db880d3b47ff8f744dc",
        url="https://pypi.org/packages/1c/7a/7a0f6c8367c96542d01fc1de8cedce8d93c8e3d9ded4e5b03eaefdcbcc82/breathe-4.7.3-py2.py3-none-any.whl",
    )
    version(
        "4.7.2",
        sha256="6d7eaeed9c54f3b92fe80acbbc224da21a3201cca6528f624d10dd639c34a7db",
        url="https://pypi.org/packages/82/c5/0220a19b26f2e4bdf7b3b762c05d3591f02092d0bcf4cfc2a4a6cd0f70dc/breathe-4.7.2-py2.py3-none-any.whl",
    )
    version(
        "4.7.1",
        sha256="01603def2e9f19a18a25744480aaf88e9cf0a00e778c15984813d2b20621a1d7",
        url="https://pypi.org/packages/52/e5/f28e9ab2d59b3731b82230797e694c77b4424080656bada4e5b3ed98fd88/breathe-4.7.1-py2.py3-none-any.whl",
    )
    version(
        "4.7.0",
        sha256="d90c309ca44811f0cc3fe45b99ef7de1418ab7ba7d9897b14671c7352d761f65",
        url="https://pypi.org/packages/da/a7/19fab4d5d2224b3bf8ac7b76d09c43a51e9448ed97a1892bb747d8f11bba/breathe-4.7.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils@0.12:", when="@4.28:")
        depends_on("py-docutils@0.5:", when="@4.7")
        depends_on("py-six@1.4:", when="@4.7")
        depends_on("py-sphinx@4.0.0:5.0.0-beta1,5.0.1:", when="@4.35:")
        depends_on("py-sphinx@4.0.0:5.0.0-beta1,5.0.1:5", when="@4.34")
        depends_on("py-sphinx@3.0.0:4", when="@4.29.1:4.33")
        depends_on("py-sphinx@1.4:", when="@4.7")

    # Note: Pygments is missing from the setup.py in 4.34.0 but is listed in
    # the requirements file and used by breathe.filetypes.

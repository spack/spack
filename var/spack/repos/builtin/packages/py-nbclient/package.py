# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbclient(PythonPackage):
    """A client library for executing notebooks.

    Formally nbconvert's ExecutePreprocessor."""

    homepage = "https://jupyter.org/"
    pypi = "nbclient/nbclient-0.5.0.tar.gz"
    git = "https://github.com/jupyter/nbclient.git"

    license("BSD-3-Clause")

    version(
        "0.8.0",
        sha256="25e861299e5303a0477568557c4045eccc7a34c17fc08e7959558707b9ebe548",
        url="https://pypi.org/packages/ac/5a/d670ca51e6c3d98574b9647599821590efcd811d71f58e9c89fc59a17685/nbclient-0.8.0-py3-none-any.whl",
    )
    version(
        "0.7.2",
        sha256="d97ac6257de2794f5397609df754fcbca1a603e94e924eb9b99787c031ae2e7c",
        url="https://pypi.org/packages/15/49/ea7a0c7e649c54883d76f5119a3e0be592d82a7df1a9b87124fa6663d9c7/nbclient-0.7.2-py3-none-any.whl",
    )
    version(
        "0.6.7",
        sha256="d4e32459e7e96783285d1daac92dc2c60ee7b8a82b7cf7d2e55be9d89d7ac463",
        url="https://pypi.org/packages/ba/bf/e89f683a24dd76ea2eac195035014529f3db6295f5e2a04ede01f27d0d1b/nbclient-0.6.7-py3-none-any.whl",
    )
    version(
        "0.6.6",
        sha256="09bae4ea2df79fa6bc50aeb8278d8b79d2036792824337fa6eee834afae17312",
        url="https://pypi.org/packages/68/88/a3f13adcf5708cf0d5f9c4c95e12d1527f6498d87b30d463b588bb466c15/nbclient-0.6.6-py3-none-any.whl",
    )
    version(
        "0.5.13",
        sha256="47ac905af59379913c1f8f541098d2550153cf8dc58553cbe18c702b181518b0",
        url="https://pypi.org/packages/db/f7/436bb1add1814911efec4a4a5a358c7559e9b1fd19f4ef89a2a71d707c2b/nbclient-0.5.13-py3-none-any.whl",
    )
    version(
        "0.5.5",
        sha256="542b1dfd492bc2524fff52064461149208ac3d53fa6353ce21da2219910b0cfc",
        url="https://pypi.org/packages/61/f0/693c0d157d2d2af3be700f31225206ac7573790cd0ac8d64cc4e68c66e31/nbclient-0.5.5-py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="8a6e27ff581cee50895f44c41936ce02369674e85e2ad58643d8d4a6c36771b0",
        url="https://pypi.org/packages/c3/c0/b8802a7cd2bb7a81a64a580eb65047d2931fd9fea8c038ff3ada2a6bd0ae/nbclient-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@0.8:")
        depends_on("python@3.7:", when="@0.5.10:0.7")
        depends_on("py-async-generator", when="@0.5.4:0.5.9 ^python@:3.6")
        depends_on("py-async-generator", when="@0.2:0.5.3")
        depends_on("py-jupyter-client@6.1.12:", when="@0.7.2:")
        depends_on("py-jupyter-client@6.1.5:", when="@0.4.1:0.7.0")
        depends_on("py-jupyter-core@4.12:4,5.1:", when="@0.7.2:")
        depends_on("py-nbformat@5.1:", when="@0.7.2:")
        depends_on("py-nbformat@5:", when="@:0.7.0")
        depends_on("py-nest-asyncio", when="@0.2:0.7.0")
        depends_on("py-traitlets@5.4:", when="@0.8:")
        depends_on("py-traitlets@5.3:5.3.0.0,5.4:", when="@0.7.2:0.7")
        depends_on("py-traitlets@5.2.2:", when="@0.6.4:0.7.0")
        depends_on("py-traitlets@5.0.0:", when="@0.5.12:0.6.3")
        depends_on("py-traitlets@4.2:", when="@:0.5.11")

    # Historical dependencies

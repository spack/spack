# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsttokens(PythonPackage):
    """Annotate AST trees with source code positions."""

    homepage = "https://github.com/gristlabs/asttokens"
    pypi = "asttokens/asttokens-2.0.5.tar.gz"

    license("Apache-2.0")

    version(
        "2.4.0",
        sha256="cf8fc9e61a86461aa9fb161a14a0841a03c405fa829ac6b202670b3495d2ce69",
        url="https://pypi.org/packages/4f/25/adda9979586d9606300415c89ad0e4c5b53d72b92d2747a3c634701a6a02/asttokens-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.2.1",
        sha256="6b0ac9e93fb0335014d382b8fa9b3afa7df546984258005da0b9e7095b3deb1c",
        url="https://pypi.org/packages/f3/e1/64679d9d0759db5b182222c81ff322c2fe2c31e156a59afd6e9208c960e5/asttokens-2.2.1-py2.py3-none-any.whl",
    )
    version(
        "2.0.8",
        sha256="e3305297c744ae53ffa032c45dc347286165e4ffce6875dc662b205db0623d86",
        url="https://pypi.org/packages/2d/1b/fdbdf82b86e07ca90985740ac160a1dd4ab09cb81071ec12d71c701e1138/asttokens-2.0.8-py2.py3-none-any.whl",
    )
    version(
        "2.0.5",
        sha256="0844691e88552595a6f4a4281a9f7f79b8dd45ca4ccea82e5e05b4bbdb76705c",
        url="https://pypi.org/packages/16/d5/b0ad240c22bba2f4591693b0ca43aae94fbd77fb1e2b107d54fff1462b6f/asttokens-2.0.5-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six@1.12:", when="@2.3:")
        depends_on("py-six", when="@:2.2")

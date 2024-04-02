# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgcomplete(PythonPackage):
    """Bash tab completion for argparse."""

    homepage = "https://github.com/kislyuk/argcomplete"
    pypi = "argcomplete/argcomplete-1.12.0.tar.gz"

    version(
        "3.1.2",
        sha256="d97c036d12a752d1079f190bc1521c545b941fda89ad85d15afa909b4d1b9a99",
        url="https://pypi.org/packages/1e/05/223116a4a5905d6b26bff334ffc7b74474fafe23fcb10532caf0ef86ca69/argcomplete-3.1.2-py3-none-any.whl",
    )
    version(
        "3.0.8",
        sha256="e36fd646839933cbec7941c662ecb65338248667358dd3d968405a4506a60d9b",
        url="https://pypi.org/packages/ab/ce/2141e1cabe39c90e01fde7feb44c07867fb49bf1c0c091d68fd8924fd6a2/argcomplete-3.0.8-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="cffa11ea77999bb0dd27bb25ff6dc142a6796142f68d45b1a26b11f58724561e",
        url="https://pypi.org/packages/d3/e5/c5509683462e51b070df9e83e7f72c1ccfe3f733f328b4a0f06804c27278/argcomplete-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.12.3",
        sha256="291f0beca7fd49ce285d2f10e4c1c77e9460cf823eef2de54df0c0fec88b0d81",
        url="https://pypi.org/packages/b7/9e/9dc74d330c07866d72f62d553fe8bdbe32786ff247a14e68b5659963e6bd/argcomplete-1.12.3-py2.py3-none-any.whl",
    )
    version(
        "1.12.0",
        sha256="91dc7f9c7f6281d5a0dce5e73d2e33283aaef083495c13974a7dd197a1cdc949",
        url="https://pypi.org/packages/89/4d/b8e035cca2c9b2484ac12d20e0fb68019e17f0b09918f2765e0a381127fb/argcomplete-1.12.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.1",
        sha256="f9bb1e017aa61e52b28023936475963d97d62046a1f87e0f0dfc5a5b439949ff",
        url="https://pypi.org/packages/b2/64/f622fc5e6a202f802343cf6363fe0ff6a1e7f99cd7e0184a71f038cdbb4e/argcomplete-1.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-importlib-metadata@0.23:6", when="@3.1:3.1.2 ^python@:3.7")

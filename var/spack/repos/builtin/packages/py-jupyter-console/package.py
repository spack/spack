# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterConsole(PythonPackage):
    """Jupyter Terminal Console"""

    homepage = "https://github.com/jupyter/jupyter_console"
    pypi = "jupyter_console/jupyter_console-6.4.0.tar.gz"

    version(
        "6.4.4",
        sha256="756df7f4f60c986e7bc0172e4493d3830a7e6e75c08750bbe59c0a5403ad6dee",
        url="https://pypi.org/packages/8b/0c/f9382ca7b7499c8594a5158817a72c95b4c09a6c6f2de10553bfe8905924/jupyter_console-6.4.4-py3-none-any.whl",
    )
    version(
        "6.4.3",
        sha256="e630bcb682c0088dda45688ad7c2424d4a825c8acf494cb036ced03ed0424841",
        url="https://pypi.org/packages/fc/e9/5d4e1e616f7d7a8a9d7f313ac14bf43d1ea33cae6859eeb761b8cac364c2/jupyter_console-6.4.3-py3-none-any.whl",
    )
    version(
        "6.4.0",
        sha256="7799c4ea951e0e96ba8260575423cb323ea5a03fcf5503560fa3e15748869e27",
        url="https://pypi.org/packages/59/cd/aa2670ffc99eb3e5bbe2294c71e4bf46a9804af4f378d09d7a8950996c9b/jupyter_console-6.4.0-py3-none-any.whl",
    )
    version(
        "6.1.0",
        sha256="b392155112ec86a329df03b225749a0fa903aa80811e8eda55796a40b5e470d8",
        url="https://pypi.org/packages/0a/89/742fa5a80b552ffcb6a8922712697c6e6828aee7b91ee4ae2b79f00f8401/jupyter_console-6.1.0-py2.py3-none-any.whl",
    )
    version(
        "5.2.0",
        sha256="3f928b817fc82cda95e431eb4c2b5eb21be5c483c2b43f424761a966bb808094",
        url="https://pypi.org/packages/77/82/6469cd7fccf7958cbe5dce2e623f1e3c5e27f1bb1ad36d90519bc2d5d370/jupyter_console-5.2.0-py2.py3-none-any.whl",
    )
    version(
        "5.0.0",
        sha256="650a3f2c47aefe9103c17e08664af48587698882ddb0f91dae14cd7fe52d5c15",
        url="https://pypi.org/packages/f4/21/b4208374b500ba31f98fc0909def785eaa40a3623b64c8d311d856986230/jupyter_console-5.0.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="2b9775afc4f02515134e2ea858f5e9e10e0eaa6367d780476dd94c2109b409aa",
        url="https://pypi.org/packages/1b/dd/525c3400823f2661f4aa129dd3c9010223bf250677af4b115d9d775b7f8a/jupyter_console-4.1.1-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="10a1113a68e719934733571e05283b16f42a0571f718495e1dc9139ec4b42af8",
        url="https://pypi.org/packages/e1/47/4151ebbe41c3229e2f6a67dc9d7ec015723e624a5d1f0c4e49ee807a3668/jupyter_console-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.3",
        sha256="ee6ce278897abf45d5abc6e83e685847d198eecfdbc59bfda45b5798200db2c2",
        url="https://pypi.org/packages/7c/c2/5e865900de40f7bf80b5cfbf9a79532f540a6679c7ded8f793f99cf546fa/jupyter_console-4.0.3-py2.py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="b04dde36fb82bbe0176c2a8130e03eb0b3a233d6906357bb52df7d8fa1a45ff0",
        url="https://pypi.org/packages/01/18/bd0165448c3eb0cd4c35a154918dcc7795cf137f2acc8637a724c3ea96e2/jupyter_console-4.0.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@6.4.4:")
        depends_on("py-ipykernel", when="@4.1:6.4")
        depends_on("py-ipython", when="@4.1:")
        depends_on("py-jupyter-client@7.0.0:", when="@6.4.3:")
        depends_on("py-jupyter-client", when="@4.1:6.4.2")
        depends_on("py-prompt-toolkit@2,3.0.2:", when="@6.1:6.4")
        depends_on("py-prompt-toolkit@1", when="@5")
        depends_on("py-pygments", when="@5:")
        depends_on("py-pyreadline", when="@4.1:4 platform=windows")

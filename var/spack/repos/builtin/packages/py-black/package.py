# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBlack(PythonPackage):
    """Black is the uncompromising Python code formatter. By using it, you agree to
    cede control over minutiae of hand-formatting. In return, Black gives you
    speed, determinism, and freedom from pycodestyle nagging about formatting.
    """

    homepage = "https://github.com/psf/black"
    pypi = "black/black-22.1.0.tar.gz"

    maintainers("adamjstewart")

    version("23.1.0", sha256="b0bd97bea8903f5a2ba7219257a44e3f1f9d00073d6cc1add68f0beec69692ac")
    version("22.12.0", sha256="229351e5a18ca30f447bf724d007f890f97e13af070bb6ad4c0a441cd7596a2f")
    version("22.10.0", sha256="f513588da599943e0cde4e32cc9879e825d58720d6557062d1098c5ad80080e1")
    version("22.8.0", sha256="792f7eb540ba9a17e8656538701d3eb1afcb134e3b45b71f20b25c77a8db7e6e")
    version("22.6.0", sha256="6c6d39e28aed379aec40da1c65434c77d75e65bb59a1e1c283de545fb4e7c6c9")
    version("22.3.0", sha256="35020b8886c022ced9282b51b5a875b6d1ab0c387b31a065b84db7c33085ca79")
    version("22.1.0", sha256="a7c0192d35635f6fc1174be575cb7915e92e5dd629ee79fdaf0dcfa41a80afb5")

    # This is the last v21 release, and it's needed to format for Python 2.7
    version(
        "21.12b0",
        sha256="77b80f693a569e2e527958459634f18df9b0ba2625ba4e0c2d5da5be42e6f2b3",
        deprecated=True,
    )

    variant("colorama", default=False, description="enable colorama support")
    variant("uvloop", default=False, description="enable uvloop support")
    variant("d", default=False, description="enable blackd HTTP server")
    variant("jupyter", default=False, description="enable Jupyter support")

    depends_on("py-hatchling@1.8:", when="@22.10:", type="build")
    depends_on("py-hatch-vcs", when="@22.10:", type="build")
    depends_on("py-hatch-fancy-pypi-readme", when="@22.10:", type="build")
    depends_on("py-setuptools@45:", when="@:22.8", type=("build", "run"))
    depends_on("py-setuptools-scm@6.3.1:+toml", when="@:22.8", type="build")
    # Needed to ensure that Spack can bootstrap black with Python 3.6
    depends_on("python@3.7:", when="@22.10:", type=("build", "run"))
    depends_on("py-click@8:", type=("build", "run"))
    depends_on("py-mypy-extensions@0.4.3:", type=("build", "run"))
    depends_on("py-packaging@22:", when="@23.1:", type=("build", "run"))
    depends_on("py-pathspec@0.9:", type=("build", "run"))
    depends_on("py-platformdirs@2:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@22.8: ^python@:3.10", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@21.7:22.6", type=("build", "run"))
    depends_on("py-typed-ast@1.4.2:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-typing-extensions@3.10:", when="^python@:3.9", type=("build", "run"))
    depends_on("py-colorama@0.4.3:", when="+colorama", type=("build", "run"))
    depends_on("py-uvloop@0.15.2:", when="+uvloop", type=("build", "run"))
    depends_on("py-aiohttp@3.7.4:", when="+d", type=("build", "run"))
    depends_on("py-ipython@7.8:", when="+jupyter", type=("build", "run"))
    depends_on("py-tokenize-rt@3.2:", when="+jupyter", type=("build", "run"))

    # Needed because this package is used to bootstrap Spack (Spack supports Python 3.6+)
    depends_on("py-dataclasses@0.6:", when="^python@:3.6", type=("build", "run"))

    # see: https://github.com/psf/black/issues/2964
    # note that pip doesn't know this constraint.
    depends_on("py-click@:8.0", when="@:22.2", type=("build", "run"))

    @property
    def import_modules(self):
        modules = ["blib2to3", "blib2to3.pgen2", "black"]

        if "+d" in self.spec:
            modules.append("blackd")

        return modules

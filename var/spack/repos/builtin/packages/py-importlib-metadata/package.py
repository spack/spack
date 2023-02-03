# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibMetadata(Package, PythonExtension):
    """Read metadata from Python packages."""

    homepage = "https://github.com/python/importlib_metadata"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/i/importlib-metadata/importlib_metadata-6.0.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/importlib-metadata/"
    git = "https://github.com/python/importlib_metadata"

    version("6.0.0", sha256="7efb448ec9a5e313a57655d35aa54cd3e01b7e1fbcf72dce1bf06119420f5bad", expand=False)
    version("4.12.0", sha256="7401a975809ea1fdc658c3aa4f78cc2195a0e019c5cbc4c06122884e9ae80c23", expand=False)
    version("4.11.1", sha256="e0bc84ff355328a4adfc5240c4f211e0ab386f80aa640d1b11f0618a1d282094", expand=False)
    version("4.8.2", sha256="53ccfd5c134223e497627b9815d5030edf77d2ed573922f7a0b8f8bb81a1c100", expand=False)
    version("4.8.1", sha256="b618b6d2d5ffa2f16add5697cf57a46c76a56229b0ed1c438322e4e95645bd15", expand=False)
    version("4.6.1", sha256="9f55f560e116f8643ecf2922d9cd3e1c7e8d52e683178fecd9d08f6aa357e11e", expand=False)
    version("3.10.1", sha256="2ec0faae539743ae6aaa84b49a169670a465f7f5d64e6add98388cc29fd1f2f6", expand=False)
    version("3.10.0", sha256="d2d46ef77ffc85cbf7dac7e81dd663fde71c45326131bea8033b9bad42268ebe", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-zipp@0.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.4:", when="^python@:3.7", type=("build", "run"))

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)

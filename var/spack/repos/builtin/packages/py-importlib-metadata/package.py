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

    version(
        "6.0.0",
        sha256="7efb448ec9a5e313a57655d35aa54cd3e01b7e1fbcf72dce1bf06119420f5bad",
        expand=False,
    )
    version(
        "4.12.0",
        sha256="7401a975809ea1fdc658c3aa4f78cc2195a0e019c5cbc4c06122884e9ae80c23",
        expand=False,
    )
    version(
        "4.11.1",
        sha256="e0bc84ff355328a4adfc5240c4f211e0ab386f80aa640d1b11f0618a1d282094",
        expand=False,
    )
    version(
        "4.8.2",
        sha256="53ccfd5c134223e497627b9815d5030edf77d2ed573922f7a0b8f8bb81a1c100",
        expand=False,
    )
    version(
        "4.8.1",
        sha256="b618b6d2d5ffa2f16add5697cf57a46c76a56229b0ed1c438322e4e95645bd15",
        expand=False,
    )
    version(
        "4.6.1",
        sha256="9f55f560e116f8643ecf2922d9cd3e1c7e8d52e683178fecd9d08f6aa357e11e",
        expand=False,
    )
    version(
        "3.10.1",
        sha256="2ec0faae539743ae6aaa84b49a169670a465f7f5d64e6add98388cc29fd1f2f6",
        expand=False,
    )
    version(
        "3.10.0",
        sha256="d2d46ef77ffc85cbf7dac7e81dd663fde71c45326131bea8033b9bad42268ebe",
        expand=False,
    )
    version(
        "2.0.0",
        sha256="cefa1a2f919b866c5beb7c9f7b0ebb4061f30a8a9bf16d609b000e2dfaceb9c3",
        expand=False,
    )
    version(
        "1.7.0",
        sha256="dc15b2969b4ce36305c51eebe62d418ac7791e9a157911d58bfb1f9ccd8e2070",
        expand=False,
    )
    version(
        "1.2.0",
        sha256="3a8b2dfd0a2c6a3636e7c016a7e54ae04b997d30e69d5eacdca7a6c2221a1402",
        expand=False,
    )
    version(
        "0.23",
        sha256="d5f18a79777f3aa179c145737780282e27b508fc8fd688cb17c7a813e8bd39af",
        expand=False,
    )
    version(
        "0.19",
        sha256="80d2de76188eabfbfcf27e6a37342c2827801e59c4cc14b0371c56fed43820e3",
        expand=False,
    )
    version(
        "0.18",
        sha256="6dfd58dfe281e8d240937776065dd3624ad5469c835248219bd16cf2e12dbeb7",
        expand=False,
    )

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-zipp@0.5:", type=("build", "run"))
    depends_on("py-typing-extensions@3.6.4:", when="@3: ^python@:3.7", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/i/importlib-metadata/importlib_metadata-{1}-{0}-none-any.whl"
        if version >= Version("3"):
            language = "py3"
        else:
            language = "py2.py3"
        return url.format(language, version)

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)

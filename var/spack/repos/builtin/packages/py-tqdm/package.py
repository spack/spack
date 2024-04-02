# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTqdm(PythonPackage):
    """A Fast, Extensible Progress Meter"""

    homepage = "https://github.com/tqdm/tqdm"
    pypi = "tqdm/tqdm-4.45.0.tar.gz"

    version(
        "4.66.1",
        sha256="d302b3c5b53d47bce91fea46679d9c3c6508cf6332229aa1e7d8653723793386",
        url="https://pypi.org/packages/00/e5/f12a80907d0884e6dff9c16d0c0114d81b8cd07dc3ae54c5e962cc83037e/tqdm-4.66.1-py3-none-any.whl",
    )
    version(
        "4.65.0",
        sha256="c4f53a17fe37e132815abceec022631be8ffe1b9381c2e6e30aa70edc99e9671",
        url="https://pypi.org/packages/e6/02/a2cff6306177ae6bc73bc0665065de51dfb3b9db7373e122e2735faf0d97/tqdm-4.65.0-py3-none-any.whl",
    )
    version(
        "4.64.1",
        sha256="6fee160d6ffcd1b1c68c65f14c829c22832bc401726335ce92c52d395944a6a1",
        url="https://pypi.org/packages/47/bb/849011636c4da2e44f1253cd927cfb20ada4374d8b3a4e425416e84900cc/tqdm-4.64.1-py2.py3-none-any.whl",
    )
    version(
        "4.64.0",
        sha256="74a2cdefe14d11442cedf3ba4e21a3b84ff9a2dbdc6cfae2c34addb2a14a5ea6",
        url="https://pypi.org/packages/8a/c4/d15f1e627fff25443ded77ea70a7b5532d6371498f9285d44d62587e209c/tqdm-4.64.0-py2.py3-none-any.whl",
    )
    version(
        "4.62.3",
        sha256="8dd278a422499cd6b727e6ae4061c40b48fce8b76d1ccbf5d34fca9b7f925b0c",
        url="https://pypi.org/packages/63/f3/b7a1b8e40fd1bd049a34566eb353527bb9b8e9b98f8b6cf803bb64d8ce95/tqdm-4.62.3-py2.py3-none-any.whl",
    )
    version(
        "4.59.0",
        sha256="9fdf349068d047d4cfbe24862c425883af1db29bcddf4b0eeb2524f6fbdb23c7",
        url="https://pypi.org/packages/f8/3e/2730d0effc282960dbff3cf91599ad0d8f3faedc8e75720fdf224b31ab24/tqdm-4.59.0-py2.py3-none-any.whl",
    )
    version(
        "4.58.0",
        sha256="2c44efa73b8914dba7807aefd09653ac63c22b5b4ea34f7a80973f418f1a3089",
        url="https://pypi.org/packages/4e/8c/f1035bd24b0e352ddba7be320abc1603fc4c9976fcda6971ed287be59164/tqdm-4.58.0-py2.py3-none-any.whl",
    )
    version(
        "4.56.2",
        sha256="a89be573bfddb81bb0b395a416d5e55e3ecc73ce95a368a4f6360bedea33195e",
        url="https://pypi.org/packages/b3/db/dcda019790a8d989b8b0e7290f1c651a0aaef10bbe6af00032155e04858d/tqdm-4.56.2-py2.py3-none-any.whl",
    )
    version(
        "4.46.0",
        sha256="acdafb20f51637ca3954150d0405ff1a7edde0ff19e38fb99a80a66210d2a28f",
        url="https://pypi.org/packages/c9/40/058b12e8ba10e35f89c9b1fdfc2d4c7f8c05947df2d5eb3c7b258019fda0/tqdm-4.46.0-py2.py3-none-any.whl",
    )
    version(
        "4.45.0",
        sha256="ea9e3fd6bd9a37e8783d75bfc4c1faf3c6813da6bd1c3e776488b41ec683af94",
        url="https://pypi.org/packages/4a/1c/6359be64e8301b84160f6f6f7936bbfaaa5e9a4eab6cbc681db07600b949/tqdm-4.45.0-py2.py3-none-any.whl",
    )
    version(
        "4.36.1",
        sha256="dd3fcca8488bb1d416aa7469d2f277902f26260c45aa86b667b074cd44b3b115",
        url="https://pypi.org/packages/e1/c1/bc1dba38b48f4ae3c4428aea669c5e27bd5a7642a74c8348451e0bd8ff86/tqdm-4.36.1-py2.py3-none-any.whl",
    )
    version(
        "4.8.4",
        sha256="a28f0ee0b8ec63659604c5432291e77147fb0c66e78242ed343aaccf89362f6d",
        url="https://pypi.org/packages/3a/c0/2653e9a90aef358da8880980c155218791f79b9a1d479a9a00f88ac42aac/tqdm-4.8.4-py2.py3-none-any.whl",
    )

    variant("notebook", default=False, description="Enable Jupyter Notebook support")
    variant("telegram", default=False, description="Enable Telegram bot support")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@4.65:")
        depends_on("py-colorama", when="@4.61.2: platform=windows")
        depends_on("py-importlib-resources", when="@4.63:4.64 ^python@:3.6")
        depends_on("py-ipywidgets@6.0.0:", when="@4.59:+notebook")
        depends_on("py-requests", when="@4.55:+telegram")

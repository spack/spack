# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "https://importlib-metadata.readthedocs.io/"
    pypi = "importlib_metadata/importlib_metadata-1.2.0.tar.gz"
    git = "https://github.com/python/importlib_metadata"

    license("Apache-2.0")

    version(
        "7.0.1",
        sha256="4805911c3a4ec7c3966410053e9ec6a1fecd629117df5adee56dfc9432a1081e",
        url="https://pypi.org/packages/c0/8b/d8427f023c081a8303e6ac7209c16e6878f2765d5b59667f3903fbcfd365/importlib_metadata-7.0.1-py3-none-any.whl",
    )
    version(
        "6.6.0",
        sha256="43dd286a2cd8995d5eaef7fee2066340423b818ed3fd70adf0bad5f1fac53fed",
        url="https://pypi.org/packages/30/bb/bf2944b8b88c65b797acc2c6a2cb0fb817f7364debf0675792e034013858/importlib_metadata-6.6.0-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="d84d17e21670ec07990e1044a99efe8d615d860fd176fc29ef5c306068fda313",
        url="https://pypi.org/packages/e1/16/1f59f5d87d256012e9cdf0e8af8810965fa253e835cfecce64f4b11d4f2d/importlib_metadata-5.1.0-py3-none-any.whl",
    )
    version(
        "4.12.0",
        sha256="7401a975809ea1fdc658c3aa4f78cc2195a0e019c5cbc4c06122884e9ae80c23",
        url="https://pypi.org/packages/d2/a2/8c239dc898138f208dd14b441b196e7b3032b94d3137d9d8453e186967fc/importlib_metadata-4.12.0-py3-none-any.whl",
    )
    version(
        "4.11.4",
        sha256="c58c8eb8a762858f49e18436ff552e83914778e50e9d2f1660535ffb364552ec",
        url="https://pypi.org/packages/ab/b5/1bd220dd470b0b912fc31499e0d9c652007a60caf137995867ccc4b98cb6/importlib_metadata-4.11.4-py3-none-any.whl",
    )
    version(
        "4.11.1",
        sha256="e0bc84ff355328a4adfc5240c4f211e0ab386f80aa640d1b11f0618a1d282094",
        url="https://pypi.org/packages/f9/5f/8f5e198c94a04163fc2e1c425d3963197d59b631614db52bc02b11ee4cff/importlib_metadata-4.11.1-py3-none-any.whl",
    )
    version(
        "4.8.3",
        sha256="65a9576a5b2d58ca44d133c42a241905cc45e34d2c06fd5ba2bafa221e5d7b5e",
        url="https://pypi.org/packages/a0/a1/b153a0a4caf7a7e3f15c2cd56c7702e2cf3d89b1b359d1f1c5e59d68f4ce/importlib_metadata-4.8.3-py3-none-any.whl",
    )
    version(
        "4.8.2",
        sha256="53ccfd5c134223e497627b9815d5030edf77d2ed573922f7a0b8f8bb81a1c100",
        url="https://pypi.org/packages/c4/1f/e2238896149df09953efcc53bdcc7d23597d6c53e428c30e572eda5ec6eb/importlib_metadata-4.8.2-py3-none-any.whl",
    )
    version(
        "4.8.1",
        sha256="b618b6d2d5ffa2f16add5697cf57a46c76a56229b0ed1c438322e4e95645bd15",
        url="https://pypi.org/packages/71/c2/cb1855f0b2a0ae9ccc9b69f150a7aebd4a8d815bd951e74621c4154c52a8/importlib_metadata-4.8.1-py3-none-any.whl",
    )
    version(
        "4.6.4",
        sha256="ed5157fef23a4bc4594615a0dd8eba94b2bb36bf2a343fa3d8bb2fa0a62a99d5",
        url="https://pypi.org/packages/c0/72/4512a88e402d4dc3bab49a845130d95ac48936ef3a9469b55cc79a60d84d/importlib_metadata-4.6.4-py3-none-any.whl",
    )
    version(
        "4.6.1",
        sha256="9f55f560e116f8643ecf2922d9cd3e1c7e8d52e683178fecd9d08f6aa357e11e",
        url="https://pypi.org/packages/3f/e1/e5bba549a033adf77448699a34ecafc7a32adaeeb4369396b35f56d5cc3e/importlib_metadata-4.6.1-py3-none-any.whl",
    )
    version(
        "3.10.1",
        sha256="2ec0faae539743ae6aaa84b49a169670a465f7f5d64e6add98388cc29fd1f2f6",
        url="https://pypi.org/packages/52/d0/bdb31463f2d9ca111e39b268518e9baa3542ef73ca449b711a7b4da69764/importlib_metadata-3.10.1-py3-none-any.whl",
    )
    version(
        "3.10.0",
        sha256="d2d46ef77ffc85cbf7dac7e81dd663fde71c45326131bea8033b9bad42268ebe",
        url="https://pypi.org/packages/99/8f/b0ac918b2234848ec5bd2a887d2be7d6686355fcb22d7a0efe878d5c1555/importlib_metadata-3.10.0-py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="cefa1a2f919b866c5beb7c9f7b0ebb4061f30a8a9bf16d609b000e2dfaceb9c3",
        url="https://pypi.org/packages/6d/6d/f4bb28424bc677bce1210bc19f69a43efe823e294325606ead595211f93e/importlib_metadata-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.7.0",
        sha256="dc15b2969b4ce36305c51eebe62d418ac7791e9a157911d58bfb1f9ccd8e2070",
        url="https://pypi.org/packages/8e/58/cdea07eb51fc2b906db0968a94700866fc46249bdc75cac23f9d13168929/importlib_metadata-1.7.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="3a8b2dfd0a2c6a3636e7c016a7e54ae04b997d30e69d5eacdca7a6c2221a1402",
        url="https://pypi.org/packages/e7/59/cc2a91f71957dfb32f25e6b19d8c6dfdbe524e0998e7f7a58a75126ce0cd/importlib_metadata-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "0.23",
        sha256="d5f18a79777f3aa179c145737780282e27b508fc8fd688cb17c7a813e8bd39af",
        url="https://pypi.org/packages/f6/d2/40b3fa882147719744e6aa50ac39cf7a22a913cbcba86a0371176c425a3b/importlib_metadata-0.23-py2.py3-none-any.whl",
    )
    version(
        "0.19",
        sha256="80d2de76188eabfbfcf27e6a37342c2827801e59c4cc14b0371c56fed43820e3",
        url="https://pypi.org/packages/ad/aa/25fcbded2ab4ed4ff3071d1e000cd4f8f9c65653d2d7157dd105a8e81d42/importlib_metadata-0.19-py2.py3-none-any.whl",
    )
    version(
        "0.18",
        sha256="6dfd58dfe281e8d240937776065dd3624ad5469c835248219bd16cf2e12dbeb7",
        url="https://pypi.org/packages/bd/23/dce4879ec58acf3959580bfe769926ed8198727250c5e395e6785c764a02/importlib_metadata-0.18-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@6.8:")
        depends_on("python@3.7:", when="@4.9:6.7")
        depends_on("py-typing-extensions@3.6.5:", when="@3.2: ^python@:3.7")
        depends_on("py-zipp@0.5:", when="@0.11:")

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPbr(PythonPackage):
    """PBR is a library that injects some useful and sensible default
    behaviors into your setuptools run."""

    pypi = "pbr/pbr-5.4.3.tar.gz"

    # Skip 'pbr.tests' imports
    import_modules = ["pbr", "pbr.cmd", "pbr.hooks"]

    version(
        "5.10.0",
        sha256="da3e18aac0a3c003e9eea1a81bd23e5a3a75d745670dcf736317b7d966887fdf",
        url="https://pypi.org/packages/88/fb/c7958b2d571c7b15091b8574a727ad14328e8de590644198e57de9b5ee57/pbr-5.10.0-py2.py3-none-any.whl",
    )
    version(
        "5.7.0",
        sha256="60002958e459b195e8dbe61bf22bcf344eedf1b4e03a321a5414feb15566100c",
        url="https://pypi.org/packages/58/4e/98f141d6edcb41b4dd50bb2b70f072dcd4facb6f96685c2fca1f647d71f5/pbr-5.7.0-py2.py3-none-any.whl",
    )
    version(
        "5.4.3",
        sha256="b32c8ccaac7b1a20c0ce00ce317642e6cf231cf038f9875e0280e28af5bf7ac9",
        url="https://pypi.org/packages/46/a4/d5c83831a3452713e4b4f126149bc4fbda170f7cb16a86a00ce57ce0e9ad/pbr-5.4.3-py2.py3-none-any.whl",
    )
    version(
        "5.2.1",
        sha256="0ce920b865091450bbcd452b35cf6d6eb8a6d9ce13ad2210d6e77557f85cf32b",
        url="https://pypi.org/packages/49/a2/e641de6c7e559e0a03a8d3c7b42199158b17a8cf2f96e11e7f725c2e730d/pbr-5.2.1-py2.py3-none-any.whl",
    )
    version(
        "3.1.1",
        sha256="60c25b7dfd054ef9bb0ae327af949dd4676aa09ac3a9471cdc871d8a9213f9ac",
        url="https://pypi.org/packages/0c/5d/b077dbf309993d52c1d71e6bf6fe443a8029ea215135ebbe0b1b10e7aefc/pbr-3.1.1-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="d9b69a26a5cb4e3898eb3c5cea54d2ab3332382167f04e30db5e1f54e1945e45",
        url="https://pypi.org/packages/e9/c0/8f7f54d7b9b8ceb73ac30d769fdd722431e95ad0d2cd689def382e8b9eec/pbr-2.0.0-py2.py3-none-any.whl",
    )
    version(
        "1.10.0",
        sha256="f5cf7265a80636ecff66806d13494cbf9d77a3758a65fd8b4d4d4bee81b0c375",
        url="https://pypi.org/packages/b8/a1/7abb01fd93d66fc71e24e5df9ca6d7d9acfb4b715937d2a38fd739f266e6/pbr-1.10.0-py2.py3-none-any.whl",
    )
    version(
        "1.8.1",
        sha256="46c8db75ae75a056bd1cc07fa21734fe2e603d11a07833ecc1eeb74c35c72e0c",
        url="https://pypi.org/packages/fc/37/94af8387babb09796d306b18cf94ee5c70388c875a16d8a88e471500452c/pbr-1.8.1-py2.py3-none-any.whl",
    )

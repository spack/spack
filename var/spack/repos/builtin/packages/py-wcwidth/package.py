# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWcwidth(PythonPackage):
    """Measures number of Terminal column cells of wide-character codes"""

    homepage = "https://github.com/jquast/wcwidth"
    pypi = "wcwidth/wcwidth-0.1.7.tar.gz"

    license("MIT")

    version(
        "0.2.7",
        sha256="fabf3e32999d9b0dab7d19d845149f326f04fe29bac67709ee071dbd92640a36",
        url="https://pypi.org/packages/91/c3/3b3a1db90a21ddff1dbfb412d0ce00881d7820b01dfa47faf09d317ce51f/wcwidth-0.2.7-py2.py3-none-any.whl",
    )
    version(
        "0.2.5",
        sha256="beb4802a9cebb9144e99086eff703a642a13d6a0052920003a230f3294bbe784",
        url="https://pypi.org/packages/59/7c/e39aca596badaf1b78e8f547c807b04dae603a433d3e7a7e04d67f2ef3e5/wcwidth-0.2.5-py2.py3-none-any.whl",
    )
    version(
        "0.1.7",
        sha256="f4ebe71925af7b40a864553f761ed559b43544f8f71746c2d756c7fe788ade7c",
        url="https://pypi.org/packages/7e/9f/526a6947247599b084ee5232e4f9190a38f398d7300d866af3ab571a5bfe/wcwidth-0.1.7-py2.py3-none-any.whl",
    )

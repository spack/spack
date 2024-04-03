# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepunits(PythonPackage):
    """Units and constants in the HEP system of units."""

    git = "https://github.com/scikit-hep/hepunits.git"
    pypi = "hepunits/hepunits-1.2.1.tar.gz"
    homepage = "https://github.com/scikit-hep/hepunits"

    tags = ["hep"]

    maintainers("vvolkl")

    license("BSD-3-Clause")

    version(
        "2.3.2",
        sha256="96267ca79908b8d3c44bd09c3ad98887a7394118d9495657c2471b8e2264d759",
        url="https://pypi.org/packages/77/18/b4365c940075b74a4d76269e334dc8a6d966346162491197f661043005f5/hepunits-2.3.2-py3-none-any.whl",
    )
    version(
        "2.3.1",
        sha256="e070c3145fb50526a9a5d2fb557faafdd8bb9b8cb0045a27d2d6ac489269b24d",
        url="https://pypi.org/packages/91/48/76b99f9cf2ec8fadea882f70ec7866d227644b857791f49892a86083ac82/hepunits-2.3.1-py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="7a48643261e7bf74f91b7a9338be15e555711f1dde8f1d02c7607925a1716c69",
        url="https://pypi.org/packages/27/55/27f39857f74ca2ca2a95c98d9086b11058a36ad60e0faa9a8b530a54a0bb/hepunits-2.3.0-py3-none-any.whl",
    )
    version(
        "2.2.1",
        sha256="b165e50e9b8f5c6302e22f8d2a295c317f7215535e5852f0d295a0857dc143f0",
        url="https://pypi.org/packages/13/b6/436505aae22ad16e7c39d093a2932aeeb712e19503e471549eef742f79e3/hepunits-2.2.1-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="a5f2fb1d53674caaf1bac049437030e398114735c7c0a923d738ebc5b6ffdfb1",
        url="https://pypi.org/packages/86/21/babdb7374766fad577bf81df10de08fbbc6a55128642063ac697a32961a8/hepunits-2.2.0-py3-none-any.whl",
    )
    version(
        "2.1.3",
        sha256="7f7a8077178e7f57173ec42e9e7c086043a59d417df067c62596fa0b13a27b06",
        url="https://pypi.org/packages/7d/30/a6d1f2148cbaf860c9b35cb463954d9ea82c54a56c254a455c4a693ffe43/hepunits-2.1.3-py2.py3-none-any.whl",
    )
    version(
        "2.1.2",
        sha256="27f857fb88a5f5a2e8fa961b0c0d5f9387ff19fb8d4c6376e5f7571bc0259dd0",
        url="https://pypi.org/packages/9c/d4/e9c67b7fff6616062783fe3ac291c17ae94c4482d56fc93dd039dbb63529/hepunits-2.1.2-py2.py3-none-any.whl",
    )
    version(
        "2.1.1",
        sha256="b3d69929003595a179e8496137082f63661a40deb718910b8317e1e59f101198",
        url="https://pypi.org/packages/3f/40/080cf95a028a6010a8ca0143fad67f6a0316d7eca0151cc274cbbe59817e/hepunits-2.1.1-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="e85da92394feee9477ef951855f7ce521dc82c7b8907ad51728cc9060bf4d851",
        url="https://pypi.org/packages/35/92/96cb7336fcc0529c1abff3b80ebe00ce7a8f4a8a85d6d092202ede0b3c2f/hepunits-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="03e788d6eca982a6588d5759ce326dc81b7366965bbe6066b50ae888a549999b",
        url="https://pypi.org/packages/3b/8d/55d81e46988179d6513f5915bf326ff5adbc5ee2647d952f7df6d097425e/hepunits-1.2.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.3:")

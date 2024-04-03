# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBabel(PythonPackage):
    """Babel is an integrated collection of utilities that assist in
    internationalizing and localizing Python applications, with an
    emphasis on web-based applications."""

    homepage = "https://babel.pocoo.org/en/latest/"
    pypi = "Babel/Babel-2.7.0.tar.gz"
    git = "https://github.com/python-babel/babel"

    license("BSD-3-Clause")

    version(
        "2.12.1",
        sha256="b4246fb7677d3b98f501a39d43396d3cafdc8eadb045f4a31be01863f655c610",
        url="https://pypi.org/packages/df/c4/1088865e0246d7ecf56d819a233ab2b72f7d6ab043965ef327d0731b5434/Babel-2.12.1-py3-none-any.whl",
    )
    version(
        "2.10.3",
        sha256="ff56f4892c1c4bf0d814575ea23471c230d544203c7748e8c68f0089478d48eb",
        url="https://pypi.org/packages/2e/57/a4177e24f8ed700c037e1eca7620097fdfbb1c9b358601e40169adf6d364/Babel-2.10.3-py3-none-any.whl",
    )
    version(
        "2.9.1",
        sha256="ab49e12b91d937cd11f0b67cb259a57ab4ad2b59ac7a3b41d6c06c0ac5b0def9",
        url="https://pypi.org/packages/aa/96/4ba93c5f40459dc850d25f9ba93f869a623e77aaecc7a9344e19c01942cf/Babel-2.9.1-py2.py3-none-any.whl",
    )
    version(
        "2.7.0",
        sha256="af92e6106cb7c55286b25b38ad7695f8b4efb36a90ba483d7f7a6628c46158ab",
        url="https://pypi.org/packages/2c/60/f2af68eb046c5de5b1fe6dd4743bf42c074f7141fe7b2737d3061533b093/Babel-2.7.0-py2.py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="6778d85147d5d85345c14a26aada5e478ab04e39b078b0745ee6870c2b5cf669",
        url="https://pypi.org/packages/b8/ad/c6f60602d3ee3d92fbed87675b6fb6a6f9a38c223343ababdb44ba201f10/Babel-2.6.0-py2.py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="e86ca5a3a6bb64b9bbb62b9dac37225ec0ab5dfaae3c2492ebd648266468042f",
        url="https://pypi.org/packages/5f/cf/17935db603f7044d188ce3e3a6545c4b4500dbaa8835d50da2934b738111/Babel-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.4",
        sha256="3318ed2960240d61cbc6558858ee00c10eed77a6508c4d1ed8e6f7f48399c975",
        url="https://pypi.org/packages/b4/ec/acd307eac2e23f9cab1c8bdbe29b3b1d43215e31c32f8aa91b3a97925b5b/Babel-2.3.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.12:")
        depends_on("py-pytz@2015.7:", when="@2.12: ^python@:3.8")
        depends_on("py-pytz@2015.7:", when="@2.7:2.11")
        depends_on("py-pytz", when="@2.1:2.6")

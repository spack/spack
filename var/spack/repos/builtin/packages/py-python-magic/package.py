# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonMagic(PythonPackage):
    """A python wrapper for libmagic.

    This project is named python-magic but imports as the module name "magic".
    """

    homepage = "https://github.com/ahupp/python-magic"
    pypi = "python-magic/python-magic-0.4.15.tar.gz"

    license("MIT")

    version(
        "0.4.24",
        sha256="4fec8ee805fea30c07afccd1592c0f17977089895bdfaae5fec870a84e997626",
        url="https://pypi.org/packages/d3/99/c89223c6547df268596899334ee77b3051f606077317023617b1c43162fb/python_magic-0.4.24-py2.py3-none-any.whl",
    )
    version(
        "0.4.15",
        sha256="f2674dcfad52ae6c49d4803fa027809540b130db1dec928cfbb9240316831375",
        url="https://pypi.org/packages/42/a1/76d30c79992e3750dac6790ce16f056f870d368ba142f83f75f694d93001/python_magic-0.4.15-py2.py3-none-any.whl",
    )

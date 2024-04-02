# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhonenumbers(PythonPackage):
    """Python version of Google's common library for parsing, formatting
    and validating international phone numbers."""

    homepage = "https://github.com/daviddrysdale/python-phonenumbers"
    pypi = "phonenumbers/phonenumbers-8.12.16.tar.gz"

    version(
        "8.12.16",
        sha256="56ad29025b8f885945506350b06d77afbc506c5463141d77a5df767280a7ee0b",
        url="https://pypi.org/packages/c1/ac/57ea656c1ff9a8b5dc9729d9b75f4d568c3598d4e4a7df31c1791ed9a095/phonenumbers-8.12.16-py2.py3-none-any.whl",
    )
    version(
        "8.12.15",
        sha256="13d499f7114c4b37c54ee844b188d5e7441951a7da41de5fc1a25ff8fdceef80",
        url="https://pypi.org/packages/59/b2/97909573e16946c8512c6f996bbbd34c9419d48a0b34df1a88bcd6f58cb4/phonenumbers-8.12.15-py2.py3-none-any.whl",
    )
    version(
        "8.12.14",
        sha256="d60a3902d7648288624ee9568b8bc7a53b31de07bd7cb80993a3704c674dce32",
        url="https://pypi.org/packages/92/9a/ca61b4502e68812f0b33976fb7c1239039363fffd64434523f90f9ee60e8/phonenumbers-8.12.14-py2.py3-none-any.whl",
    )

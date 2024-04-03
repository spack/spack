# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIdna(PythonPackage):
    """Internationalized Domain Names for Python (IDNA 2008 and UTS #46)"""

    homepage = "https://github.com/kjd/idna"
    pypi = "idna/idna-3.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "3.4",
        sha256="90b77e79eaa3eba6de819a0c442c0b4ceefc341a7a2ab77d7562bf49f425c5c2",
        url="https://pypi.org/packages/fc/34/3030de6f1370931b9dbb4dad48f6ab1015ab1d32447850b9fc94e60097be/idna-3.4-py3-none-any.whl",
    )
    version(
        "3.3",
        sha256="84d9dd047ffa80596e0f246e2eab0b391788b0503584e8945f2368256d2735ff",
        url="https://pypi.org/packages/04/a2/d918dcd22354d8958fe113e1a3630137e0fc8b44859ade3063982eacd2a4/idna-3.3-py3-none-any.whl",
    )
    version(
        "3.2",
        sha256="14475042e284991034cb48e06f6851428fb14c4dc953acd9be9a5e95c7b6dd7a",
        url="https://pypi.org/packages/d7/77/ff688d1504cdc4db2a938e2b7b9adee5dd52e34efbd2431051efc9984de9/idna-3.2-py3-none-any.whl",
    )
    version(
        "2.9",
        sha256="a068a21ceac8a4d63dbfd964670474107f541babbd2250d61922f029858365fa",
        url="https://pypi.org/packages/89/e3/afebe61c546d18fb1709a61bee788254b40e736cff7271c7de5de2dc4128/idna-2.9-py2.py3-none-any.whl",
    )
    version(
        "2.8",
        sha256="ea8b7f6188e6fa117537c3df7da9fc686d485087abf6ac197f9c46432f7e4a3c",
        url="https://pypi.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl",
    )
    version(
        "2.5",
        sha256="cc19709fd6d0cbfed39ea875d29ba6d4e22c0cebc510a76d6302a28385e8bb70",
        url="https://pypi.org/packages/11/7d/9bbbd7bb35f34b0169542487d2a8859e44306bb2e6a4455d491800a5621f/idna-2.5-py2.py3-none-any.whl",
    )

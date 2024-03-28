# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRx(PythonPackage):
    """Reactive Extensions (Rx) for Python"""

    homepage = "http://reactivex.io/"
    pypi = "Rx/Rx-3.2.0.tar.gz"

    maintainers("dorton21")

    version(
        "3.2.0",
        sha256="922c5f4edb3aa1beaa47bf61d65d5380011ff6adcd527f26377d05cb73ed8ec8",
        url="https://pypi.org/packages/e2/a9/efeaeca4928a9a56d04d609b5730994d610c82cf4d9dd7aa173e6ef4233e/Rx-3.2.0-py3-none-any.whl",
    )
    version(
        "1.6.1",
        sha256="7357592bc7e881a95e0c2013b73326f704953301ab551fbc8133a6fadab84105",
        url="https://pypi.org/packages/33/0f/5ef4ac78e2a538cc1b054eb86285fe0bf7a5dbaeaac2c584757c300515e2/Rx-1.6.1-py2.py3-none-any.whl",
    )

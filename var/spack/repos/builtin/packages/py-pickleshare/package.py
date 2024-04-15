# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPickleshare(PythonPackage):
    """Tiny 'shelve'-like database with concurrency support"""

    pypi = "pickleshare/pickleshare-0.7.4.tar.gz"

    license("MIT")

    version(
        "0.7.5",
        sha256="9649af414d74d4df115d5d718f82acb59c9d418196b7b4290ed47a12ce62df56",
        url="https://pypi.org/packages/9a/41/220f49aaea88bc6fa6cba8d05ecf24676326156c23b991e80b3f2fc24c77/pickleshare-0.7.5-py2.py3-none-any.whl",
    )
    version(
        "0.7.4",
        sha256="c9a2541f25aeabc070f12f452e1f2a8eae2abd51e1cd19e8430402bdf4c1d8b5",
        url="https://pypi.org/packages/9f/17/daa142fc9be6b76f26f24eeeb9a138940671490b91cb5587393f297c8317/pickleshare-0.7.4-py2.py3-none-any.whl",
    )

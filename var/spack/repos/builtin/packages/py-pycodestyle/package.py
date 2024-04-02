# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycodestyle(PythonPackage):
    """pycodestyle is a tool to check your Python code against some of the
    style conventions in PEP 8. Note: formerly called pep8."""

    homepage = "https://github.com/PyCQA/pycodestyle"
    pypi = "pycodestyle/pycodestyle-2.8.0.tar.gz"

    license("MIT")

    version(
        "2.11.0",
        sha256="5d1013ba8dc7895b548be5afb05740ca82454fd899971563d2ef625d090326f8",
        url="https://pypi.org/packages/31/c2/e1508ed4395793f69e40fd8c6b5a690e1d568e649aae9492076a7b6befb4/pycodestyle-2.11.0-py2.py3-none-any.whl",
    )
    version(
        "2.10.0",
        sha256="8a4eaf0d0495c7395bdab3589ac2db602797d76207242c17d470186815706610",
        url="https://pypi.org/packages/a2/54/001fdc0d69e8d0bb86c3423a6fa6dfada8cc26317c2635ab543e9ac411bd/pycodestyle-2.10.0-py2.py3-none-any.whl",
    )
    version(
        "2.9.1",
        sha256="d1735fc58b418fd7c5f658d28d943854f8a849b01a5d0a1e6f3f3fdd0166804b",
        url="https://pypi.org/packages/67/e4/fc77f1039c34b3612c4867b69cbb2b8a4e569720b1f19b0637002ee03aff/pycodestyle-2.9.1-py2.py3-none-any.whl",
    )
    version(
        "2.9.0",
        sha256="289cdc0969d589d90752582bef6dff57c5fbc6949ee8b013ad6d6449a8ae9437",
        url="https://pypi.org/packages/a4/9e/2f9e7d5b13ad7c326f99d08d36757fc02fcd137cd5898b216a9faca38f9a/pycodestyle-2.9.0-py2.py3-none-any.whl",
    )
    version(
        "2.8.0",
        sha256="720f8b39dde8b293825e7ff02c475f3077124006db4f440dcbc9a20b76548a20",
        url="https://pypi.org/packages/15/94/bc43a2efb7b8615e38acde2b6624cae8c9ec86faf718ff5676c5179a7714/pycodestyle-2.8.0-py2.py3-none-any.whl",
    )
    version(
        "2.7.0",
        sha256="514f76d918fcc0b55c6680472f0a37970994e07bbb80725808c17089be302068",
        url="https://pypi.org/packages/de/cc/227251b1471f129bc35e966bb0fceb005969023926d744139642d847b7ae/pycodestyle-2.7.0-py2.py3-none-any.whl",
    )
    version(
        "2.6.0",
        sha256="2295e7b2f6b5bd100585ebcb1f616591b652db8a741695b3d8f5d28bdc934367",
        url="https://pypi.org/packages/10/5b/88879fb861ab79aef45c7e199cae3ef7af487b5603dcb363517a50602dd7/pycodestyle-2.6.0-py2.py3-none-any.whl",
    )
    version(
        "2.5.0",
        sha256="95a2219d12372f05704562a14ec30bc76b05a5b297b21a5dfe3f6fac3491ae56",
        url="https://pypi.org/packages/0e/0c/04a353e104d2f324f8ee5f4b32012618c1c86dd79e52a433b64fceed511b/pycodestyle-2.5.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.1",
        sha256="6c4245ade1edfad79c3446fadfc96b0de2759662dc29d07d80a6f27ad1ca6ba9",
        url="https://pypi.org/packages/e4/81/78fe51eb4038d1388b7217dd63770b0f428370207125047312886c923b26/pycodestyle-2.3.1-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="ae308be77310759b722965cfe4a81b69c10aacaecb2db2c874ceb1720cc8f1aa",
        url="https://pypi.org/packages/32/09/8e580517e4af96141c41f531bca14c4408e7cb716864022737811aaac1be/pycodestyle-2.3.0-py2.py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="60c4e1c36f301ac539a550a29e9d16862069ec240472d86e5e71c4fc645829cb",
        url="https://pypi.org/packages/46/95/0b74196cb512cbf5127c27636115d63126c0f1a10383d828b9ad7295f381/pycodestyle-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="14588a4a51f464b784eb199ade0a04103e93f9ed7d69551f29f295a9e9668030",
        url="https://pypi.org/packages/49/16/455af11e9afef9a38804c516910ba8093f673981a55dbfd4688974b45f40/pycodestyle-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "2.0.0",
        sha256="2ce83f2046f5ab85c652ceceddfbde7a64a909900989b4b43e92b10b743d0ce5",
        url="https://pypi.org/packages/73/31/136a79364c1681a3c276796d1f5090833bd03461b78a1b037638d1a2c484/pycodestyle-2.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@2.11:")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pycodestyle requires py-setuptools during runtime as well.

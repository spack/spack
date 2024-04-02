# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTomlkit(PythonPackage):
    """Style preserving TOML library"""

    homepage = "https://github.com/sdispater/tomlkit"
    pypi = "tomlkit/tomlkit-0.7.0.tar.gz"

    license("MIT")

    version(
        "0.12.1",
        sha256="712cbd236609acc6a3e2e97253dfc52d4c2082982a88f61b640ecf0817eab899",
        url="https://pypi.org/packages/a0/6d/808775ed618e51edaa7bbe6759e22e1c7eafe359af6e084700c6d39d3455/tomlkit-0.12.1-py3-none-any.whl",
    )
    version(
        "0.11.4",
        sha256="25d4e2e446c453be6360c67ddfb88838cfc42026322770ba13d1fbd403a93a5c",
        url="https://pypi.org/packages/18/31/2a87f292f752d39c6c207f9e44137e3e1d4250da880a9fbc0bbf630138e0/tomlkit-0.11.4-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="0f4050db66fd445b885778900ce4dd9aea8c90c4721141fde0d6ade893820ef1",
        url="https://pypi.org/packages/96/6b/67e390f8efdd095c4fce0fa648ad711eb795fef2d954a01c289238e39076/tomlkit-0.11.0-py3-none-any.whl",
    )
    version(
        "0.7.2",
        sha256="173ad840fa5d2aac140528ca1933c29791b79a374a0861a80347f42ec9328117",
        url="https://pypi.org/packages/eb/ef/5bd27c1a8040874cc863c263bf38857b5607017b656943c6c93b29bc8f42/tomlkit-0.7.2-py2.py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="6babbd33b17d5c9691896b0e68159215a9387ebfa938aa3ac42f4a4beeb2b831",
        url="https://pypi.org/packages/bc/01/a0ee34fe37dd54f795e8f8a820af57c9a94d7358276acf6cdc21ae8d9533/tomlkit-0.7.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.11.7:")
        depends_on("python@:3", when="@0.8:0.11.5")

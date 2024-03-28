# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGooglePasta(PythonPackage):
    """pasta is an AST-based Python refactoring library."""

    homepage = "https://github.com/google/pasta"
    pypi = "google-pasta/google-pasta-0.1.8.tar.gz"

    license("Apache-2.0")

    version(
        "0.2.0",
        sha256="b32482794a366b5366a32c92a9a9201b107821889935a02b3e51f6b432ea84ed",
        url="https://pypi.org/packages/a3/de/c648ef6835192e6e2cc03f40b19eeda4382c49b5bafb43d88b931c4c74ac/google_pasta-0.2.0-py3-none-any.whl",
    )
    version(
        "0.1.8",
        sha256="644dcf3784cf7147ab01de5dc22e60a638d219d4e4a3a7464eb98997ae2fe66f",
        url="https://pypi.org/packages/c3/fd/1e86bc4837cc9a3a5faf3db9b1854aa04ad35b5f381f9648fbe81a6f94e4/google_pasta-0.1.8-py3-none-any.whl",
    )
    version(
        "0.1.7",
        sha256="40b4f55ba7b44823eac96d055000572c84ce48cacb3e91c100869844064b2d07",
        url="https://pypi.org/packages/d0/33/376510eb8d6246f3c30545f416b2263eee461e40940c2a4413c711bdf62d/google_pasta-0.1.7-py3-none-any.whl",
    )
    version(
        "0.1.6",
        sha256="477b14e952f50beba4643dd90171379009aa89736548855a3f09ae2c78ab50e6",
        url="https://pypi.org/packages/f9/68/a14620bfb042691f532dcde8576ff82ee82e4c003cdc0a3dbee5f289cee6/google_pasta-0.1.6-py3-none-any.whl",
    )
    version(
        "0.1.5",
        sha256="cf3118359dc9a32ebffc0023647d90f52cb6cafe382b9186490a1576d8764bef",
        url="https://pypi.org/packages/64/bb/f1bbc131d6294baa6085a222d29abadd012696b73dcbf8cf1bf56b9f082a/google_pasta-0.1.5-py3-none-any.whl",
    )
    version(
        "0.1.4",
        sha256="2a40a43cd38d7560b1e42e28c8d1c055951da76fb4328e6cac25b83456083a29",
        url="https://pypi.org/packages/8c/96/adbd4eafe72ce9b5ca6f168fbf109386e1b601f7c59926a11e9d7b7a5b44/google_pasta-0.1.4-py3-none-any.whl",
    )
    version(
        "0.1.3",
        sha256="be372625ed326f3f577504c10bb1aa3d36a399c1e4c4338ef46320795ad9e1ed",
        url="https://pypi.org/packages/1a/bf/15a18fa7017d17eff945704bc708153973a8e79f90855aa016dce6b61e70/google_pasta-0.1.3-py3-none-any.whl",
    )
    version(
        "0.1.2",
        sha256="253c7232d9655acb6904d0a66e262681b8fe9e5093ab28776720000465577a67",
        url="https://pypi.org/packages/38/81/4a1dd556f594bfe73dc8332ca718b199219d6059143506e0802bb6f8c201/google_pasta-0.1.2-py3-none-any.whl",
    )
    version(
        "0.1.1",
        sha256="06d74fdadd6e1164c0e73b05472d1612812aa849f545052fa3b9fdd841b56002",
        url="https://pypi.org/packages/86/6c/9eabce1c1cdaa657751a802f94d71ca29b8f82e10cac97c3fd5f8c82736c/google_pasta-0.1.1-py3-none-any.whl",
    )
    version(
        "0.1",
        sha256="7632625f7c532d2cf75ce85f106cecc8d7624d05e8d3ccda1dd1064d93d767b9",
        url="https://pypi.org/packages/a5/e2/7d191b4613b20fa149e9ebc952f954650fc1dbcabb39e9387f6f1cd5d313/google_pasta-0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-six", when="@0.1.8:")

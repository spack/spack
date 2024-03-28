# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyparsing(PythonPackage):
    """A Python Parsing Module."""

    homepage = "https://pyparsing-docs.readthedocs.io/en/latest/"
    pypi = "pyparsing/pyparsing-2.4.2.tar.gz"

    license("MIT")

    version(
        "3.0.9",
        sha256="5026bae9a10eeaefb61dab2f09052b9f4307d44aee4eda64b309723d8d206bbc",
        url="https://pypi.org/packages/6c/10/a7d0fa5baea8fe7b50f448ab742f26f52b80bfca85ac2be9d35cdd9a3246/pyparsing-3.0.9-py3-none-any.whl",
    )
    version(
        "3.0.6",
        sha256="04ff808a5b90911829c55c4e26f75fa5ca8a2f5f36aa3a51f68e27033341d3e4",
        url="https://pypi.org/packages/a0/34/895006117f6fce0b4de045c87e154ee4a20c68ec0a4c9a36d900888fb6bc/pyparsing-3.0.6-py3-none-any.whl",
    )
    version(
        "2.4.7",
        sha256="ef9d7589ef3c200abe66653d3f1ab1033c3c419ae9b9bdb1240a85b024efc88b",
        url="https://pypi.org/packages/8a/bb/488841f56197b13700afd5658fc279a2025a39e22449b7cf29864669b15d/pyparsing-2.4.7-py2.py3-none-any.whl",
    )
    version(
        "2.4.2",
        sha256="d9338df12903bbf5d65a0e4e87c2161968b10d2e489652bb47001d82a9b028b4",
        url="https://pypi.org/packages/11/fa/0160cd525c62d7abd076a070ff02b2b94de589f1a9789774f17d7c54058e/pyparsing-2.4.2-py2.py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="9b6323ef4ab914af344ba97510e966d64ba91055d6b9afa6b30799340e89cc03",
        url="https://pypi.org/packages/dd/d9/3ec19e966301a6e25769976999bd7bbe552016f0d32b577dc9d63d2e0c49/pyparsing-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.1",
        sha256="f6c5ef0d7480ad048c054c37632c67fca55299990fff127850181659eea33fc3",
        url="https://pypi.org/packages/de/0a/001be530836743d8be6c2d85069f46fecf84ac6c18c7f5fb8125ee11d854/pyparsing-2.3.1-py2.py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="fee43f17a9c4087e7ed1605bd6df994c6173c1e977d7ade7b651292fab2bd010",
        url="https://pypi.org/packages/6a/8a/718fd7d3458f9fab8e67186b00abdd345b639976bc7fb3ae722e1b026a50/pyparsing-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.10",
        sha256="67101d7acee692962f33dd30b5dce079ff532dd9aa99ff48d52a3dad51d2fe84",
        url="https://pypi.org/packages/2b/f7/e5a178fc3ea4118a0edce2a8d51fc14e680c745cf4162e4285b437c43c94/pyparsing-2.1.10-py2.py3-none-any.whl",
    )
    version(
        "2.0.3",
        sha256="a9c896bab06dbf3759ad5fb63cfdb3777191e2c4ae640e6dd69ed37530f6ba56",
        url="https://pypi.org/packages/8f/f4/3a70b5e5b865b1ec45fe48dc5a57cd4facb5c7bd80e5cb1255c362732e81/pyparsing-2.0.3-py2.py3-none-any.whl",
    )

    import_modules = ["pyparsing"]

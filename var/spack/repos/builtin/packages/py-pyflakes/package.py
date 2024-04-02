# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyflakes(PythonPackage):
    """A simple program which checks Python source files for errors."""

    homepage = "https://github.com/PyCQA/pyflakes"
    pypi = "pyflakes/pyflakes-2.4.0.tar.gz"

    license("MIT")

    version(
        "3.1.0",
        sha256="4132f6d49cb4dae6819e5379898f2b8cce3c5f23994194c24b77d5da2e36f774",
        url="https://pypi.org/packages/00/e9/1e1fd7fae559bfd07704991e9a59dd1349b72423c904256c073ce88a9940/pyflakes-3.1.0-py2.py3-none-any.whl",
    )
    version(
        "3.0.1",
        sha256="ec55bf7fe21fff7f1ad2f7da62363d749e2a470500eab1b555334b67aa1ef8cf",
        url="https://pypi.org/packages/af/4c/b1c7008aa7788b3e26c06c60aa18da7d3aa1f00e344aa3f18ac92768854b/pyflakes-3.0.1-py2.py3-none-any.whl",
    )
    version(
        "2.5.0",
        sha256="4579f67d887f804e67edb544428f264b7b24f435b263c4614f384135cea553d2",
        url="https://pypi.org/packages/dc/13/63178f59f74e53acc2165aee4b002619a3cfa7eeaeac989a9eb41edf364e/pyflakes-2.5.0-py2.py3-none-any.whl",
    )
    version(
        "2.4.0",
        sha256="3bb3a3f256f4b7968c9c788781e4ff07dce46bdf12339dcda61053375426ee2e",
        url="https://pypi.org/packages/43/fb/38848eb494af7df9aeb2d7673ace8b213313eb7e391691a79dbaeb6a838f/pyflakes-2.4.0-py2.py3-none-any.whl",
    )
    version(
        "2.3.0",
        sha256="910208209dcea632721cb58363d0f72913d9e8cf64dc6f8ae2e02a3609aba40d",
        url="https://pypi.org/packages/57/7e/188ea51830ff05ecf6154b849cd420cf581c0deb60c173215d326e8af197/pyflakes-2.3.0-py2.py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="0d94e0e05a19e57a99444b6ddcf9a6eb2e5c68d3ca1e98e90707af8152c90a92",
        url="https://pypi.org/packages/69/5b/fd01b0c696f2f9a6d2c839883b642493b431f28fa32b29abc465ef675473/pyflakes-2.2.0-py2.py3-none-any.whl",
    )
    version(
        "2.1.1",
        sha256="17dbeb2e3f4d772725c777fabc446d5634d1038f234e77343108ce445ea69ce0",
        url="https://pypi.org/packages/84/f2/ed0ffb887f8138a8fe5a621b8c0bb9598bfb3989e029f6c6a85ee66628ee/pyflakes-2.1.1-py2.py3-none-any.whl",
    )
    version(
        "2.1.0",
        sha256="f277f9ca3e55de669fba45b7393a1449009cff5a37d1af10ebb76c52765269cd",
        url="https://pypi.org/packages/16/3b/b6a508ad148ce1ef50bd7a9a783afbb8d775616fc4ae5e3007c8815a3c85/pyflakes-2.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="08bd6a50edf8cffa9fa09a463063c425ecaaf10d1eb0335a7e8b1401aef89e6f",
        url="https://pypi.org/packages/d7/40/733bcc64da3161ae4122c11e88269f276358ca29335468005cb0ee538665/pyflakes-1.6.0-py2.py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="cc5eadfb38041f8366128786b4ca12700ed05bbf1403d808e89d57d67a3875a7",
        url="https://pypi.org/packages/27/49/924098b3b85c286696f37e014475d79471ffc44509613af420645a3c12cb/pyflakes-1.5.0-py2.py3-none-any.whl",
    )
    version(
        "1.4.0",
        sha256="a3ecf40567dc470c006c19abbac9c8b4a77a8a5a01e975bb6452b8814818ad3f",
        url="https://pypi.org/packages/d7/ed/665746776f005f4bb51747e70e89d8d687584f0241cb44220c598391fed8/pyflakes-1.4.0-py2.py3-none-any.whl",
    )
    version(
        "1.3.0",
        sha256="ad89dafee8ca32282116209a0ca4dff050bdc343af958721d5517d242c1215d5",
        url="https://pypi.org/packages/6a/10/4ca0cd9b71739dc4aef92434747743a63acbdb5cb5938242db6e2cf5e5b8/pyflakes-1.3.0-py2.py3-none-any.whl",
    )
    version(
        "1.2.3",
        sha256="e87bac26c62ea5b45067cc89e4a12f56e1483f1f2cda17e7c9b375b9fd2f40da",
        url="https://pypi.org/packages/74/55/98f59358be6d7240ba546b8a74813cc21841a9145a0c1a3a7998f50acbe7/pyflakes-1.2.3-py2.py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="3ffa8db8eb8873971ba1a7328ac5fdbc167212f2824c23789d5d158cc902fd66",
        url="https://pypi.org/packages/48/f7/f5864b0c2b640039cabf17bea109d6f230e3ab1d073ecb32f7f367558394/pyflakes-1.2.2-py2.py3-none-any.whl",
    )
    version(
        "1.2.1",
        sha256="79951a4d3c1a139191e6aade392936565ec5e1987d04c0495ab32d32149c19e3",
        url="https://pypi.org/packages/bf/1d/00af5299878b6b68009b63692e4f7e7a39d920588d5ff1ab0d2b3db79e43/pyflakes-1.2.1-py2.py3-none-any.whl",
    )
    version(
        "1.2.0",
        sha256="a2e2a2f68e8321822cb68ccf687a4d8c1668e850135267659ce8152d86adf0d8",
        url="https://pypi.org/packages/e2/ac/5497dd04fa6ab3dcc9e154b5687459577efef5fcd83097bb65aa35954940/pyflakes-1.2.0-py2.py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="c2ec174a7cff6486176b1f53e7d15d34380c3688410f88d86b323608cc0906fb",
        url="https://pypi.org/packages/05/00/2867f51e4c2526fd8524176520aecfcd1562033cc5f7110673012294fcc7/pyflakes-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.2",
        sha256="05df584a29eeea9a2a2110dd362e53d04e0c4bb1754b4d71234f651917f3c2f0",
        url="https://pypi.org/packages/59/70/6fbc74a5554fd6f0230f6cc298c9e74847cc727bdbf07c9f9d01ad8c0dc3/pyflakes-0.9.2-py2.py3-none-any.whl",
    )
    version(
        "0.9.1",
        sha256="0aaa2e555db3fc5084a1e6143cb54b787e8d5dbfb436d616ba3cb2d634f02923",
        url="https://pypi.org/packages/f2/56/7ddb2c7ba7c6c6583784043d9408a8f165b9fd0a319400ceae0043dea892/pyflakes-0.9.1-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="763e6dc73539e90badfdb6f476d71fc68abc8ef572b3ef2022ddc9cc6baec4c3",
        url="https://pypi.org/packages/aa/72/c2cc75d9eb4da5edb6ad23955df0b52048cdada68eb569d4177955f7c6e0/pyflakes-0.9.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3.1:")

    # Most Python packages only require py-setuptools as a build dependency.
    # However, py-pyflakes requires py-setuptools during runtime as well.

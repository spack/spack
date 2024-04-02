# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNbsphinx(PythonPackage):
    """nbsphinx is a Sphinx extension that provides a source parser for
    *.ipynb files.
    """

    # It should be noted that in order to have nbsphinx work,
    # one must create a Spack view of the dependencies.

    homepage = "https://nbsphinx.readthedocs.io"
    pypi = "nbsphinx/nbsphinx-0.8.0.tar.gz"

    license("MIT")

    version(
        "0.8.8",
        sha256="c6c3875f8735b9ea57d65f81a7e240542daa613cad10661c54e0adee4e77938c",
        url="https://pypi.org/packages/6d/ec/13038168ecd191aded1de0443817ce6574ec9434d5b7eca7acd16719d610/nbsphinx-0.8.8-py3-none-any.whl",
    )
    version(
        "0.8.7",
        sha256="8862f291f98c1a163bdb5bac8adf25c61585a81575ac5c613320c6f3fe5c472f",
        url="https://pypi.org/packages/eb/4d/2c07c13682465e0d2159af292fa20cee26e6a6e322c02764e0ac5d74a824/nbsphinx-0.8.7-py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="ef75e15047e36faa9741267286b9dc7d5a0d16302f65adee73885e8949ec6f75",
        url="https://pypi.org/packages/1b/1d/b65dff2f8dc45460e77cef7bb8b761444ecf25759d847c955db02277eb3a/nbsphinx-0.8.1-py3-none-any.whl",
    )
    version(
        "0.8.0",
        sha256="14ccbbd3d5944fd7e14087f67b83ea75cd41c9eb679561258237987d322e9381",
        url="https://pypi.org/packages/6f/7a/9828e8981e472e717f695da957f52b389e91086532797005999342f487b5/nbsphinx-0.8.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-docutils")
        depends_on("py-jinja2", when="@:0.8.4,0.8.6:")
        depends_on("py-nbconvert@:5.3,5.4.1:")
        depends_on("py-nbformat")
        depends_on("py-sphinx@1.8.0:", when="@0.5:")
        depends_on("py-traitlets", when="@:0.8.8")

    # https://nbsphinx.readthedocs.io/en/latest/installation.html

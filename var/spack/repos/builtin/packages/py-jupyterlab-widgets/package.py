# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterlabWidgets(PythonPackage):
    """A JupyterLab extension."""

    homepage = "https://github.com/jupyter-widgets/ipywidgets"
    # Source is also available, but I'm having issues getting it to build:
    # https://github.com/jupyter-widgets/ipywidgets/issues/3324
    url = "https://files.pythonhosted.org/packages/py3/j/jupyterlab_widgets/jupyterlab_widgets-1.0.2-py3-none-any.whl"

    license("BSD-3-Clause")

    version(
        "3.0.3",
        sha256="6aa1bc0045470d54d76b9c0b7609a8f8f0087573bae25700a370c11f82cb38c8",
        url="https://pypi.org/packages/d8/52/2f4b8f5975312fb58f4eacab2e6f6cfd2efd05704514a60a151a4e69d608/jupyterlab_widgets-3.0.3-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="c2a9bd3789f120f64d73268c066ed3b000c56bc1dda217be5cdc43e7b4ebad3f",
        url="https://pypi.org/packages/5f/2c/7331aa9c5041e8b107d712d853268e137f55014b858407816b5487289d11/jupyterlab_widgets-1.1.0-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="f5d9efface8ec62941173ba1cffb2edd0ecddc801c11ae2931e30b50492eb8f7",
        url="https://pypi.org/packages/18/4d/22a93473bca99c80f2d23f867ebbfee2f6c8e186bf678864eec641500910/jupyterlab_widgets-1.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.0.0-beta1:")

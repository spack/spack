# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMarkdownItPy(PythonPackage):
    """Markdown parser, done right.
    100% CommonMark support, extensions, syntax plugins & high speed"""

    homepage = "https://github.com/executablebooks/markdown-it-py"
    git = "https://github.com/executablebooks/markdown-it-py"
    pypi = "markdown-it-py/markdown-it-py-1.1.0.tar.gz"

    license("MIT")

    version(
        "3.0.0",
        sha256="355216845c60bd96232cd8d8c40e8f9765cc86f46880e43a8fd22dc1a1a8cab1",
        url="https://pypi.org/packages/42/d7/1ec15b46af6af88f19b8e5ffea08fa375d433c998b8a7639e76935c14f1f/markdown_it_py-3.0.0-py3-none-any.whl",
    )
    version(
        "2.2.0",
        sha256="5a35f8d1870171d9acc47b99612dc146129b631baf04970128b568f190d0cc30",
        url="https://pypi.org/packages/bf/25/2d88e8feee8e055d015343f9b86e370a1ccbec546f2865c98397aaef24af/markdown_it_py-2.2.0-py3-none-any.whl",
    )
    version(
        "1.1.0",
        sha256="98080fc0bc34c4f2bcf0846a096a9429acbd9d5d8e67ed34026c03c61c464389",
        url="https://pypi.org/packages/08/6b/33c40781e26c76e26825528f417f5414c501807f1f7fced82119c29aa832/markdown_it_py-1.1.0-py3-none-any.whl",
    )

    variant("linkify", default=False, description="Linkify support")
    variant("plugins", default=False, description="plugins")

    with default_args(type="run"):
        depends_on("python@3.8:", when="@3:")
        depends_on("python@3.7:", when="@2.1:2")
        depends_on("python@:3", when="@:2.0")
        depends_on("py-attrs@19:21", when="@1.1:2.0")
        depends_on("py-linkify-it-py@1:", when="@2.2:+linkify")
        depends_on("py-linkify-it-py@1", when="@0.5.8:2.1+linkify")
        depends_on("py-mdit-py-plugins", when="@1.0.0-beta2:+plugins")
        depends_on("py-mdurl@0.1:", when="@2:")
        depends_on("py-typing-extensions@3.7.4:", when="@1.0.0-beta3:2 ^python@:3.7")

    # Historical dependencies

# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJinja2Cli(PythonPackage):
    """A CLI interface to Jinja2"""

    homepage = "https://github.com/mattrobenolt/jinja2-cli"
    pypi = "jinja2-cli/jinja2-cli-0.6.0.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.8.2",
        sha256="b91715c79496beaddad790171e7258a87db21c1a0b6d2b15bca3ba44b74aac5d",
        url="https://pypi.org/packages/57/4a/032f945db179b83dc6375dcd3f6aa61a0107bfa210458f6fbd68e5556c6f/jinja2_cli-0.8.2-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="33e7c442e940812eca251a6bd41c812f16b126ffb81280462f220c4903512765",
        url="https://pypi.org/packages/ca/0f/dd461ac244fec4310c425e9cec9553d8ae8523c36837792e7666c6e53393/jinja2_cli-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jinja2", when="@0.6:")

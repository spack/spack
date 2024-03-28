# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribMermaid(PythonPackage):
    """This extension allows you to embed
    `Mermaid <http://knsv.github.io/mermaid/>`_ graphs in your documents,
    including general flowcharts, sequence and gantt diagrams."""

    homepage = "https://github.com/mgaitan/sphinxcontrib-mermaid"
    pypi = "sphinxcontrib-mermaid/sphinxcontrib-mermaid-0.4.0.tar.gz"

    version(
        "0.7.1",
        sha256="3e20de1937c30dfa807e446bf99983d73d0dd3dc5c6524addda59800fe928762",
        url="https://pypi.org/packages/24/cf/6f45fd1637d26b30360b019767b0ebbc81acc8d2bff58ab63c6bb06d5e41/sphinxcontrib_mermaid-0.7.1-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="01b3301af659555313e25ebe3cfd6ba209318044b7443148a20d5580f47baa1d",
        url="https://pypi.org/packages/fc/40/538db54f816aa65d73f31bc4b45f3784e52d27f610124b4c20f8d2b51199/sphinxcontrib_mermaid-0.4.0-py2.py3-none-any.whl",
    )

# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribMermaid(PythonPackage):
    """This extension allows you to embed
    `Mermaid <http://knsv.github.io/mermaid/>`_ graphs in your documents,
    including general flowcharts, sequence and gantt diagrams."""

    homepage = "https://github.com/mgaitan/sphinxcontrib-mermaid"
    pypi = "sphinxcontrib-mermaid/sphinxcontrib-mermaid-0.4.0.tar.gz"

    version('0.6.1', sha256='75ba8ab66b5157864360f5654a335af4a78384d5e9659c8d8e9ec9601d0a81b6')
    version('0.6.0', sha256='e23d7bf90603814cf099434576994558f1e083ae21c2d7d136412957dfd9ddb6')
    version('0.4.0', sha256='0ee45ba45b9575505eacdd6212e4e545213f4f93dfa32c7eeca32720dbc3b468')

    depends_on('py-sphinx@1.7:')

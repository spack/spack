# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtml2text(PythonPackage):
    """Turn HTML into equivalent Markdown-structured text."""

    homepage = "https://github.com/Alir3z4/html2text/"
    pypi = "html2text/html2text-2016.9.19.tar.gz"

    version('2020.1.16', sha256='e296318e16b059ddb97f7a8a1d6a5c1d7af4544049a01e261731d2d5cc277bbb')
    version('2019.9.26', sha256='6f56057c5c2993b5cc5b347cb099bdf6d095828fef1b53ef4e2a2bf2a1be9b4f')
    version('2019.8.11', sha256='f516b9c10284174e2a974d86f91cab02b3cf983a17752075da751af0e895ef5e')
    version('2018.1.9',  sha256='627514fb30e7566b37be6900df26c2c78a030cc9e6211bda604d8181233bcdd4')
    version('2017.10.4', sha256='02ab8df206e90a395b7e188e26eb1906680439ce4a636a00217851cef58c1fad')
    version('2016.9.19', sha256='554ef5fd6c6cf6e3e4f725a62a3e9ec86a0e4d33cd0928136d1c79dbeb7b2d55')

    depends_on('py-setuptools', type='build')

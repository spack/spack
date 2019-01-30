# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
        of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    url      = "https://pypi.io/packages/source/P/Pympler/Pympler-0.4.3.tar.gz"

    version('0.4.3', 'bbb4239126e9c99e2effc83b02bf8755')
    version('0.4.2', '6bdfd913ad4c94036e8a2b358e49abd7')
    version('0.4.1', '2d54032a6da91ff438f48d5f36b719a6')
    version('0.4',   '68e4a8aa4a268996fa6a321b664918af')
    version('0.3.1', '906ce437f46fb30991007671a59d4319')

    depends_on('python@2.5:')

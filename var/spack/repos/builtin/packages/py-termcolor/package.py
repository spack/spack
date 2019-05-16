# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTermcolor(PythonPackage):
    """Cross-platform abstraction for writing colored text to a terminal"""

    homepage = "https://pypi.org/project/termcolor/"
    url      = "https://files.pythonhosted.org/packages/8a/48/a76be51647d0eb9f10e2a4511bf3ffb8cc1e6b14e9e4fab46173aa79f981/termcolor-1.1.0.tar.gz"

    version('1.1.0', '043e89644f8909d462fbbfa511c768df')

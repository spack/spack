# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJoblib(PythonPackage):
    """Python function as pipeline jobs"""

    homepage = "http://packages.python.org/joblib/"
    url      = "https://pypi.io/packages/source/j/joblib/joblib-0.13.2.tar.gz"

    import_modules = [
        'joblib', 'joblib.externals', 'joblib.externals.cloudpickle',
        'joblib.externals.loky', 'joblib.externals.loky.backend'
    ]

    version('0.13.2', sha256='315d6b19643ec4afd4c41c671f9f2d65ea9d787da093487a81ead7b0bac94524')
    version('0.10.3', '455401ccfaf399538d8e5333086df2d3')
    version('0.10.2', 'ebb42af4342c2445b175f86bd478d869')
    version('0.10.0', '61e40322c4fed5c22905f67d7d1aa557')

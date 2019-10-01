# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycares(PythonPackage):
    """pycares is a Python module which provides an interface to c-ares. c-ares
    is a C library that performs DNS requests and name resolutions
    asynchronously."""

    homepage = "https://github.com/saghul/pycares"
    url      = "https://github.com/saghul/pycares/archive/pycares-3.0.0.tar.gz"

    version('3.0.0', '5f938c037c5905ebc5617a157c654088')

    depends_on('python@2.6:')
    depends_on('py-cffi')

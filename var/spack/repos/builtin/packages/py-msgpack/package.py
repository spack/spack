# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMsgpack(PythonPackage):
    """MessagePack (de)serializer."""

    homepage = "https://msgpack.org/"
    url      = "https://pypi.io/packages/source/m/msgpack/msgpack-0.6.2.tar.gz"

    version('0.6.2', sha256='ea3c2f859346fcd55fc46e96885301d9c2f7a36d453f5d8f2967840efa1e1830')

    depends_on('py-setuptools', type='build')

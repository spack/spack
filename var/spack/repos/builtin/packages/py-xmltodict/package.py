# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXmltodict(PythonPackage):
    """xmltodict is a Python module that makes working with XML feel like
    you are working with JSON."""

    homepage = "https://github.com/martinblech/xmltodict"
    git      = "https://github.com/martinblech/xmltodict.git"

    version('0.12.0', tag='v0.12.0')
    version('0.11.0', tag='v0.11.0')
    version('0.10.2', tag='v0.10.2')
    version('0.10.1', tag='v0.10.1')
    version('0.10.0', tag='v0.10.0')
    version('0.9.2', tag='v0.9.2')
    version('0.9.1', tag='v0.9.1')
    version('0.9.0', tag='v0.9.0')
    version('0.8.7', tag='v0.8.7')
    version('0.8.6', tag='v0.8.6')
    version('0.8.5', tag='v0.8.5')
    version('0.8.4', tag='v0.8.4')
    version('0.8.3', tag='v0.8.3')
    version('0.8.2', tag='v0.8.2')
    version('0.8.1', tag='v0.8.1')
    version('0.8.0', tag='v0.8.0')
    version('0.7.0', tag='v0.7.0')
    version('0.6.0', tag='v0.6.0')
    version('0.5.1', tag='v0.5.1')
    version('0.5.0', tag='v0.5.0')
    version('0.4.6', tag='v0.4.6')
    version('0.4.5', tag='v0.4.5')
    version('0.4.4', tag='v0.4.4')
    version('0.4.3', tag='v0.4.3')
    version('0.4.2', tag='v0.4.2')
    version('0.4.1', tag='v0.4.1')
    version('0.4.0', tag='v0.4')
    version('0.3.0', tag='v0.3')
    version('0.2.0', tag='v0.2')

    depends_on('py-setuptools', type='build')

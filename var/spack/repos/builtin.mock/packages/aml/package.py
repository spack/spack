# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Aml(AutotoolsPackage):
    """Uses libtool-version, as a build dependency"""
    version('0.1.0', sha256='cc89a8768693f1f11539378b21cdca9f0ce3fc5cb564f9b3e4154a051dcea69b')
    depends_on('libtool-version', type='build')

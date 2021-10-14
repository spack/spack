##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyEfel(PythonPackage):
    """The Electrophys Feature Extract Library (eFEL) allows
    neuroscientists to automatically extract features from time series data
    recorded from neurons (both in vitro and in silico).
    Examples are the action potential width and amplitude in
    voltage traces recorded during whole-cell patch clamp experiments.
    The user of the library provides a set of traces and selects the
    features to be calculated. The library will then extract the requested
    features and return the values to the user."""
    homepage = "https://github.com/BlueBrain/eFEL"
    url = "https://pypi.io/packages/source/e/efel/efel-3.0.80.tar.gz"

    version('4.0.4', sha256='258c506776df609edc799338fd773e78f0f0315fd6f3e2f969478bda401a8894')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type='run')
    depends_on('py-six', type='run')

# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ont-guppy-gpu
#
# You can edit this file again by typing:
#
#     spack edit ont-guppy-gpu
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class OntGuppyGpu(Package):
    """"Local, GPU-accelerated basecalling for Nanopore data"""

    homepage = "https://community.nanoporetech.com/downloads/guppy/release_notes"
    url      = "https://cdn.oxfordnanoportal.com/software/analysis/ont-guppy_6.1.7_linux64.tar.gz"

    version('6.1.7', sha256='c3dd8f8b7567061a155d1921586dd95540410b35b2ccb8a33a463d9db8642711')

    depends_on('cuda@11.0.0:')

    #def install(self, spec, prefix):
    #    make('install')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install minigan
#
# You can edit this file again by typing:
#
#     spack edit minigan
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Minigan(Package):
    """miniGAN is a generative adversarial network code developed as part of the Exascale Computing Project's (ECP) ExaLearn project at Sandia National Laboratories."""

    homepage = "https://github.com/SandiaMLMiniApps/miniGAN"
    url      = "https://github.com/SandiaMLMiniApps/miniGAN/archive/1.0.0.tar.gz"

    version('1.0.0', sha256='ef6d5def9c7040af520acc64b7a8b6c8ec4b7901721b11b0cb25a583ea0c8ae3')

    depends_on('python@3.5.2')
    depends_on('py-torch@1.3.1')
    depends_on('py-numpy')
    depends_on('py-horovod@0.18.0')
    depends_on('py-torchvision')
    depends_on('matplotlib@3.0.0')


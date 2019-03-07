# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PySip(Package):
    """SIP is a tool that makes it very easy to create Python bindings for C
       and C++ libraries."""
    homepage = "http://www.riverbankcomputing.com/software/sip/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/sip/sip-4.16.5/sip-4.16.5.tar.gz"

    version('4.19.13', sha256='e353a7056599bf5fbd5d3ff9842a6ab2ea3cf4e0304a0f925ec5862907c0d15e')
    version('4.16.7', '32abc003980599d33ffd789734de4c36')
    version('4.16.5', '6d01ea966a53e4c7ae5c5e48c40e49e5')

    extends('python')

    def install(self, spec, prefix):
        python('configure.py',
               '--destdir=%s' % site_packages_dir,
               '--bindir=%s' % spec.prefix.bin,
               '--incdir=%s' % python_include_dir,
               '--sipdir=%s' % os.path.join(spec.prefix.share, 'sip'))
        make()
        make('install')

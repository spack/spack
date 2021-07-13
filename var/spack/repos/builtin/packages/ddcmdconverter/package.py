# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install ddcmdconverter
#
# You can edit this file again by typing:
#
#     spack edit ddcmdconverter
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Ddcmdconverter(PythonPackage):
    """ddcMD Converter: a Python tool to convert GROMACS files to ddcMD inputs.."""
        
    homepage = "https://github.com/LLNL/ddcMDconverter"
    url      = "https://github.com/LLNL/ddcMDconverter/archive/refs/tags/v1.0.5.tar.gz"
    git      = "git@github.com:LLNL/ddcMDconverter.git"
    maintainers = ['bhatiaharsh']

    version('1.0.5', sha256='332059215144d9b8b2ec89df64853e96419fcd62d462058635e1369f48ba13f5')
    version('1.0.4',  git='git@github.com:LLNL/ddcMDconverter.git', tag='v1.0.4')
    '''
    # older versions linked to the internal repo
    #version('master', git='ssh://git@cz-bitbucket.llnl.gov:7999/xzr/ddcmdconvertor.git')
    version('1.0.3',  git='ssh://git@cz-bitbucket.llnl.gov:7999/xzr/ddcmdconvertor.git', tag='v1.0.3')
    version('1.0.1.dev0',  git='ssh://git@cz-bitbucket.llnl.gov:7999/xzr/ddcmdconvertor.git', commit='2ad0498dd5e')
    version('1.0.1',  git='ssh://git@cz-bitbucket.llnl.gov:7999/xzr/ddcmdconvertor.git', tag='v1.0.1')
    version('1.0.0',  git='ssh://git@cz-bitbucket.llnl.gov:7999/xzr/ddcmdconvertor.git', tag='v1.0.0')
    '''

    depends_on('py-setuptools')
    depends_on('py-six')
    depends_on('py-numpy')

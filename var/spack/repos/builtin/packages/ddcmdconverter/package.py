# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)



from spack import *


class Ddcmdconverter(PythonPackage):
    """ddcMD Converter: a Python tool to convert GROMACS files to ddcMD inputs.."""
        
    homepage = "https://github.com/LLNL/ddcMDconverter"
    url      = "https://github.com/LLNL/ddcMDconverter/archive/refs/tags/v1.0.5.tar.gz"
    git      = "git@github.com:LLNL/ddcMDconverter.git"

    maintainers = ['XiaohuaZhangLLNL, 'bhatiaharsh']

    version('1.0.5', sha256='332059215144d9b8b2ec89df64853e96419fcd62d462058635e1369f48ba13f5')

    depends_on('py-setuptools')
    depends_on('py-six')
    depends_on('py-numpy')

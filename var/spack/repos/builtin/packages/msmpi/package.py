# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import sys

import spack.build_environment
from spack import *


class Msmpi(Package):
    """A Windows-specced build of MPICH provided directly by
    Microsoft Support Team
    """
    homepage = 'https://www.microsoft.com/en-us/download/default.aspx'
    url = 'https://www.microsoft.com/en-us/download/confirmation.aspx?id=57467'
    maintainers = ['jpopelar']

    version('10.0', sha256='7dae13797627726f67fab9c1d251aec2df9ecd25939984645ec05748bdffd396', extension='exe')

    provides('mpi')
    
    conflicts('platform=linux')
    conflicts('platform=darwin')
    conflicts('platform=cray')

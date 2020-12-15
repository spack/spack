# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os

class Gridsim2d(MakefilePackage):

    git        = "ssh://git@cz-bitbucket.llnl.gov:7999/~tomaso/gridcorr2d.git"
    homepage   = "https://lc.llnl.gov/bitbucket/users/tomaso/repos/gridcorr2d/browse"

    version('master', branch='master')
    version('campaign-3', branch='Campaign-3')
    version('v2020-09-16', tag='v2020-09-16')
    version('v2020-10-01', tag='v2020-10-01')
    version('v2020-10-09', tag='v2020-10-09')
    version('v2020-10-09.2', tag='v2020-10-09.2')
    version('v2020-10-16-summit', tag='v2020-10-16-summit')
    version('v2020-10-23-scaling', tag='v2020-10-23-scaling')  ## Added by tomaso, 2020-10-23
    version('v2020-11-13', tag='v2020-11-13')  ## Added by tomaso, 2020-11-13
    version('v2020-12-04', tag='v2020-12-04')

    depends_on('mpi')
    depends_on('fftw')
    
    def build(self, spec, prefix):
        make('clean')
        make()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('gridsim2dras', prefix.bin)

        with working_dir('c3-test'):
            #mfiles = ['pmfcode.m', 'make_pmf.m', 'interpolate.m', 'pmfsmooth2.m']
            ## Added by tomaso 2020-11-13:
            mfiles = ['run2400hack.cfg','atoms.init','bonds.init', \
                      'cofr_ij_hack_smooth_full.dat','cofk_ij.txt','rep12_pot.dat', \
                      'pmf_RASa_smooth.txt' ,'pmf_RASb_smooth.txt' ,'pmf_RASc_smooth.txt' , \
                      'pmf_mRASa_smooth.txt','pmf_mRASb_smooth.txt','pmf_zRAFa_smooth.txt', \
                      'pmf_mRAFa_smooth.txt','pmf_mRAFb_smooth.txt','pmf_zRASa_smooth.txt', \
                      'pmfcode.m','make_pmf.m','pmfsmooth2.m','interpolate.m']
            mfiles = [] # This is for version v2020-12-04
            for m in mfiles:
                install(m, prefix.bin)


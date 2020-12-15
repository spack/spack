# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Mummi(PythonPackage):
    """FIXME: Put a proper description of your package here."""

    NEW_REPO = True

    # -------------------------------------------------------------------
    if NEW_REPO:
        homepage = "https://code.ornl.gov/bhatiah/mummi"
        git      = "git@code.ornl.gov:bhatiah/mummi.git"
        version('develop', branch='develop')

    else:
        homepage = "https://code.ornl.gov/v33/pilot2-splash-app"
        git      = "git@code.ornl.gov:v33/pilot2-splash-app.git"

        version('0.3b.0', tag='v0.3b.0') #commit='527f44e4a543f0e44daeab5d1375ce8c610eb9a0')
        version('0.2.0', tag='v0.2.0') #commit='372e85318181530731f191b5a48b747f60bfadd2')
        version('develop', branch='develop')
        version('python3', branch='python3')
        version('python3_merged', commit='33ca89df')

        #version('port', branch='port/splash', git='igit@code.ornl.gov:bhatiah/mummi.git')
        #build_directory = 'mummi'
        #version('1.0.1', tag='v1.0.1')
        #version('2014-10-08', commit='9d38cd4e2c94c3cea97d0e2924814acc')
        #version('1.0', 'f43fb8126c138db96b489655914ed2bd5a469412')

    # -------------------------------------------------------------------

    extends('python@3.7.3')

    # build dependencies
    depends_on('cmake@3.14.5',  type='build')
    depends_on('swig@3.0.12',  type='build')

    # generic
    depends_on('py-numpy@1.16.4')
    depends_on('py-scipy@1.3.0')

    '''
    # ml
    depends_on('cudnn@7.5.1-10.1-ppc64le')			      	        #TODO: these settings are for powerpc
    depends_on('faiss@1.5.3 +python')
    #depends_on('py-theano@1.0.4 +cuda ^cudnn@7.5.1-10.1-ppc64le')	#TODO: these settings are for powerpc
    #depends_on('py-theano@1.0.4 +cuda')
    depends_on('py-keras@2.2.4')
    #depends_on('py-h5py@2.9.0~mpi ^hdf5~mpi+hl')
    '''
    # analysis
    depends_on('talass@process-statistics')
    depends_on('py-scikit-learn')
    depends_on('py-matplotlib@3.0.2')

    # macro
    #depends_on('gridsim2d@v2020-10-09.2')

    # cg and aa
    depends_on('ddcmdconverter@1.0.4')
    depends_on('py-mdanalysis-mummi@mda_1.0.1_ddcmd')
    depends_on('dssp@3.1.4')
    depends_on('py-parmed@3.2.0')
    depends_on('py-tqdm@4.36.1')

    #depends_on('fftw@3.3.8 +mpi~openmp~pfft_patches precision=double,float')
    depends_on('gromacs@2019.06 +cuda')

    # databroker
    #depends_on('databroker@0.7.1 +python')

    # flux
    #depends_on('flux-sched@0.11.0 +cuda')
    #depends_on('py-maestrowf')

    # shared daemon
    depends_on('py-cryptography@2.3.1')

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mummi(PythonPackage):
    """The MuMMI framework facilitates the coordination of massively parallel 
    multiscale simulations using a machine learning driven sampling approach."

    homepage = "https://github.com/mummi-framework"
    git      = "git@github.com:mummi-framework/mummi-ras.git"
    version('main', branch='main')

    maintainers = ['bhatiaharsh']


    # -------------------------------------------------------------------
    extends('python@3.7:')

    # build dependencies
    depends_on('cmake', type='build')
    depends_on('swig', type='build')

    # generic
    depends_on('py-numpy')
    depends_on('py-scipy')

    # ml
    depends_on('faiss@1.6.3 +cuda+python')
    depends_on('py-theano@1.0.4 ~cuda')
    depends_on('py-h5py~mpi ^hdf5~mpi')

    # analysis
    depends_on('talass@process-statistics')
    depends_on('py-scikit-learn')
    depends_on('py-matplotlib@3:')

    # cg and aa
    depends_on('ddcmdconverter@1.0.5')
    depends_on('py-mdanalysis-mummi@mda_1.0.4_ddcmd')

    depends_on('dssp@3.1.4')
    depends_on('py-parmed@3.2.0')

    depends_on('fftw@3.3.8 +mpi~openmp~pfft_patches precision=double,float')
    depends_on('gromacs@2019.6 +blas+lapack~cuda~mpi~double build_type=Release')

    # databroker
    depends_on('redis')
    depends_on('py-redis')

    # flux
    depends_on('flux-sched@0.11.0 +cuda')
    depends_on('py-maestrowf')

    # shared daemon
    depends_on('py-cryptography')


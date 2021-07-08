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
#     spack install py-mdanalysis-mummi
#
# You can edit this file again by typing:
#
#     spack edit py-mdanalysis-mummi
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyMdanalysisMummi(PythonPackage):
    """MDAnalysis-MuMMI is the customization of MDAnalysis for MuMMI to 
    support DDCMD and DDCMD-TAR file formats.
    
    MDAnalysis is a Python toolkit to analyze molecular dynamics
    trajectories generated by a wide range of popular simulation
    packages including DL_Poly, CHARMM, Amber, NAMD, LAMMPS, and
    Gromacs. (See the lists of supported trajectory formats and
    topology formats.)"""

    homepage = "https://github.com/XiaohuaZhangLLNL/mdanalysis"

    version('mda_1.0.1_ddcmd', tag='mda_1.0.1_ddcmd', git='git@github.com:XiaohuaZhangLLNL/mdanalysis.git')
    version('mda_1.0.0_ddcmd', tag='mda_1.0.0_ddcmd', git='git@github.com:XiaohuaZhangLLNL/mdanalysis.git')
    version('mda_1.0.3_ddcmd', tag='mda_1.0.3_ddcmd', git='git@github.com:XiaohuaZhangLLNL/mdanalysis.git')
    version('mda_1.0.4_ddcmd', tag='mda_1.0.4_ddcmd', git='git@github.com:XiaohuaZhangLLNL/mdanalysis.git')

    # removed this because their deps are diff
    # need to consult with py-mdanalysis if these are needed
    #version('mda0.19.2_ddcmd_lessmem', '72c970b64fa13d9a15dd683da833af55', url="https://github.com/XiaohuaZhangLLNL/mdanalysis/archive/mda0.19.2_ddcmd_lessmem.tar.gz")
    #version('mda0.19.2_with_ddcmd',    'f9d21c12e064aa05f6031256351a1fc7', url="https://github.com/XiaohuaZhangLLNL/mdanalysis/archive/mda0.19.2_with_ddcmd.tar.gz")

    build_directory = 'package'

    depends_on('python@3:')
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.16:', type='build')

    depends_on('py-numpy@1.5.0:', type=('build', 'run'))
    depends_on('py-scipy@1.0.0:', type=('build', 'run'))

    depends_on('py-six@1.4.0:',      type=('build', 'run'))
    depends_on('py-networkx@1.0:',   type=('build', 'run'))
    depends_on('py-biopython@1.71:', type=('build', 'run'))

    depends_on('py-gsd@1.4.0:',         type=('build', 'run'))
    depends_on('py-mmtf-python@1.0.0:', type=('build', 'run'))
    depends_on('py-mock',               type=('build', 'run'))
    depends_on('py-tqdm@4.43.0:',       type=('build', 'run'))
    depends_on('py-joblib@0.12:',       type=('build', 'run'))
    depends_on('py-griddataformats@0.4:', type=('build', 'run'))

    depends_on('py-matplotlib@1.5.1:', type=('build', 'run'))
    depends_on('py-seaborn', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))

    #depends_on('py-netcdf4@1.0:', when='+amber', type=('build', 'run'))
    #depends_on('hdf5', when='+amber', type=('run'))


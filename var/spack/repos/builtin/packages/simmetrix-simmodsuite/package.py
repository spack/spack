##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os
import sys
from distutils import dir_util

def simmodsuite_releases():
  releases = [
    {
      'version': '12.0-180606dev',
      'components': {
         'mscore'          : ['82640540d1ad80efd403d7768c80e9f8', 'base'],
         'fdcore'          : ['24f27ada05068ccd19a678ed6120f8b0', 'base'],
         'gmcore'          : ['8a70d159613c1834340347be42678566', 'base'],
         'msadapt'         : ['edae9c50f4e8b09a24bca9b11e0f1e52', 'base'],
         'aciskrnl'        : ['901c8ea87c4a3205f76ddd4dadf6da69', 'acis'],
         'psint'           : ['82d88db82bc9bc8c9f1e1091495f9339', 'parasolid'],
         'pskrnl'          : ['32142b23db0656cf603b020788391824', 'parasolid'],
         'discrete'        : ['ab145a80c7ebc7724816f692f732c901', 'discrete'],
         'gmabstract'      : ['5bc2dd69ef992eef3e557fb59c1a6915', 'abstract'],
         'gmadv'           : ['51c1036e583fd7a14ee4ebb8301b86ac', 'advmodel'],
         'gmimport'        : ['d8c93a3f0ba2bf6c9574c97efb21338a', 'import'],
         'gmvoxel'         : ['db00665dcba8c017fd4fb102657e4ccb', 'voxel'],
         'msadv'           : ['4ea584436165ca5431a3f0ba0bcd4210', 'adv'],
         'msparalleladapt' : ['94e617a1f361ef22a6803bde050beb55', 'paralleladapt'],
         'msparallelmesh'  : ['72e4bb6d60b00c82d39642f75ed4a665', 'parallelmesh']
      },
      'docs': {
         'FieldSim'            : ['7eee54361cce486b268a8fd78e8eddf4', 'base'],
         'GeomSim'             : ['a0eca9ec56a31682dc817f6aa6d73823', 'base'],
         'MeshSim'             : ['4c360a6ad6f47d674d08f84cdd272df4', 'base'],
         'MeshSimAdapt'        : ['d6f3f06a1a43b5003fd302dd219a55df', 'base'],
         'GeomSimAcis'         : ['24ac7f8516a65ce487c2b31d39dbe407', 'acis'],
         'GeomSimParasolid'    : ['b1914bbcaa2d91808eea364fdaba9f4a', 'parasolid'],
         'GeomSimDiscrete'     : ['cee3f1e7dc0b3aeafeeafcb59eecbf40', 'discrete'],
         'GeomSimAbstract'     : ['e3c02ab678c6aeada01c83f059e575bb', 'abstract'],
         'GeomSimAdvanced'     : ['fabf3b53dce09a5082b084e26e8a80ef', 'advmodel'],
         'GeomSimImport'       : ['16cc4bad9e6e84d97583ac84e5968954', 'import'],
         'GeomSimVoxel'        : ['d9e10e2cb89e215534c2c04538994233', 'voxel'],
         'MeshSimAdvanced'     : ['2623d6edce07103ebbac4b7e9b38332d', 'adv'],
         'ParallelMeshSimAdapt': ['f82a8f60760503f524714634ffe85cfb', 'paralleladapt'],
         'ParallelMeshSim'     : ['17596e3618f91c8d4a8be750051271a5', 'parallelmesh']
      }
    }
  ]
  return releases

def simmetrix_getKernel():
  """only supporting the linux libraries"""
  return "linux"

def simmetrix_getWordSz():
  """only supporting 64b libraries"""
  return "64"

def simmetrix_makeComponentUrl(name):
  """only supporting the linux libraries"""
  prefix="file://{0}/".format(os.getcwd())
  suffix="-"+simmetrix_getKernel()+simmetrix_getWordSz()+'.tgz'
  return prefix+name+suffix

def simmetrix_makeDocUrl(name):
  """doc zip files are not os/arch specific"""
  prefix="file://{0}/".format(os.getcwd())
  suffix='.zip'
  return prefix+name+suffix

def simmetrix_resource(name,url,md5,condition):
  # The tarballs/zips each have the same directory structure.  Because of
  # this, and the bug in spack described here:
  # https://github.com/spack/spack/pull/3553#issuecomment-391424244
  # , they cannot be expanded into the source root directory.
  # Once this is fixed the 'destination=name' argument can be removed.
  resource(
    name=name,
    url=url,
    md5=md5,
    destination=name,
    when=condition
  )


def simmetrix_copytree(src, dst):
  dir_util.copy_tree(src,dst)

class SimmetrixSimmodsuite(Package):
    """Simmetrix' Simulation Modeling Suite is a set of component software
    toolkits that allow developers to easily implement geometry-based simulation
    applications.  
    Each component of the Simulation Modeling Suite is designed to address
    specific capabilities:
    | MeshSim - automatic mesh generation
    | FieldSim - simulation data management 
    | GeomSim - direct, untranslated access to geometry from a wide variety of sources
    """

    homepage = "http://www.simmetrix.com/products/SimulationModelingSuite/main.html"

    license_required = True
    license_vars     = ['SIM_LICENSE_FILE']

    variant('rhel7', default=True, description='libraries built on RedHat 7 Enterprise Linux')
    variant('rhel6', default=False, description='libraries built on RedHat 6 Enterprise Linux')
    variant('base', default=True, description='enable the base components')
    variant('advmodel', default=False, description='enable advaced modeling')
    variant('abstract', default=False, description='enable abstract modeling')
    variant('voxel', default=False, description='enable voxel modeling')
    variant('discrete', default=False, description='enable discrete modeling')
    variant('acis', default=False, description='enable acis modeling')
    variant('parasolid', default=False, description='enable parasolid modeling')
    variant('granite', default=False, description='enable granite modeling')
    variant('import', default=False, description='enable import modeling')
    variant('adv', default=False, description='enable advanced meshing')
    variant('parallelmesh', default=False, description='enable parallel meshing')
    variant('paralleladapt', default=False, description='enable parallel adaptation')

    depends_on('mpi')
  
    releases=simmodsuite_releases()
    for release in releases:
      # define the version using the mscore tarball
      simVersion=release['version']
      mainPkgName='mscore'
      url=simmetrix_makeComponentUrl(mainPkgName)
      md5=release['components'][mainPkgName][0]
      version(simVersion, md5=md5, url=url)
      # define resources for the other tarballs
      for name, atts in release['components'].items():
        # skip the tarball used for the version(...) call
        if name is 'mscore':
          continue  
        md5=atts[0]
        feature=atts[1]
        url=simmetrix_makeComponentUrl(name)
        condition="@{0}+{1}".format(simVersion,feature)
        simmetrix_resource(name,url,md5,condition)
      # define resources for the document zip files
      for name, atts in release['docs'].items():
        md5=atts[0]
        feature=atts[1]
        url=simmetrix_makeDocUrl(name)
        condition="@{0}+{1}".format(simVersion,feature)
        simmetrix_resource(name,url,md5,condition)

    def install(self, spec, prefix):
      source_path = self.stage.source_path
      for release in simmodsuite_releases():
        simVersion=release['version']
        if simVersion == spec.version.string:
          for name, atts in release['components'].items():
            feature=atts[1]
            if '+'+feature in spec:
              if name is 'mscore':
                simmetrix_copytree(join_path(source_path,'lib'),prefix.lib)
                simmetrix_copytree(join_path(source_path,'include'),prefix.include)
              else:
                path=join_path(source_path,name,self.version.string)
                simmetrix_copytree(path,prefix)
          for name, atts in release['docs'].items():
            feature=atts[1]
            if '+'+feature in spec:
              path=join_path(source_path,name,self.version.string)
              simmetrix_copytree(path,prefix)

      workdir=join_path(prefix,'code','PartitionWrapper')
      if '+parallelmesh' in spec:
        with working_dir(workdir):
          mpi_id=spec['mpi'].name+spec['mpi'].version.string
          make("-f", "Makefile.custom",
              "CC=%s" % spec['mpi'].mpicc,
              "CXX=%s" % spec['mpi'].mpicxx,
              "PARALLEL=%s" % mpi_id,
              "PQUAL=-%s" % mpi_id,
              "OPTFLAGS=-O2 -DNDEBUG -fPIC")
          wrapperLibPath=join_path(workdir,
              'lib','libSimPartitionWrapper-'+mpi_id+'.a')
          if '+rhel7' in spec:
            install(wrapperLibPath, join_path(prefix.lib,'x64_rhel7_gcc48'))
          if '+rhel6' in spec:
            install(wrapperLibPath, join_path(prefix.lib,'x64_rhel6_gcc44'))

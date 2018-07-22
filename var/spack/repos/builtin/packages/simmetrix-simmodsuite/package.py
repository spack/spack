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
from distutils import dir_util


def simmodsuite_releases():
    releases = [
    {
      'version': '12.0-180713',
      'components': {
           'fdcore': ['f94e6811e8a3b8b5561f1977f8b32654', 'base'],
           'gmvoxel': ['135b9345a41b54938823a5e6eafba306', 'voxel'],
           'aciskrnl': ['f9ddc559bd1468999e64941dd98bd63f', 'acis'],
           'msadapt': ['102ba29161961e659574e1bb141e5955', 'base'],
           'gmimport': ['1f11765282d32eccb2267582e9471112', 'import'],
           'discrete': ['a46af8f50e8eee5601011270d50bd70f', 'discrete'],
           'mscore': ['af56e845f30ab50ac37834b9af0c60ef', 'base'],
           'gmadv': ['e9641e24c934e9ad879fa72a714e4876', 'advmodel'],
           'msparalleladapt': ['cd1a7aaee0534da96db0a13b8cbd708e', 'paralleladapt'],
           'gmcore': ['6b3082559c4b72ea1679050055b38094', 'base'],
           'pskrnl': ['6565bfbbe5d71a0140edd700f1efa740', 'parasolid'],
           'msparallelmesh': ['655348b93ffa39424e35d1a5de393e26', 'parallelmesh'],
           'msadv': ['469045a87c48bab75a26d58dc389caa6', 'adv'],
           'gmabstract': ['0c9cebf2e45a80e48693990b3eda611d', 'abstract'],
           'psint': ['5f3260aa3f8daac06a3560113809c79f', 'parasolid'],
        },
        'docs': {
           'GeomSimSolidWorks': ['e44a532c5911278f95bfc141476cbd40', 'parasolid'],
           'MeshSim': ['b4b9e3d0022117c46878c69be3bb7bed', 'base'],
           'MeshSimAdapt': ['2eaef5ff82571822d976dc1844e59b28', 'base'],
           'GeomSimProe': ['7b95bbf5946c3bc4c701dfa166fd2ae9', 'granite'],
           'GeomSimAdvanced': ['e501e90d88f16ba58ffd01dcd1747300', 'advmodel'],
           'ParallelMeshSim': ['c193f9cc545ad72275fa6fa21f02a51b', 'parallelmesh'],
           'GeomSimVoxel': ['2637412c0cb5755abe284fb3281e7caf', 'voxel'],
           'GeomSimAcis': ['9818c2b84e2473cfdcc2c49bf00887e3', 'acis'],
           'ParallelMeshSimAdapt': ['22a40ddc8722a5556d0c94f84b2aa5b9', 'paralleladapt'],
           'GeomSimImport': ['470048d8a0bfbe2fe1557ddeb7801ab0', 'import'],
           'GeomSim': ['fbda330d478c21f98df9b1f4f8e4fd9c', 'base'],
           'GeomSimAbstract': ['dfe7cf16119e699aa1714159629bf8ba', 'abstract'],
           'GeomSimParasolid': ['c385375cec376582c5dc3e67669cd502', 'parasolid'],
           'FieldSim': ['9a2aa744bf76975329f8e119d406e114', 'base'],
           'GeomSimDiscrete': ['c395c01a42d1fe4f6c412df3eab6c944', 'discrete'],
        }
    },
    {
      'version': '12.0-180606dev',
      'components': {
         'mscore': ['82640540d1ad80efd403d7768c80e9f8', 'base'],
         'fdcore': ['24f27ada05068ccd19a678ed6120f8b0', 'base'],
         'gmcore': ['8a70d159613c1834340347be42678566', 'base'],
         'msadapt': ['edae9c50f4e8b09a24bca9b11e0f1e52', 'base'],
         'aciskrnl': ['901c8ea87c4a3205f76ddd4dadf6da69', 'acis'],
         'psint': ['82d88db82bc9bc8c9f1e1091495f9339', 'parasolid'],
         'pskrnl': ['32142b23db0656cf603b020788391824', 'parasolid'],
         'discrete': ['ab145a80c7ebc7724816f692f732c901', 'discrete'],
         'gmabstract': ['5bc2dd69ef992eef3e557fb59c1a6915', 'abstract'],
         'gmadv': ['51c1036e583fd7a14ee4ebb8301b86ac', 'advmodel'],
         'gmimport': ['d8c93a3f0ba2bf6c9574c97efb21338a', 'import'],
         'gmvoxel': ['db00665dcba8c017fd4fb102657e4ccb', 'voxel'],
         'msadv': ['4ea584436165ca5431a3f0ba0bcd4210', 'adv'],
         'msparalleladapt': ['94e617a1f361ef22a6803bde050beb55', 'paralleladapt'],
         'msparallelmesh': ['72e4bb6d60b00c82d39642f75ed4a665', 'parallelmesh']
      },
      'docs': {
         'FieldSim': ['7eee54361cce486b268a8fd78e8eddf4', 'base'],
         'GeomSim': ['a0eca9ec56a31682dc817f6aa6d73823', 'base'],
         'MeshSim': ['4c360a6ad6f47d674d08f84cdd272df4', 'base'],
         'MeshSimAdapt': ['d6f3f06a1a43b5003fd302dd219a55df', 'base'],
         'GeomSimAcis': ['24ac7f8516a65ce487c2b31d39dbe407', 'acis'],
         'GeomSimParasolid': ['b1914bbcaa2d91808eea364fdaba9f4a', 'parasolid'],
         'GeomSimDiscrete': ['cee3f1e7dc0b3aeafeeafcb59eecbf40', 'discrete'],
         'GeomSimAbstract': ['e3c02ab678c6aeada01c83f059e575bb', 'abstract'],
         'GeomSimAdvanced': ['fabf3b53dce09a5082b084e26e8a80ef', 'advmodel'],
         'GeomSimImport': ['16cc4bad9e6e84d97583ac84e5968954', 'import'],
         'GeomSimVoxel': ['d9e10e2cb89e215534c2c04538994233', 'voxel'],
         'MeshSimAdvanced': ['2623d6edce07103ebbac4b7e9b38332d', 'adv'],
         'ParallelMeshSimAdapt': ['f82a8f60760503f524714634ffe85cfb', 'paralleladapt'],
         'ParallelMeshSim': ['17596e3618f91c8d4a8be750051271a5', 'parallelmesh']
      }
    },
    {
      'version': '11.0-180619',
      'components': {
         'gmvoxel': ['b3fef983a5a23b9cdc17d69dcd4d7689', 'voxel'],
         'msadapt': ['b762d2429bdccf83085f9766beba8799', 'base'],
         'mscore': ['ef694c4b928893bb9021eec8c9273230', 'base'],
         'fdcore': ['1f9bb2ff299e323ec7cbafc3c633f481', 'base'],
         'msadv': ['c625d3aaa59db0977cef36c887f902ca', 'adv'],
         'psint': ['6e52c7be443f8b0fffc0e8489d6e7965', 'parasolid'],
         'aciskrnl': ['201a136fb8f5aea6799db630548acdc0', 'acis'],
         'discrete': ['289c21baf8690b5cdda3f5499f97fda0', 'discrete'],
         'gmimport': ['7b5c9b1a75dc9eb283dce80e5e0747eb', 'import'],
         'gmadv': ['1d1a01752efc3d2c38ec6f2e9aa8727b', 'advmodel'],
         'msparallelmesh': ['fc014dab94e5e1dcbc82db68dd99262c', 'parallelmesh'],
         'gmabstract': ['249ca5620801439bff8cec6d7f9dd0d0', 'abstract'],
         'gmcore': ['1b6b3874f5ed4027681a27a6a7c9369c', 'base'],
         'pskrnl': ['6ea83d632484bdd0a05511e66fe5fa67', 'parasolid'],
         'msparalleladapt': ['d8882e5cb680805f1174df5ceea11414', 'paralleladapt'],
      },
      'docs': {
         'MeshSimAdv': ['f5c2c0f58aeaeebbe04527d681386eeb', 'adv'],
         'GeomSimAcis': ['9da1c3486fac8ed7deb5d65f163cd4e0', 'acis'],
         'GeomSimImport': ['828d1db75cad7d8920471a31fb777c4b', 'import'],
         'GeomSimSolidWorks': ['4fcdc8a9a73e1b2a65d77d6875bc5fc9', 'parasolid'],
         'ParallelMeshSimAdapt': ['f11d765df98175c806a67a8fbc0aaf5a', 'paralleladapt'],
         'GeomSimVoxel': ['0a20ab050ae67a9e7d8c10a3ca6d33b9', 'voxel'],
         'GeomSim': ['3d9c30616475636f4d2c0da85684274c', 'base'],
         'GeomSimAdvanced': ['d178a1ad442147b54d6eeb00480506dc', 'advmodel'],
         'MeshSimAdapt': ['ea2272dd9577f8d52fd749efc33e9c15', 'base'],
         'ParallelMeshSim': ['2729d1a03764a1fe015eac881c4ca73a', 'parallelmesh'],
         'MeshSim': ['ea2246f55e1fcf732355afb832252b0c', 'base'],
         'FieldSim': ['aeca95adfa92710bc6b731108124d961', 'base'],
         'GeomSimParasolid': ['59680124b20a45fe3122f364be485398', 'parasolid'],
         'GeomSimAbstract': ['dfe2559a7d1fb837a39afd9b24f12a26', 'abstract'],
         'GeomSimDiscrete': ['233fa79ef98483ad69d45647ec409e48', 'discrete'],
         'GeomSimProe': ['b2587521678eb121384d22d686b5456d', 'granite'],
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


def simmetrix_getLibDir(os):
    osLibDir = {'rhel6': 'x64_rhel6_gcc44',
                'rhel7': 'x64_rhel7_gcc48'}
    return osLibDir[os]


def simmetrix_makeComponentUrl(name):
    """only supporting the linux libraries"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = "-" + simmetrix_getKernel() + simmetrix_getWordSz() + '.tgz'
    return prefix + name + suffix


def simmetrix_makeDocUrl(name):
    """doc zip files are not os/arch specific"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = '.zip'
    return prefix + name + suffix


def simmetrix_setKernelCMakePrefixPath(spec, path, env):
    if '+acis' in spec:
        env.append_path('CMAKE_PREFIX_PATH', join_path(path, 'acisKrnl'))
    if '+parasolid' in spec:
        env.append_path('CMAKE_PREFIX_PATH', join_path(path, 'psKrnl'))


def simmetrix_resource(name, url, md5, condition):
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
    dir_util.copy_tree(src, dst)


class SimmetrixSimmodsuite(Package):
    """Simmetrix' Simulation Modeling Suite is a set of component software
    toolkits that allow developers to easily implement geometry-based
    simulation applications.
    Each component of the Simulation Modeling Suite is designed to address
    specific capabilities:
    | MeshSim - automatic mesh generation
    | FieldSim - simulation data management
    | GeomSim - direct, untranslated access to geometry from a wide variety
    of sources
    """

    homepage = "http://www.simmetrix.com/products/SimulationModelingSuite/main.html"

    license_required = True
    license_vars     = ['SIM_LICENSE_FILE']

    variant('sim_os', default='rhel7', values=('rhel7', 'rhel6'),
      description='installs libraries built on RedHat 6 or 7 Enterprise Linux')
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

    releases = simmodsuite_releases()
    for release in releases:
        # define the version using the mscore tarball
        simVersion = release['version']
        mainPkgName = 'mscore'
        url = simmetrix_makeComponentUrl(mainPkgName)
        md5 = release['components'][mainPkgName][0]
        version(simVersion, md5=md5, url=url)
        # define resources for the other tarballs
        for name, atts in release['components'].items():
            # skip the tarball used for the version(...) call
            if name is 'mscore':
                continue
            md5 = atts[0]
            feature = atts[1]
            url = simmetrix_makeComponentUrl(name)
            condition = "@{0}+{1}".format(simVersion, feature)
            simmetrix_resource(name, url, md5, condition)
        # define resources for the document zip files
        for name, atts in release['docs'].items():
            md5 = atts[0]
            feature = atts[1]
            url = simmetrix_makeDocUrl(name)
            condition = "@{0}+{1}".format(simVersion, feature)
            simmetrix_resource(name, url, md5, condition)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if self.spec.satisfies('sim_os=rhel7'):
            oslib = simmetrix_getLibDir('rhel7')
            archlib = join_path(prefix.lib, oslib)
            spack_env.append_path('CMAKE_PREFIX_PATH', archlib)
            simmetrix_setKernelCMakePrefixPath(self.spec, archlib, spack_env)
        elif self.spec.satisfies('sim_os=rhel6'):
            oslib = simmetrix_getLibDir('rhel6')
            archlib = join_path(prefix.lib, oslib)
            spack_env.append_path('CMAKE_PREFIX_PATH', archlib)
            simmetrix_setKernelCMakePrefixPath(self.spec, archlib, spack_env)

    def setup_environment(self, spack_env, run_env):
        if self.spec.satisfies('sim_os=rhel7'):
            oslib = simmetrix_getLibDir('rhel7')
            archlib = join_path(prefix.lib, oslib)
            run_env.append_path('CMAKE_PREFIX_PATH', archlib)
            simmetrix_setKernelCMakePrefixPath(self.spec, archlib, run_env)
        elif self.spec.satisfies('sim_os=rhel6'):
            oslib = simmetrix_getLibDir('rhel6')
            archlib = join_path(prefix.lib, oslib)
            run_env.append_path('CMAKE_PREFIX_PATH', archlib)
            simmetrix_setKernelCMakePrefixPath(self.spec, archlib, run_env)

    def install(self, spec, prefix):
        source_path = self.stage.source_path
        for release in simmodsuite_releases():
            simVersion = release['version']
            if simVersion != spec.version.string:
                continue
            for name, atts in release['components'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    if name is 'mscore':
                        simmetrix_copytree(
                            join_path(source_path, 'lib'),
                            prefix.lib)
                        simmetrix_copytree(
                            join_path(source_path, 'include'),
                            prefix.include)
                    else:
                        path = join_path(
                            source_path,
                            name,
                            self.version.string)
                        simmetrix_copytree(path, prefix)
            for name, atts in release['docs'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    path = join_path(
                        source_path,
                        name,
                        self.version.string)
                    simmetrix_copytree(path, prefix)

        workdir = join_path(prefix, 'code', 'PartitionWrapper')
        if '+parallelmesh' in spec:
            with working_dir(workdir):
                mpi_id = spec['mpi'].name + spec['mpi'].version.string
                # build the wrapper lib
                make("-f", "Makefile.custom",
                     "CC=%s" % spec['mpi'].mpicc,
                     "CXX=%s" % spec['mpi'].mpicxx,
                     "PARALLEL=%s" % mpi_id,
                     "PQUAL=-%s" % mpi_id,
                     "OPTFLAGS=-O2 -DNDEBUG -fPIC")
                libname = 'libSimPartitionWrapper-' + mpi_id + '.a'
                wrapperLibPath = join_path(workdir, 'lib', libname)
                if spec.satisfies('sim_os=rhel7'):
                    osdir = simmetrix_getLibDir('rhel7')
                    install(wrapperLibPath, join_path(prefix.lib, osdir))
                elif spec.satisfies('sim_os=rhel6'):
                    osdir = simmetrix_getLibDir('rhel6')
                    install(wrapperLibPath, join_path(prefix.lib, osdir))

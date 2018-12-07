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


def simmodsuite_releases():
    releases = [
    {
      'version': '12.0-180922',
      'components': {
           'gmabstract': ['7ad5e9ade43fcd5fd8e6db0ad228db67', 'abstract'],
           'discrete': ['9dcd0e815a0beaf1a5f77a68184fce5e', 'discrete'],
           'gmadv': ['2a25ec4ef95af9e8d0b2f316d55448fa', 'advmodel'],
           'gmimport': ['5dbfab5fefa0752104893c425e13c596', 'import'],
           'pskrnl': ['94af5b91ee45694a9f61e75aec47ae41', 'parasolid'],
           'aciskrnl': ['5fcb24da969ba59afae22351f3dc8f16', 'acis'],
           'gmcore': ['10538628bd9bacc10485978ab30ea2c9', 'base'],
           'msparallelmesh': ['20f5074034e843076524471f90c26a2d', 'parallelmesh'],
           'fdcore': ['81d696d051ade4eb63d4eb5a905de52c', 'base'],
           'mscore': ['456b34253d14ebe80d34c32ffef16978', 'base'],
           'msadapt': ['bd07fb5638c3af0ace93542afb1d5259', 'base'],
           'gmvoxel': ['8dfd0f20ef722fdc9fd7816ed0870a3c', 'voxel'],
           'msparalleladapt': ['aac2316212e3f8b20c67661c8f9ceff4', 'paralleladapt'],
           'msadv': ['42b4d19eb4fcec02e694840328955f49', 'adv'],
           'psint': ['af2e190a9fc8663add1b0400f6e8ebf3', 'parasolid'],
      },
      'docs': {
           'FieldSim': ['be82e9c4f3767b476fb08564184a1e06', 'base'],
           'MeshSimAdapt': ['3ff2955b99c9eb93b893a768af1deaf4', 'base'],
           'ParallelMeshSim': ['c5206a068db7329c29c1abc3b802395e', 'parallelmesh'],
           'GeomSimDiscrete': ['09ed96538a5849d642374c5394ec6984', 'discrete'],
           'GeomSimAbstract': ['9a3883bc456903b8003a69ee23816a1a', 'abstract'],
           'GeomSim': ['9511d3503f2934ab2a033ce485951b32', 'base'],
           'ParallelMeshSimAdapt': ['a3a4a416d62ab17c7370694507805e85', 'paralleladapt'],
           'GeomSimAcis': ['055bf404cb0c0d19c916ab463fb6e250', 'acis'],
           'GeomSimSolidWorks': ['14376a23c3066627455a549df493c135', 'parasolid'],
           'GeomSimProe': ['d070d863da26b27ae6cba11fa2896484', 'granite'],
           'MeshSim': ['cdaffaa22f5909ef0a373dd9936b7fb1', 'base'],
           'GeomSimParasolid': ['60fa6fb7dde2c133388bc688ec14b344', 'parasolid'],
           'GeomSimVoxel': ['bfbd55e18a67f58dadf3b9d62adc46bc', 'voxel'],
           'GeomSimAdvanced': ['9fa46cf586bf42eac354bf642484e2e7', 'advmodel'],
           'GeomSimImport': ['5f27fe06309748b8f4aa66abed0733d2', 'import'],
      }
    },
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


def simmetrix_makecomponenturl(name):
    """only supporting the linux libraries"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = "-" + "linux64.tgz"
    return prefix + name + suffix


def simmetrix_makedocurl(name):
    """doc zip files are not os/arch specific"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = '.zip'
    return prefix + name + suffix


def simmetrix_setkernelcmakeprefixpath(spec, path, env):
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

    oslib = 'x64_rhel7_gcc48'

    releases = simmodsuite_releases()
    for release in releases:
        # define the version using the mscore tarball
        simVersion = release['version']
        mainPkgName = 'mscore'
        url = simmetrix_makecomponenturl(mainPkgName)
        md5 = release['components'][mainPkgName][0]
        version(simVersion, md5=md5, url=url)
        # define resources for the other tarballs
        for name, atts in release['components'].items():
            # skip the tarball used for the version(...) call
            if name is 'mscore':
                continue
            md5 = atts[0]
            feature = atts[1]
            url = simmetrix_makecomponenturl(name)
            condition = "@{0}+{1}".format(simVersion, feature)
            simmetrix_resource(name, url, md5, condition)
        # define resources for the document zip files
        for name, atts in release['docs'].items():
            md5 = atts[0]
            feature = atts[1]
            url = simmetrix_makedocurl(name)
            condition = "@{0}+{1}".format(simVersion, feature)
            simmetrix_resource(name, url, md5, condition)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        archlib = join_path(prefix.lib, self.oslib)
        spack_env.append_path('CMAKE_PREFIX_PATH', archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, spack_env)

    def setup_environment(self, spack_env, run_env):
        archlib = join_path(prefix.lib, self.oslib)
        run_env.append_path('CMAKE_PREFIX_PATH', archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, run_env)

    def install(self, spec, prefix):
        if not spec.satisfies('platform=linux'):
            raise InstallError('Only the linux platform is supported')
        source_path = self.stage.source_path
        for release in simmodsuite_releases():
            simversion = release['version']
            if simversion != spec.version.string:
                continue
            for name, atts in release['components'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    if name is 'mscore':
                        install_tree(join_path(source_path, 'lib'), prefix.lib)
                        install_tree(
                            join_path(source_path, 'include'),
                            prefix.include)
                    else:
                        path = join_path(
                            source_path,
                            name,
                            self.version.string)
                        install_tree(path, prefix)
            for name, atts in release['docs'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    path = join_path(
                        source_path,
                        name,
                        self.version.string)
                    install_tree(path, prefix)

        workdir = prefix.code.PartitionWrapper
        if '+parallelmesh' in spec:
            with working_dir(workdir):
                mpi_id = spec['mpi'].name + spec['mpi'].version.string
                # build the wrapper lib
                make("-f", "Makefile.custom",
                     "CC=%s" % spec['mpi'].mpicc,
                     "CXX=%s" % spec['mpi'].mpicxx,
                     "PARALLEL=%s" % mpi_id,
                     "PQUAL=-%s" % mpi_id,
                     "OPTFLAGS=-O2 -DNDEBUG " + self.compiler.pic_flag)
                libname = 'libSimPartitionWrapper-' + mpi_id + '.a'
                wrapperlibpath = join_path(workdir, 'lib', libname)
                install(wrapperlibpath, join_path(prefix.lib, self.oslib))

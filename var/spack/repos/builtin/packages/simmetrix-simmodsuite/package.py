# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


def simmodsuite_releases():
    releases = [
    {
        'version': '12.0-181124',
        'components': {
           'msadv': ['266977643de96937c44c9fb712393949', 'adv'],
           'psint': ['308a9da4ebee34a35c8a99b0f1a554f0', 'parasolid'],
           'fdcore': ['317e7fe2d8178b3d95f62b5cfaa8a5b7', 'base'],
           'mscore': ['474f6af30bd624f541199822f0fc4692', 'base'],
           'pskrnl': ['69ebea229c7722d69a733a2e49a468ac', 'parasolid'],
           'msparallelmesh': ['67d121846a982f9727350593f559079d', 'parallelmesh'],
           'gmcore': ['065fef92ce37661c194555d965bd00c3', 'base'],
           'msparalleladapt': ['7b8205dda0145df7f209a2c73cfbbd24', 'paralleladapt'],
           'gmadv': ['36f25932e694c00107f8d032a26554c2', 'advmodel'],
           'aciskrnl': ['a54ec6e79029f18e4d0126f9b83a8a72', 'acis'],
           'gmimport': ['d9712c063bc55c4cf0c4d6f02ccd6bb9', 'import'],
           'discrete': ['ae312b940afc8540b95859594f38135d', 'discrete'],
           'msadapt': ['91af0c3b766b63dd63556ad70ab39187', 'base'],
           'gmabstract': ['9f0ab14b1980740cafa2b6e5c8ab5504', 'abstract'],
           'gmvoxel': ['8f533f93a569c72fd38b87ed0d78149a', 'voxel'],
        },
        'docs': {
           'FieldSim': ['810f237944f56ffe494fcbbb4b9eafe7', 'base'],
           'GeomSimDiscrete': ['c9b3b994d9bd219b7804580635ff112c', 'discrete'],
           'MeshSim': ['a18456926018b326330df3931af5be3e', 'base'],
           'GeomSimAbstract': ['62fa4c5ea8abfa903acdf704d52883fc', 'abstract'],
           'GeomSimParasolid': ['f059c25e203501175178374a4a608ed5', 'parasolid'],
           'GeomSimImport': ['2b2656cd75757d64ec099497e346c373', 'import'],
           'GeomSimAcis': ['8baafac8e8d08767bf560afafb4b0bff', 'acis'],
           'GeomSimVoxel': ['6c94bc980fe70334b9b48e5001efc665', 'voxel'],
           'GeomSimDiscreteModeling': ['f57e2b3a95973bed15aa99048b6ebbc2', 'discrete'],
           'ParallelMeshSim': ['df06fe4b3e850c8b9804be7107776351', 'parallelmesh'],
           'GeomSimAdvanced': ['111d1407bdce792ff3b3e88bb8e5f1c2', 'advmodel'],
           'MeshSimAdvanced': ['6845fa170b42d02697fbb21ff902dd95', 'adv'],
           'ParallelMeshSimAdapt': ['ced7a09b9154bf5177dced35052f00ec', 'paralleladapt'],
           'GeomSim': ['43ffc86a2a0275c8b182a4221e9e8a5b', 'base'],
           'MeshSimAdapt': ['1ee82ef272292196d719db92454aa704', 'base'],
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
        env.append_path('LD_LIBRARY_PATH', join_path(path, 'acisKrnl'))
    if '+parasolid' in spec:
        env.append_path('CMAKE_PREFIX_PATH', join_path(path, 'psKrnl'))
        env.append_path('LD_LIBRARY_PATH', join_path(path, 'psKrnl'))


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

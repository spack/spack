# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hepmc(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "http://hepmc.web.cern.ch/hepmc/"
    url      = "http://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.09.tgz"

    version('3.2.0', sha256='f132387763d170f25a7cc9f0bd586b83373c09acf0c3daa5504063ba460f89fc')
    version('3.1.2', sha256='4133074b3928252877982f3d4b4c6c750bb7a324eb6c7bb2afc6fa256da3ecc7')
    version('3.1.1', sha256='2fcbc9964d6f9f7776289d65f9c73033f85c15bf5f0df00c429a6a1d8b8248bb')
    version('3.1.0', sha256='cd37eed619d58369041018b8627274ad790020a4714b54ac05ad1ebc1a6e7f8a')
    version('3.0.0',   sha256='7ac3c939a857a5ad67bea1e77e3eb16e80d38cfdf825252ac57160634c26d9ec')
    version('2.06.10', sha256='5adedd9e3f7447e1e5fc01b72f745ab87da2c1611df89208bb3d7c6ea94c11a4')
    version('2.06.09', sha256='e0f8fddd38472c5615210894444686ac5d72df3be682f7d151b562b236d9b422')
    version('2.06.08', sha256='8be6c1793e0a045f07ddb88bb64b46de7e66a52e75fb72b3f82f9a3e3ba8a8ce')
    version('2.06.07', sha256='a0bdd6f36a3cc4cb59d6eb15cef9d46ce9b3739cae3324e81ebb2df6943e4594')
    version('2.06.06', sha256='8cdff26c10783ed4248220a84a43b7e1f9b59cc2c9a29bd634d024ca469db125')
    version('2.06.05', sha256='4c411077cc97522c03b74f973264b8d9fd2b6ccec0efc7ceced2645371c73618')

    variant('python', default=False, description='Enable Python bindings')
    variant('rootio', default=False, description='Enable ROOT I/O')
    variant('interfaces', default=False, description='Install interfaces for some Monte-Carlo Event Gens')

    depends_on('cmake@2.8.9:', type='build')
    depends_on('python', when='+python')
    depends_on('root', when='+rootio')

    conflicts('+python', when='@:3.1')
    conflicts('+rootio', when='@:2')
    conflicts('+interfaces', when='@:2')

    @when('@:2')
    def cmake_args(self):
        return ['-Dmomentum:STRING=GEV', '-Dlength:STRING=MM']

    @when('@3:')
    def cmake_args(self):
        spec = self.spec
        args = [
            '-Dmomentum:STRING=GEV',
            '-Dlength:STRING=MM',
            '-DHEPMC3_ENABLE_PYTHON={0}'.format(spec.satisfies('+python')),
            '-DHEPMC3_ENABLE_ROOTIO={0}'.format(spec.satisfies('+rootio')),
            '-DHEPMC3_INSTALL_INTERFACES={0}'.format(
                spec.satisfies('+interfaces')),
        ]

        if self.spec.satisfies('+python'):
            py_ver = spec['python'].version.up_to(2)
            py_sitepkg = join_path(self.prefix, site_packages_dir)
            args.extend([
                '-DHEPMC3_PYTHON_VERSIONS={0}'.format(py_ver),
                '-DHEPMC3_Python_SITEARCH{0}={1}'.format(
                    py_ver.joined, py_sitepkg)
            ])

        if self.spec.satisfies('+rootio'):
            args.append('-DROOT_DIR={0}'.format(self.spec['root'].prefix))

        return args

    def url_for_version(self, version):
        if version > Version("3.0.0"):
            url = "http://hepmc.web.cern.ch/hepmc/releases/HepMC3-{0}.tar.gz"
        elif version <= Version("2.06.08"):
            url = "http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-{0}.tar.gz"
        else:
            url = "http://hepmc.web.cern.ch/hepmc/releases/hepmc{0}.tgz"
        return url.format(version)

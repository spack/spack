# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class AwsParallelcluster(PythonPackage):
    """AWS ParallelCluster is an AWS supported Open Source cluster management
    tool to deploy and manage HPC clusters in the AWS cloud."""

    homepage = "https://github.com/aws/aws-parallelcluster"
    url      = "https://pypi.io/packages/source/a/aws-parallelcluster/aws-parallelcluster-2.7.0.tar.gz"

    maintainers = [
        'sean-smith', 'demartinofra', 'enrico-usai', 'lukeseawalker', 'rexcsn',
        'ddeidda', 'tilne'
    ]
    import_modules = [
        'pcluster', 'awsbatch', 'pcluster.dcv', 'pcluster.configure',
        'pcluster.config', 'pcluster.networking'
    ]

    version('2.7.0', sha256='7c34995acfcc256a6996541d330575fc711e1fd5735bf3d734d4e96c1dc8df60')
    version('2.6.1', sha256='2ce9015d90b5d4dc88b46a44cb8a82e8fb0bb2b4cca30335fc5759202ec1b343')
    version('2.6.0', sha256='aaed6962cf5027206834ac24b3d312da91e0f96ae8607f555e12cb124b869f0c')
    version('2.5.1', sha256='4fd6e14583f8cf81f9e4aa1d6188e3708d3d14e6ae252de0a94caaf58be76303')
    version('2.5.0', sha256='3b0209342ea0d9d8cc95505456103ad87c2d4e35771aa838765918194efd0ad3')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-boto3@1.10.15:', type=('build', 'run'))
    depends_on('py-future@0.16.0:0.18.2', type=('build', 'run'))
    depends_on('py-tabulate@0.8.2:0.8.3', type=('build', 'run'))
    depends_on('py-ipaddress@1.0.22:', type=('build', 'run'))
    depends_on('py-enum34@1.1.6:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.2:', type=('build', 'run'))
    depends_on('py-configparser@3.5.0:3.8.1', when='^python@:2', type=('build', 'run'))

    # https://github.com/aws/aws-parallelcluster/pull/1633
    patch('enum34.patch', when='@:2.5.1')

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def install_test(self):
        # Make sure executables work
        for exe in ['awsbhosts', 'awsbkill', 'awsbout', 'awsbqueues',
                    'awsbstat', 'awsbsub', 'pcluster']:
            exe = Executable(os.path.join(self.prefix.bin, exe))
            exe('--help')

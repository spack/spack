# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTensorflow(Package):
    """TensorFlow is an Open Source Software Library for Machine Intelligence
    This is a wheel based recipe as opposed to source-based installation in
    the upstream spack."""

    homepage = "https://www.tensorflow.org"
    url      = "https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.5.0-cp38-cp38-manylinux2010_x86_64.whl"

    maintainers = ['pramodk', 'matz-e']
    import_modules = ['tensorflow']

    # For now only support python 38 wheels on linux with gpu. Mac os urls
    # are broken on the docuementation page. Below dict is setup so that this
    # can be easily extended.
    tensorflow_sha = {
        ('2.4.2', 'gpu-2.4.2-cp38-cp38-manylinux2010_x86_64'): 'a33acffb4816c5456eb0cbc1654e3f270d17245322aa3d7bfdd22a610c862e0a',
    }

    def wheel_url(version_id):
        return (
            'https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_{0}.whl'  # noqa: E501
        ).format(version_id)

    # add all version
    for key in tensorflow_sha.keys():
        version(key[0], url=wheel_url(key[1]), sha256=tensorflow_sha[key], expand=False)

    extends('python')

    depends_on('cudnn@8:')
    depends_on('cuda@11:')
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pip', type='build')

    # compatible versions of py-h5py and py-six needs to be added
    # otherwise setup.py tries to uninstall them
    depends_on('py-h5py@2.10:2.99', when='@:2.4.99', type=('build', 'run'))
    depends_on('py-h5py@3:', when='@2.5:', type=('build', 'run'))
    depends_on('py-six@1.15.0', when='@:2.4.99', type=('build', 'run'))
    depends_on('py-six@1.16:', when='@2.5:', type=('build', 'run'))

    # no versions for Mac OS added
    conflicts('platform=darwin', msg='macOS is not supported')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        with working_dir('spack-test', create=True):
            for module in self.import_modules:
                python('-c', 'import {0}'.format(module))

    def setup_run_environment(self, env):
        env.prepend_path('LD_LIBRARY_PATH', self.spec['cuda'].prefix.lib64)
        env.prepend_path('LD_LIBRARY_PATH', self.spec['cuda'].prefix.extras.CUPTI.lib64)  # noqa: E501
        env.prepend_path('LD_LIBRARY_PATH', self.spec['cudnn'].prefix.lib64)

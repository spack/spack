# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTraitsui(PythonPackage):
    """The TraitsUI project contains a toolkit-independent GUI abstraction
    layer, which is used to support the "visualization" features of the Traits
    package. Thus, you can write model in terms of the Traits API and specify a
    GUI in terms of the primitives supplied by TraitsUI (views, items, editors,
    etc.), and let TraitsUI and your selected toolkit and back-end take care of
    the details of displaying them."""

    homepage = "https://docs.enthought.com/traitsui"
    pypi = "traitsui/traitsui-6.1.3.tar.gz"

    version('7.1.1', sha256='77d9dc5830c4e7ab94f9225bc2f082430399d95c943f1616db41e83a94df38e5')
    version('7.1.0', sha256='b699aeea588b55723860ddc6b2bd9b5013c4a72e18d1bbf51c6689cc7c6a562a')
    version('7.0.1', sha256='74fb4db848ac1343241fa4dc5d9bf3fab561f309826c602e8a3568309df91fe3')
    version('7.0.0', sha256='e569f359a58e4567b14265abe89b3de4b0f95bbbf8f491a9a7d45219628735ec')
    version('6.1.3', sha256='48381763b181efc58eaf288431d1d92d028d0d97dfdd33eba7809aae8aef814f')

    variant('backend', default='pyqt5', description='Default backend',
            values=('wx', 'pyqt', 'pyqt5', 'pyside'), multi=False)

    depends_on('py-setuptools', type='build')
    depends_on('py-traits', type=('build', 'run'))
    depends_on('py-pyface@6.0.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Backends
    depends_on('py-wxpython@2.8.10:', when='backend=wx', type=('build', 'run'))
    depends_on('py-numpy', when='backend=wx', type=('build', 'run'))
    depends_on('py-pyqt4@4.10:', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt', type=('build', 'run'))
    depends_on('py-pyqt5@5:', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyqt5', type=('build', 'run'))
    depends_on('py-pyside@1.2:', when='backend=pyside', type=('build', 'run'))
    depends_on('py-pygments', when='backend=pyside', type=('build', 'run'))

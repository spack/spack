from spack.package import *
from spack.pkg.builtin.py_py4j import PyPy4j as BuiltinPyPy4j


class PyPy4j(BuiltinPyPy4j):
    __doc__ = BuiltinPyPy4j.__doc__

    version('0.10.9.5',
            url='https://files.pythonhosted.org/packages/ce/1f/b00295b6da3bd2f050912b9f71fdb436ae8f1601cf161365937d8553e24b/py4j-0.10.9.5.tar.gz',
            sha256='276a4a3c5a2154df1860ef3303a927460e02e97b047dc0a47c1c3fb8cce34db6')
    version('0.10.9.3',
            url='https://files.pythonhosted.org/packages/d1/c4/9674152db7bb6dd67e5c93eeb48b727a840551932c88a44e20143cb661c1/py4j-0.10.9.3.tar.gz',
            sha256='0d92844da4cb747155b9563c44fc322c9a1562b3ef0979ae692dbde732d784dd')

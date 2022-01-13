from spack import *
from spack.pkg.builtin.py_breathe import PyBreathe as BuiltinPyBreathe


class PyBreathe(BuiltinPyBreathe):
    version('4.31.0', sha256='63edd18240b7aeb155c6b3d7de13c1322dd7c150f2ad2e9742e95e51b0dc48a8')
    version('4.30.0', sha256='540ca6d694aa2e194ba33265f58e0070465799f6feabb726d198cb039972a5a3')
    version('4.29.2', sha256='e71dfb5dd1176b91bb27d26b7c210d8bd0be5e1f31f10e22ab8d38412a74b52e')
    version('4.29.1', sha256='72cf9ade88f3e9163e0730e4089fde7b92464f691d29250019983457a977df44')
    version('4.29.0', sha256='5fc965cfd248c01909a4ba78f3d7130d85e08b6f373b5224f4fc682cbfd760b4')

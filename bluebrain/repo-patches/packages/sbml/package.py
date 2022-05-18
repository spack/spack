from spack import *
from spack.pkg.builtin.sbml import Sbml as BuiltinSbml


class Sbml(BuiltinSbml):
    __doc__ = BuiltinSbml.__doc__

    version('5.19.0', sha256='a7f0e18be78ff0e064e4cdb1cd86634d08bc33be5250db4a1878bd81eeb8b547')

    depends_on('py-setuptools', type='build', when='+python')
    extends('python', when='+python')

    def cmake_args(self):
        args = super().cmake_args()
        if '+python' in self.spec:
            args.extend([
                '-DPYTHON_INSTALL_IN_PREFIX:BOOL=OFF',
                '-DPYTHON_INSTALL_WITH_SETUP:BOOL=ON',
            ])
        return args

    def patch(self):
        if self.spec.satisfies('+python'):
            # Piggy-back on an actual Python package to get the
            # proper installation prefixes
            # Brittle join, `shlex.join` is better but Python 3.8+
            args = ' '.join(
                self.spec['py-setuptools'].package.install_args(
                    self.spec,
                    self.prefix
                )
            )
            # --no-user-cfg is not recognized by setup.py, drop it
            filter_file(
                'setup.py install',
                'setup.py install {0}'.format(args),
                'src/bindings/python/CMakeLists.txt'
            )
            # PyPI sbml identifies as python-libsbml
            filter_file(
                r'(name\s*= ")(libsbml)',
                r'\1python-\2',
                'src/bindings/python/setup.py.cmake'
            )

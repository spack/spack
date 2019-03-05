from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import glob

extensions = []

excludes = ['spack/main.py', 'spack/paths.py']

for f in glob.glob('spack/*.py'):
    if f in excludes:
        continue
    extensions.append(Extension(f.replace('spack/', 'spack.').replace('.py',
                                                                      ''),
                                [f]))

extensions.append(Extension('llnl.util.lang', ['llnl/util/lang.py']))
setup(name="spack", ext_modules=cythonize(extensions))

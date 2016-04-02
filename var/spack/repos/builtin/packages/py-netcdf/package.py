from spack import *
import os


# --------------------------------------
def walk_dependencies(spec, deps):
# see: spec.Spec.traverse()
    if str(spec.version) == 'system':
        # No Spack module for system-installed packages
        return

    for dep in spec.dependencies.values():
        walk_dependencies(dep, deps)

    deps.append(spec)



# --------------------------------------


class PyNetcdf(Package):
    """Python interface to the netCDF Library."""
    homepage = "http://unidata.github.io/netcdf4-python"
    url      = "https://github.com/Unidata/netcdf4-python/tarball/v1.2.3.1rel"

    version('1.2.3.1', '4fc4320d4f2a77b894ebf8da1c9895af')

    extends('python')
    depends_on('py-numpy')
    depends_on('py-cython')
    depends_on('netcdf')

    def install(self, spec, prefix):

        # ---- Set up LD_LIBRARY_PATH coming from py-numpy:blas
        # (because py-numpy isn't built with RPATH)
        # Our install process imports numpy, and that needs to work.
        deps = list()
        py_numpy = spec['py-numpy']
        if 'blas' in py_numpy:
            walk_dependencies(spec['py-numpy']['blas'], deps)

        seen = set()
        deps_unique = list()
        for dep in deps:
            if id(dep) not in seen:
                deps_unique.append(dep)
                seen.add(id(dep))

        LD_LIBRARY_PATH = []
        for dep in deps_unique:
            LD_LIBRARY_PATH.append(join_path(dep.prefix, 'lib'))
        # --------------------------------

        os.environ['LD_LIBRARY_PATH'] = ':'.join(LD_LIBRARY_PATH)
        python('setup.py', 'install', '--prefix=%s' % prefix)

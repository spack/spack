from spack.pkg.builtin.caliper import Caliper as BuiltinCaliper


class Caliper(BuiltinCaliper):
    __doc__ = BuiltinCaliper.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        if '+cuda' in self.spec:
            # this avoids the CMake install step erasing the RPATH entry
            # pointing to /path/to/cuda/extras/CUPTI/lib64, which is correctly
            # added by Caliper's CMake but is not known to Spack. See upstream
            # Spack issue: https://github.com/spack/spack/issues/24724
            args.append('-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=On')
        return args

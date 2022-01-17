from spack import *
from spack.pkg.builtin.itk import Itk as BuiltinItk


class Itk(BuiltinItk):
    __doc__ = BuiltinItk.__doc__

    variant('antspy', default=False, description='support features for antspy')

    def cmake_args(self):
        from_variant = self.define_from_variant
        args = super().cmake_args()
        args.extend([
            from_variant('Module_MGHIO', 'antspy'),
            from_variant('Module_GenericLabelInterpolator', 'antspy'),
            from_variant('Module_AdaptiveDenoising', 'antspy'),
        ])
        return args

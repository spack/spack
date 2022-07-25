from spack import *
from spack.pkg.builtin.mvapich2 import Mvapich2 as BuiltinMvapich2


class Mvapich2(BuiltinMvapich2):
    __doc__ = BuiltinMvapich2.__doc__

    # Adds IME variant to enable the IME driver in ROMIO
    variant(
        'file_systems',
        description='List of the ROMIO file systems to activate',
        values=auto_or_any_combination_of('lustre', 'gpfs', 'nfs', 'ufs', 'ime'),
    )

    @property
    def file_system_options(self):
        spec = self.spec

        fs = []
        for x in ('lustre', 'gpfs', 'nfs', 'ufs', 'ime'):
            if 'file_systems={0}'.format(x) in spec:
                fs.append(x)

        opts = []
        if len(fs) > 0:
            opts.append('--with-file-system=%s' % '+'.join(fs))

        return opts
